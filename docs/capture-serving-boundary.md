# Capture And Serving Boundary

This document defines the current dual-database boundary for `black-tonny-backend-base`.

For the overall runtime structure, use [runtime-boundaries.md](./runtime-boundaries.md).
For the full docs index, use [docs/README.md](./README.md).

## Current Truth

The repository keeps two database targets:
- `CAPTURE_DB_URL`
- `SERVING_DB_URL`

The current runtime facts are:
- `/api/v1/ready` checks both capture and serving database connectivity
- the capture migration target is still empty in the current mainline metadata
- the serving migration target already contains the current runtime tables
- the current auth and management-style runtime APIs use serving database sessions

Current serving-side runtime tables include:
- `user`
- `tier`
- `rate_limit`
- `token_blacklist`

Current capture-side runtime tables have not been landed yet in the mainline metadata.

## Boundary Rules

The current boundary is:
- capture is reserved for raw or near-raw intake once future scoped migrations introduce formal capture models
- serving is the runtime database for the repository's current auth and management APIs
- runtime and business-serving APIs read serving, not capture
- future transform or projection paths may read capture and write serving only after a later scoped migration

The readiness path is the current exception that checks both databases for health, but it is still a probe path rather than a business data read path.

## Reference And Archive Separation

Reference docs, archive docs, and reference examples can help plan future migration work, but they do not define current database truth.

That means:
- `docs/reference/**` is not a runtime schema source
- `docs/archive/**` is not a runtime schema source
- `src/examples/**` is not mounted into runtime routers and is not imported by the app

## What This Document Does Not Claim

This document does not claim that:
- legacy capture services have already been migrated
- research scripts have entered runtime
- future serving projections have already landed
- old runtime business modules are current repository behavior
