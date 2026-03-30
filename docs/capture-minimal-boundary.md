# Capture Minimal Boundary

This document defines the minimal formal capture boundary currently landed in `black-tonny-backend-base`.

For the dual-database boundary, use [capture-serving-boundary.md](./capture-serving-boundary.md).
For the future transform input edge, use [transform-input-boundary.md](./transform-input-boundary.md).
For the narrower admitted transform input edge, use [admitted-transform-input-boundary.md](./admitted-transform-input-boundary.md).
For the narrower transform readiness edge, use [transform-readiness-boundary.md](./transform-readiness-boundary.md).
For the narrower transform state-transition edge, use [transform-state-transition-boundary.md](./transform-state-transition-boundary.md).
For the current semantics of transform-adjacent batch fields, use [capture-batch-field-semantics.md](./capture-batch-field-semantics.md).
For the repository docs index, use [docs/README.md](./README.md).

The current repository database premise for this formal capture boundary is PostgreSQL.

## Scope

This boundary is intentionally narrow.
It only formalizes:
- capture-side ORM models
- capture-side schemas and CRUD helpers
- a minimal capture write helper
- a minimal capture constants module
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
- `src/app/services/capture_write.py`
- `src/app/constants/capture.py`
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

Current transform-adjacent field semantics stay intentionally restrained:
- `batch_status` is a persisted lifecycle label, not current transform policy
- `transformed_at` is a nullable persisted fact, not current transform completion proof
- `error_message` is optional persisted diagnostic context, not current terminal-state policy
- `updated_at` is a system-managed modification timestamp, not current transform progress or reservation state
- under the current PostgreSQL boundary, `error_message` is stored as `TEXT`

Use [capture-batch-field-semantics.md](./capture-batch-field-semantics.md) for the full field-level note.

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
- under the current PostgreSQL boundary, `payload_json` and `request_params` are stored as `TEXT`

Current formal association:
- `capture_endpoint_payloads.capture_batch_id` references `capture_batches.capture_batch_id`

## Relation To Future Transform Input

The current capture boundary is the only formal source for any future transform input candidate.

That means a later scoped transform migration may only start from persisted rows that already exist under this boundary.
Reference material, archive material, examples, legacy scripts, and copied payload files are outside the formal transform input edge.

If a later scoped migration defines admitted transform input, that admitted subset must still be derived from this same persisted capture boundary.
It cannot be widened through `docs/reference/**`, `src/examples/**`, `docs/archive/**`, legacy samples, or temporary files.

If a later scoped migration defines transform-ready input, that ready subset must also be derived from this same persisted capture boundary through the narrower admitted-input layer.
It cannot be widened through reference material, transition examples, archive material, legacy samples, or temporary files.

If a later scoped migration defines transform state transitions, those lifecycle rules must also stay anchored to this same persisted capture boundary through the narrower admitted-input and ready-input layers.
They must not be inherited from legacy orchestration or widened through reference material, transition examples, archive material, legacy samples, or temporary files.

Current fields such as `transformed_at`, `route_kind`, `page_cursor`, and `request_params` may support later scoped transform work,
but they do not imply that transform behavior is already implemented.

## Code Locations

The current formal capture boundary is implemented in:
- `src/app/models/capture_batch.py`
- `src/app/models/capture_endpoint_payload.py`
- `src/app/schemas/capture.py`
- `src/app/crud/crud_capture_batches.py`
- `src/app/crud/crud_capture_endpoint_payloads.py`
- `src/app/services/capture_write.py`
- `src/app/constants/capture.py`
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

Current formal minimal write/helper surface:
- `create_capture_batch`
- `update_capture_batch`
- `append_capture_payload`

Current formal minimal constants surface:
- `CAPTURE_BATCH_DEFAULT_STATUS`
- capture string-length constants used by the current models and schemas

## Current Read/List Boundary

Current list-read shape:
- list helpers return a fixed boundary shape with `data` and `total_count`
- filtered empty results keep `data=[]` and `total_count=0`
- paginated results keep stable ordering while `total_count` remains the full filtered count

### Supported Query Boundary

- `list_capture_batch_reads` supports equality filters on `batch_status` and `source_name`
- `list_capture_endpoint_payload_reads` supports equality filters on `capture_batch_id` and `source_endpoint`
- current list helpers support default `limit`, explicit `limit`, and `offset`
- current list helpers keep a fixed ascending sort boundary through the helper implementation

### Unsupported Query Boundary

- no OR-style filters
- no fuzzy or full-text search
- no range filters
- no caller-supplied sort overrides
- no joined reads or projection queries

## Current Verified Boundary Coverage

The current minimal boundary coverage is verified at the formal-layer test level, not through a runtime API.

The current coverage exercises:
- read one `capture_batches` row through a formal read helper that returns `CaptureBatchRead`
- list filtered `capture_batches` rows through a formal read helper with stable `capture_batch_id` ordering
- verify paginated batch reads keep a stable subset while `total_count` still reflects the full filtered result
- verify empty batch reads return `data=[]` with `total_count=0`
- verify batch reads stay stable when `batch_status` and `source_name` are combined with default or explicit pagination
- read one `capture_endpoint_payloads` row through a formal read helper that returns `CaptureEndpointPayloadRead`
- list filtered `capture_endpoint_payloads` rows through a formal read helper with stable `id` ordering
- verify paginated payload reads keep a stable subset while `total_count` still reflects the full filtered result
- verify empty payload reads return `data=[]` with `total_count=0`
- verify payload reads stay stable when `capture_batch_id` and `source_endpoint` are combined with default or explicit pagination
- create one `capture_batches` row through the formal CRUD path
- append one `capture_endpoint_payloads` row through the formal CRUD path
- update the batch lifecycle row and confirm `updated_at` refreshes
- verify PostgreSQL dialect compilation keeps `error_message`, `request_params`, and `payload_json` at `TEXT`
- verify the current formal create/update schemas do not add explicit `maxLength` caps around those fields
- exercise one focused large-text round-trip through the current formal-layer test base
- reject caller attempts to override `updated_at` through `CaptureBatchUpdate`
- reject invalid `batch_status` values at the database boundary layer
- reject orphan payload writes that do not point at an existing `capture_batches.capture_batch_id`

The current verification file is:
- `tests/test_capture_formal_boundary.py`

## Explicit Non-Goals

This document does not claim that:
- `analysis_batches` has been migrated in this step
- serving projections have been migrated in this step
- legacy `*_capture_admission_service.py` files belong in the new repository
- research or evidence-chain logic belongs in the runtime path
- old capture services can be copied into `src/app/services/`
