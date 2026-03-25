import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..app.core.config import settings
from ..app.core.db.serving_database import serving_session
from ..app.models.tier import Tier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_first_tier(session: AsyncSession) -> Tier:
    query = select(Tier).where(Tier.name == settings.TIER_NAME)
    result = await session.execute(query)
    tier = result.scalar_one_or_none()

    if tier is not None:
        logger.info("Tier %s already exists.", settings.TIER_NAME)
        return tier

    tier = Tier(name=settings.TIER_NAME)
    session.add(tier)
    await session.commit()
    await session.refresh(tier)
    logger.info("Tier %s created successfully.", settings.TIER_NAME)
    return tier


async def main() -> None:
    async with serving_session() as session:
        await create_first_tier(session)


if __name__ == "__main__":
    asyncio.run(main())
