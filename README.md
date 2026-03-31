# Black Tonny Backend Base

Clean FastAPI dual-database base repository bootstrapped from `FastAPI-boilerplate`.

This repository is intentionally restrained:
- no admin
- no runtime demo business modules
- only a minimal runtime surface

What remains is the long-term base:
- FastAPI app startup and router aggregation
- config and logging
- `capture` / `serving` dual-database skeleton
- Redis cache layer, Redis-backed rate limiting, Redis-backed job queue, and client cache middleware
- basic `health` / `ready`
- worker settings and optional scheduled-job skeleton
- serving-db-backed `login` / `refresh` / `logout` auth flow
- boilerplate-style `users` / `tiers` / `rate_limits` runtime APIs on the serving side
- preserved `exceptions` / `utils` / `worker` extension packages
- preserved `api/dependencies.py` as a shared auth dependency location
- Alembic baseline
- isolated transition reference patterns under `src/examples/` for later migration work
- an in-place `login` chain under `src/app` to preserve directory/style consistency

## Documentation

Start with the [docs index](./docs/README.md).

Current formal docs:
- [docs/runtime-boundaries.md](./docs/runtime-boundaries.md)
- [docs/capture-serving-boundary.md](./docs/capture-serving-boundary.md)
- [docs/capture-minimal-boundary.md](./docs/capture-minimal-boundary.md)
- [docs/transform-input-boundary.md](./docs/transform-input-boundary.md)
- [docs/admitted-transform-input-boundary.md](./docs/admitted-transform-input-boundary.md)
- [docs/transform-readiness-boundary.md](./docs/transform-readiness-boundary.md)
- [docs/transform-state-transition-boundary.md](./docs/transform-state-transition-boundary.md)
- [docs/capture-batch-field-semantics.md](./docs/capture-batch-field-semantics.md)
- [docs/transform-rule-set-questions.md](./docs/transform-rule-set-questions.md)

Planning, reference, and archive material stays linked from [docs/README.md](./docs/README.md).

Current capture already has a minimal formal surface and formal capture docs.
For the current capture state and reading path, start from [docs/README.md](./docs/README.md) and the formal capture docs linked there.

Current research support remains a minimal formal surface only.
For the current state and reading path, use the research support entries linked from [docs/README.md](./docs/README.md).

## Migration Guardrails

`black-tonny-backend-base` is the only source of truth for ongoing backend migration work.

The current migration boundary stays explicit:
- do not copy whole directories from the legacy repo
- do not migrate legacy `app/services`
- do not migrate legacy `scripts`
- do not wire `capture` into runtime business APIs
- do not wire `research` into runtime
- do not change public API behavior as part of documentation work

Current long-term rules:
- business APIs read `serving`, not `capture`
- reference and archive docs do not define runtime behavior
- future migration work should land in the base layering instead of recreating a flat service-heavy structure
- legacy planning material remains planning-only unless it is rewritten into the formal docs listed above

## Quick Start

```bash
python setup.py local
cp src/.env.example src/.env
```

Update `src/.env` with your database URLs, then run:

```bash
docker compose up
```

Or run locally without Docker:

```bash
uv sync
uv run uvicorn src.app.main:app --reload
```

Default docs URL:

```text
http://127.0.0.1:8000/docs
```

## Serving Startup Checklist

From a clean checkout, the shortest serving-side path is:

```bash
python setup.py local
cp src/.env.example src/.env
docker compose up
cd src && uv run alembic -c alembic_serving.ini upgrade head
cd ..
uv run python -m src.scripts.seed_serving_baseline
```

Then you can:
- sign in with `ADMIN_USERNAME` / `ADMIN_PASSWORD`
- create or inspect tiers and rate limits through the runtime API
- enable the `queue` profile only when Redis-backed queue or schedule behavior is needed

## Environment Variables

Required database settings:

```text
CAPTURE_DB_URL=postgresql+asyncpg://...
SERVING_DB_URL=postgresql+asyncpg://...
```

Auth and Redis settings:

```text
SECRET_KEY=change-this-secret-key-to-32-bytes-min
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
COOKIE_SECURE=false|true
COOKIE_SAMESITE=lax|strict|none
COOKIE_PATH=/
# COOKIE_DOMAIN=example.com
ADMIN_NAME=admin
ADMIN_EMAIL=admin@admin.com
ADMIN_USERNAME=admin
ADMIN_PASSWORD=!Ch4ng3Th1sP4ssW0rd!
TIER_NAME=free
REDIS_CACHE_ENABLED=false
REDIS_CACHE_HOST=redis
REDIS_CACHE_PORT=6379
REDIS_CACHE_DB=0
# REDIS_CACHE_PASSWORD=
REDIS_CACHE_SSL=false
REDIS_QUEUE_ENABLED=false
REDIS_QUEUE_HOST=redis
REDIS_QUEUE_PORT=6379
REDIS_QUEUE_DB=0
# REDIS_QUEUE_PASSWORD=
REDIS_QUEUE_SSL=false
CLIENT_CACHE_MAX_AGE=60
REDIS_RATE_LIMIT_ENABLED=false
REDIS_RATE_LIMIT_HOST=redis
REDIS_RATE_LIMIT_PORT=6379
REDIS_RATE_LIMIT_DB=0
# REDIS_RATE_LIMIT_PASSWORD=
REDIS_RATE_LIMIT_SSL=false
DEFAULT_RATE_LIMIT_LIMIT=10
DEFAULT_RATE_LIMIT_PERIOD=3600
WORKER_SCHEDULE_ENABLED=false
```

When Redis-backed features are disabled, `/api/v1/ready` returns `redis=disabled`.
When cache, queue, or rate limiting is enabled, `/api/v1/ready` requires Redis to be healthy.
`/api/v1/ready` also reports `redis_cache`, `redis_queue`, and `redis_rate_limit` separately so split Redis failures are visible.

Other important settings:

```text
ENVIRONMENT=local|staging|production
ALEMBIC_DB_TARGET=capture|serving
```

`ALEMBIC_DB_TARGET` is only needed for generic Alembic tooling. Day-to-day migration commands should prefer
`alembic_capture.ini` or `alembic_serving.ini`.
For local browser testing, keep `COOKIE_SECURE=false`. Set it to `true` behind HTTPS in staging and production.
For managed Redis or shared Redis instances, use the `*_DB`, `*_PASSWORD`, and `*_SSL` settings to keep cache, queue,
and rate-limit traffic isolated without changing code.

## Migrations

Run migrations against the capture database:

```bash
cd src
uv run alembic -c alembic_capture.ini upgrade head
```

Run migrations against the serving database:

```bash
cd src
uv run alembic -c alembic_serving.ini upgrade head
```

The serving side includes the baseline auth / user / tier / rate-limit migration.
The capture side now includes the minimal formal capture boundary tables:
- `capture_batches`
- `capture_endpoint_payloads`

These capture tables establish a persistence boundary and migration targets only.
They are not mounted into runtime routers and do not change current API behavior.
The generic [alembic.ini](./src/alembic.ini) keeps both revision branches visible, but the target-specific ini files are
the safe default because they keep capture
and serving revision paths separate.

## Serving Bootstrap

After the serving migration is applied, you can seed the minimal serving baseline:

```bash
uv run python -m src.scripts.create_first_tier
uv run python -m src.scripts.create_first_superuser
```

Or run both with one command:

```bash
uv run python -m src.scripts.seed_serving_baseline
```

The baseline seed intentionally stays small:
- create the first tier from `TIER_NAME`
- create the first superuser from `ADMIN_*`
- assign that tier to the first superuser if it is not already assigned

Rate-limit rows are not auto-seeded because they are policy-specific. Add them through the runtime API once you know the
real serving limits you want.

## Transition Reference Patterns

Transition reference code lives under `src/examples/`:

- `capture_crud_reference`
- `serving_read_reference`

See [src/examples/README.md](./src/examples/README.md) for the ownership boundary of this directory.

These files are intentionally isolated:
- they are not mounted into runtime routers
- they do not appear in `/docs`
- they are not imported by the app
- they are not the long-term formal home for capture or serving boundaries

Current ownership stays explicit:
- the formal capture boundary lives under `src/app/**`, `src/migrations/**`, and the formal docs linked from [docs/README.md](./docs/README.md)
- `src/examples/**` is a transition reference-pattern area only
- research notes, traceability samples, and troubleshooting templates belong under `docs/reference/**`, not under formal runtime modules

The auth chain is kept in the original app layout:

- `src/app/api/v1/login.py`
- `src/app/api/v1/logout.py`
- `src/app/core/security.py`
- `src/app/crud/crud_users.py`
- `src/app/models/user.py`
- `src/app/core/db/token_blacklist.py`
- `src/app/core/db/crud_token_blacklist.py`

This chain is implemented as a real runtime auth capability and uses the serving database session provider.

The queue and worker chain is also preserved in the original locations:

- `src/app/api/v1/tasks.py`
- `src/app/core/utils/queue.py`
- `src/app/core/worker/functions.py`
- `src/app/core/worker/settings.py`

Queue processing is optional. Enable `REDIS_QUEUE_ENABLED=true` to expose a working Redis-backed queue path, and
enable `WORKER_SCHEDULE_ENABLED=true` if you want the worker to include the reference cron skeleton.
The worker cron skeleton uses ARQ's unique cron mode with a stable job ID so multiple worker replicas do not enqueue
the same scheduled reference job repeatedly.

The `web` service no longer hard-depends on the local `redis` container. This keeps Redis optional for base startup.
Redis is started through the `queue` profile together with the worker path.

## Worker And Queue Runbook

Start just the web stack:

```bash
docker compose up
```

Start the optional queue stack:

```bash
docker compose --profile queue up worker
```

If the web app enables Redis-backed cache or Redis-backed rate limiting, start Redis with the queue profile as well:

```bash
docker compose --profile queue up redis web
```

Run the worker without Docker:

```bash
uv run arq src.app.core.worker.settings.WorkerSettings
```

Operational defaults:
- keep `REDIS_QUEUE_ENABLED=true` only when the queue path is intended to be live
- keep `WORKER_SCHEDULE_ENABLED=true` only on worker deployments that should run the reference cron skeleton
- `/api/v1/ready` reports `redis_cache`, `redis_queue`, and `redis_rate_limit` separately so feature-specific Redis failures stay visible

## Current Runtime API

- `GET /api/v1/health`
- `GET /api/v1/ready`
- `POST /api/v1/login`
- `POST /api/v1/refresh`
- `POST /api/v1/logout`
- `POST /api/v1/user`
- `GET /api/v1/users`
- `GET /api/v1/user/me/`
- `GET /api/v1/user/{username}`
- `PATCH /api/v1/user/{username}`
- `DELETE /api/v1/user/{username}`
- `DELETE /api/v1/db_user/{username}`
- `GET /api/v1/user/{username}/rate_limits`
- `GET /api/v1/user/{username}/tier`
- `PATCH /api/v1/user/{username}/tier`
- `POST /api/v1/tier`
- `GET /api/v1/tiers`
- `GET /api/v1/tier/{name}`
- `PATCH /api/v1/tier/{name}`
- `DELETE /api/v1/tier/{name}`
- `POST /api/v1/tier/{tier_name}/rate_limit`
- `GET /api/v1/tier/{tier_name}/rate_limits`
- `GET /api/v1/tier/{tier_name}/rate_limit/{id}`
- `PATCH /api/v1/tier/{tier_name}/rate_limit/{id}`
- `DELETE /api/v1/tier/{tier_name}/rate_limit/{id}`
- `POST /api/v1/tasks/task`
- `GET /api/v1/tasks/task/{task_id}`

## License

[`MIT`](./LICENSE.md)
