# /erp/orders First-Slice Field Dictionary

状态：source-intelligence / working field dictionary

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../../README.md)
- [docs/README.md](../../README.md)
- [docs/](../../README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

这份 field dictionary 是 `/erp/orders` 的第一份真实字段级样板。

它只做一件事：
- 把当前 first `sales_orders` slice 已经真正消费、且最有 serving 价值的 `/erp/orders` 字段，重写成可复用 field dictionary 记录

当前上游对象：
- [migration-charter.md](../migration-charter.md)
- [erp-orders-api-dossier.md](../apis/erp-orders-api-dossier.md)

当前配套 relation doc 样板位于：
- [erp-orders-first-slice-relation-doc.md](../relations/erp-orders-first-slice-relation-doc.md)

当前配套 serving-readiness 样板位于：
- [erp-orders-first-slice-serving-readiness.md](../serving-readiness/erp-orders-first-slice-serving-readiness.md)

这份 field dictionary 不做：
- 不做 `/erp/orders` 全量字段大全
- 不做 adjacent item-like fields 的 source truth
- 不做 relation baseline
- 不做 serving-readiness doc
- 不把 downstream persistence vocabulary 自动升级成 source-side field truth

## Selection Boundary

当前只收录第一批高价值字段：
- `order_id`
- `paid_at`
- `paid_amount`
- `payment_status`
- `store_id`

选择规则只有一条：
- 这些字段已经被 current first path 直接消费，且对 `sales_orders` downstream serving 判断最有价值

当前明确不收录：
- injected context fields，例如 `analysis_batch_id`、`capture_batch_id`
- rows-adjacent item-like candidate vocabulary，例如 `sku_id`、`style_code`、`color_code`、`size_code`、`quantity`
- top-level envelope sibling keys

## Dictionary Summary

| field name | payload path | evidence level | current serving value | current limit |
| --- | --- | --- | --- | --- |
| `order_id` | `rows[*].order_id` | `Confirmed` | current first-slice row identity clue; combines with injected `analysis_batch_id` into the current `sales_orders` unique key | does not settle broader source-side order identity semantics |
| `paid_at` | `rows[*].paid_at` | `Confirmed` | current paid timestamp clue written into `sales_orders.paid_at` | timezone / freshness / business clock semantics remain unclosed |
| `paid_amount` | `rows[*].paid_amount` | `Confirmed` | current paid amount clue written into `sales_orders.paid_amount` | currency / refund / rounding semantics remain unclosed |
| `payment_status` | `rows[*].payment_status` | `Confirmed` | current explicit payment-state clue required by the first contract | enum vocabulary and broader lifecycle semantics remain unclosed |
| `store_id` | `rows[*].store_id` | `Supported` | optional store reference clue passed through into `sales_orders.store_id` | store taxonomy and stronger source-side meaning remain unclosed |

## Field Records

### `order_id`

- field name: `order_id`
- payload path: `rows[*].order_id`
- meaning:
  - current repo treats this as the required non-empty order-level identifier clue for the first `sales_orders` slice
  - current path normalizes it into `SalesOrderProjectionFact.order_id`
  - current contract combines it with injected `analysis_batch_id` to identify one `sales_orders` projection row
- evidence level: `Confirmed`
- source evidence / provenance note:
  - current path requires `row.get("order_id")` to be a non-empty string
  - current path docs list `order_id` as a required row clue
  - current `sales_orders` contract defines `analysis_batch_id + order_id` as the current identity and upsert key
- current serving value:
  - required to normalize any `/erp/orders` row into the current first-slice serving fact
  - required to dedupe and upsert current `sales_orders` rows
- current risk / unresolved note:
  - current repo only confirms first-slice serving identity use
  - it does not yet settle broader source-side order identity semantics across the whole `/erp/orders` line

### `paid_at`

- field name: `paid_at`
- payload path: `rows[*].paid_at`
- meaning:
  - current repo treats this as the required paid timestamp clue for the first `sales_orders` slice
  - current path accepts either a `datetime` object or an ISO-8601 string, and normalizes it into `SalesOrderProjectionFact.paid_at`
- evidence level: `Confirmed`
- source evidence / provenance note:
  - current path requires `row.get("paid_at")`
  - `_parse_datetime` rejects non-datetime and non-ISO-8601-compatible inputs
  - current path docs list `paid_at` as a required row clue
- current serving value:
  - persisted into `sales_orders.paid_at`
  - participates in the minimal downstream paid-order record shape
- current risk / unresolved note:
  - current repo does not yet formalize timezone policy, source clock semantics, or freshness expectations

### `paid_amount`

- field name: `paid_amount`
- payload path: `rows[*].paid_amount`
- meaning:
  - current repo treats this as the required paid amount clue for the first `sales_orders` slice
  - current path normalizes it into a decimal-compatible `SalesOrderProjectionFact.paid_amount`
- evidence level: `Confirmed`
- source evidence / provenance note:
  - current path requires `row.get("paid_amount")`
  - `_parse_decimal` rejects values that are not decimal-compatible
  - current path docs list `paid_amount` as a required row clue
- current serving value:
  - persisted into `sales_orders.paid_amount`
  - provides the current minimal amount fact for first-slice serving output
- current risk / unresolved note:
  - current repo does not yet formalize currency, unit policy, refund interaction, or rounding policy

### `payment_status`

- field name: `payment_status`
- payload path: `rows[*].payment_status`
- meaning:
  - current repo treats this as the required explicit payment-state clue for the first `sales_orders` slice
  - current path normalizes it into `SalesOrderProjectionFact.payment_status`
  - current `sales_orders` contract requires callers to provide it explicitly
- evidence level: `Confirmed`
- source evidence / provenance note:
  - current path requires `row.get("payment_status")` to be a non-empty string
  - current path docs list `payment_status` as a required row clue
  - current contract states the broader table default `payment_status = "paid"` is not the contract helper's admission or overwrite rule
- current serving value:
  - persisted into `sales_orders.payment_status`
  - keeps current serving writes from silently inheriting the broader table default
- current risk / unresolved note:
  - current repo does not yet formalize the allowed enum vocabulary, transition rules, or broader payment lifecycle semantics

### `store_id`

- field name: `store_id`
- payload path: `rows[*].store_id`
- meaning:
  - current repo treats this as an optional row-level store reference clue for the first `sales_orders` slice
  - when provided, current path passes it through into `SalesOrderProjectionFact.store_id`
  - current contract persists it but does not treat it as identity or upsert key material
- evidence level: `Supported`
- source evidence / provenance note:
  - current path accepts `row.get("store_id")` only when it is a non-empty string
  - current path docs list `store_id` as an optional row clue
  - current contract explicitly excludes `store_id` from the current identity and upsert key
- current serving value:
  - carries optional store context into `sales_orders.store_id`
  - preserves a useful downstream slice dimension without making the current identity wider
- current risk / unresolved note:
  - current repo confirms optional pass-through behavior, but does not yet formalize stronger source-side store taxonomy, hierarchy, or normalization semantics

## Deferred / Out-Of-Scope Fields

当前明确不进入这份样板的字段，包括：

- `analysis_batch_id`
- `capture_batch_id`
- `sku_id`
- `style_code`
- `color_code`
- `size_code`
- `quantity`

当前原因：
- `analysis_batch_id` 与 `capture_batch_id` 是 injected context，不是 `/erp/orders` payload path 字段
- item-like vocabulary 目前仍主要是 adjacent candidate / downstream vocabulary 线索，不应在这份 first-slice field dictionary 里被误写成 source truth

## What This Dictionary Makes Explicit

这份字典当前新增了三件明确的 repo-owned knowledge：

1. `/erp/orders` 第一批最有 serving 价值的 fields，已经能被单独沉淀成 field-level asset，而不是继续散在 dossier 和 contract docs 里。
2. current first `sales_orders` slice 的 required field set 与 optional field set 可以被清楚拆开：
   - required: `order_id` / `paid_at` / `paid_amount` / `payment_status`
   - optional: `store_id`
3. field-level certainty 和 field-level risk 可以同时存在：
   - required first-slice fields mostly land at `Confirmed`
   - optional context field `store_id` 保持在 `Supported`

## What This Dictionary Does Not Claim

这份字典不声称：
- `/erp/orders` 全量字段已经盘清
- rows-level full glossary 已完成
- item-like fields 已经成为 source truth
- broader relation semantics 已经闭合
- broader serving-readiness 已经成立
