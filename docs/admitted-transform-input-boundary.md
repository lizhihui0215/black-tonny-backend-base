# Admitted Transform Input Boundary

This document defines the minimal future admitted transform input boundary for `black-tonny-backend-base`.

For the current capture formal boundary, use [capture-minimal-boundary.md](./capture-minimal-boundary.md).
For the broader future transform input candidate edge, use [transform-input-boundary.md](./transform-input-boundary.md).
For the narrower transform readiness edge, use [transform-readiness-boundary.md](./transform-readiness-boundary.md).
For the current semantics of transform-adjacent batch fields, use [capture-batch-field-semantics.md](./capture-batch-field-semantics.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

No admitted transform input flow is currently implemented in `black-tonny-backend-base`.

That means this document does not describe a running admission path, transform path, or serving projection path.
It only defines the narrowest future boundary a later scoped migration must respect before any persisted capture data could be treated as admitted transform input.

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

If later work needs the narrower readiness edge, that scope must continue into [transform-readiness-boundary.md](./transform-readiness-boundary.md) rather than being inferred from this admitted-input layer alone.

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

## What This Document Does Not Claim

This document does not claim that:
- transform admission is currently implemented
- any current batch is already marked as admitted transform input
- `batch_status` already encodes transform admission policy
- readiness checks already exist for transform admission
- legacy admission orchestration belongs in the new repository
- research, evidence, or troubleshooting material can define admitted transform input

## Future Scoped Migration Requirement

If a later scoped migration introduces admitted transform input behavior, it must explicitly define:
- the admission rule set beyond this structural minimum
- whether batch-level readiness is a separate concept from admitted input
- how admission interacts with state transitions
- whether admitted input is consumed only by transform or also by later serving projection paths

Until that later scoped migration happens, this document is only a formal boundary note.
