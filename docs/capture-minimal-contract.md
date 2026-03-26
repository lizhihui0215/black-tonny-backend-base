# Capture Minimal Contract

This document defines the minimal formal capture contract currently landed in `black-tonny-backend-base`.

For the dual-database boundary, use [capture-serving-boundary.md](./capture-serving-boundary.md).
For the repository docs index, use [docs/README.md](./README.md).

## Scope

This contract is intentionally narrow.
It only formalizes:
- capture-side ORM models
- capture-side CRUD contracts
- capture target metadata loading
- capture Alembic migration targets

It does not introduce:
- runtime routers
- runtime business APIs
- legacy `app/services` orchestration
- legacy `scripts`
- admission or research-driven capture logic

## Landed Tables

The current formal capture tables are:
- `capture_batches`
- `capture_endpoint_payloads`

### `capture_batches`

Current contract fields:
- `capture_batch_id`
- `batch_status`
- `source_name`
- `pulled_at`
- `transformed_at`
- `created_at`
- `updated_at`
- `error_message`

Current purpose:
- track one formal capture batch identifier
- record minimal capture lifecycle state
- keep failure and timing metadata without introducing orchestration logic

### `capture_endpoint_payloads`

Current contract fields:
- `id`
- `capture_batch_id`
- `source_endpoint`
- `payload_json`
- `checksum`
- `pulled_at`
- `route_kind`
- `page_cursor`
- `page_no`
- `request_params`
- `created_at`

Current purpose:
- persist raw or near-raw endpoint payload snapshots
- keep enough page-level metadata for replay, audit, and later scoped transforms
- avoid admitting any research or serving projection logic into the contract itself

## Code Locations

The current formal capture contract is landed in:
- `src/app/models/capture_batch.py`
- `src/app/models/capture_endpoint_payload.py`
- `src/app/schemas/capture.py`
- `src/app/crud/crud_capture_batches.py`
- `src/app/crud/crud_capture_endpoint_payloads.py`
- `src/app/core/migration_targets.py`
- `src/migrations/capture_versions/20260326_02_add_capture_contract_tables.py`

These files define persistence contracts only.
They do not wire capture into routers, workers, or API handlers.

## Explicit Non-Goals

This document does not claim that:
- `analysis_batches` has been migrated in this step
- serving projections have been migrated in this step
- legacy `*_capture_admission_service.py` files belong in the new repository
- research or evidence-chain logic belongs in the runtime path
- old capture services can be copied into `src/app/services/`
