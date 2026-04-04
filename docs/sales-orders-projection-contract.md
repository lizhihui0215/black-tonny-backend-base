# Sales Orders Projection Contract

This document defines the current first `sales_orders` serving projection contract landed in `black-tonny-backend-base`.

For the broader serving persistence surface that this contract narrows, use [serving-projection-minimal-boundary.md](./serving-projection-minimal-boundary.md).
For the current transform readiness edge that stays upstream of this contract, use [transform-readiness-boundary.md](./transform-readiness-boundary.md).
For the current transform state-transition edge that stays adjacent to this contract, use [transform-state-transition-boundary.md](./transform-state-transition-boundary.md).
For the current first minimal end-to-end path that now invokes this contract, use [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md).
For the minimum future question list that a first adjacent `/erp/orders` contract must answer before it becomes formal repository behavior, use [orders-first-adjacent-contract-questions.md](./orders-first-adjacent-contract-questions.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

A minimal first-slice `sales_orders` serving projection contract is now implemented in `black-tonny-backend-base`.

That contract is intentionally narrow.
It only formalizes how one current first-slice bundle of transform-ready normalized facts is written into `sales_orders`.

It does not define:
- a runtime serving path
- a full transform executor
- a capture-to-serving orchestration path
- `sales_order_items`
- inventory projections
- dashboard or summary runtime behavior

## Current Contract Input

Current contract input:
- one or more `SalesOrderProjectionFact` values

Current fact shape:
- `analysis_batch_id`
- `capture_batch_id`
- `store_id`
- `order_id`
- `paid_at`
- `paid_amount`
- `payment_status`

Current input guardrails:
- `analysis_batch_id`, `capture_batch_id`, `order_id`, `paid_at`, `paid_amount`, and `payment_status` are required by the current first-slice contract
- `store_id` remains optional
- the current contract requires callers to provide `payment_status` explicitly
- the broader table-level `payment_status = "paid"` default remains part of the generic persistence surface and is not the current contract helper's admission or overwrite rule

## Current Identity And Upsert Key

Current first-slice identity:
- one `sales_orders` projection row per `analysis_batch_id + order_id`

Current upsert key:
- `analysis_batch_id`
- `order_id`

Current persistence constraint:
- `sales_orders` now keeps a unique constraint on `analysis_batch_id + order_id`

Current migration assumption:
- the current serving migration assumes the existing `sales_orders` table does not already contain duplicate `analysis_batch_id + order_id` pairs
- if historical duplicates ever exist in a real serving database, a dedicated dedupe migration must run before the current unique constraint can be applied safely

`capture_batch_id` is part of the current normalized fact input and persisted output, but it is not part of the current identity or upsert key.
`store_id` is also not part of the current identity or upsert key.

## Current Dedupe And Overwrite Strategy

Current in-call dedupe strategy:
- when multiple input facts in one apply call share the same upsert key, the last fact in input order wins

Current apply-transaction rule:
- one current contract apply call runs inside one serving-side transaction
- if any current create or update step raises before the apply call finishes, the helper rolls back the current serving-side writes from that apply call before it re-raises the failure

Current overwrite strategy for an existing row matched by the current upsert key:
- keep the existing row identity and `created_at`
- overwrite `capture_batch_id`
- overwrite `store_id`
- overwrite `paid_at`
- overwrite `paid_amount`
- overwrite `payment_status`
- let `updated_at` continue as the system-managed modification timestamp

Current overwrite non-goals:
- no multi-row merge logic
- no partial-field conflict resolution
- no retry or replay policy
- no cross-slice overwrite policy

## Relationship To The Broader Persistence Surface

The broader `sales_orders` persistence surface still exists under [serving-projection-minimal-boundary.md](./serving-projection-minimal-boundary.md).

That broader surface continues to formalize:
- the `sales_orders` model
- the `sales_orders` schema types
- generic CRUD helpers
- serving migrations

This narrower contract adds:
- one first-slice identity
- one first-slice upsert key
- one first-slice dedupe rule
- one first-slice overwrite rule
- one helper that applies those rules

The generic CRUD helpers remain broader than this contract.
They are not the current first-slice contract helper, and they are not a capture-to-serving runtime path by themselves.
The current first capture-to-serving path now calls this contract through a separate narrower path service.

## Current Code Locations

The current first `sales_orders` contract is implemented in:
- `src/app/models/sales_order.py`
- `src/app/schemas/sales.py`
- `src/app/crud/crud_sales_orders.py`
- `src/app/services/sales_orders_projection_contract.py`
- `src/migrations/serving_versions/20260402_04_add_sales_orders_projection_contract.py`

## Current Verified Coverage

The current contract coverage is verified at the formal-layer test level.

The current coverage exercises:
- insert one first-slice `sales_orders` row through the current contract helper
- update one existing row through the current upsert key while preserving row identity
- dedupe duplicate input facts within one apply call by keeping the last fact in input order
- enforce the current unique key at the persistence layer
- roll back serving-side writes from one apply call when a later write in the same call fails

The current verification files are:
- `tests/test_sales_orders_projection_contract.py`
- `tests/test_serving_projection_contract_docs.py`

## What Is Still Not Defined

The following points are intentionally left to a later scoped migration:
- how transform-ready normalized facts are produced end to end from the current capture-side inputs
- how broader runtime or orchestration entry points invoke the current first-slice path
- whether `sales_order_items` adopts a parallel contract and, if so, with what identity and overwrite policy
- whether later slices reuse this identity pattern or require different keys
- whether retry, replay, resume, or scheduling rules affect serving writes
- whether broader serving-side summaries or runtime APIs read from this contract

## What This Document Does Not Claim

This document does not claim that:
- a full capture-to-serving projection path is already implemented
- `sales_order_items` now shares the same contract
- inventory projections share this contract
- runtime serving routes now write `sales_orders`
- a broader serving orchestration layer already exists
