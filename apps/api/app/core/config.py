from functools import lru_cache
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "apps/api/.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite+aiosqlite:///./anubhavgpt.db"
    google_api_key: str = ""
    llm_provider: str = "fake"
    llm_model: str = "fake-anubhavgpt"
    llm_timeout_seconds: int = Field(default=45, ge=1, le=120)
    allowed_origins: Annotated[list[str], NoDecode] = ["http://localhost:5173"]
    fake_llm: bool = True

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @property
    def provider_enabled(self) -> bool:
        return not self.fake_llm and self.llm_provider == "google_genai"


@lru_cache
def get_settings() -> Settings:
    return Settings()
