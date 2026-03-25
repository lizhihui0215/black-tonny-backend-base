import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..app.core.config import settings
from ..app.core.db.serving_database import serving_session
from ..app.core.security import get_password_hash
from ..app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_first_superuser(session: AsyncSession) -> User:
    query = select(User).where(User.email == settings.ADMIN_EMAIL)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is not None:
        logger.info("Admin user %s already exists.", settings.ADMIN_USERNAME)
        return user

    user = User(
        name=settings.ADMIN_NAME,
        email=settings.ADMIN_EMAIL,
        username=settings.ADMIN_USERNAME,
        hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
        is_superuser=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    logger.info("Admin user %s created successfully.", settings.ADMIN_USERNAME)
    return user


async def main() -> None:
    async with serving_session() as session:
        await create_first_superuser(session)


if __name__ == "__main__":
    asyncio.run(main())
