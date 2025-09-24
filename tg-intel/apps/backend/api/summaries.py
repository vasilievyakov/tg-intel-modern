from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from apps.backend.core.db import require_pool
from apps.backend.services.ai import summarize


router = APIRouter()


class SummaryOut(BaseModel):
    post_id: int
    summary: str
    cached: bool


@router.post("/posts/{post_id}/summarize", response_model=SummaryOut)
async def summarize_post(post_id: int, model: Optional[str] = None) -> Any:
    pool = require_pool()
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("select id, text from posts where id=%s", (post_id,))
            post = await cur.fetchone()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        async with conn.cursor() as cur:
            await cur.execute("select summary from summaries where post_id=%s", (post_id,))
            cached = await cur.fetchone()
        if cached:
            return {"post_id": post_id, "summary": cached[0], "cached": True}

        text: Optional[str] = post[1]
        if text is None or len(text) <= 500:
            return {"post_id": post_id, "summary": text or "", "cached": False}

        result = await summarize(text, model_id=model)
        async with conn.cursor() as cur:
            await cur.execute(
                "insert into summaries (post_id, model_id, summary, tokens) values (%s, %s, %s, %s) on conflict (post_id) do update set summary=excluded.summary, model_id=excluded.model_id",
                (post_id, model or "", result, 0),
            )
        return {"post_id": post_id, "summary": result, "cached": False}


