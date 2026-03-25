from typing import Any, cast

from src.app.api.dependencies import get_current_superuser, get_current_user
from src.app.core.config import settings
from src.app.core.db.serving_database import async_get_serving_db
from src.app.main import app
from tests.conftest import build_session_override


def test_login_route_uses_configured_cookie_settings(
    client,
    healthy_session,
    patch_auth_user,
    blacklisted_tokens,
) -> None:
    _ = patch_auth_user, blacklisted_tokens
    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)

    original_cookie_secure = settings.COOKIE_SECURE
    original_cookie_samesite = settings.COOKIE_SAMESITE
    original_cookie_path = settings.COOKIE_PATH
    original_cookie_domain = settings.COOKIE_DOMAIN
    settings.COOKIE_SECURE = False
    settings.COOKIE_SAMESITE = "strict"
    settings.COOKIE_PATH = "/auth"
    settings.COOKIE_DOMAIN = "example.com"

    try:
        response = client.post(
            "/api/v1/login",
            data={"username": "demouser", "password": "demo-password"},
        )
    finally:
        settings.COOKIE_SECURE = original_cookie_secure
        settings.COOKIE_SAMESITE = original_cookie_samesite
        settings.COOKIE_PATH = original_cookie_path
        settings.COOKIE_DOMAIN = original_cookie_domain

    assert response.status_code == 200
    set_cookie_header = response.headers["set-cookie"]
    assert "Path=/auth" in set_cookie_header
    assert "SameSite=strict" in set_cookie_header
    assert "Domain=example.com" in set_cookie_header
    assert "Secure" not in set_cookie_header


def test_write_user_returns_created_user(client, healthy_session, monkeypatch) -> None:
    async def fake_exists(*_args: object, **_kwargs: object) -> bool:
        return False

    async def fake_create(*_args: object, **_kwargs: object) -> dict[str, object]:
        return {
            "id": 1,
            "name": "Demo User",
            "username": "demouser",
            "email": "demouser@example.com",
            "profile_image_url": "https://www.profileimageurl.com",
            "tier_id": None,
        }

    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)
    monkeypatch.setattr("src.app.api.v1.users.crud_users.exists", fake_exists)
    monkeypatch.setattr("src.app.api.v1.users.crud_users.create", fake_create)

    response = client.post(
        "/api/v1/user",
        json={
            "name": "Demo User",
            "username": "demouser",
            "email": "demouser@example.com",
            "password": "Str1ngst!",
        },
    )

    assert response.status_code == 201
    assert response.json()["username"] == "demouser"


def test_read_users_me_returns_current_user(client) -> None:
    async def override_current_user() -> dict[str, Any]:
        return {
            "id": 1,
            "name": "Demo User",
            "username": "demouser",
            "email": "demouser@example.com",
            "profile_image_url": "https://www.profileimageurl.com",
            "tier_id": None,
        }

    app.dependency_overrides[get_current_user] = override_current_user

    response = client.get("/api/v1/user/me/")

    assert response.status_code == 200
    assert response.json()["email"] == "demouser@example.com"


def test_patch_user_tier_returns_success(client, healthy_session, monkeypatch) -> None:
    async def override_superuser() -> dict[str, object]:
        return {"id": 1, "is_superuser": True}

    async def fake_get_user(*_args: object, **_kwargs: object) -> dict[str, object]:
        return {
            "id": 1,
            "name": "Demo User",
            "username": "demouser",
            "email": "demouser@example.com",
            "profile_image_url": "https://www.profileimageurl.com",
            "tier_id": None,
        }

    async def fake_get_tier(*_args: object, **_kwargs: object) -> dict[str, object]:
        return {"id": 2, "name": "vip"}

    updated_payload: dict[str, object] = {}

    async def fake_update(*_args: object, **kwargs: object) -> dict[str, object]:
        update_values = cast(dict[str, object], kwargs["object"])
        updated_payload.update(update_values)
        return {"message": "updated"}

    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)
    app.dependency_overrides[get_current_superuser] = override_superuser
    monkeypatch.setattr("src.app.api.v1.users.crud_users.get", fake_get_user)
    monkeypatch.setattr("src.app.api.v1.users.crud_tiers.get", fake_get_tier)
    monkeypatch.setattr("src.app.api.v1.users.crud_users.update", fake_update)

    response = client.patch("/api/v1/user/demouser/tier", json={"tier_id": 2})

    assert response.status_code == 200
    assert response.json()["message"] == "User Demo User Tier updated"
    assert updated_payload == {"tier_id": 2}


def test_read_user_rate_limits_returns_joined_payload(client, healthy_session, monkeypatch) -> None:
    async def override_superuser() -> dict[str, object]:
        return {"id": 1, "is_superuser": True}

    async def fake_get_user(*_args: object, **_kwargs: object) -> dict[str, object]:
        return {
            "id": 1,
            "name": "Demo User",
            "username": "demouser",
            "email": "demouser@example.com",
            "profile_image_url": "https://www.profileimageurl.com",
            "tier_id": 3,
        }

    async def fake_get_tier(*_args: object, **_kwargs: object) -> dict[str, object]:
        return {"id": 3, "name": "free"}

    async def fake_get_multi(*_args: object, **_kwargs: object) -> dict[str, object]:
        return {
            "data": [
                {
                    "id": 1,
                    "tier_id": 3,
                    "name": "api_v1_users:10:3600",
                    "path": "api_v1_users",
                    "limit": 10,
                    "period": 3600,
                }
            ]
        }

    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)
    app.dependency_overrides[get_current_superuser] = override_superuser
    monkeypatch.setattr("src.app.api.v1.users.crud_users.get", fake_get_user)
    monkeypatch.setattr("src.app.api.v1.users.crud_tiers.get", fake_get_tier)
    monkeypatch.setattr("src.app.api.v1.users.crud_rate_limits.get_multi", fake_get_multi)

    response = client.get("/api/v1/user/demouser/rate_limits")

    assert response.status_code == 200
    assert response.json()["tier_rate_limits"][0]["path"] == "api_v1_users"
