from __future__ import annotations

from typing import Any, Optional

import httpx

from apps.backend.core.config import settings


class SummarizationError(RuntimeError):
    pass


async def summarize(text: str, model_id: Optional[str] = None, max_tokens: int = 256, lang: str = "ru") -> str:
    if not text:
        return ""
    if model_id is None:
        model_id = settings.ai_summary_model_id or ""
    endpoint = settings.ai_summary_endpoint
    if not endpoint or not model_id:
        # No provider configured; return a simple truncation as placeholder
        return text[: max_tokens * 4]

    payload = {
        "model": model_id,
        "max_tokens": max_tokens,
        "lang": lang,
        "input": text,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(endpoint, json=payload)
        if resp.status_code != 200:
            raise SummarizationError(f"Provider error: {resp.status_code} {resp.text}")
        data: Any = resp.json()
        # Expect either { summary: "..." } or provider-specific
        return data.get("summary") or data.get("output") or ""


