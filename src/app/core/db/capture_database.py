from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from .database import create_engine_and_session, get_db_session

capture_engine, capture_session = create_engine_and_session(settings.CAPTURE_DB_URL)


async def async_get_capture_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_session(capture_session):
        yield session
