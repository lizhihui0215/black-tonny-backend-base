# Capture And Serving Boundary

This document defines the current dual-database boundary for `black-tonny-backend-base`.

For the overall runtime structure, use [runtime-boundaries.md](./runtime-boundaries.md).
For the full docs index, use [docs/README.md](./README.md).
For the minimal capture persistence boundary, use [capture-minimal-boundary.md](./capture-minimal-boundary.md).
For the minimal serving projection persistence boundary, use [serving-projection-minimal-boundary.md](./serving-projection-minimal-boundary.md).
For the current first minimal `capture -> transform -> serving` path, use [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md).
For the future transform input edge, use [transform-input-boundary.md](./transform-input-boundary.md).

## Current Truth

The repository keeps two database targets:
- `CAPTURE_DB_URL`
- `SERVING_DB_URL`

The current repository facts are:
- `/api/v1/ready` checks both capture and serving database connectivity
- the capture migration target now contains the minimal formal capture tables
- the serving migration target already contains the current runtime tables
- the current auth and management-style runtime APIs use serving database sessions
- a minimal first `capture -> transform -> serving` path now exists in repo code for the `sales_orders` slice without adding any runtime route

Current capture-side formal tables include:
- `analysis_batches`
- `capture_batches`
- `capture_endpoint_payloads`

Current serving-side runtime tables include:
- `user`
- `tier`
- `rate_limit`
- `token_blacklist`

Current serving-side formal projection tables include:
- `sales_orders`
- `sales_order_items`
- `inventory_current`
- `inventory_daily_snapshot`

These capture and serving projection tables establish persistence boundaries only.
They are not mounted into runtime routers and they do not change the current serving-only runtime read rule.
Their formal ownership stays under `src/app/**` and `src/migrations/**`, not under `src/examples/**` and not under research/reference material.

## Boundary Rules

The current boundary is:
- capture now has a minimal formal boundary for raw or near-raw intake metadata
- serving is the runtime database for the repository's current auth and management APIs
- runtime and business-serving APIs read serving, not capture
- the current first `sales_orders` path may read capture and write serving through repo-internal services only
- broader future transform or projection paths still require later scoped migration work

This document does not define the future transform input shape by itself.
That input edge is scoped separately in [transform-input-boundary.md](./transform-input-boundary.md) so current serving truth and future transform scope do not get conflated.

The readiness path is the current exception that checks both databases for health, but it is still a probe path rather than a business data read path.

## Reference And Archive Separation

Reference docs, archive docs, and reference examples can help plan future migration work, but they do not define current database truth.

That means:
- `docs/reference/**` is not a runtime schema source
- `docs/archive/**` is not a runtime schema source
- `src/examples/**` is a transition reference-pattern area, not a formal owner of capture truth
- `src/examples/**` is not mounted into runtime routers and is not imported by the app

## What This Document Does Not Claim

This document does not claim that:
- legacy capture services have already been migrated
- capture admission or research coupling has entered the runtime
- research scripts have entered runtime
- future serving projections have already landed
- old runtime business modules are current repository behavior
