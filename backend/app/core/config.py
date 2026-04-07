from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "healthy_system backend"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./healthy_system.db"
    DASHSCOPE_API_KEY: str = ""
    LLM_PROVIDER: str = "mock"
    ALLOWED_ORIGINS: str = "*"
    CHAT_MEMORY_LIMIT: int = 6
    PROACTIVE_SCHEDULER_ENABLED: bool = True
    PROACTIVE_SCHEDULER_MINUTES: int = 1

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env.example"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()