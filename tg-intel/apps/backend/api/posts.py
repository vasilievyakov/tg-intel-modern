from __future__ import annotations

from typing import Any, Optional, List

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from apps.backend.core.db import fetch_all, fetch_val


router = APIRouter()


class PostOut(BaseModel):
    id: int
    channel_id: int
    tg_message_id: int
    posted_at: Optional[str] = None
    text: Optional[str] = None
    views: Optional[int] = None
    forwards: Optional[int] = None
    replies: Optional[int] = None
    reactions: Optional[int] = None


class PostsPage(BaseModel):
    items: List[PostOut]
    page: int
    page_size: int
    total: int


@router.get("/channels/{channel_id}/posts", response_model=PostsPage)
async def list_posts(
    channel_id: int,
    query: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> Any:
    offset = (page - 1) * page_size
    # Validate channel exists
    ch = await fetch_val("select 1 from channels where id=%s", channel_id)
    if not ch:
        raise HTTPException(status_code=404, detail="Channel not found")

    if query:
        tsquery = query
        sql_items = (
            "select id, channel_id, tg_message_id, posted_at, text, "
            "       nullif(raw->>'views','')::int as views, "
            "       nullif(raw->>'forwards','')::int as forwards, "
            "       nullif(raw->>'replies','')::int as replies, "
            "       nullif(raw->>'reactions','')::int as reactions "
            "from posts "
            "where channel_id=%s and text_tsv @@ plainto_tsquery('simple', %s) "
            "order by posted_at desc nulls last limit %s offset %s"
        )
        sql_count = (
            "select count(*) from posts where channel_id=%s and text_tsv @@ plainto_tsquery('simple', %s)"
        )
        rows = await fetch_all(sql_items, channel_id, tsquery, page_size, offset)
        total = await fetch_val(sql_count, channel_id, tsquery)
    else:
        rows = await fetch_all(
            "select id, channel_id, tg_message_id, posted_at, text, "
            "       nullif(raw->>'views','')::int as views, "
            "       nullif(raw->>'forwards','')::int as forwards, "
            "       nullif(raw->>'replies','')::int as replies, "
            "       nullif(raw->>'reactions','')::int as reactions "
            "from posts where channel_id=%s order by posted_at desc nulls last limit %s offset %s",
            channel_id,
            page_size,
            offset,
        )
        total = await fetch_val(
            "select count(*) from posts where channel_id=%s",
            channel_id,
        )

    # Normalize posted_at to ISO string for response model compatibility
    items = []
    for r in rows:
        item = dict(r)
        pa = item.get("posted_at")
        if pa is not None and hasattr(pa, "isoformat"):
            item["posted_at"] = pa.isoformat()
        items.append(item)
    return {"items": items, "page": page, "page_size": page_size, "total": int(total)}


