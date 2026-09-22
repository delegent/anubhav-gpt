from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.db.session import get_session


async def db_session() -> AsyncIterator[AsyncSession]:
    async for session in get_session():
        yield session


def settings() -> Settings:
    return get_settings()
