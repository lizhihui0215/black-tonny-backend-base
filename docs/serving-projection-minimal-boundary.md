# Serving Projection Minimal Boundary

This document defines the minimal formal serving projection boundary currently landed in `black-tonny-backend-base`.

For the current dual-database split, use [capture-serving-boundary.md](./capture-serving-boundary.md).
For the repository runtime structure, use [runtime-boundaries.md](./runtime-boundaries.md).
For the current capture formal boundary, use [capture-minimal-boundary.md](./capture-minimal-boundary.md).
For the current first `sales_orders` serving projection contract layered on top of this persistence surface, use [sales-orders-projection-contract.md](./sales-orders-projection-contract.md).
For the repository docs index, use [docs/README.md](./README.md).

The current repository database premise for this formal serving projection boundary is PostgreSQL.

## Scope

This boundary is intentionally narrow.
It only formalizes:
- serving-side ORM models
- serving-side schemas and CRUD helpers
- serving Alembic migration targets
- the first `sales_orders` serving projection contract helper and its persistence constraint

It does not introduce:
- runtime routers
- runtime serving APIs
- transform behavior
- serving projection executors
- any projection identity or upsert policy beyond the current first `sales_orders` slice

## Formal Ownership

The current formal ownership is:
- `src/app/models/`
- `src/app/schemas/`
- `src/app/crud/`
- `src/app/services/sales_orders_projection_contract.py`
- `src/app/core/migration_targets.py`
- `src/migrations/serving_versions/`

It does not belong to:
- `src/examples/`
- `docs/reference/**`
- `docs/archive/**`

## Landed Tables

The current minimal formal serving projection tables are:
- `sales_orders`
- `sales_order_items`
- `inventory_current`
- `inventory_daily_snapshot`

### `sales_orders`

Current formal fields:
- `id`
- `analysis_batch_id`
- `capture_batch_id`
- `store_id`
- `order_id`
- `paid_at`
- `paid_amount`
- `payment_status`
- `created_at`
- `updated_at`

Current purpose:
- persist one minimal sales-order projection row
- keep batch linkage as persisted facts only
- avoid admitting transform execution or runtime serving behavior into the boundary itself
- support one narrower first-slice `sales_orders` projection contract without expanding to broader serving behavior

Current guardrails:
- `analysis_batch_id`, `order_id`, `paid_at`, and `paid_amount` are required at the current minimal persistence stage
- `paid_amount` is stored as PostgreSQL `NUMERIC(18,2)` and is exposed through the current schemas as `Decimal`
- `capture_batch_id` and `store_id` stay nullable
- `payment_status` defaults to `paid`
- under the current minimal persistence boundary, that default is a temporary persisted placeholder, not a finalized serving business contract or filter policy
- the narrower first-slice `sales_orders` contract now defines one explicit identity, upsert key, dedupe rule, and overwrite rule through [sales-orders-projection-contract.md](./sales-orders-projection-contract.md)

### `sales_order_items`

Current formal fields:
- `id`
- `analysis_batch_id`
- `capture_batch_id`
- `order_id`
- `sku_id`
- `style_code`
- `color_code`
- `size_code`
- `quantity`
- `created_at`
- `updated_at`

Current purpose:
- persist one minimal sales-order-item projection row
- keep item-level sales quantity facts without admitting transform or runtime serving behavior

Current guardrails:
- `analysis_batch_id`, `order_id`, `sku_id`, and `quantity` are required at the current minimal persistence stage
- `capture_batch_id`, `style_code`, `color_code`, and `size_code` stay nullable
- `order_id` is currently a non-enforced business reference that is intended to correspond to `sales_orders.order_id` when both tables are populated
- the current boundary does not enforce that correspondence with a foreign key, uniqueness rule, or joined-read contract

### `inventory_current`

Current formal fields:
- `id`
- `analysis_batch_id`
- `capture_batch_id`
- `store_id`
- `sku_id`
- `style_code`
- `color_code`
- `size_code`
- `on_hand_qty`
- `safe_stock_qty`
- `season_tag`
- `is_all_season`
- `is_target_size`
- `is_active_sale`
- `updated_at`

Current purpose:
- persist one minimal current-inventory projection row
- keep quantitative inventory facts and optional inventory classification flags without admitting transform or runtime serving behavior

Current guardrails:
- `analysis_batch_id`, `sku_id`, `on_hand_qty`, and `safe_stock_qty` are required at the current minimal persistence stage
- `on_hand_qty` and `safe_stock_qty` are stored as PostgreSQL `NUMERIC(18,2)` and are exposed through the current schemas as `Decimal`
- `capture_batch_id`, `store_id`, `style_code`, `color_code`, `size_code`, `season_tag`, `is_all_season`, `is_target_size`, and `is_active_sale` stay nullable
- nullable inventory flags are persisted facts only at this stage; a missing flag does not imply `true`, `false`, or any finalized inventory classification policy
- `updated_at` is a system-managed modification timestamp, not current serving freshness or transform-policy truth

### `inventory_daily_snapshot`

Current formal fields:
- `id`
- `analysis_batch_id`
- `capture_batch_id`
- `snapshot_date`
- `store_id`
- `sku_id`
- `style_code`
- `color_code`
- `size_code`
- `on_hand_qty`
- `safe_stock_qty`
- `season_tag`
- `is_all_season`
- `is_target_size`
- `is_active_sale`
- `created_at`

Current purpose:
- persist one minimal daily inventory snapshot row
- keep snapshot-date inventory facts without admitting transform or runtime serving behavior

Current guardrails:
- `analysis_batch_id`, `snapshot_date`, `sku_id`, `on_hand_qty`, and `safe_stock_qty` are required at the current minimal persistence stage
- `on_hand_qty` and `safe_stock_qty` are stored as PostgreSQL `NUMERIC(18,2)` and are exposed through the current schemas as `Decimal`
- `capture_batch_id`, `store_id`, `style_code`, `color_code`, `size_code`, `season_tag`, `is_all_season`, `is_target_size`, and `is_active_sale` stay nullable
- nullable inventory flags are persisted facts only at this stage; a missing flag does not imply `true`, `false`, or any finalized inventory classification policy
- `snapshot_date` is a persisted date fact, not a finalized reporting-window or delta-computation contract

## Code Locations

The current formal serving projection boundary is implemented in:
- `src/app/models/inventory_current.py`
- `src/app/models/inventory_daily_snapshot.py`
- `src/app/models/sales_order.py`
- `src/app/models/sales_order_item.py`
- `src/app/schemas/inventory.py`
- `src/app/schemas/sales.py`
- `src/app/crud/crud_inventory_current.py`
- `src/app/crud/crud_inventory_daily_snapshots.py`
- `src/app/crud/crud_sales_orders.py`
- `src/app/crud/crud_sales_order_items.py`
- `src/app/services/sales_orders_projection_contract.py`
- `src/app/core/migration_targets.py`
- `src/migrations/serving_versions/20260401_02_add_sales_projection_tables.py`
- `src/migrations/serving_versions/20260401_03_add_inventory_projection_tables.py`
- `src/migrations/serving_versions/20260402_04_add_sales_orders_projection_contract.py`

## Current Read/List Boundary

Current formal read helpers:
- `get_inventory_current_read`
- `list_inventory_current_reads`
- `get_inventory_daily_snapshot_read`
- `list_inventory_daily_snapshot_reads`
- `get_sales_order_read`
- `get_sales_order_read_by_projection_key`
- `list_sales_order_reads`
- `get_sales_order_item_read`
- `list_sales_order_item_reads`

Current list-read shape:
- list helpers return a fixed boundary shape with `data` and `total_count`
- filtered empty results keep `data=[]` and `total_count=0`
- paginated results keep stable ascending `id` ordering while `total_count` remains the full filtered count

Supported query boundary:
- `list_inventory_current_reads` supports equality filters on `analysis_batch_id`, `store_id`, and `sku_id`
- `list_inventory_daily_snapshot_reads` supports equality filters on `analysis_batch_id`, `snapshot_date`, and `sku_id`
- `get_sales_order_read_by_projection_key` supports one exact-match read on `analysis_batch_id + order_id`
- `list_sales_order_reads` supports equality filters on `analysis_batch_id` and `order_id`
- `list_sales_order_item_reads` supports equality filters on `analysis_batch_id`, `order_id`, and `sku_id`

Unsupported query boundary:
- no joined reads
- no upsert helpers beyond the current first `sales_orders` contract helper
- no projection overwrite policy beyond the current first `sales_orders` slice
- no caller-supplied sort overrides
- no runtime summary queries

## Current Verified Boundary Coverage

The current minimal boundary coverage is verified at the formal-layer test level, not through a runtime API.

The current coverage exercises:
- create, read, and update one `inventory_current` row through the formal CRUD path
- list filtered `inventory_current` rows with stable pagination and empty-result shape
- create, read, and update one `inventory_daily_snapshot` row through the formal CRUD path
- list filtered `inventory_daily_snapshot` rows with stable pagination and empty-result shape
- create, read, and update one `sales_orders` row through the formal CRUD path
- list filtered `sales_orders` rows with stable pagination and empty-result shape
- create, read, and update one `sales_order_items` row through the formal CRUD path
- list filtered `sales_order_items` rows with stable pagination and empty-result shape
- apply the current first `sales_orders` projection contract through the dedicated helper
- enforce the current first `sales_orders` identity at the persistence layer
- verify minimal defaults and field-length constraints for all current serving projection tables
- verify serving migration target metadata includes these tables while capture metadata does not

The current verification files are:
- `tests/test_inventory_projection_formal_surface.py`
- `tests/test_sales_projection_formal_surface.py`
- `tests/test_sales_orders_projection_contract.py`
- `tests/test_serving_projection_contract_docs.py`
- `tests/test_migration_targets.py`

## Explicit Non-Goals

This document does not claim that:
- a serving projection runtime path is implemented
- any projection identity or upsert contract beyond the current first `sales_orders` slice is finalized
- transform writes into these tables are implemented
- dashboard or summary runtime APIs read these tables yet
- low-stock, seasonal, target-size, or active-sale policy is finalized
