from __future__ import annotations

from typing import Any, Optional, List
import re
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl

from apps.backend.core.db import require_pool
from apps.backend.services.telegram import resolve_channel
from apps.backend.core.logger import logger


router = APIRouter()


class ChannelCreate(BaseModel):
    tg_url: str
def _normalize_tg_url_or_422(raw: str) -> str:
    s = (raw or "").strip()
    if not s:
        raise HTTPException(status_code=422, detail="tg_url is required")
    # Allow @username
    if s.startswith("@"):  # @durov
        username = s[1:].strip("/")
        if not re.fullmatch(r"[A-Za-z0-9_]{3,64}", username or ""):
            raise HTTPException(status_code=422, detail="Invalid Telegram username")
        return f"https://t.me/{username}"
    # Allow t.me/username (with or without scheme)
    if s.startswith("t.me/") or s.startswith("telegram.me/"):
        s = "https://" + s
    s = s.replace("https://telegram.me/", "https://t.me/")
    s = s.replace("http://t.me/", "https://t.me/")
    parsed = urlparse(s)
    if parsed.scheme not in {"http", "https"} or parsed.netloc not in {"t.me", "www.t.me"}:
        raise HTTPException(status_code=422, detail="tg_url must be @username or https://t.me/<username>")
    path = (parsed.path or "").strip("/")
    if not path:
        raise HTTPException(status_code=422, detail="Missing Telegram username in URL")
    username = path.split("/")[0]
    if not re.fullmatch(r"[A-Za-z0-9_]{3,64}", username):
        raise HTTPException(status_code=422, detail="Invalid Telegram username in URL")
    return f"https://t.me/{username}"


class ChannelOut(BaseModel):
    id: int
    tg_url: str
    title: Optional[str] = None
    status: str
    created_at: str


@router.post("", response_model=ChannelOut, status_code=status.HTTP_201_CREATED)
async def create_channel(payload: ChannelCreate) -> Any:
    pool = require_pool()
    tg_url = _normalize_tg_url_or_422(str(payload.tg_url))
    async with pool.connection() as conn:
        async with conn.transaction():
            async with conn.cursor() as cur:
                await cur.execute("select id, tg_url, title, status, created_at from channels where tg_url=%s", (tg_url,))
                existing = await cur.fetchone()
            if existing:
                # Do not enqueue initial job for existing channels
                return {
                    "id": existing[0],
                    "tg_url": existing[1],
                    "title": existing[2],
                    "status": existing[3],
                    "created_at": existing[4].isoformat() if hasattr(existing[4], 'isoformat') else str(existing[4]),
                }

            async with conn.cursor() as cur:
                await cur.execute(
                    "insert into channels (tg_url, status) values (%s, 'pending') returning id, tg_url, title, status, created_at",
                    (tg_url,),
                )
                row = await cur.fetchone()
            if row is None:
                raise HTTPException(status_code=500, detail="Failed to create channel")

            # Enqueue initial fetch job
            async with conn.cursor() as cur:
                await cur.execute(
                    "insert into fetch_jobs (channel_id, status) values (%s, 'queued') returning id",
                    (row[0],),
                )
                await cur.fetchone()

            return {
                "id": row[0],
                "tg_url": row[1],
                "title": row[2],
                "status": row[3],
                "created_at": row[4].isoformat() if hasattr(row[4], 'isoformat') else str(row[4]),
            }


@router.get("", response_model=List[ChannelOut])
async def list_channels() -> Any:
    pool = require_pool()
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "select id, tg_url, title, status, created_at from channels order by created_at desc"
            )
            rows = await cur.fetchall()
            out = []
            for r in rows:
                out.append(
                    {
                        "id": r[0],
                        "tg_url": r[1],
                        "title": r[2],
                        "status": r[3],
                        "created_at": r[4].isoformat() if hasattr(r[4], 'isoformat') else str(r[4]),
                    }
                )
            return out
@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(channel_id: int):
    pool = require_pool()
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("delete from channels where id=%s", (channel_id,))
            # 204 even if not found, to make UI idempotent


class FetchResult(BaseModel):
    enqueued: bool
    resolved: bool
    channel_id: int


@router.post("/{channel_id}/fetch", response_model=FetchResult)
async def force_fetch(channel_id: int) -> Any:
    """Resolve channel if needed and enqueue a fetch job."""
    pool = require_pool()
    resolved = False
    async with pool.connection() as conn:
        # Read channel
        async with conn.cursor() as cur:
            await cur.execute(
                "select id, tg_id, tg_url from channels where id=%s",
                (channel_id,),
            )
            row = await cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Channel not found")

        ch_id, tg_id, tg_url = row[0], row[1], row[2]

        # Resolve if tg_id missing
        if tg_id is None and tg_url:
            try:
                resolved_info = await resolve_channel(tg_url)
                async with conn.cursor() as cur:
                    await cur.execute(
                        "update channels set tg_id=%s, title=coalesce(title,%s), status='active' where id=%s",
                        (resolved_info.tg_id, resolved_info.title, ch_id),
                    )
                resolved = True
            except Exception as e:  # noqa: BLE001
                # Keep status pending; still enqueue job to retry later
                logger.exception("Failed to resolve channel", extra={"channel_id": ch_id, "tg_url": tg_url})
                resolved = False

        # Enqueue job
        async with conn.cursor() as cur:
            await cur.execute(
                "insert into fetch_jobs (channel_id, status) values (%s, 'queued') returning id",
                (ch_id,),
            )
            await cur.fetchone()

    return {"enqueued": True, "resolved": resolved, "channel_id": channel_id}


class JobOut(BaseModel):
    id: int
    status: Optional[str]
    started_at: Optional[str]
    finished_at: Optional[str]
    error: Optional[str]
    stats: Optional[dict]


@router.get("/{channel_id}/jobs/latest", response_model=Optional[JobOut])
async def latest_job(channel_id: int) -> Any:
    pool = require_pool()
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "select id, status, started_at, finished_at, error, stats from fetch_jobs where channel_id=%s order by id desc limit 1",
                (channel_id,),
            )
            row = await cur.fetchone()
            if not row:
                return None
            return {
                "id": row[0],
                "status": row[1],
                "started_at": row[2].isoformat() if row[2] else None,
                "finished_at": row[3].isoformat() if row[3] else None,
                "error": row[4],
                "stats": row[5],
            }


