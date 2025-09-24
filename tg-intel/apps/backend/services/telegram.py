from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from telethon import TelegramClient

from apps.backend.core.config import settings


_client: Optional[TelegramClient] = None


def get_client() -> TelegramClient:
    global _client
    if _client is None:
        if settings.tg_api_id is None or not settings.tg_api_hash:
            raise RuntimeError("TG_API_ID/TG_API_HASH are not configured")
        _client = TelegramClient(settings.tg_session_path, settings.tg_api_id, settings.tg_api_hash)
    return _client


async def start_client() -> None:
    client = get_client()
    if not client.is_connected():
        await client.connect()


async def stop_client() -> None:
    global _client
    if _client is not None:
        await _client.disconnect()


@dataclass
class ResolvedChannel:
    tg_id: int
    title: str


async def resolve_channel(tg_url: str) -> ResolvedChannel:
    client = get_client()
    await start_client()
    entity = await client.get_entity(tg_url)
    if not hasattr(entity, "id"):
        raise ValueError("Unsupported entity type")
    title = getattr(entity, "title", None) or getattr(entity, "username", "") or str(entity.id)
    return ResolvedChannel(tg_id=int(entity.id), title=title)


async def fetch_history(tg_ref: str | int, limit: int = 200) -> Iterable[dict]:
    """Fetch recent messages using a robust entity resolution.

    tg_ref may be a t.me URL, username, or numeric id. For reliability,
    prefer URL/username so Telethon resolves access_hash automatically.
    """
    client = get_client()
    await start_client()
    entity = await client.get_entity(tg_ref)
    async for message in client.iter_messages(entity=entity, limit=limit):
        views = getattr(message, "views", None)
        forwards = getattr(message, "forwards", None)
        replies_obj = getattr(message, "replies", None)
        replies = int(getattr(replies_obj, "replies", 0)) if replies_obj is not None else None
        reactions_total = None
        reactions_obj = getattr(message, "reactions", None)
        if reactions_obj is not None:
            try:
                results = getattr(reactions_obj, "results", None)
                if results is not None:
                    total = 0
                    for r in results:  # type: ignore[assignment]
                        count = getattr(r, "count", 0)
                        total += int(count or 0)
                    reactions_total = total
            except Exception:  # noqa: BLE001
                reactions_total = None

        yield {
            "id": int(message.id),
            "date": message.date.isoformat() if message.date else None,
            "text": message.text or None,
            "views": int(views) if views is not None else None,
            "forwards": int(forwards) if forwards is not None else None,
            "replies": replies,
            "reactions": reactions_total,
        }


