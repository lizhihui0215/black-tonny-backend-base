# Transform Readiness Boundary

This document defines the minimal future transform readiness boundary for `black-tonny-backend-base`.

For the current capture formal boundary, use [capture-minimal-boundary.md](./capture-minimal-boundary.md).
For the broader future transform input candidate edge, use [transform-input-boundary.md](./transform-input-boundary.md).
For the narrower admitted transform input edge, use [admitted-transform-input-boundary.md](./admitted-transform-input-boundary.md).
For the narrower transform state-transition edge, use [transform-state-transition-boundary.md](./transform-state-transition-boundary.md).
For the current semantics of transform-adjacent batch fields, use [capture-batch-field-semantics.md](./capture-batch-field-semantics.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

A minimal transform readiness evaluator is now implemented in `black-tonny-backend-base`.
A minimal admitted transform input selector may now exist upstream of this boundary, but the readiness evaluator remains a separate narrower step.

That evaluator is intentionally narrow.
It decides only whether admitted input is ready for the current first `sales_orders` slice.
It does not execute transform behavior, write serving-side outputs, schedule work, reserve work, or advance capture-side lifecycle fields.

## Admitted Versus Ready Input

The distinction stays explicit:
- admitted transform input is the narrower future subset that a later scoped migration is allowed to accept into transform scope
- transform-ready input is the even narrower future subset that a later scoped migration is allowed to treat as ready for transform behavior

Transform-ready input may still be broader than the future set of lifecycle transitions that a later scoped migration chooses to formalize.

This document defines the current first readiness evaluator plus the minimum readiness floor beyond it.
It does not define when transform runs or how serving-side outputs are produced.

## Minimum Transform Readiness Conditions

Future transform-ready input must first satisfy the full admitted transform input boundary in [admitted-transform-input-boundary.md](./admitted-transform-input-boundary.md).

On top of that, the minimum readiness conditions are:
- the admitted batch row remains readable from the current formal capture boundary as the batch-level owner of the input set
- the admitted payload rows remain readable and linked to that batch through `capture_batch_id`
- any future readiness decision must be derived from persisted capture-side facts that already live under the formal capture boundary
- readiness must not be inferred from external samples, copied payload files, reference docs, archive docs, or transition examples

At the current minimum boundary, readiness is still capture-side only.
`analysis_batches` is not a current minimum prerequisite for transform readiness.

At this stage, readiness only means that the admitted input set satisfies the current minimum formal persisted-input conditions for the current first slice.
It does not mean that transform has run, been scheduled, been reserved, or will necessarily execute.
No current field, including `batch_status` and `transformed_at`, is by itself a formal readiness proof.

## Current Readiness Evaluator Boundary

Current evaluator input:
- one `AdmittedTransformInputSnapshot`

Current evaluator output:
- one `TransformReadinessDecision`

Current first-slice definition:
- the narrow `sales_orders` source slice
- identified only by one or more admitted payload snapshots whose `source_endpoint` equals `/erp/orders`

Current evaluator behavior:
- returns `is_ready=True` only when the current admitted bundle contains one or more `/erp/orders` payload snapshots
- requires the admitted batch snapshot to keep `batch_status == "captured"`
- requires the admitted batch snapshot to keep `transformed_at is None`
- does not require `analysis_batches`
- does not gate on `error_message`
- does not write lifecycle fields
- does not write serving projection rows
- does not schedule, reserve, or execute transform work

Current decision shape:
- `capture_batch_id`
- `slice_name`
- `is_ready`
- `reason`
- `matched_payload_count`

These readiness conditions are intentionally narrow.
They only constrain where future readiness may start and what kind of persisted truth it may depend on.
They do not define a general-purpose readiness policy, scheduler, or state machine.

If later work needs the narrower state-transition edge, that scope must continue into [transform-state-transition-boundary.md](./transform-state-transition-boundary.md) rather than being inferred from this readiness layer alone.

## What Is Still Not Defined

The following points are intentionally left to a later scoped migration:
- which statuses beyond the current first-slice `captured` gate are eligible for transform-ready input
- whether slices beyond the current `/erp/orders` sales-orders slice require different endpoint, page, or source completeness rules
- whether partial captures can ever become transform-ready input
- whether duplicate payloads block readiness, are ignored, or are coalesced
- whether freshness windows, replay rules, or retry semantics affect readiness
- whether readiness requires locking, reservation, or concurrency coordination
- whether `analysis_batches` later becomes required context, optional supporting context, or remains outside the first readiness slice
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

## Current Code Locations

The current minimal readiness evaluator implementation lives under:
- `src/app/services/transform_readiness_evaluator.py`
- `src/app/schemas/transform.py`
- `src/app/services/admitted_transform_selector.py`

## What This Document Does Not Claim

This document does not claim that:
- every current batch is already transform-ready input
- `batch_status` already encodes transform readiness policy
- a general-purpose readiness checker already exists in code
- legacy readiness orchestration belongs in the new repository
- research, evidence, troubleshooting, or reference material can define transform-ready input

## Current Verified Coverage

The current readiness evaluator coverage is verified at the formal-layer test level.

The current coverage exercises:
- return `ready` for the current first sales-orders slice when admitted input keeps `batch_status == "captured"` and `transformed_at is None`
- return a non-ready decision when `/erp/orders` payload snapshots are missing
- return a non-ready decision when the admitted batch snapshot is not `captured`
- return a non-ready decision when the admitted batch snapshot already carries `transformed_at`

The current verification file is:
- `tests/test_transform_readiness_and_lifecycle.py`

## Future Scoped Migration Requirement

If a later scoped migration introduces transform readiness behavior, it must explicitly define:
- the readiness rule set beyond this structural minimum
- whether readiness is separate from admission or derived from it
- how readiness interacts with state transitions and transform execution
- whether transform-ready input writes only serving outputs or also updates capture-side lifecycle facts

Beyond the current first readiness evaluator, later scoped migration work is still required before broader transform readiness behavior becomes formal repository behavior.
