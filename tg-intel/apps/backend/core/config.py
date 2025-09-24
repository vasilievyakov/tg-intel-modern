import os
from pathlib import Path
from dotenv import load_dotenv


# Load .env explicitly from repo root to avoid CWD issues
ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env", override=True)


class Settings:
    supabase_url: "str | None" = os.getenv("SUPABASE_URL")
    supabase_db_url: "str | None" = os.getenv("SUPABASE_DB_URL")
    port: int = int(os.getenv("BACKEND_PORT", "8000"))
    cron_fetch_minutes: int = int(os.getenv("CRON_FETCH_MINUTES", "5"))
    # Telegram
    tg_api_id: "int | None" = int(os.getenv("TG_API_ID")) if os.getenv("TG_API_ID") else None
    tg_api_hash: "str | None" = os.getenv("TG_API_HASH")
    tg_session_path: str = os.getenv("TG_SESSION_PATH", "./.secrets/telethon.session")
    tg_proxy_url: "str | None" = os.getenv("TG_PROXY_URL")
    # AI
    ai_summary_endpoint: "str | None" = os.getenv("AI_SUMMARY_ENDPOINT")
    ai_summary_model_id: "str | None" = os.getenv("AI_SUMMARY_MODEL_ID")
    # CORS
    _cors_origins_env: "str | None" = os.getenv("CORS_ORIGINS")
    cors_allow_credentials: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    cors_origin_regex_env: "str | None" = os.getenv("CORS_ORIGIN_REGEX")

    @property
    def cors_origins(self) -> "list[str]":
        """Return allowed CORS origins.

        If CORS_ORIGINS env var is set, it should be a comma-separated list.
        Falls back to localhost defaults suitable for development.
        """
        if self._cors_origins_env:
            # Split by comma and strip whitespace
            origins = [o.strip() for o in self._cors_origins_env.split(",") if o.strip()]
            # Remove trailing slashes for consistency
            return [o[:-1] if o.endswith("/") else o for o in origins]
        return [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]

    @property
    def cors_origin_regex(self) -> "str | None":
        """Optional regex to allow local dev hosts and LAN IPs by default.

        Can be overridden via CORS_ORIGIN_REGEX. Useful to avoid CORS issues
        when accessing backend from http://192.168.x.x:3000, etc.
        """
        if self.cors_origin_regex_env:
            return self.cors_origin_regex_env
        # Permit http(s)://localhost|127.0.0.1|192.168.x.x(:port)? for dev
        return r"https?://(localhost|127\.0\.0\.1|192\.168\.[0-9]{1,3}\.[0-9]{1,3})(:[0-9]+)?"


settings = Settings()


