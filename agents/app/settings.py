"""Typed runtime settings loaded from the environment."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Later files override earlier ones, so `.env.local` wins over `.env`.
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    openrouter_api_key: str = Field(default="", alias="OPENROUTER_API_KEY")
    openrouter_model_fast: str = Field(
        default="openai/gpt-4o-mini", alias="OPENROUTER_MODEL_FAST"
    )
    openrouter_model_smart: str = Field(
        default="anthropic/claude-sonnet-4.5", alias="OPENROUTER_MODEL_SMART"
    )
    openrouter_referer: str = Field(
        default="http://localhost:5173", alias="OPENROUTER_REFERER"
    )
    openrouter_app_title: str = Field(
        default="Hamza & Co. Oracles", alias="OPENROUTER_APP_TITLE"
    )

    backend_url: str = Field(default="http://localhost:8080", alias="BACKEND_URL")

    allowed_origins: str = Field(
        default="http://localhost:5173,http://localhost:4173",
        alias="ALLOWED_ORIGINS",
    )

    port: int = Field(default=8001, alias="PORT")

    rate_limit_per_minute: int = Field(default=20, alias="RATE_LIMIT_PER_MINUTE")
    session_ttl_seconds: int = Field(default=3600, alias="SESSION_TTL_SECONDS")

    embedding_model: str = Field(
        default="BAAI/bge-small-en-v1.5", alias="EMBEDDING_MODEL"
    )

    @property
    def allowed_origins_list(self) -> list[str]:
        raw = self.allowed_origins.strip()
        if raw in {"", "*"}:
            return ["*"]
        return [origin.strip() for origin in raw.split(",") if origin.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
