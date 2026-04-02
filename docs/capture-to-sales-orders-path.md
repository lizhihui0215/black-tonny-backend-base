# Capture To Sales Orders Path

This document defines the current first minimal `capture -> transform -> serving` path landed in `black-tonny-backend-base`.

For the broader capture/serving dual-database split, use [capture-serving-boundary.md](./capture-serving-boundary.md).
For the admitted input selector that stays upstream of this path, use [admitted-transform-input-boundary.md](./admitted-transform-input-boundary.md).
For the first readiness evaluator that stays upstream of this path, use [transform-readiness-boundary.md](./transform-readiness-boundary.md).
For the first lifecycle helper that stays adjacent to this path, use [transform-state-transition-boundary.md](./transform-state-transition-boundary.md).
For the first `sales_orders` serving projection contract that stays downstream of this path, use [sales-orders-projection-contract.md](./sales-orders-projection-contract.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

A minimal first `capture -> transform -> serving` path is now implemented for the `sales_orders` slice in `black-tonny-backend-base`.

That path is intentionally narrow.
It only chains together:
- the admitted transform input selector
- the first-slice readiness evaluator
- the narrow capture-batch lifecycle helper
- the first `sales_orders` serving projection contract

It does not define:
- a general orchestration engine
- multi-slice transform behavior
- `sales_order_items`
- inventory projections
- runtime serving APIs
- retry, reopen, resume, or scheduling behavior

## Current Path Input

Current path function input:
- `capture_db`
- `serving_db`
- `capture_batch_id`

Current persisted-input dependency:
- one admitted transform input bundle selected from the current capture-side persisted facts
- exactly one linked `analysis_batches` row for the same `capture_batch_id`

`analysis_batches` remains outside the current admitted-input and readiness minimums.
At the current first path boundary, it is a downstream normalization prerequisite for the `sales_orders` contract rather than an upstream admission or readiness proof.

## Current Path Output

Current path output:
- one `CaptureToSalesOrdersPathResult`

Current output shape:
- `capture_batch_id`
- `slice_name`
- `status`
- `reason`
- `readiness_decision`
- `analysis_batch_id`
- `projection_result`
- `lifecycle_batch`
- `failure_message`

## Current Path Behavior

Current path order:
1. select admitted input from capture-side persisted facts
2. evaluate readiness for the current first `sales_orders` slice
3. resolve exactly one linked `analysis_batches` row
4. normalize `/erp/orders` payload rows into `SalesOrderProjectionFact` values
5. apply the `sales_orders` projection contract on the serving database
6. mark the capture batch as `transformed` only after the serving contract apply succeeds

Current `/erp/orders` normalization rule:
- only payload snapshots whose `source_endpoint == "/erp/orders"` participate in the current first path
- each participating payload must decode as one JSON object with a top-level `rows` list
- each current row must provide:
  - `order_id`
  - `paid_at`
  - `paid_amount`
  - `payment_status`
- each current row may optionally provide:
  - `store_id`
- the current path injects:
  - `analysis_batch_id` from the one linked `analysis_batches` row
  - `capture_batch_id` from the admitted batch snapshot
- duplicate normalized `analysis_batch_id + order_id` keys stay governed by the downstream `sales_orders` contract

## Current No-Op Boundary

Current no-op behavior:
- when the admitted selector returns `None`, the path returns:
  - `status = "noop"`
  - `reason = "missing_admitted_input"`
- in that case, the path does not:
  - write serving projection rows
  - write lifecycle fields

At the current narrow boundary, this no-op result intentionally covers both selector-level cases:
- the batch row is missing
- the batch row exists but no linked payload rows are readable

The path does not currently split those two selector-level cases into separate path statuses.

## Current Non-Ready Boundary

Current non-ready behavior:
- when admitted input exists but the current first readiness evaluator returns `is_ready=False`, the path returns:
  - `status = "non_ready"`
  - `reason = "not_ready"`
  - the current `readiness_decision`

In that case, the path does not:
- write serving projection rows
- write lifecycle fields

## Current Success Boundary

Current success behavior:
- when admitted input exists
- and the current first readiness evaluator returns `ready`
- and exactly one linked `analysis_batches` row is readable
- and `/erp/orders` payload rows normalize successfully
- and the downstream `sales_orders` contract apply succeeds

Then the path:
- writes the current first-slice `sales_orders` projection rows on the serving database
- writes `captured -> transformed` on the capture batch through the narrow lifecycle helper
- returns:
  - `status = "succeeded"`
  - `reason = "applied"`
  - the current `readiness_decision`
  - the resolved `analysis_batch_id`
  - the downstream `projection_result`
  - the transformed `lifecycle_batch`

## Current Failure Boundary

Current failure-write behavior:
- after readiness has already returned `ready`, the path writes `captured -> failed` through the narrow lifecycle helper when any of the following current failures happens before success is finalized:
  - no linked `analysis_batches` row is readable
  - more than one linked `analysis_batches` row is readable
  - `/erp/orders` payload JSON cannot be normalized into the current first-slice row shape
  - the downstream `sales_orders` contract apply raises an exception

In that case, the path returns:
- `status = "failed"`
- one current failure `reason`
- the current `readiness_decision`
- the latest `failure_message`
- the failed `lifecycle_batch`

Current failure-write guardrail:
- the path writes `captured -> failed` only for this narrow post-readiness failure slice
- current no-op and non-ready results do not write `failed`

## Current Code Locations

The current first path is implemented in:
- `src/app/services/capture_to_sales_orders_path.py`
- `src/app/services/admitted_transform_selector.py`
- `src/app/services/transform_readiness_evaluator.py`
- `src/app/services/capture_batch_lifecycle.py`
- `src/app/services/sales_orders_projection_contract.py`
- `src/app/schemas/transform.py`
- `src/app/schemas/sales.py`

## Current Verified Coverage

The current first path coverage is verified at the formal-layer test level.

The current coverage exercises:
- apply the full success path through selector, readiness, contract apply, and `captured -> transformed`
- return a selector-level no-op result without writes
- return a non-ready result without writes
- mark the batch as `failed` when linked analysis context is missing after readiness
- mark the batch as `failed` when the downstream contract apply raises

The current verification files are:
- `tests/test_capture_to_sales_orders_path.py`
- `tests/test_capture_to_sales_orders_path_docs.py`

## What This Document Does Not Claim

This document does not claim that:
- a general transform or serving orchestration layer already exists
- multiple slices are already chained together
- `sales_order_items` is already part of this path
- inventory projections are already part of this path
- runtime serving routes invoke this path
- retry, reopen, resume, reservation, locking, or scheduling behavior is already formalized
