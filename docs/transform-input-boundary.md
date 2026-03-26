# Transform Input Boundary

This document defines the minimal future transform input boundary for `black-tonny-backend-base`.

For the current capture formal boundary, use [capture-minimal-boundary.md](./capture-minimal-boundary.md).
For the current dual-database split, use [capture-serving-boundary.md](./capture-serving-boundary.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

No transform module, transform runtime path, or serving projection path is currently landed in `black-tonny-backend-base`.

That means this document does not describe current runtime behavior.
It only defines the smallest formal boundary that a later scoped migration must respect if transform work is introduced.

## Minimum Future Transform Input

Future transform work may only treat persisted capture-side rows as formal transform input candidates.

The minimal allowed input boundary is:
- one persisted `capture_batches` row
- one or more persisted `capture_endpoint_payloads` rows linked to that batch through `capture_batch_id`

The minimum required persisted input fields are:
- batch identity: `capture_batches.capture_batch_id`
- payload linkage: `capture_endpoint_payloads.capture_batch_id`
- source traceability: `capture_endpoint_payloads.source_endpoint`
- raw or near-raw content: `capture_endpoint_payloads.payload_json`
- dedupe/audit trace: `capture_endpoint_payloads.checksum`
- capture timing: `capture_endpoint_payloads.pulled_at`

The following fields may help later scoped transform work, but they do not by themselves imply that transform has landed:
- `capture_batches.batch_status`
- `capture_batches.transformed_at`
- `capture_endpoint_payloads.route_kind`
- `capture_endpoint_payloads.page_cursor`
- `capture_endpoint_payloads.page_no`
- `capture_endpoint_payloads.request_params`

## Boundary Rules

Future transform input must come from:
- `src/app/models/capture_batch.py`
- `src/app/models/capture_endpoint_payload.py`
- the persisted rows created under the current capture formal boundary

Future transform input must not come from:
- `docs/reference/**`
- `docs/archive/**`
- `src/examples/**`
- legacy repo samples, scripts, or research notes
- temporary files or ad hoc payload copies outside the formal capture tables

## What This Document Does Not Claim

This document does not claim that:
- transform is currently implemented
- serving projection is currently implemented
- capture batches automatically progress through a transform lifecycle
- `transformed_at` proves that a transform module already exists
- legacy transform orchestration belongs in the new repository
- research, evidence, or admission logic is part of the transform input boundary

## Future Scoped Migration Requirement

If a later scoped migration introduces transform behavior, it must explicitly define:
- where transform code lives
- whether transform reads only capture or also writes serving
- how batch state transitions are managed
- what serving-side outputs are formalized

Until that later scoped migration happens, this document is only a formal boundary note.
