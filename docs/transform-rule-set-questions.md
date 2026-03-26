# Transform Rule-Set Questions

This document defines the minimum future rule-set questions that a later scoped migration must answer before `black-tonny-backend-base` treats transform behavior as formal repository behavior.

For the current capture persistence boundary, use [capture-minimal-boundary.md](./capture-minimal-boundary.md).
For the current semantics of transform-adjacent batch fields, use [capture-batch-field-semantics.md](./capture-batch-field-semantics.md).
For the future transform state-transition note, use [transform-state-transition-boundary.md](./transform-state-transition-boundary.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

No transform rule-set is currently implemented or finalized in `black-tonny-backend-base`.

That means this document does not define transform behavior.
It only lists the minimum questions that a later scoped migration must answer explicitly instead of leaving them implicit, inherited, or assumed.

## What This Note Is For

This note is intentionally narrow.
It exists to make one thing explicit:
- current persisted facts and current formal boundaries are already documented
- future transform behavior still requires a small but explicit rule-set
- that rule-set must be answered in the new repository, not inferred from legacy behavior

This note does not provide the answers.

## Minimum Future Rule-Set Questions

Any later scoped migration that introduces transform behavior must explicitly answer at least these questions:

### 1. Admission And Readiness Relationship

- Is readiness always downstream of admission, or can they diverge?
- Can admitted input exist that is intentionally not ready?
- Does readiness depend only on persisted capture facts, or also on other formalized conditions?

### 2. `batch_status` Semantics

- Does future transform behavior reuse the current `batch_status` vocabulary as-is?
- If not, which meanings stay stable and which meanings are narrowed, expanded, or replaced?
- Is `batch_status` the canonical lifecycle field for transform behavior, or only one participating field among several?

### 3. `transformed_at` Write Semantics

- Under exactly what condition may `transformed_at` be written?
- Does it mark transform completion, a completion attempt, or something narrower?
- Can it ever be cleared, recomputed, or rewritten?

### 4. `error_message` Failure Semantics

- When does `error_message` represent current failure context versus retained historical context?
- Is it terminal-state evidence, retry context, or only free-form diagnostics?
- When may it be cleared, overwritten, or preserved?

### 5. Retry, Failure, And Terminal-State Rules

- Which failures are retryable?
- Which failures or partial states are terminal?
- What conditions reopen a batch after failure or partial completion?
- What idempotency guarantees must hold across retries?

### 6. Capture Lifecycle Versus Serving Outputs

- Does transform transition completion depend on serving-side writes?
- If serving writes fail, what capture-side lifecycle fact should remain true?
- Must capture-side lifecycle updates and serving-side outputs succeed together, or can they be staged separately?

## What Must Not Be Assumed

The later rule-set must not assume by default that:
- legacy admission or transform rules still apply
- the current `batch_status` values already answer the lifecycle policy questions
- `transformed_at` already means formal completion
- `error_message` already carries terminal failure semantics
- retry and failure behavior can be inferred from old scripts, samples, or troubleshooting notes

## What This Document Does Not Claim

This document does not claim that:
- transform is currently implemented
- readiness or transition rules are currently implemented
- the current fields already answer the rule-set questions above
- legacy answers should be accepted unless someone objects

Until a later scoped migration defines explicit answers, these remain open future rule questions rather than current repository behavior.
