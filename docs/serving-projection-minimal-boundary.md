# Serving Projection Minimal Boundary

This document defines the minimal formal serving projection boundary currently landed in `black-tonny-backend-base`.

For the current dual-database split, use [capture-serving-boundary.md](./capture-serving-boundary.md).
For the repository runtime structure, use [runtime-boundaries.md](./runtime-boundaries.md).
For the current capture formal boundary, use [capture-minimal-boundary.md](./capture-minimal-boundary.md).
For the repository docs index, use [docs/README.md](./README.md).

The current repository database premise for this formal serving projection boundary is PostgreSQL.

## Scope

This boundary is intentionally narrow.
It only formalizes:
- serving-side ORM models
- serving-side schemas and CRUD helpers
- serving Alembic migration targets

It does not introduce:
- runtime routers
- runtime serving APIs
- transform behavior
- serving projection executors
- projection identity or upsert policy

## Formal Ownership

The current formal ownership is:
- `src/app/models/`
- `src/app/schemas/`
- `src/app/crud/`
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

Current guardrails:
- `analysis_batch_id`, `order_id`, `paid_at`, and `paid_amount` are required at the current minimal persistence stage
- `capture_batch_id` and `store_id` stay nullable
- `payment_status` defaults to `paid`

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

## Code Locations

The current formal serving projection boundary is implemented in:
- `src/app/models/sales_order.py`
- `src/app/models/sales_order_item.py`
- `src/app/schemas/sales.py`
- `src/app/crud/crud_sales_orders.py`
- `src/app/crud/crud_sales_order_items.py`
- `src/app/core/migration_targets.py`
- `src/migrations/serving_versions/20260401_02_add_sales_projection_tables.py`

## Current Read/List Boundary

Current formal read helpers:
- `get_sales_order_read`
- `list_sales_order_reads`
- `get_sales_order_item_read`
- `list_sales_order_item_reads`

Current list-read shape:
- list helpers return a fixed boundary shape with `data` and `total_count`
- filtered empty results keep `data=[]` and `total_count=0`
- paginated results keep stable ascending `id` ordering while `total_count` remains the full filtered count

Supported query boundary:
- `list_sales_order_reads` supports equality filters on `analysis_batch_id` and `order_id`
- `list_sales_order_item_reads` supports equality filters on `analysis_batch_id`, `order_id`, and `sku_id`

Unsupported query boundary:
- no joined reads
- no upsert helpers
- no projection overwrite policy
- no caller-supplied sort overrides
- no runtime summary queries

## Current Verified Boundary Coverage

The current minimal boundary coverage is verified at the formal-layer test level, not through a runtime API.

The current coverage exercises:
- create, read, and update one `sales_orders` row through the formal CRUD path
- list filtered `sales_orders` rows with stable pagination and empty-result shape
- create, read, and update one `sales_order_items` row through the formal CRUD path
- list filtered `sales_order_items` rows with stable pagination and empty-result shape
- verify minimal defaults and field-length constraints for both tables
- verify serving migration target metadata includes these tables while capture metadata does not

The current verification files are:
- `tests/test_sales_projection_formal_surface.py`
- `tests/test_migration_targets.py`

## Explicit Non-Goals

This document does not claim that:
- a serving projection runtime path is implemented
- a projection identity or upsert contract is finalized
- transform writes into these tables are implemented
- dashboard or summary runtime APIs read these tables yet
