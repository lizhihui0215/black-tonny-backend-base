from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Response
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.config import settings
from ...core.db.serving_database import async_get_serving_db
from ...core.exceptions.http_exceptions import UnauthorizedException
from ...core.security import blacklist_tokens, oauth2_scheme

router = APIRouter(tags=["login"])


@router.post("/logout")
async def logout(
    response: Response,
    access_token: str = Depends(oauth2_scheme),
    refresh_token: Optional[str] = Cookie(None, alias="refresh_token"),
    db: AsyncSession = Depends(async_get_serving_db),
) -> dict[str, str]:
    try:
        if not refresh_token:
            raise UnauthorizedException("Refresh token not found")

        await blacklist_tokens(access_token=access_token, refresh_token=refresh_token, db=db)
        cookie_domain = settings.COOKIE_DOMAIN or None
        response.delete_cookie(
            key="refresh_token",
            path=settings.COOKIE_PATH,
            domain=cookie_domain,
            secure=settings.COOKIE_SECURE,
            httponly=True,
            samesite=settings.COOKIE_SAMESITE,
        )

        return {"message": "Logged out successfully"}

    except JWTError:
        raise UnauthorizedException("Invalid token.")
