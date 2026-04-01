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

A minimal capture-batch lifecycle helper is now implemented in `black-tonny-backend-base`.
A selector and a minimal readiness evaluator may now exist upstream of this boundary, but the lifecycle helper remains a separate narrower step.

That helper is intentionally narrow.
It only formalizes the current first two capture-side lifecycle writes:
- `captured -> transformed`
- `captured -> failed`

It does not define a general transition executor, broader state machine, scheduler, or serving projection path.

## Ready Input Versus State-Transition Boundary

The distinction stays explicit:
- transform-ready input is the narrower future subset that a later scoped migration is allowed to treat as ready for transform behavior
- transform state-transition boundary is the future rule boundary that constrains how persisted capture lifecycle facts may be advanced, failed, retried, or completed if transform behavior is introduced

This document only defines the minimum transition floor.
It defines the current narrow lifecycle helper plus the minimum transition floor beyond it.
It does not define a broader state machine, transition executor, or serving projection behavior.

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

At the current minimum boundary, broader lifecycle-transition minimums remain future formal constraints beyond the current first helper.
They do not mean that any broader lifecycle transition graph has already been proven, executed, scheduled, reserved, or coordinated.
`analysis_batches` is not a current minimum prerequisite or proof source for transform lifecycle transitions.

The current fields above do not currently prove any formal source-to-target transition:
- `capture_batches.batch_status` does not by itself prove that a formal lifecycle transition has occurred
- `capture_batches.transformed_at` does not by itself prove that a formal completion transition has occurred
- `capture_batches.error_message` does not by itself prove that a formal failed or terminal transition has been declared
- `capture_batches.updated_at` does not prove transition progress, transition ordering, reservation, or execution

## Current Lifecycle Helper Boundary

Current helper inputs:
- `capture_batch_id`
- one latest failure message for the failed edge
- one optional explicit `transformed_at` override for the transformed edge

Current helper output:
- one updated `CaptureBatchRead`
- `None` when the batch row is missing

Current helper behavior:
- `mark_capture_batch_transformed` requires the current batch row to keep `batch_status == "captured"`
- `mark_capture_batch_transformed` writes only:
  - `batch_status = "transformed"`
  - `transformed_at = now` or one explicit override value
- `mark_capture_batch_transformed` does not clear `error_message`
- `mark_capture_batch_failed` requires the current batch row to keep `batch_status == "captured"`
- `mark_capture_batch_failed` writes only:
  - `batch_status = "failed"`
  - `error_message` overwritten with the latest failure text
- `mark_capture_batch_failed` does not write `transformed_at`
- both helper functions raise `ValueError` when the current batch row is not in the `captured` source state
- neither helper function retries, reopens, resumes, reserves, or schedules work
- neither helper function writes serving projection rows
- neither helper function acts as a general transition executor

These current helper behaviors are intentionally narrow.
They constrain only the first landed lifecycle write helper, not the broader future state-transition rule set.

These conditions are intentionally narrow.
They only constrain where future transform state transitions may start and which current persisted lifecycle facts they may depend on.
They do not define the allowed transition graph beyond the current two landed helper edges.

## What Is Still Not Defined

The following points are intentionally left to a later scoped migration:
- which source-to-target transitions beyond the current `captured -> transformed` and `captured -> failed` edges are allowed among `queued`, `captured`, `partial`, `failed`, and `transformed`
- whether future transform behavior should keep the current `batch_status` vocabulary or formalize new semantics
- when `transformed_at` may be written, preserved, cleared, or recomputed beyond the current helper edge
- when `error_message` is preserved, cleared, overwritten, or considered terminal evidence beyond the current helper edge
- whether a selector or readiness evaluator is required before any lifecycle transition write beyond the current helper contract is allowed
- whether a broader lifecycle helper or transition executor exists, and if so, what narrower or broader write contract it owns
- whether retries reopen failed or partial states
- whether partial or failed transitions are terminal, recoverable, or resumable
- whether scheduling or orchestration is required before any lifecycle transition write is allowed
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

## Current Code Locations

The current minimal lifecycle helper implementation lives under:
- `src/app/services/capture_batch_lifecycle.py`
- `src/app/services/transform_readiness_evaluator.py`
- `src/app/services/admitted_transform_selector.py`
- `src/app/schemas/capture.py`

## What This Document Does Not Claim

This document does not claim that:
- a full transform state machine already exists in code
- a general transition executor already exists in code
- the current `batch_status` values already encode a formal transform transition graph
- `transformed_at` by itself already proves a formal transform completion transition
- `error_message` or `updated_at` by itself already proves that a broader formal lifecycle transition has occurred
- overwrite, retry, failure-recovery, scheduling, or orchestration policy is already formalized
- legacy orchestration belongs in the new repository
- research, evidence, troubleshooting, or reference material can define transform state-transition rules

## Current Verified Coverage

The current lifecycle helper coverage is verified at the formal-layer test level.

The current coverage exercises:
- mark one `captured` batch as `transformed` while writing `transformed_at` and preserving `error_message`
- mark one `captured` batch as `failed` while overwriting `error_message` and leaving `transformed_at` untouched
- reject lifecycle helper writes when the source state is not `captured`
- return `None` when the target batch row is missing

The current verification file is:
- `tests/test_transform_readiness_and_lifecycle.py`

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

Beyond the current narrow lifecycle helper, later scoped migration work is still required before broader transform state-transition behavior becomes formal repository behavior.
