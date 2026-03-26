# Transform Readiness Boundary

This document defines the minimal future transform readiness boundary for `black-tonny-backend-base`.

For the current capture formal boundary, use [capture-minimal-boundary.md](./capture-minimal-boundary.md).
For the broader future transform input candidate edge, use [transform-input-boundary.md](./transform-input-boundary.md).
For the narrower admitted transform input edge, use [admitted-transform-input-boundary.md](./admitted-transform-input-boundary.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

No transform readiness flow, readiness checker, or transform execution path is currently implemented in `black-tonny-backend-base`.

That means this document does not describe current runtime behavior.
It only defines the narrowest future boundary a later scoped migration must respect before any admitted transform input could be treated as transform-ready input.

## Admitted Versus Ready Input

The distinction stays explicit:
- admitted transform input is the narrower future subset that a later scoped migration is allowed to accept into transform scope
- transform-ready input is the even narrower future subset that a later scoped migration is allowed to treat as ready for transform behavior

This document only defines the minimum readiness floor.
It does not define how readiness is checked, when transform runs, or how serving-side outputs are produced.

## Minimum Transform Readiness Conditions

Future transform-ready input must first satisfy the full admitted transform input boundary in [admitted-transform-input-boundary.md](./admitted-transform-input-boundary.md).

On top of that, the minimum readiness conditions are:
- the admitted batch row remains readable from the current formal capture boundary as the batch-level owner of the input set
- the admitted payload rows remain readable and linked to that batch through `capture_batch_id`
- any future readiness decision must be derived from persisted capture-side facts that already live under the formal capture boundary
- readiness must not be inferred from external samples, copied payload files, reference docs, archive docs, or transition examples

These readiness conditions are intentionally narrow.
They only constrain where future readiness may start and what kind of persisted truth it may depend on.
They do not define a readiness policy, checker, or state machine.

## What Is Still Not Defined

The following points are intentionally left to a later scoped migration:
- which `batch_status` values are eligible for transform-ready input
- whether readiness requires full endpoint completeness, page completeness, or source-specific completeness rules
- whether partial captures can ever become transform-ready input
- whether duplicate payloads block readiness, are ignored, or are coalesced
- whether freshness windows, replay rules, or retry semantics affect readiness
- whether readiness requires locking, reservation, or concurrency coordination
- how readiness interacts with admission policy, state transitions, `transformed_at`, or failure recovery
- what serving-side outputs are produced after readiness leads to transform behavior

## Boundary Rules

Future transform-ready input must not be defined from:
- `docs/reference/**`
- `docs/archive/**`
- `src/examples/**`
- legacy repo readiness, admission, or transform orchestration files
- temporary files, copied payload snapshots, or ad hoc evidence bundles outside the formal capture tables

Future transform-ready input must continue to originate from the current formal capture boundary under `src/app/**` and `src/migrations/**`.

## What This Document Does Not Claim

This document does not claim that:
- transform readiness is currently implemented
- any current batch is already marked or known as transform-ready input
- `batch_status` already encodes transform readiness policy
- a readiness checker already exists in code
- legacy readiness orchestration belongs in the new repository
- research, evidence, troubleshooting, or reference material can define transform-ready input

## Future Scoped Migration Requirement

If a later scoped migration introduces transform readiness behavior, it must explicitly define:
- the readiness rule set beyond this structural minimum
- whether readiness is separate from admission or derived from it
- how readiness interacts with state transitions and transform execution
- whether transform-ready input writes only serving outputs or also updates capture-side lifecycle facts

Until that later scoped migration happens, this document is only a formal boundary note.
