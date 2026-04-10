from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
# 定位backend根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 把环境变量自动映射成python可以配置的对象
# 以后别的文件访问直接通过settings.xxx读取配置

class Settings(BaseSettings):
    PROJECT_NAME: str = "healthy_system_fastapi"
    APP_ENV: str = "dev"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "sqlite:///./healthy_system.db"

    JWT_SECRET_KEY: str = "replace_this_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    # Token 用什么密钥签名
    # Token 用什么算法签名
    # Token 多久过期
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    LLM_PROVIDER: str = "dashscope"
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = ""
    LLM_MODEL_NAME: str = "qwen-plus"

    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            if not value.strip():
                return []
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

# 保证 Settings() 只初始化一次
# 避免每次导入都重复读取环境变量
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()