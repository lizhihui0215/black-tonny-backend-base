# Runtime Boundaries

This document defines the current runtime structure and migration guardrails for `black-tonny-backend-base`.

For the docs entrypoint, use [docs/README.md](./README.md).
For the database split, use [capture-serving-boundary.md](./capture-serving-boundary.md).
For the minimal capture persistence boundary, use [capture-minimal-boundary.md](./capture-minimal-boundary.md).

## Repository Role

`black-tonny-backend-base` is a restrained backend base repository.

Its current runtime keeps only the capabilities that already exist in this repository:
- health and readiness probes
- serving-backed auth endpoints
- serving-backed `users`, `tiers`, and `rate_limits` APIs
- optional queue-backed task endpoints
- optional Redis-backed cache, queue, and rate-limiting infrastructure

It does not claim that legacy business modules, capture flows, or research pipelines have already landed here.
The repository now also contains a minimal capture persistence boundary, but it is not mounted into runtime routes.
That capture boundary belongs to the formal mainline, not to `src/examples/` and not to research/reference material.

## Current Route Organization

The runtime route tree is composed as:
- `src/app/api/__init__.py` -> `/api`
- `src/app/api/v1/__init__.py` -> `/api/v1`

The current route groups are:
- `health` and `ready`
- `login`, `refresh`, and `logout`
- `users`
- `tiers`
- `rate_limits`
- `tasks`

This is the current base route surface.
Legacy runtime APIs from `black-tonny-backend` are not part of the current repository truth unless they are explicitly reintroduced later.

## Current Package Boundaries

- `src/app/api/`
  - route composition and dependency wiring
- `src/app/core/`
  - config, database setup, security, health, logging, shared utilities, and worker settings
- `src/app/models/`
  - current serving runtime ORM models plus minimal capture persistence models
- `src/app/schemas/`
  - current request and response models plus capture CRUD schemas and read/write helper types
- `src/app/crud/`
  - current persistence access for serving-side runtime tables and the minimal capture persistence boundary
- `src/app/middleware/`
  - runtime middleware
- `src/examples/`
  - transition reference patterns only, not a formal home for capture or serving boundaries

`src/examples/` is intentionally not part of the runtime import path or mounted route tree.
The capture boundary modules under `src/app/models/`, `src/app/schemas/`, and `src/app/crud/` do not add new runtime APIs by themselves.

## Migration Guardrails

The current mainline rules are:
- this repository is the only source of truth for ongoing backend migration work
- do not copy legacy `app/services` into the runtime
- do not copy legacy `scripts` into the runtime
- do not let research or archive material define current package structure
- if future orchestration modules are needed, they must be narrow and explicit rather than a flat catch-all service layer

The planning register in [legacy-backend-migration-mapping.md](./legacy-backend-migration-mapping.md) is still useful,
but it is planning material, not the runtime source of truth.

## Response-Shape Boundary

The base does not currently promote one repository-wide response envelope as a formal source of truth.

Current routes use route-specific response models and payload shapes validated by the current code and tests.
That means the legacy response-standard candidate remains only a migration input until the runtime actually standardizes on it.
