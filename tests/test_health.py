import asyncio
from types import SimpleNamespace
from typing import cast

from fastapi import Request
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from src.app.api import router as api_router
from src.app.api.dependencies import get_current_superuser, rate_limiter_dependency
from src.app.core.config import EnvironmentOption, settings
from src.app.core.db.capture_database import async_get_capture_db
from src.app.core.db.serving_database import async_get_serving_db
from src.app.core.security import create_access_token, create_refresh_token
from src.app.core.setup import create_application
from src.app.core.utils import queue
from src.app.core.worker.settings import WorkerSettings
from src.app.main import app
from tests.conftest import build_session_override


def test_health(client) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready_returns_200_when_both_databases_are_healthy(client, healthy_session) -> None:
    app.dependency_overrides[async_get_capture_db] = build_session_override(healthy_session)
    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)

    response = client.get("/api/v1/ready")

    assert response.status_code == 200
    assert response.json()["capture_database"] == "healthy"
    assert response.json()["serving_database"] == "healthy"
    assert response.json()["redis"] == "disabled"
    assert response.json()["redis_cache"] == "disabled"
    assert response.json()["redis_queue"] == "disabled"
    assert response.json()["redis_rate_limit"] == "disabled"


def test_ready_returns_503_when_one_database_is_unhealthy(client, healthy_session, failing_session) -> None:
    app.dependency_overrides[async_get_capture_db] = build_session_override(healthy_session)
    app.dependency_overrides[async_get_serving_db] = build_session_override(failing_session)

    response = client.get("/api/v1/ready")

    assert response.status_code == 503
    assert response.json()["capture_database"] == "healthy"
    assert response.json()["serving_database"] == "unhealthy"


def test_ready_returns_503_when_redis_feature_enabled_but_redis_unavailable(client, healthy_session) -> None:
    app.dependency_overrides[async_get_capture_db] = build_session_override(healthy_session)
    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)

    original_cache_enabled = settings.REDIS_CACHE_ENABLED
    settings.REDIS_CACHE_ENABLED = True
    try:
        response = client.get("/api/v1/ready")
    finally:
        settings.REDIS_CACHE_ENABLED = original_cache_enabled

    assert response.status_code == 503
    assert response.json()["redis"] == "unhealthy"
    assert response.json()["redis_cache"] == "unhealthy"
    assert response.json()["redis_queue"] == "disabled"
    assert response.json()["redis_rate_limit"] == "disabled"


def test_ready_returns_503_when_queue_enabled_but_redis_unavailable(client, healthy_session) -> None:
    app.dependency_overrides[async_get_capture_db] = build_session_override(healthy_session)
    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)

    original_queue_enabled = settings.REDIS_QUEUE_ENABLED
    settings.REDIS_QUEUE_ENABLED = True
    try:
        response = client.get("/api/v1/ready")
    finally:
        settings.REDIS_QUEUE_ENABLED = original_queue_enabled

    assert response.status_code == 503
    assert response.json()["redis"] == "unhealthy"
    assert response.json()["redis_cache"] == "disabled"
    assert response.json()["redis_queue"] == "unhealthy"
    assert response.json()["redis_rate_limit"] == "disabled"


def test_login_route_returns_access_token(client, healthy_session, patch_auth_user, blacklisted_tokens) -> None:
    _ = patch_auth_user, blacklisted_tokens
    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)

    response = client.post(
        "/api/v1/login",
        data={"username": "demouser", "password": "demo-password"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()


def test_refresh_route_returns_access_token(client, healthy_session, patch_auth_user, blacklisted_tokens) -> None:
    _ = patch_auth_user, blacklisted_tokens
    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)
    refresh_token = asyncio.run(create_refresh_token({"sub": "demouser"}))
    client.cookies.set("refresh_token", refresh_token)

    response = client.post("/api/v1/refresh")

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()

    client.cookies.clear()


def test_refresh_route_rejects_deleted_user(client, healthy_session, monkeypatch, blacklisted_tokens) -> None:
    _ = blacklisted_tokens
    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)

    async def fake_missing_user(*_args: object, **_kwargs: object) -> None:
        return None

    monkeypatch.setattr("src.app.core.security.crud_users.get", fake_missing_user)

    refresh_token = asyncio.run(create_refresh_token({"sub": "deleted-user"}))
    client.cookies.set("refresh_token", refresh_token)

    response = client.post("/api/v1/refresh")

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid refresh token."
    client.cookies.clear()


def test_logout_route_blacklists_tokens_and_revokes_refresh(
    client,
    healthy_session,
    patch_auth_user,
    blacklisted_tokens,
) -> None:
    _ = patch_auth_user
    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)
    access_token = asyncio.run(create_access_token({"sub": "demouser"}))
    refresh_token = asyncio.run(create_refresh_token({"sub": "demouser"}))
    client.cookies.set("refresh_token", refresh_token)

    logout_response = client.post(
        "/api/v1/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert logout_response.status_code == 200
    assert logout_response.json() == {"message": "Logged out successfully"}
    assert access_token in blacklisted_tokens
    assert refresh_token in blacklisted_tokens

    client.cookies.set("refresh_token", refresh_token)
    refresh_response = client.post("/api/v1/refresh")

    assert refresh_response.status_code == 401
    assert refresh_response.json()["detail"] == "Invalid refresh token."
    client.cookies.clear()


def test_logout_route_is_idempotent(client, healthy_session, patch_auth_user, monkeypatch) -> None:
    _ = patch_auth_user
    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)

    blacklisted: set[str] = set()

    async def fake_exists(_db: object, token: str) -> bool:
        return token in blacklisted

    async def fake_create(_db: object, object: object) -> dict[str, object]:
        token = getattr(object, "token")
        if token in blacklisted:
            raise IntegrityError("duplicate token", params=None, orig=Exception("duplicate token"))
        blacklisted.add(token)
        return {"id": len(blacklisted), "token": token}

    monkeypatch.setattr("src.app.core.security.crud_token_blacklist.exists", fake_exists)
    monkeypatch.setattr("src.app.core.security.crud_token_blacklist.create", fake_create)

    access_token = asyncio.run(create_access_token({"sub": "demouser"}))
    refresh_token = asyncio.run(create_refresh_token({"sub": "demouser"}))

    client.cookies.set("refresh_token", refresh_token)
    first_response = client.post("/api/v1/logout", headers={"Authorization": f"Bearer {access_token}"})

    client.cookies.set("refresh_token", refresh_token)
    second_response = client.post("/api/v1/logout", headers={"Authorization": f"Bearer {access_token}"})

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert blacklisted == {access_token, refresh_token}
    client.cookies.clear()


def test_logout_route_requires_refresh_cookie(client, healthy_session, patch_auth_user, blacklisted_tokens) -> None:
    _ = patch_auth_user, blacklisted_tokens
    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)
    access_token = asyncio.run(create_access_token({"sub": "demouser"}))

    response = client.post(
        "/api/v1/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Refresh token not found"


def test_docs_require_auth_outside_local_environment() -> None:
    original_environment = settings.ENVIRONMENT
    settings.ENVIRONMENT = EnvironmentOption.STAGING

    try:
        staging_app = create_application(router=api_router, settings=settings)
        with TestClient(staging_app) as staging_client:
            response = staging_client.get("/docs")
    finally:
        settings.ENVIRONMENT = original_environment

    assert response.status_code == 401


def test_write_tier_returns_created_tier(client, healthy_session, monkeypatch) -> None:
    async def override_superuser() -> dict[str, object]:
        return {"id": 1, "is_superuser": True}

    async def fake_exists(*_args: object, **_kwargs: object) -> bool:
        return False

    async def fake_create(*_args: object, **_kwargs: object) -> dict[str, object]:
        return {"id": 1, "name": "free", "created_at": "2026-03-26T00:00:00"}

    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)
    app.dependency_overrides[get_current_superuser] = override_superuser
    monkeypatch.setattr("src.app.api.v1.tiers.crud_tiers.exists", fake_exists)
    monkeypatch.setattr("src.app.api.v1.tiers.crud_tiers.create", fake_create)

    response = client.post("/api/v1/tier", json={"name": "free"})

    assert response.status_code == 201
    assert response.json()["name"] == "free"


def test_write_rate_limit_returns_created_rate_limit(client, healthy_session, monkeypatch) -> None:
    async def override_superuser() -> dict[str, object]:
        return {"id": 1, "is_superuser": True}

    created_payload: dict[str, object] = {}

    async def fake_get_tier(*_args: object, **_kwargs: object) -> dict[str, object]:
        return {"id": 1, "name": "free"}

    async def fake_exists(*_args: object, **_kwargs: object) -> bool:
        return False

    async def fake_create(*_args: object, **kwargs: object) -> dict[str, object]:
        rate_limit_object = kwargs["object"]
        created_payload["path"] = getattr(rate_limit_object, "path")
        return {
            "id": 1,
            "tier_id": 1,
            "name": "api_v1_users:5:60",
            "path": getattr(rate_limit_object, "path"),
            "limit": 5,
            "period": 60,
        }

    app.dependency_overrides[async_get_serving_db] = build_session_override(healthy_session)
    app.dependency_overrides[get_current_superuser] = override_superuser
    monkeypatch.setattr("src.app.api.v1.rate_limits.crud_tiers.get", fake_get_tier)
    monkeypatch.setattr("src.app.api.v1.rate_limits.crud_rate_limits.exists", fake_exists)
    monkeypatch.setattr("src.app.api.v1.rate_limits.crud_rate_limits.create", fake_create)

    response = client.post(
        "/api/v1/tier/free/rate_limit",
        json={"name": "api_v1_users:5:60", "path": "/api/v1/users", "limit": 5, "period": 60},
    )

    assert response.status_code == 201
    assert response.json()["path"] == "api_v1_users"
    assert created_payload["path"] == "api_v1_users"


def test_rate_limiter_dependency_uses_tier_specific_limit(healthy_session, monkeypatch) -> None:
    request = cast(
        Request,
        SimpleNamespace(
            url=SimpleNamespace(path="/api/v1/tasks/task"),
            client=SimpleNamespace(host="127.0.0.1"),
        ),
    )
    captured: dict[str, object] = {}

    async def fake_get_tier(*_args: object, **_kwargs: object) -> dict[str, object]:
        return {"id": 1, "name": "free"}

    async def fake_get_rate_limit(*_args: object, **_kwargs: object) -> dict[str, object]:
        return {"limit": 5, "period": 60}

    async def fake_is_rate_limited(*_args: object, **kwargs: object) -> bool:
        captured.update(kwargs)
        return False

    original_rate_limit_enabled = settings.REDIS_RATE_LIMIT_ENABLED
    settings.REDIS_RATE_LIMIT_ENABLED = True
    monkeypatch.setattr("src.app.api.dependencies.crud_tiers.get", fake_get_tier)
    monkeypatch.setattr("src.app.api.dependencies.crud_rate_limits.get", fake_get_rate_limit)
    monkeypatch.setattr("src.app.api.dependencies.rate_limiter.is_rate_limited", fake_is_rate_limited)

    try:
        asyncio.run(
            rate_limiter_dependency(
                request=request,
                db=healthy_session,
                user={"id": 1, "tier_id": 1},
            )
        )
    finally:
        settings.REDIS_RATE_LIMIT_ENABLED = original_rate_limit_enabled

    assert captured["path"] == "api_v1_tasks_task"
    assert captured["limit"] == 5
    assert captured["period"] == 60


def test_rate_limiter_dependency_degrades_open_when_backend_errors(healthy_session, monkeypatch) -> None:
    request = cast(
        Request,
        SimpleNamespace(
            url=SimpleNamespace(path="/api/v1/tasks/task"),
            client=SimpleNamespace(host="127.0.0.1"),
        ),
    )

    async def fake_is_rate_limited(*_args: object, **_kwargs: object) -> bool:
        raise RuntimeError("redis unavailable")

    original_rate_limit_enabled = settings.REDIS_RATE_LIMIT_ENABLED
    settings.REDIS_RATE_LIMIT_ENABLED = True
    monkeypatch.setattr("src.app.api.dependencies.rate_limiter.is_rate_limited", fake_is_rate_limited)

    try:
        asyncio.run(rate_limiter_dependency(request=request, db=healthy_session, user=None))
    finally:
        settings.REDIS_RATE_LIMIT_ENABLED = original_rate_limit_enabled


def test_create_task_returns_503_when_queue_is_disabled(client) -> None:
    response = client.post("/api/v1/tasks/task", params={"message": "hello"})

    assert response.status_code == 503
    assert response.json()["detail"] == "Queue is disabled"


def test_create_task_returns_job_id_when_queue_is_available(client) -> None:
    class FakeJob:
        job_id = "job-123"

    class FakeQueue:
        async def enqueue_job(self, *_args: object, **_kwargs: object) -> FakeJob:
            return FakeJob()

    original_queue_enabled = settings.REDIS_QUEUE_ENABLED
    original_queue_pool = queue.pool
    settings.REDIS_QUEUE_ENABLED = True
    queue.pool = FakeQueue()  # type: ignore[assignment]

    try:
        response = client.post("/api/v1/tasks/task", params={"message": "hello"})
    finally:
        settings.REDIS_QUEUE_ENABLED = original_queue_enabled
        queue.pool = original_queue_pool

    assert response.status_code == 201
    assert response.json() == {"id": "job-123"}


def test_create_task_returns_503_when_queue_backend_errors(client) -> None:
    class BrokenQueue:
        async def enqueue_job(self, *_args: object, **_kwargs: object) -> None:
            raise RuntimeError("queue unavailable")

    original_queue_enabled = settings.REDIS_QUEUE_ENABLED
    original_queue_pool = queue.pool
    settings.REDIS_QUEUE_ENABLED = True
    queue.pool = BrokenQueue()  # type: ignore[assignment]

    try:
        response = client.post("/api/v1/tasks/task", params={"message": "hello"})
    finally:
        settings.REDIS_QUEUE_ENABLED = original_queue_enabled
        queue.pool = original_queue_pool

    assert response.status_code == 503
    assert response.json()["detail"] == "Queue backend unavailable"


def test_get_task_returns_job_info_when_queue_is_available(client, monkeypatch) -> None:
    class FakeQueue:
        async def enqueue_job(self, *_args: object, **_kwargs: object) -> None:
            return None

    class FakeArqJob:
        def __init__(self, task_id: str, _pool: object) -> None:
            self.task_id = task_id

        async def info(self) -> SimpleNamespace:
            return SimpleNamespace(job_id=self.task_id, function="sample_background_task")

    original_queue_enabled = settings.REDIS_QUEUE_ENABLED
    original_queue_pool = queue.pool
    settings.REDIS_QUEUE_ENABLED = True
    queue.pool = FakeQueue()  # type: ignore[assignment]
    monkeypatch.setattr("src.app.api.v1.tasks.ArqJob", FakeArqJob)

    try:
        response = client.get("/api/v1/tasks/task/job-123")
    finally:
        settings.REDIS_QUEUE_ENABLED = original_queue_enabled
        queue.pool = original_queue_pool

    assert response.status_code == 200
    assert response.json()["job_id"] == "job-123"
    assert response.json()["function"] == "sample_background_task"


def test_get_task_returns_503_when_queue_backend_errors(client, monkeypatch) -> None:
    class FakeQueue:
        async def enqueue_job(self, *_args: object, **_kwargs: object) -> None:
            return None

    class BrokenArqJob:
        def __init__(self, _task_id: str, _pool: object) -> None:
            pass

        async def info(self) -> None:
            raise RuntimeError("queue unavailable")

    original_queue_enabled = settings.REDIS_QUEUE_ENABLED
    original_queue_pool = queue.pool
    settings.REDIS_QUEUE_ENABLED = True
    queue.pool = FakeQueue()  # type: ignore[assignment]
    monkeypatch.setattr("src.app.api.v1.tasks.ArqJob", BrokenArqJob)

    try:
        response = client.get("/api/v1/tasks/task/job-123")
    finally:
        settings.REDIS_QUEUE_ENABLED = original_queue_enabled
        queue.pool = original_queue_pool

    assert response.status_code == 503
    assert response.json()["detail"] == "Queue backend unavailable"


def test_worker_schedule_uses_unique_cron_job_id() -> None:
    if not WorkerSettings.cron_jobs:
        assert settings.WORKER_SCHEDULE_ENABLED is False
        return

    cron_job = WorkerSettings.cron_jobs[0]
    assert cron_job.unique is True
    assert cron_job.job_id == "cron:sample_scheduled_task"
