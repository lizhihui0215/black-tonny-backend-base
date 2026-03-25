import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from ..app.core.db.serving_database import serving_session
from .create_first_superuser import create_first_superuser
from .create_first_tier import create_first_tier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_serving_baseline(session: AsyncSession) -> None:
    tier = await create_first_tier(session)
    user = await create_first_superuser(session)

    if user.tier_id is None:
        user.tier_id = tier.id
        session.add(user)
        await session.commit()
        await session.refresh(user)
        logger.info("Assigned tier %s to admin user %s.", tier.name, user.username)


async def main() -> None:
    async with serving_session() as session:
        await seed_serving_baseline(session)


if __name__ == "__main__":
    asyncio.run(main())
