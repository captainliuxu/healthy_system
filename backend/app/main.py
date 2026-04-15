import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.exception import register_exception_handlers
from app.core.logging_config import configure_logging
from app.core.scheduler import shutdown_scheduler, start_scheduler
from app.ws.manager import realtime_manager

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    realtime_manager.bind_loop(asyncio.get_running_loop())
    start_scheduler()

    try:
        yield
    finally:
        shutdown_scheduler()
        realtime_manager.reset()


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    register_exception_handlers(app)

    return app


app = create_application()
