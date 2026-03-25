from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.scripts.create_first_superuser import create_first_superuser
from src.scripts.create_first_tier import create_first_tier
from src.scripts.seed_serving_baseline import seed_serving_baseline


@pytest.fixture
def script_session() -> Mock:
    session = Mock(spec=AsyncSession)
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.add = Mock()
    return session


def build_scalar_result(value: object) -> object:
    return SimpleNamespace(scalar_one_or_none=lambda: value)


@pytest.mark.asyncio
async def test_create_first_superuser_returns_existing_user(script_session) -> None:
    existing_user = SimpleNamespace(email="admin@admin.com", username="admin")
    script_session.execute.return_value = build_scalar_result(existing_user)

    user = await create_first_superuser(script_session)

    assert user is existing_user
    script_session.add.assert_not_called()
    script_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_first_superuser_creates_user_when_missing(script_session) -> None:
    script_session.execute.return_value = build_scalar_result(None)

    user = await create_first_superuser(script_session)

    assert user.username == "admin"
    assert user.is_superuser is True
    script_session.add.assert_called_once()
    script_session.commit.assert_awaited_once()
    script_session.refresh.assert_awaited_once_with(user)


@pytest.mark.asyncio
async def test_create_first_tier_returns_existing_tier(script_session) -> None:
    existing_tier = SimpleNamespace(name="free")
    script_session.execute.return_value = build_scalar_result(existing_tier)

    tier = await create_first_tier(script_session)

    assert tier is existing_tier
    script_session.add.assert_not_called()
    script_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_first_tier_creates_tier_when_missing(script_session) -> None:
    script_session.execute.return_value = build_scalar_result(None)

    tier = await create_first_tier(script_session)

    assert tier.name == "free"
    script_session.add.assert_called_once()
    script_session.commit.assert_awaited_once()
    script_session.refresh.assert_awaited_once_with(tier)


@pytest.mark.asyncio
async def test_seed_serving_baseline_assigns_default_tier(monkeypatch, script_session) -> None:
    tier = SimpleNamespace(id=1, name="free")
    user = SimpleNamespace(username="admin", tier_id=None)

    async def fake_create_first_tier(_session: AsyncSession) -> object:
        return tier

    async def fake_create_first_superuser(_session: AsyncSession) -> object:
        return user

    monkeypatch.setattr("src.scripts.seed_serving_baseline.create_first_tier", fake_create_first_tier)
    monkeypatch.setattr("src.scripts.seed_serving_baseline.create_first_superuser", fake_create_first_superuser)

    await seed_serving_baseline(script_session)

    assert user.tier_id == 1
    script_session.add.assert_called_once_with(user)
    script_session.commit.assert_awaited_once()
    script_session.refresh.assert_awaited_once_with(user)


@pytest.mark.asyncio
async def test_seed_serving_baseline_keeps_existing_tier(monkeypatch, script_session) -> None:
    tier = SimpleNamespace(id=1, name="free")
    user = SimpleNamespace(username="admin", tier_id=3)

    async def fake_create_first_tier(_session: AsyncSession) -> object:
        return tier

    async def fake_create_first_superuser(_session: AsyncSession) -> object:
        return user

    monkeypatch.setattr("src.scripts.seed_serving_baseline.create_first_tier", fake_create_first_tier)
    monkeypatch.setattr("src.scripts.seed_serving_baseline.create_first_superuser", fake_create_first_superuser)

    await seed_serving_baseline(script_session)

    assert user.tier_id == 3
    script_session.add.assert_not_called()
    script_session.commit.assert_not_awaited()
    script_session.refresh.assert_not_awaited()
