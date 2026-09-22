from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.error_handlers import add_error_handlers
from app.api.routes import chat, conversations, health
from app.core.config import get_settings
from app.core.logging import RequestIdMiddleware, configure_logging
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title="AnubhavGPT API", version="0.1.0", lifespan=lifespan)
app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["content-type", "x-request-id"],
)
add_error_handlers(app)

app.include_router(health.router, prefix="/api/v1")
app.include_router(conversations.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
