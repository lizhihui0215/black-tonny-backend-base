# Admitted Transform Input Boundary

This document defines the minimal future admitted transform input boundary for `black-tonny-backend-base`.

For the current capture formal boundary, use [capture-minimal-boundary.md](./capture-minimal-boundary.md).
For the broader future transform input candidate edge, use [transform-input-boundary.md](./transform-input-boundary.md).
For the narrower transform readiness edge, use [transform-readiness-boundary.md](./transform-readiness-boundary.md).
For the current semantics of transform-adjacent batch fields, use [capture-batch-field-semantics.md](./capture-batch-field-semantics.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

A minimal admitted transform input selector is now implemented in `black-tonny-backend-base`.

That selector is intentionally narrow.
It does not describe a running transform path, readiness path, lifecycle-transition path, or serving projection path.
It only defines and selects the current minimum persisted capture-side bundle that may be treated as admitted transform input.

## Candidate Versus Admitted Input

The distinction stays explicit:
- a future transform input candidate is any persisted capture-side material that satisfies the boundary in [transform-input-boundary.md](./transform-input-boundary.md)
- admitted transform input is the narrower future subset that a later scoped migration is allowed to accept into transform scope

Admitted transform input is still broader than transform-ready input.
A later scoped migration may treat only a narrower subset of admitted input as ready for transform behavior.

This document only defines the smallest admitted-input floor.
It does not define when transform execution starts, how batches become ready, or how serving-side outputs are produced.

## Minimum Admitted Input Conditions

Future admitted transform input must first satisfy the full future transform input candidate boundary.

On top of that, the minimum admitted conditions are:
- one persisted `capture_batches` row remains readable as the batch-level owner of the input set
- one or more persisted `capture_endpoint_payloads` rows remain readable and linked to that batch through `capture_batch_id`
- the required persisted fields for transform input candidates are present in the stored rows:
  - `capture_batches.capture_batch_id`
  - `capture_endpoint_payloads.capture_batch_id`
  - `capture_endpoint_payloads.source_endpoint`
  - `capture_endpoint_payloads.payload_json`
  - `capture_endpoint_payloads.checksum`
  - `capture_endpoint_payloads.pulled_at`
- the linkage between batch row and payload rows remains formal repository truth under the current capture boundary, not an external sample or copied payload file

These admitted conditions are intentionally structural.
They define the minimum persisted shape that a later scoped migration may choose to admit, but they do not define readiness policy or transform behavior.

At the current minimum boundary, the admitted-input floor is still capture-side only.
`analysis_batches` is not a current minimum prerequisite for admitted transform input.
If an `analysis_batches` row exists and links back through `capture_batch_id`, it remains optional persisted context rather than current admission truth.

No current `batch_status` value, including `captured`, is by itself a formal admission marker.
Current admitted-input minimums also do not reinterpret `transformed_at` as admission proof.

## Current Selector Boundary

Current selector input:
- `capture_batch_id`

Current selector output:
- one `AdmittedTransformInputSnapshot` bundle when the structural admitted-input minimum is satisfied
- `None` when the batch row is missing
- `None` when the batch row exists but no linked payload rows are currently readable

Current selector behavior:
- reads the persisted `capture_batches` row by `capture_batch_id`
- reads linked `capture_endpoint_payloads` rows by `capture_batch_id`
- keeps payload row ordering stable through the current read-helper boundary
- does not require `analysis_batches`
- does not gate on `batch_status`
- does not gate on `transformed_at`
- does not answer readiness or lifecycle-transition questions

Current selector bundle shape:
- batch snapshot:
  - `capture_batch_id`
  - `batch_status`
  - `transformed_at`
  - `error_message`
- payload snapshots:
  - `capture_batch_id`
  - `source_endpoint`
  - `payload_json`
  - `checksum`
  - `pulled_at`

The narrower readiness edge is defined separately in [transform-readiness-boundary.md](./transform-readiness-boundary.md).
It must not be inferred from this admitted-input layer alone.

## What Is Still Not Defined

The following points are intentionally left to a later scoped migration:
- which `batch_status` values are eligible for admitted transform input
- whether partial captures are admissible, deferred, or rejected
- whether additional completeness checks are required across endpoints or pages
- whether duplicate payloads are rejected, coalesced, or tolerated
- whether any freshness window or replay rule is required
- whether admitted input can be retried after failure
- whether `analysis_batches` later becomes required context, optional supporting context, or remains outside the first admitted slice
- how admitted input affects batch readiness, state transitions, or serving-side outputs

## Boundary Rules

Future admitted transform input must not be defined from:
- `docs/reference/**`
- `docs/archive/**`
- `src/examples/**`
- legacy repo admission or transform orchestration files
- temporary files, copied payload snapshots, or ad hoc evidence bundles outside the formal capture tables

Future admitted transform input must continue to originate from the current formal capture boundary under `src/app/**` and `src/migrations/**`.

The current minimal selector implementation lives under:
- `src/app/services/admitted_transform_selector.py`
- `src/app/schemas/transform.py`
- current capture-side CRUD/read helpers under `src/app/crud/`

## What This Document Does Not Claim

This document does not claim that:
- every current batch is already admitted transform input
- `batch_status` already encodes transform admission policy
- readiness checks already exist for transform admission
- legacy admission orchestration belongs in the new repository
- research, evidence, or troubleshooting material can define admitted transform input

## Current Verified Coverage

The current admitted-input selector coverage is verified at the formal-layer test level.

The current coverage exercises:
- return one admitted bundle when one batch row and linked payload rows satisfy the current structural minimum
- keep admitted selection independent from `analysis_batches`
- return `None` when a batch row exists without linked payload rows
- keep selection structural even when `batch_status` and `transformed_at` carry persisted values that are not current admission proof

The current verification file is:
- `tests/test_admitted_transform_input_selector.py`

## Future Scoped Migration Requirement

If a later scoped migration introduces admitted transform input behavior, it must explicitly define:
- the admission rule set beyond this structural minimum
- whether batch-level readiness is a separate concept from admitted input
- how admission interacts with state transitions
- whether admitted input is consumed only by transform or also by later serving projection paths

Beyond the current minimal selector implementation, later scoped migration work is still required before broader admitted transform input behavior becomes formal repository behavior.
