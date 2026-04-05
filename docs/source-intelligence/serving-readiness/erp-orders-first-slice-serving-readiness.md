# /erp/orders First-Slice Serving Readiness

状态：source-intelligence / working serving-readiness doc

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../../README.md)
- [docs/README.md](../../README.md)
- [docs/](../../README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

这份 serving-readiness doc 是 `/erp/orders` current first slice 的第一份真实 readiness 样板。

它只做一件事：
- 把当前 first `sales_orders` slice 已经 readiness 到什么程度、哪些已可服务 serving、哪些仍不能升级承认，重写成一份可复用 serving-readiness doc

当前上游对象：
- [migration-charter.md](../migration-charter.md)
- [erp-orders-api-dossier.md](../apis/erp-orders-api-dossier.md)
- [erp-orders-first-slice-field-dictionary.md](../fields/erp-orders-first-slice-field-dictionary.md)
- [erp-orders-first-slice-relation-doc.md](../relations/erp-orders-first-slice-relation-doc.md)

这份 serving-readiness doc 不做：
- 不做全局 readiness map
- 不做第二个 relation doc
- 不做第二个 API dossier
- 不做 broader inventory readiness
- 不把 item-like candidate relations 升级成 serving-ready truth

## Scope Boundary

当前只回答三类 readiness 问题：

1. `/erp/orders` current first slice 哪些 source fields / relations 已经足以服务 current `sales_orders` downstream slice
2. 当前 landed downstream target 到底是谁
3. 哪些 candidate / deferred areas 仍不能升级承认为 serving-ready truth

当前明确不回答：
- broader `/erp/orders` adjacent readiness
- item-like source truth
- inventory readiness
- runtime API readiness

## Readiness Summary Matrix

| readiness statement | readiness status | evidence level | repo-owned basis | current implication | current limit |
| --- | --- | --- | --- | --- | --- |
| `/erp/orders` endpoint anchor is ready for the current first `sales_orders` slice | `ready now` | `Confirmed` | current first path formal docs/code/tests | current first slice already has one landed source endpoint anchor | does not mean the whole `/erp/orders` source line is ready |
| top-level payload carrier `object + rows list` is ready for the current first slice | `ready now` | `Confirmed` | current first path formal docs/code/tests | current first slice has a stable top-level carrier floor | does not settle sibling envelope fields |
| `order_id / paid_at / paid_amount / payment_status` are ready as the current required first-slice source field set | `ready now` | `Confirmed` | current field dictionary; current path normalization rule; current contract | current first slice can produce `SalesOrderProjectionFact` values for `sales_orders` | does not settle full rows-level glossary |
| `store_id` is serving-usable optional context for the current first slice | `ready but narrow` | `Supported` | current field dictionary; current path optional parse rule; current contract | optional store context can flow into `sales_orders.store_id` | stronger store taxonomy and semantics remain open |
| injected `analysis_batch_id` and `capture_batch_id` are ready as current normalization context | `ready now` | `Confirmed` | current path formal docs/code; current relation doc | current first slice has the extra context it needs to write `sales_orders` rows | these are not source payload fields |
| landed downstream target for this first-slice readiness answer is `sales_orders` | `ready now` | `Confirmed` | current path formal docs; `sales_orders` serving contract | current first slice already supports one landed downstream serving target | does not auto-extend to broader adjacent targets |
| item-like clue cluster (`sku_id/style_code/color_code/size_code/quantity`) is not serving-ready for source-side upgrade | `not ready` | `Candidate` | current relation doc; adjacent payload-family baseline; `sales_order_items` serving contract exclusions | current repo can keep this as a later neighborhood only | does not prove source field existence or mapping |
| broader rows-to-item relation stays outside current serving-ready truth | `cannot upgrade now` | `Deferred` | current relation doc; current dossier; current field dictionary boundary | blocks automatic readiness promotion to adjacent targets | does not mean the lane is irrelevant |

## Current Serving-Ready Core

### Ready Source Fields

当前已 serving-ready 的 source payload fields，只包括 current first `sales_orders` slice 直接消费的这一组：

- `rows[*].order_id`
- `rows[*].paid_at`
- `rows[*].paid_amount`
- `rows[*].payment_status`

evidence level:
- `Confirmed`

当前 serving value:
- 这四个字段已经足以支撑 current first path 把 `/erp/orders` row normalize 成 current `SalesOrderProjectionFact`
- 它们已经被 current `sales_orders` serving contract 接住并落到 serving

当前限制：
- 这只是 current first-slice required set
- 不等于 `/erp/orders` rows-level full field dictionary 已 ready

### Narrow Optional Serving Context

当前可保守承认的 optional source field 只有：

- `rows[*].store_id`

evidence level:
- `Supported`

当前 serving value:
- 当前 first slice 可以把它作为 optional store context 写入 `sales_orders.store_id`

当前限制：
- 只能说明 current optional pass-through behavior 已可用
- 不能推出 stronger source-side store taxonomy、normalization、或 cross-page/store semantics 已 ready

### Ready Source-To-Serving Relations

当前已 serving-ready 的 direct relations 只有：

- `rows[*].order_id` -> `sales_orders.order_id`
- `rows[*].paid_at` -> `sales_orders.paid_at`
- `rows[*].paid_amount` -> `sales_orders.paid_amount`
- `rows[*].payment_status` -> `sales_orders.payment_status`

evidence level:
- `Confirmed`

`rows[*].store_id` -> `sales_orders.store_id` 当前只应保守写成：
- `ready but narrow`
- `Supported`

## Current Landed Downstream Target

当前这份 readiness 样板唯一承认的 landed downstream target 是：

- `sales_orders`

evidence level:
- `Confirmed`

当前支撑：
- current first `capture -> transform -> serving` path 已 landed
- current first `sales_orders` serving projection contract 已 landed
- current first slice 的 required source fields / relations 已被当前 path 和 contract 实际消费

当前最多能说明：
- `/erp/orders` current first slice 已足以服务一个 narrow downstream target：`sales_orders`

当前不能推出：
- broader adjacent targets 已经 automatically serving-ready
- `sales_order_items` 已经被当前 source-side readiness answer 覆盖

## Current Injected-Context Readiness

当前 first slice 除了 source payload fields 之外，还依赖两类 injected context：

- linked `analysis_batches.analysis_batch_id`
- admitted batch `capture_batch_id`

evidence level:
- `Confirmed`

当前 serving value:
- `analysis_batch_id` 与 `order_id` 共同形成 current `sales_orders` serving identity
- `capture_batch_id` 保留当前 serving row 的 batch traceability

当前边界结论：
- 它们是 current first slice 的 readiness prerequisite
- 但它们不是 `/erp/orders` source payload fields

这条边界当前已经 readiness 到足以支持 first slice，
但还不能被误写成完整 lineage model。

## Current Not-Yet-Serving-Ready Areas

以下对象当前仍不能升级承认为 serving-ready truth：

### Item-Like Clue Cluster

- `sku_id`
- `style_code`
- `color_code`
- `size_code`
- `quantity`

current status:
- `not ready`

evidence level:
- `Candidate`

当前不能升级的原因：
- current repo 只证明 downstream `sales_order_items` serving vocabulary 存在
- current repo 没有证明这些名字已经作为 `/erp/orders` source payload fields 成立
- current repo 没有证明它们的 source carrier / container / attachment rule
- current repo 没有 landed source-to-serving path feeding the `sales_order_items` contract

### Broader Rows-To-Item Relation

current status:
- `cannot upgrade now`

evidence level:
- `Deferred`

当前不能升级的原因：
- current relation sample 只覆盖 first `sales_orders` slice
- broader row-to-item relation 仍缺 source-side carrier、relation、detail clue 的 repo-owned answer

### Request-Side Contract And Broader Source Surface

current status:
- `not ready`

evidence level:
- `Candidate`

当前不能升级的原因：
- current repo 仍未形成 `/erp/orders` request-side contract answer
- menu/page mapping 仍然只到 supported context，不是 current serving prerequisite truth
- top-level `rows` 之外的 sibling carrier 仍未形成 repo-owned answer

## Hard Prerequisites Still Missing

在 current first slice 之外，如果要把 broader adjacent targets 升级成 serving-ready truth，至少还缺这些硬前提：

1. repo-owned source evidence，证明 item-like fields 确实存在于 `/erp/orders` source payload
2. repo-owned carrier answer，说明这些 item-like clues 到底挂在什么 source carrier/container 上
3. repo-owned source-to-serving relation answer，说明它们如何映到 downstream target，而不是只停留在 vocabulary 邻接
4. 一个 landed 或至少已 formalized 的 adjacent lane readiness / normalization answer，证明 current source input 真能喂入 broader adjacent target
5. 明确的 target boundary answer，说明为什么新 readiness 只服务某个 narrow adjacent target，而不是自动扩写成 broader `/erp/orders` truth

这些缺口当前都是硬前提，不是软性润色。

## Why The Current First Slice Supports `sales_orders` But Not Broader Adjacent Targets

当前 first slice 可以支撑 `sales_orders`，是因为这五件事同时成立：

1. `/erp/orders` endpoint anchor 已 landed
2. `object + top-level rows list` carrier 已 landed
3. required first-slice source field set 已 landed
4. injected context strategy 已 landed
5. downstream `sales_orders` path + contract 已 landed

当前 first slice 不能自动支撑 broader adjacent targets，是因为以下几点仍不成立：

1. item-like fields 还没有 source-side existence proof
2. item-like relation 还没有 source-side carrier / attachment answer
3. `sales_order_items` 虽然已有 narrow serving contract，但它明确不是 source truth，也不是 landed path
4. current first-slice readiness answer 只覆盖 `sales_orders`，没有覆盖 broader adjacent lane

## What This Serving-Readiness Doc Makes Explicit

这份样板当前新增了四件明确的 repo-owned knowledge：

1. `/erp/orders` current first slice 的 serving-readiness 已经可以被单独沉淀成 readiness-level asset。
2. current first slice 的 `ready now`、`ready but narrow`、`not ready`、`cannot upgrade now` 已经被明确分层。
3. current first slice 为什么足以支撑 `sales_orders`，现在有了一份单独、可复用的 repo-owned answer。
4. broader adjacent targets 仍缺的东西已经被写成硬前提，而不是模糊的“以后再看”。

## What This Serving-Readiness Doc Does Not Claim

这份文档不声称：
- `/erp/orders` 全局 readiness 已完成
- item-like candidate relations 已经 serving-ready
- `sales_order_items` 已经被 current source-side readiness 自动覆盖
- broader `/erp/orders` target truth 已经闭合
- inventory-connected readiness 已进入当前样板
