# Transform State-Transition Boundary

This document defines the minimal future transform state-transition boundary for `black-tonny-backend-base`.

For the current capture formal boundary, use [capture-minimal-boundary.md](./capture-minimal-boundary.md).
For the broader future transform input candidate edge, use [transform-input-boundary.md](./transform-input-boundary.md).
For the narrower admitted transform input edge, use [admitted-transform-input-boundary.md](./admitted-transform-input-boundary.md).
For the narrower transform readiness edge, use [transform-readiness-boundary.md](./transform-readiness-boundary.md).
For the current semantics of transform-adjacent batch fields, use [capture-batch-field-semantics.md](./capture-batch-field-semantics.md).
For the minimum future transform rule-set questions, use [transform-rule-set-questions.md](./transform-rule-set-questions.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

No transform state-transition flow, state machine, or transition executor is currently implemented in `black-tonny-backend-base`.

That means this document does not describe current runtime behavior.
It only defines the narrowest future boundary a later scoped migration must respect before any transform-related lifecycle transition could be treated as formal repository behavior.

## Ready Input Versus State-Transition Boundary

The distinction stays explicit:
- transform-ready input is the narrower future subset that a later scoped migration is allowed to treat as ready for transform behavior
- transform state-transition boundary is the future rule boundary that constrains how persisted capture lifecycle facts may be advanced, failed, retried, or completed if transform behavior is introduced

This document only defines the minimum transition floor.
It does not define a state machine, transition executor, or serving projection behavior.

## Minimum State-Transition Conditions

Future transform state transitions must first operate on transform-ready input that satisfies the full boundary in [transform-readiness-boundary.md](./transform-readiness-boundary.md).

On top of that, the minimum state-transition conditions are:
- any future transform transition must remain anchored to the persisted `capture_batches` row that owns the input set
- any future transform transition may only interpret or update lifecycle facts that already exist under the current formal capture boundary unless a later scoped migration explicitly formalizes new fields
- the current formal lifecycle facts that may later participate in transform state-transition rules are:
  - `capture_batches.batch_status`
  - `capture_batches.transformed_at`
  - `capture_batches.error_message`
  - `capture_batches.updated_at`
- any future transition rule must be defined from repository-owned formal docs and code in a later scoped migration, not inferred from external samples, copied payloads, or legacy orchestration behavior

The current field semantics for those lifecycle facts stay narrower than any future transform policy.
That means `batch_status`, `transformed_at`, `error_message`, and `updated_at` must first be read through [capture-batch-field-semantics.md](./capture-batch-field-semantics.md), not through assumed legacy behavior.

These conditions are intentionally narrow.
They only constrain where future transform state transitions may start and which current persisted lifecycle facts they may depend on.
They do not define the allowed transition graph.

## What Is Still Not Defined

The following points are intentionally left to a later scoped migration:
- which source-to-target transitions are allowed among `queued`, `captured`, `partial`, `failed`, and `transformed`
- whether future transform behavior should keep the current `batch_status` vocabulary or formalize new semantics
- when `transformed_at` may be written, preserved, cleared, or recomputed
- when `error_message` is preserved, cleared, overwritten, or considered terminal evidence
- whether retries reopen failed or partial states
- whether partial or failed transitions are terminal, recoverable, or resumable
- whether transition rules require locking, reservation, idempotency, or concurrency coordination
- whether transition completion depends on serving-side writes, and if so, how that relationship is formalized

## Boundary Rules

Future transform state-transition rules must not be defined from:
- `docs/reference/**`
- `docs/archive/**`
- `src/examples/**`
- legacy repo transform, admission, or readiness orchestration files
- temporary files, copied payload snapshots, or ad hoc evidence bundles outside the formal capture tables

Future transform state-transition rules must not be copied wholesale from the legacy repository.
If a later scoped migration intentionally adopts part of a legacy lifecycle rule, that rule must be restated explicitly in new-repo docs and code instead of being inherited by implication.

Future transform state-transition rules must continue to originate from the current formal capture boundary under `src/app/**` and `src/migrations/**`, plus any later scoped migration that formally introduces transform behavior.

## What This Document Does Not Claim

This document does not claim that:
- transform state transitions are currently implemented
- a state machine already exists in code
- the current `batch_status` values already encode a formal transform transition graph
- `transformed_at` already proves a formal transform completion transition
- legacy orchestration belongs in the new repository
- research, evidence, troubleshooting, or reference material can define transform state-transition rules

## Future Scoped Migration Requirement

If a later scoped migration introduces transform state-transition behavior, it must explicitly define:
- the allowed source-to-target transition map
- how `batch_status`, `transformed_at`, `error_message`, and `updated_at` are written or preserved
- retry, failure, terminal-state, and idempotency rules
- whether transition rules stay capture-side only or also coordinate with serving-side outputs
- whether any new lifecycle fields or statuses are introduced, and why they are needed in the new repository

Use [transform-rule-set-questions.md](./transform-rule-set-questions.md) as the minimum question list that still needs explicit answers before those rules become formal repository behavior.

For the first transform behavior PR in particular, the minimum entry condition is narrower but still explicit:
- it must say whether it is changing only one transition edge or a broader lifecycle slice
- it must say whether `batch_status`, `transformed_at`, `error_message`, or `updated_at` are being written, and under what rule
- it must say what remains intentionally out of scope for a later scoped migration

Until that later scoped migration happens, this document is only a formal boundary note.
