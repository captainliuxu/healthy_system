from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "healthy_system backend"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./healthy_system.db"
    DASHSCOPE_API_KEY: str = ""
    ALLOWED_ORIGINS: str = "*"

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env.example"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()