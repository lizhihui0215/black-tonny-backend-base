# /erp/orders First-Slice Relation Doc

状态：source-intelligence / working relation doc

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../../README.md)
- [docs/README.md](../../README.md)
- [docs/](../../README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

这份 relation doc 是 `/erp/orders` current first slice 的第一份真实关系级样板。

它只做一件事：
- 把当前 first `sales_orders` slice 已经成立的 source-to-serving 关系、source-vs-injected 边界关系、以及 item-like adjacent clue 的保守 relation status，重写成一份可复用 relation doc

当前上游对象：
- [migration-charter.md](../migration-charter.md)
- [erp-orders-api-dossier.md](../apis/erp-orders-api-dossier.md)
- [erp-orders-first-slice-field-dictionary.md](../fields/erp-orders-first-slice-field-dictionary.md)

当前配套 serving-readiness 样板位于：
- [erp-orders-first-slice-serving-readiness.md](../serving-readiness/erp-orders-first-slice-serving-readiness.md)

这份 relation doc 不做：
- 不做全局 relation graph
- 不做 `/erp/orders` full relation universe
- 不做 broader inventory relation
- 不把 item-like candidate clues 升级成 confirmed relation
- 不做 serving-readiness doc

## Scope Boundary

当前只覆盖三类关系：

1. source payload fields -> current `sales_orders` serving slice fields
2. source payload fields 与 injected context fields 的边界关系
3. current item-like / adjacent clues 的保守 relation status

当前明确不覆盖：
- relation graph beyond the current first `sales_orders` slice
- item-like source truth
- broader `/erp/orders` target relation truth
- inventory-connected relations

## Relation Summary Matrix

| relation statement | relation type | evidence level | current serving value | current limit |
| --- | --- | --- | --- | --- |
| `rows[*].order_id` -> `SalesOrderProjectionFact.order_id` -> `sales_orders.order_id` | source-to-serving field relation | `Confirmed` | forms the current first-slice order identity clue together with injected `analysis_batch_id` | does not settle broader source-side order identity semantics |
| `rows[*].paid_at` -> `SalesOrderProjectionFact.paid_at` -> `sales_orders.paid_at` | source-to-serving field relation | `Confirmed` | carries the current paid timestamp fact into serving | does not settle timezone or business clock semantics |
| `rows[*].paid_amount` -> `SalesOrderProjectionFact.paid_amount` -> `sales_orders.paid_amount` | source-to-serving field relation | `Confirmed` | carries the current paid amount fact into serving | does not settle currency, refund, or rounding semantics |
| `rows[*].payment_status` -> `SalesOrderProjectionFact.payment_status` -> `sales_orders.payment_status` | source-to-serving field relation | `Confirmed` | keeps the current first contract explicit about payment-state writes | does not settle broader lifecycle vocabulary or state machine semantics |
| `rows[*].store_id` -> `SalesOrderProjectionFact.store_id` -> `sales_orders.store_id` | source-to-serving field relation | `Supported` | preserves optional store context without widening the current identity | does not settle stronger store taxonomy or normalization semantics |
| linked `analysis_batches.analysis_batch_id` -> `SalesOrderProjectionFact.analysis_batch_id` -> `sales_orders.analysis_batch_id` | injected-context-to-serving relation | `Confirmed` | provides the batch-scoped serving identity half required by the current contract | is not a source payload field relation |
| admitted batch `capture_batch_id` -> `SalesOrderProjectionFact.capture_batch_id` -> `sales_orders.capture_batch_id` | injected-context-to-serving relation | `Confirmed` | preserves source-batch traceability in the current serving row | is not a source payload field relation and is not part of current identity |
| `analysis_batch_id` / `capture_batch_id` are outside `/erp/orders` payload rows | source-vs-injected boundary relation | `Confirmed` | keeps payload research separate from injected normalization context | does not answer broader lineage policy |
| item-like clue cluster (`sku_id/style_code/color_code/size_code/quantity`) has only downstream adjacency to the current line | adjacent clue relation | `Candidate` | marks a useful neighborhood for later narrower relation work | does not confirm source payload existence, carrier, or source-to-serving mapping |
| broader `/erp/orders` rows-to-item relation stays outside the current first-slice relation sample | adjacent clue relation | `Deferred` | prevents this sample from over-claiming item relations before source-side evidence exists | does not mean item-like work is irrelevant or absent |

## Current Source-To-Serving Field Relations

### `rows[*].order_id` -> `sales_orders.order_id`

- relation type: source-to-serving field relation
- evidence level: `Confirmed`
- source evidence / provenance note:
  - current path requires `row.get("order_id")` to be a non-empty string
  - current path normalizes it into `SalesOrderProjectionFact.order_id`
  - current `sales_orders` contract uses `analysis_batch_id + order_id` as the current identity and upsert key
- current serving value:
  - this is the current first-slice order identifier clue on the source side
  - it is the only source payload field that participates directly in the current serving unique key
- current risk / unresolved note:
  - current repo only confirms this first-slice identity use
  - it does not yet settle broader source-side order identity semantics across `/erp/orders`

### `rows[*].paid_at` -> `sales_orders.paid_at`

- relation type: source-to-serving field relation
- evidence level: `Confirmed`
- source evidence / provenance note:
  - current path requires `row.get("paid_at")`
  - current path normalizes it through ISO-8601-compatible datetime parsing
  - current contract persists the normalized value into `sales_orders.paid_at`
- current serving value:
  - gives the current first-slice serving row a paid timestamp fact
- current risk / unresolved note:
  - timezone interpretation, source clock policy, and freshness semantics remain outside the current relation answer

### `rows[*].paid_amount` -> `sales_orders.paid_amount`

- relation type: source-to-serving field relation
- evidence level: `Confirmed`
- source evidence / provenance note:
  - current path requires `row.get("paid_amount")`
  - current path normalizes it through decimal-compatible parsing
  - current contract persists the normalized value into `sales_orders.paid_amount`
- current serving value:
  - gives the current first-slice serving row its minimal monetary amount fact
- current risk / unresolved note:
  - currency meaning, unit policy, refund interaction, and rounding semantics remain outside the current relation answer

### `rows[*].payment_status` -> `sales_orders.payment_status`

- relation type: source-to-serving field relation
- evidence level: `Confirmed`
- source evidence / provenance note:
  - current path requires `row.get("payment_status")` to be a non-empty string
  - current path normalizes it into `SalesOrderProjectionFact.payment_status`
  - current contract requires explicit caller-provided `payment_status` and does not use the broader table default as the contract rule
- current serving value:
  - keeps the current serving write explicit about payment state instead of silently inheriting a persistence default
- current risk / unresolved note:
  - broader enum vocabulary, lifecycle transitions, and payment-state semantics remain outside the current relation answer

### `rows[*].store_id` -> `sales_orders.store_id`

- relation type: source-to-serving field relation
- evidence level: `Supported`
- source evidence / provenance note:
  - current path accepts `row.get("store_id")` only when provided as a non-empty string
  - current path normalizes it into optional `SalesOrderProjectionFact.store_id`
  - current contract persists it but excludes it from the current identity and upsert key
- current serving value:
  - preserves optional store context on the serving row without widening the current first-slice identity
- current risk / unresolved note:
  - current repo confirms optional pass-through behavior, but does not yet close stronger source-side store taxonomy or normalization semantics

## Source Payload Fields Vs Injected Context Fields

### `analysis_batch_id` Boundary

- relation type: source-vs-injected boundary relation
- evidence level: `Confirmed`
- source evidence / provenance note:
  - current path resolves exactly one linked `analysis_batches` row per `capture_batch_id`
  - current path docs explicitly say `analysis_batch_id` is injected from the one linked `analysis_batches` row
  - current field dictionary explicitly excludes `analysis_batch_id` from `/erp/orders` payload fields
- current serving value:
  - `analysis_batch_id` supplies the batch-scoped serving identity half for the current `sales_orders` slice
- current risk / unresolved note:
  - current repo confirms this as injected context, not as a `/erp/orders` payload field
  - broader lineage policy remains outside the current relation sample

### `capture_batch_id` Boundary

- relation type: source-vs-injected boundary relation
- evidence level: `Confirmed`
- source evidence / provenance note:
  - current path docs explicitly say `capture_batch_id` is injected from the admitted batch snapshot
  - current path code passes `admitted_input.batch.capture_batch_id` into `SalesOrderProjectionFact.capture_batch_id`
  - current field dictionary explicitly excludes `capture_batch_id` from `/erp/orders` payload fields
- current serving value:
  - preserves batch traceability on the current serving row
- current risk / unresolved note:
  - current repo confirms this as injected context, not as a `/erp/orders` payload field
  - it is persisted but not part of the current identity or upsert key

### Current Boundary Rule

- relation type: source-vs-injected boundary relation
- evidence level: `Confirmed`
- source evidence / provenance note:
  - current path docs separate required source row clues from injected context
  - current field dictionary explicitly separates payload-path fields from injected fields
- current serving value:
  - prevents source field research from accidentally absorbing downstream normalization context
- current risk / unresolved note:
  - this boundary is current first-slice truth only; it does not define a full lineage model for future slices

## Current Item-Like / Adjacent Clue Relation Status

### Item-Like Vocabulary Neighborhood

- relation type: adjacent clue relation
- evidence level: `Candidate`
- source evidence / provenance note:
  - current adjacent payload-family baseline keeps a rows-adjacent non-`sales_orders` family as a same-line candidate
  - current field dictionary keeps `sku_id`, `style_code`, `color_code`, `size_code`, and `quantity` out of the first-slice field set
  - current `sales_order_items` serving contract proves downstream item-like serving vocabulary exists, but explicitly does not claim source truth for `/erp/orders`
- current serving value:
  - marks a useful downstream neighborhood for later narrower relation work
- current risk / unresolved note:
  - this does not confirm that any of these names already exist as `/erp/orders` source payload fields
  - this does not confirm carrier, container, attachment rule, or source-to-serving mapping

### Broader Rows-To-Item Relation

- relation type: adjacent clue relation
- evidence level: `Deferred`
- source evidence / provenance note:
  - current first path and current first-slice field dictionary stop at `sales_orders`
  - current dossier keeps the rows-adjacent non-`sales_orders` family open and unresolved
- current serving value:
  - keeps this sample from over-claiming item relations before repo-owned source evidence exists
- current risk / unresolved note:
  - broader row-to-item relation still requires separate source-side carrier, relation, and detail-clue work

## What This Relation Doc Makes Explicit

这份 relation doc 当前新增了四件明确的 repo-owned knowledge：

1. `/erp/orders` first slice 的 source-to-serving field relations，已经可以被单独沉淀成 relation-level asset。
2. source payload fields 与 injected context fields 的边界现在被显式写清，而不是隐含在 path code 里。
3. first-slice direct relations 和 item-like adjacent clue relations 被明确分层：
   - first-slice direct relations mostly land at `Confirmed`
   - optional store relation stays at `Supported`
   - item-like adjacency only lands at `Candidate` / `Deferred`
4. relation doc 可以在不扩写成全局 relation graph 的前提下，承接 dossier 与 field dictionary 继续向下收口。

## What This Relation Doc Does Not Claim

这份 relation doc 不声称：
- `/erp/orders` 全局 relation graph 已完成
- item-like clue 已经形成 confirmed source-to-serving relation
- broader `/erp/orders` target relation truth 已闭合
- inventory-connected relation 已进入当前样板
- broader serving-readiness 已经成立
