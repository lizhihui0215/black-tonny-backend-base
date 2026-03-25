from collections.abc import AsyncGenerator, Generator
from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.security import get_password_hash
from src.app.main import app


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, Any, None]:
    with TestClient(app) as _client:
        yield _client


@pytest.fixture(autouse=True)
def clear_dependency_overrides() -> Generator[None, None, None]:
    app.dependency_overrides = {}
    yield
    app.dependency_overrides = {}


@pytest.fixture
def healthy_session() -> Mock:
    session = Mock(spec=AsyncSession)
    session.execute = AsyncMock(return_value=1)
    return session


@pytest.fixture
def failing_session() -> Mock:
    session = Mock(spec=AsyncSession)
    session.execute = AsyncMock(side_effect=RuntimeError("database unavailable"))
    return session


def build_session_override(session: AsyncSession):
    async def _override() -> AsyncGenerator[AsyncSession, None]:
        yield session

    return _override


@pytest.fixture
def auth_user() -> dict[str, Any]:
    return {
        "id": 1,
        "name": "Demo User",
        "username": "demouser",
        "email": "demouser@example.com",
        "hashed_password": get_password_hash("demo-password"),
        "profile_image_url": "https://www.profileimageurl.com",
        "uuid": UUID("12345678-1234-5678-1234-567812345678"),
        "is_deleted": False,
        "is_superuser": False,
        "tier_id": None,
    }


@pytest.fixture
def blacklisted_tokens(monkeypatch: pytest.MonkeyPatch) -> set[str]:
    blacklisted: set[str] = set()

    async def fake_exists(_db: AsyncSession, token: str) -> bool:
        return token in blacklisted

    async def fake_create(_db: AsyncSession, object: Any) -> dict[str, Any]:
        blacklisted.add(object.token)
        return {"id": len(blacklisted), "token": object.token, "expires_at": object.expires_at}

    monkeypatch.setattr("src.app.core.security.crud_token_blacklist.exists", fake_exists)
    monkeypatch.setattr("src.app.core.security.crud_token_blacklist.create", fake_create)

    return blacklisted


@pytest.fixture
def patch_auth_user(monkeypatch: pytest.MonkeyPatch, auth_user: dict[str, Any]) -> dict[str, Any]:
    async def fake_get(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
        return auth_user

    monkeypatch.setattr("src.app.core.security.crud_users.get", fake_get)
    monkeypatch.setattr("src.app.api.dependencies.crud_users.get", fake_get)

    return auth_user
