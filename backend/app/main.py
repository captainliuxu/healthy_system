from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes.health import router as health_router

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.ALLOWED_ORIGINS == "*" else settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.API_V1_PREFIX)

# 异常处理
from app.core.exception import (
    BusinessException,
    business_exception_handler,
    generic_exception_handler,
)

app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)