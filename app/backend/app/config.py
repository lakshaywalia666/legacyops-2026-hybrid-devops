import os
from functools import lru_cache
from typing import List


class Settings:
    app_name: str = os.getenv("APP_NAME", "Legacy Retail Operations System")
    app_env: str = os.getenv("APP_ENV", "development")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://legacyops:legacyops@localhost:5432/legacyops",
    )
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_required: bool = os.getenv("REDIS_REQUIRED", "false").lower() == "true"
    cors_origins_raw: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000",
    )

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
