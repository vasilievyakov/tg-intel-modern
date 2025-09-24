from __future__ import annotations

from datetime import datetime
from typing import Any
import asyncio
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from apps.backend.core.config import settings
from apps.backend.core.logger import logger
from apps.backend.core.db import require_pool
from apps.backend.services.telegram import resolve_channel, fetch_history
from psycopg.types.json import Json
from telethon.errors.rpcerrorlist import FloodWaitError, ChannelPrivateError


from typing import Optional
from apps.backend.core.logger import logger

scheduler: Optional[AsyncIOScheduler] = None


async def enqueue_initial_fetch_jobs() -> None:
    pool = require_pool()
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("select id, tg_url from channels where status='pending' order by created_at asc")
            rows = await cur.fetchall()
            for row in rows:
                await cur.execute(
                    "insert into fetch_jobs (channel_id, status) values (%s, 'queued')",
                    (row[0],),
                )


async def process_fetch_job(job_id: int) -> None:
    pool = require_pool()
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("select id, channel_id from fetch_jobs where id=%s", (job_id,))
            job = await cur.fetchone()
        if not job:
            return
        async with conn.cursor() as cur:
            await cur.execute("select id, tg_id, tg_url, status from channels where id=%s", (job[1],))
            channel = await cur.fetchone()
        if not channel:
            return
        try:
            async with conn.cursor() as cur:
                await cur.execute("update fetch_jobs set status='running', started_at=now() where id=%s", (job_id,))

            # Resolve channel tg_id if missing
            tg_id = channel[1]
            title = None
            if tg_id is None:
                resolved = await resolve_channel(channel[2])
                tg_id = resolved.tg_id
                title = resolved.title
                async with conn.cursor() as cur:
                    await cur.execute(
                        "update channels set tg_id=%s, title=coalesce(%s, title), status='active' where id=%s",
                        (tg_id, title, channel[0]),
                    )

            # Find last message id to continue from
            async with conn.cursor() as cur:
                await cur.execute("select max(tg_message_id) from posts where channel_id=%s", (channel[0],))
                row = await cur.fetchone()
                last_msg_id = row[0] if row else None

            inserted = 0
            fetched = 0
            started_ts = time.time()
            # Prefer using the URL/username to avoid access hash issues
            tg_ref = channel[2] if channel[2] else tg_id
            # Always refresh a recent window (e.g., 200 msgs) to backfill engagement metrics
            refresh_window = 200
            processed = 0
            async for msg in fetch_history(tg_ref, limit=1000):
                processed += 1
                if last_msg_id and msg["id"] <= last_msg_id and processed > refresh_window:
                    break
                async with conn.cursor() as cur:
                    await cur.execute(
                        """
                        insert into posts (channel_id, tg_message_id, posted_at, text, raw)
                        values (%s, %s, %s, %s, %s)
                        on conflict (channel_id, tg_message_id) do update
                          set raw = coalesce(posts.raw, '{}'::jsonb) || excluded.raw
                        """,
                        (
                            channel[0],
                            msg["id"],
                            datetime.fromisoformat(msg["date"]) if msg["date"] else None,
                            msg.get("text"),
                            Json(msg),
                        ),
                    )
                inserted += 1
                fetched += 1
                if fetched % 50 == 0:
                    await asyncio.sleep(0.5)

            async with conn.cursor() as cur:
                await cur.execute(
                    "update fetch_jobs set status='success', finished_at=now(), stats=jsonb_build_object('inserted', %s, 'duration_s', %s) where id=%s",
                    (inserted, round(time.time() - started_ts, 3), job_id),
                )
        except FloodWaitError as exc:
            logger.warning("Fetch job hit flood wait", extra={"job_id": job_id, "seconds": exc.seconds})
            async with conn.cursor() as cur:
                await cur.execute(
                    "update fetch_jobs set status='error', finished_at=now(), error=%s where id=%s",
                    (f'FLOOD_WAIT {exc.seconds}s', job_id),
                )
        except ChannelPrivateError as exc:
            logger.warning("Channel is private", extra={"job_id": job_id, "error": str(exc)})
            async with conn.cursor() as cur:
                await cur.execute(
                    "update fetch_jobs set status='error', finished_at=now(), error=%s where id=%s",
                    (str(exc), job_id),
                )
        except Exception as exc:  # noqa: BLE001
            logger.exception("Unexpected error during fetch job", extra={"job_id": job_id})
            async with conn.cursor() as cur:
                await cur.execute(
                    "update fetch_jobs set status='error', finished_at=now(), error=%s where id=%s",
                    (str(exc), job_id),
                )


def get_scheduler() -> AsyncIOScheduler:
    global scheduler
    if scheduler is None:
        scheduler = AsyncIOScheduler()
    return scheduler


def schedule_periodic_fetch() -> None:
    sch = get_scheduler()
    sch.add_job(run_periodic_fetch_cycle, "interval", minutes=settings.cron_fetch_minutes, id="periodic_fetch", replace_existing=True)


async def run_periodic_fetch_cycle() -> None:
    pool = require_pool()
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("select id from channels where status='active'")
            rows = await cur.fetchall()
            for row in rows:
                await cur.execute(
                    "insert into fetch_jobs (channel_id, status) values (%s, 'queued')",
                    (row[0],),
                )


async def process_queued_jobs(batch_limit: int = 3) -> None:
    try:
        pool = require_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "select id from fetch_jobs where status='queued' order by started_at nulls first, id asc limit %s",
                    (batch_limit,),
                )
                jobs = await cur.fetchall()
        for job in jobs:
            await process_fetch_job(job[0])
    except Exception as e:
        logger.warning(f"Could not process queued jobs: {e}")


def schedule_job_processor() -> None:
    sch = get_scheduler()
    sch.add_job(process_queued_jobs, "interval", seconds=15, id="job_processor", replace_existing=True)

