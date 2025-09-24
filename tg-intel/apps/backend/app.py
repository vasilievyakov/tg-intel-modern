from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from apps.backend.api.channels import router as channels_router
from apps.backend.api.posts import router as posts_router
from apps.backend.api.summaries import router as summaries_router
from apps.backend.core.config import settings
from apps.backend.core.logger import logger
from apps.backend.core.db import init_pool, close_pool
from apps.backend.services.fetcher import get_scheduler, schedule_periodic_fetch, schedule_job_processor, enqueue_initial_fetch_jobs

app = FastAPI(title="tg-intel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=settings.cors_origin_regex,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


app.include_router(channels_router, prefix="/api/channels", tags=["channels"])
app.include_router(posts_router, prefix="/api", tags=["posts"])
app.include_router(summaries_router, prefix="/api", tags=["summaries"])


@app.on_event("startup")
async def on_startup() -> None:
    # init DB pool if DSN is present
    db_ready = False
    if settings.supabase_db_url:
        await init_pool(settings.supabase_db_url)
        db_ready = True
    # Start scheduler only if DB is ready
    if db_ready:
        try:
            sch = get_scheduler()
            if not sch.running:
                sch.start()
            schedule_periodic_fetch()
            schedule_job_processor()
            # Enqueue initial fetch jobs for pending channels
            try:
                await enqueue_initial_fetch_jobs()
            except Exception as e:
                logger.warning(f"Could not enqueue initial fetch jobs: {e}")
        except Exception as e:
            logger.warning(f"Could not start scheduler: {e}")
    else:
        logger.warning("Database not configured - scheduler and fetch jobs disabled")


@app.on_event("shutdown")
async def on_shutdown() -> None:
    # Stop scheduler
    sch = get_scheduler()
    try:
        sch.shutdown(wait=False)
    except Exception:
        pass
    await close_pool()


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: D401
    """Catch-all handler to log unexpected exceptions with context."""
    logger.exception("Unhandled exception", extra={
        "path": request.url.path,
        "method": request.method,
        "client": getattr(request.client, "host", None),
    })
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

