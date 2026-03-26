# Capture Minimal Boundary

This document defines the minimal formal capture boundary currently landed in `black-tonny-backend-base`.

For the dual-database boundary, use [capture-serving-boundary.md](./capture-serving-boundary.md).
For the repository docs index, use [docs/README.md](./README.md).

## Scope

This boundary is intentionally narrow.
It only formalizes:
- capture-side ORM models
- capture-side schemas and CRUD helpers
- capture target metadata loading
- capture Alembic migration targets

It does not introduce:
- runtime routers
- runtime business APIs
- legacy `app/services` orchestration
- legacy `scripts`
- admission or research-driven capture logic

## Formal Ownership

`capture` belongs to the formal mainline in this repository.

That means the current formal ownership is:
- `src/app/models/`
- `src/app/schemas/`
- `src/app/crud/`
- `src/app/core/migration_targets.py`
- `src/migrations/capture_versions/`

It does not belong to:
- `src/examples/`
- `docs/reference/**`
- `docs/archive/**`

`src/examples/**` can still hold transition reference patterns, but it is not the formal home for capture.
Research notes, traceability samples, and troubleshooting templates belong in `docs/reference/**`, not in the formal capture boundary.

## Landed Tables

The current formal capture tables are:
- `capture_batches`
- `capture_endpoint_payloads`

### `capture_batches`

Current formal fields:
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

Current integrity guardrails:
- `batch_status` is constrained by the formal schema and by a database check constraint
- `updated_at` is system-managed and is not part of the caller-supplied update shape

### `capture_endpoint_payloads`

Current formal fields:
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
- avoid admitting any research or serving projection logic into the boundary itself

Current formal association:
- `capture_endpoint_payloads.capture_batch_id` references `capture_batches.capture_batch_id`

## Code Locations

The current formal capture boundary is implemented in:
- `src/app/models/capture_batch.py`
- `src/app/models/capture_endpoint_payload.py`
- `src/app/schemas/capture.py`
- `src/app/crud/crud_capture_batches.py`
- `src/app/crud/crud_capture_endpoint_payloads.py`
- `src/app/core/migration_targets.py`
- `src/migrations/capture_versions/20260326_02_add_capture_contract_tables.py`
- `src/migrations/capture_versions/20260326_03_add_capture_batch_status_check.py`

These files define the formal persistence boundary only.
They do not wire capture into routers, workers, or API handlers.
The example code under `src/examples/` can mirror this shape for transition reference purposes, but it does not define this boundary.

Current formal read helpers:
- `get_capture_batch_read`
- `list_capture_batch_reads`
- `get_capture_endpoint_payload_read`
- `list_capture_endpoint_payload_reads`

Current list-read shape:
- list helpers return a fixed boundary shape with `data` and `total_count`
- filtered empty results keep `data=[]` and `total_count=0`
- paginated results keep stable ordering while `total_count` remains the full filtered count

## Current Verified Read/Write Closure

The current minimal read/write closure is verified at the formal-layer test level, not through a runtime API.

The current coverage exercises:
- read one `capture_batches` row through a formal read helper that returns `CaptureBatchRead`
- list filtered `capture_batches` rows through a formal read helper with stable `capture_batch_id` ordering
- verify paginated batch reads keep a stable subset while `total_count` still reflects the full filtered result
- verify empty batch reads return `data=[]` with `total_count=0`
- read one `capture_endpoint_payloads` row through a formal read helper that returns `CaptureEndpointPayloadRead`
- list filtered `capture_endpoint_payloads` rows through a formal read helper with stable `id` ordering
- verify paginated payload reads keep a stable subset while `total_count` still reflects the full filtered result
- verify empty payload reads return `data=[]` with `total_count=0`
- create one `capture_batches` row through the formal CRUD path
- append one `capture_endpoint_payloads` row through the formal CRUD path
- update the batch lifecycle row and confirm `updated_at` refreshes
- reject caller attempts to override `updated_at` through `CaptureBatchUpdate`
- reject invalid `batch_status` values at the database boundary layer
- reject orphan payload writes that do not point at an existing `capture_batches.capture_batch_id`

The current verification file is:
- `tests/test_capture_write_contract.py`

## Explicit Non-Goals

This document does not claim that:
- `analysis_batches` has been migrated in this step
- serving projections have been migrated in this step
- legacy `*_capture_admission_service.py` files belong in the new repository
- research or evidence-chain logic belongs in the runtime path
- old capture services can be copied into `src/app/services/`
