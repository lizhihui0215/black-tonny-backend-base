import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

LOGGER = logging.getLogger(__name__)


async def check_database_health(db: AsyncSession) -> bool:
    try:
        await db.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        LOGGER.exception("Database health check failed with error: %s", exc)
        return False


async def check_redis_health(redis: Any | None) -> bool:
    if redis is None:
        return False

    try:
        await redis.ping()
        return True
    except Exception as exc:
        LOGGER.exception("Redis health check failed with error: %s", exc)
        return False
