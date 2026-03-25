from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import settings
from ..core.db.serving_database import async_get_serving_db
from ..core.exceptions.http_exceptions import ForbiddenException, RateLimitException, UnauthorizedException
from ..core.logger import logging
from ..core.schemas import TokenData
from ..core.security import TokenType, oauth2_scheme, verify_token
from ..core.utils.rate_limit import rate_limiter
from ..crud.crud_rate_limit import crud_rate_limits
from ..crud.crud_tier import crud_tiers
from ..crud.crud_users import crud_users
from ..schemas.rate_limit import RateLimitRead, sanitize_path
from ..schemas.tier import TierRead

logger = logging.getLogger(__name__)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(async_get_serving_db)],
) -> dict[str, Any]:
    token_data = await verify_token(token, TokenType.ACCESS, db)
    if token_data is None:
        raise UnauthorizedException("User not authenticated.")

    if "@" in token_data.username_or_email:
        user = await crud_users.get(db=db, email=token_data.username_or_email, is_deleted=False)
    else:
        user = await crud_users.get(db=db, username=token_data.username_or_email, is_deleted=False)

    if user:
        return user

    raise UnauthorizedException("User not authenticated.")


async def get_optional_user(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_serving_db)],
) -> dict[str, Any] | None:
    token = request.headers.get("Authorization")
    if not token:
        return None

    try:
        token_type, _, token_value = token.partition(" ")
        if token_type.lower() != "bearer" or not token_value:
            return None

        token_data: TokenData | None = await verify_token(token_value, TokenType.ACCESS, db)
        if token_data is None:
            return None

        return await get_current_user(token_value, db=db)

    except HTTPException:
        return None


async def get_current_superuser(current_user: Annotated[dict[str, Any], Depends(get_current_user)]) -> dict[str, Any]:
    if not current_user["is_superuser"]:
        raise ForbiddenException("You do not have enough privileges.")

    return current_user


async def rate_limiter_dependency(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_serving_db)],
    user: dict[str, Any] | None = Depends(get_optional_user),
) -> None:
    if not settings.REDIS_RATE_LIMIT_ENABLED:
        return

    path = sanitize_path(request.url.path)
    if user:
        user_id = user["id"]
        tier = await crud_tiers.get(db, id=user["tier_id"], schema_to_select=TierRead)
        if tier:
            rate_limit = await crud_rate_limits.get(
                db=db,
                tier_id=tier["id"],
                path=path,
                schema_to_select=RateLimitRead,
            )
            if rate_limit:
                limit, period = rate_limit["limit"], rate_limit["period"]
            else:
                logger.warning(
                    "User %s with tier '%s' has no specific rate limit for path '%s'. Applying default rate limit.",
                    user_id,
                    tier["name"],
                    path,
                )
                limit, period = settings.DEFAULT_RATE_LIMIT_LIMIT, settings.DEFAULT_RATE_LIMIT_PERIOD
        else:
            logger.warning("User %s has no assigned tier. Applying default rate limit.", user_id)
            limit, period = settings.DEFAULT_RATE_LIMIT_LIMIT, settings.DEFAULT_RATE_LIMIT_PERIOD
    else:
        user_id = request.client.host if request.client else "unknown"
        limit, period = settings.DEFAULT_RATE_LIMIT_LIMIT, settings.DEFAULT_RATE_LIMIT_PERIOD

    try:
        is_limited = await rate_limiter.is_rate_limited(
            db=db,
            user_id=user_id,
            path=path,
            limit=limit,
            period=period,
        )
    except Exception as exc:
        logger.exception("Rate limit backend unavailable for user %s on path %s: %s", user_id, path, exc)
        return

    if is_limited:
        raise RateLimitException("Rate limit exceeded.")
