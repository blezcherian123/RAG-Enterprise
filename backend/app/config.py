from pathlib import Path
import logging

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Company RAG Backend"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]
    ENVIRONMENT: str = "development"
    ENABLE_API_DOCS: bool = True
    SQL_POOL_SIZE: int = 5
    SQL_MAX_OVERFLOW: int = 10

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("ACCESS_TOKEN_EXPIRE_MINUTES")
    @classmethod
    def validate_token_lifetime(cls, value: int) -> int:
        if not 1 <= value <= 1440:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be between 1 and 1440")
        return value

    @model_validator(mode="after")
    def validate_deployment_settings(self):
        if len(self.SECRET_KEY.encode("utf-8")) < 32:
            if self.ENVIRONMENT.lower() == "production":
                raise ValueError("Production SECRET_KEY must contain at least 32 bytes")
            logging.getLogger(__name__).warning("SECRET_KEY is shorter than 32 bytes; use a strong random key outside local development")
        if self.ENVIRONMENT.lower() == "production":
            if self.ENABLE_API_DOCS:
                raise ValueError("Set ENABLE_API_DOCS=false in production")
            if any(origin.startswith("http://") for origin in self.ALLOWED_ORIGINS):
                raise ValueError("Production ALLOWED_ORIGINS must use HTTPS")
        return self


settings = Settings()
