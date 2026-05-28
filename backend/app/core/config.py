from pathlib import Path

from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Company RAG Backend"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: AnyUrl
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 12000
    TENANT_HEADER: str = "X-Tenant-ID"

    class Config:
        env_file = Path(__file__).resolve().parents[2] / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
