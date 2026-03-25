from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from .database import create_engine_and_session, get_db_session

serving_engine, serving_session = create_engine_and_session(settings.SERVING_DB_URL)


async def async_get_serving_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_session(serving_session):
        yield session
