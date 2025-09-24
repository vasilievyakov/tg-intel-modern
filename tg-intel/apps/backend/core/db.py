from __future__ import annotations

from typing import Any, Optional

from psycopg_pool import AsyncConnectionPool
from fastapi import HTTPException
import psycopg


_pool: Optional[AsyncConnectionPool] = None


async def init_pool(dsn: str, min_size: int = 1, max_size: int = 10) -> None:
    """Initialize a global psycopg async connection pool."""
    global _pool
    _pool = AsyncConnectionPool(conninfo=dsn, min_size=min_size, max_size=max_size, kwargs={"autocommit": True})
    await _pool.open()


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


def require_pool() -> AsyncConnectionPool:
    if _pool is None:
        # Return clear API error instead of crashing when DB is not configured
        raise HTTPException(status_code=503, detail="Database is not configured. Set SUPABASE_DB_URL or disable DB-dependent endpoints.")
    return _pool


async def fetch_one(query: str, *args: Any) -> Optional[dict]:
    pool = require_pool()
    async with pool.connection() as conn:  # type: ignore[assignment]
        async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            await cur.execute(query, args)
            return await cur.fetchone()


async def fetch_all(query: str, *args: Any) -> list[dict]:
    pool = require_pool()
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            await cur.execute(query, args)
            rows = await cur.fetchall()
            return list(rows)


async def fetch_val(query: str, *args: Any) -> Any:
    pool = require_pool()
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, args)
            row = await cur.fetchone()
            return row[0] if row else None


async def execute(query: str, *args: Any) -> str:
    pool = require_pool()
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, args)
            return "OK"


# FastAPI dependency (if needed)
async def get_db() -> AsyncConnectionPool:
    return require_pool()


