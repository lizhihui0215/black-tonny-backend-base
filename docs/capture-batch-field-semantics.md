# Capture Batch Field Semantics

This document defines the current formal semantics and ownership boundary of the transform-adjacent fields on `capture_batches`.

For the overall capture persistence boundary, use [capture-minimal-boundary.md](./capture-minimal-boundary.md).
For the future transform state-transition note, use [transform-state-transition-boundary.md](./transform-state-transition-boundary.md).
For the minimum future transform rule-set questions, use [transform-rule-set-questions.md](./transform-rule-set-questions.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

The current repository truth is still limited to persisted capture-side facts.

No transform policy, readiness checker, state machine, or serving projection path currently owns the semantics of these fields.
That means the fields below must be read first as formal persisted facts under the capture boundary, not as already-landed transform behavior.

## Current Ownership

The current formal ownership of these fields stays within:
- `src/app/models/capture_batch.py`
- `src/app/schemas/capture.py`
- `src/app/crud/crud_capture_batches.py`
- `src/migrations/capture_versions/`

Their semantics are not currently owned by:
- a transform module
- a readiness checker
- a state machine
- a serving projection path
- legacy orchestration copied from the old repository

## Field Semantics

### `capture_batches.batch_status`

Current meaning:
- a persisted lifecycle label on the batch row
- constrained by the current formal schema and database check constraint
- readable through the current formal CRUD and read-helper boundary

Current non-meaning:
- not a formal transform admission policy
- not a formal transform readiness policy
- not a formal source-to-target transition graph
- not proof that any current runtime transform flow exists

### `capture_batches.transformed_at`

Current meaning:
- a nullable persisted timestamp field on the batch row
- a stored fact that may later become relevant to transform-related lifecycle rules

Current non-meaning:
- not proof that transform is currently implemented
- not proof of transform completion
- not a formal readiness or admission marker
- not a formal serving-write completion marker

### `capture_batches.error_message`

Current meaning:
- an optional persisted text field on the batch row
- a place to retain failure or diagnostic context when the batch row is updated

Current non-meaning:
- not a formal terminal-state declaration
- not a canonical transform error taxonomy
- not a retry policy signal
- not evidence that a current transform failure path exists

### `capture_batches.updated_at`

Current meaning:
- a system-managed modification timestamp on the batch row
- refreshed by the current update path when the row changes

Current non-meaning:
- not a transform progress timestamp
- not a transform heartbeat
- not a readiness checkpoint
- not a worker-ownership or reservation signal

## Future Use Without Current Commitment

These fields may later participate in:
- transform readiness rules
- transform state-transition rules
- transform completion semantics

But that future participation is not current repository truth.
Any later scoped migration must explicitly define:
- which field meanings stay the same
- which fields gain narrower lifecycle semantics
- which writes are allowed or forbidden
- whether any new fields are needed instead of overloading the current ones

Use [transform-rule-set-questions.md](./transform-rule-set-questions.md) for the minimum future questions that still require explicit answers before those narrower semantics become formal behavior.

For the first transform behavior PR, any touched field must be called out explicitly:
- which current meanings stay unchanged
- which current non-meanings stop being true
- which new writes are being introduced now versus deferred to a later scoped migration

## What This Document Does Not Claim

This document does not claim that:
- the current fields already implement transform policy
- the current fields already encode readiness or completion rules
- the current fields should inherit legacy orchestration semantics by default
- `batch_status`, `transformed_at`, `error_message`, or `updated_at` can be reinterpreted by implication from old repository behavior

Until a later scoped migration formalizes narrower behavior, these fields remain current capture-side persisted facts with restrained semantics.
