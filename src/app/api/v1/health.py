import logging
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.config import settings
from ...core.db.capture_database import async_get_capture_db
from ...core.db.serving_database import async_get_serving_db
from ...core.health import check_database_health, check_redis_health
from ...core.schemas import HealthCheck, ReadyCheck
from ...core.utils import cache, queue
from ...core.utils.rate_limit import rate_limiter

router = APIRouter(tags=["health"])

STATUS_HEALTHY = "healthy"
STATUS_UNHEALTHY = "unhealthy"

LOGGER = logging.getLogger(__name__)


async def resolve_redis_component_status(*, enabled: bool, client: object | None) -> str:
    if not enabled:
        return "disabled"

    return STATUS_HEALTHY if await check_redis_health(client) else STATUS_UNHEALTHY


@router.get("/health", response_model=HealthCheck)
async def health() -> JSONResponse:
    http_status = status.HTTP_200_OK
    response = {
        "status": STATUS_HEALTHY,
        "environment": settings.ENVIRONMENT.value,
        "version": settings.APP_VERSION,
        "timestamp": datetime.now(UTC).isoformat(timespec="seconds"),
    }

    return JSONResponse(status_code=http_status, content=response)


@router.get("/ready", response_model=ReadyCheck)
async def ready(
    capture_db: Annotated[AsyncSession, Depends(async_get_capture_db)],
    serving_db: Annotated[AsyncSession, Depends(async_get_serving_db)],
) -> JSONResponse:
    capture_database_status = await check_database_health(db=capture_db)
    LOGGER.debug("Capture database health check status: %s", capture_database_status)
    serving_database_status = await check_database_health(db=serving_db)
    LOGGER.debug("Serving database health check status: %s", serving_database_status)

    redis_cache_status = await resolve_redis_component_status(enabled=settings.REDIS_CACHE_ENABLED, client=cache.client)
    redis_queue_status = await resolve_redis_component_status(enabled=settings.REDIS_QUEUE_ENABLED, client=queue.pool)
    redis_rate_limit_status = await resolve_redis_component_status(
        enabled=settings.REDIS_RATE_LIMIT_ENABLED,
        client=rate_limiter.client,
    )

    enabled_redis_statuses = [
        status_
        for status_ in [redis_cache_status, redis_queue_status, redis_rate_limit_status]
        if status_ != "disabled"
    ]
    redis_status = (
        "disabled"
        if not enabled_redis_statuses
        else STATUS_HEALTHY
        if all(status_ == STATUS_HEALTHY for status_ in enabled_redis_statuses)
        else STATUS_UNHEALTHY
    )

    overall_status = STATUS_HEALTHY if capture_database_status and serving_database_status else STATUS_UNHEALTHY
    if redis_status == STATUS_UNHEALTHY:
        overall_status = STATUS_UNHEALTHY

    http_status = status.HTTP_200_OK if overall_status == STATUS_HEALTHY else status.HTTP_503_SERVICE_UNAVAILABLE

    response = {
        "status": overall_status,
        "environment": settings.ENVIRONMENT.value,
        "version": settings.APP_VERSION,
        "app": STATUS_HEALTHY,
        "capture_database": STATUS_HEALTHY if capture_database_status else STATUS_UNHEALTHY,
        "serving_database": STATUS_HEALTHY if serving_database_status else STATUS_UNHEALTHY,
        "redis": redis_status,
        "redis_cache": redis_cache_status,
        "redis_queue": redis_queue_status,
        "redis_rate_limit": redis_rate_limit_status,
        "timestamp": datetime.now(UTC).isoformat(timespec="seconds"),
    }

    return JSONResponse(status_code=http_status, content=response)
