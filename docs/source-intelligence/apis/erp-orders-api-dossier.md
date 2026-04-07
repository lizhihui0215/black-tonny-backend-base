# /erp/orders API Dossier

状态：source-intelligence / working dossier

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../../README.md)
- [docs/README.md](../../README.md)
- [docs/](../../README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

这份文档是新的 source-intelligence 主线下第一份真实 API dossier 样板。

它只做一件事：
- 把当前 repo 已经拥有的 `/erp/orders` source knowledge，重写成一份可复用的 API dossier

这份 dossier 复用的 evidence taxonomy 以：
- [migration-charter.md](../migration-charter.md)
- 为准

当前配套字段字典样板位于：
- [erp-orders-first-slice-field-dictionary.md](../fields/erp-orders-first-slice-field-dictionary.md)

当前配套 relation doc 样板位于：
- [erp-orders-first-slice-relation-doc.md](../relations/erp-orders-first-slice-relation-doc.md)

当前配套 serving-readiness 样板位于：
- [erp-orders-first-slice-serving-readiness.md](../serving-readiness/erp-orders-first-slice-serving-readiness.md)

这份 dossier 不做：
- 不做全量 API inventory
- 不做字段字典大全
- 不做 relation baseline
- 不做 support code
- 不做第二个 dossier
- 不把 planning clue 直接升级成 formal truth

## API Identity

- dossier type: `API dossier`
- API identifier: `/erp/orders`
- current repo role: current source-intelligence 主线下第一份真实 dossier 样板
- current formal endpoint role: current repo 已正式吸收的第一条 source-adjacent endpoint line

当前 repo 已经明确：
- `/erp/orders` 是 current first `sales_orders` path 的唯一 endpoint anchor
- 当前 first path 只围绕这一条 endpoint line 工作

当前 repo 还没有明确：
- `/erp/orders` 对应的正式 menu key/title/tree
- `/erp/orders` 对应的正式 page key/title/entry
- request-side contract truth

## Menu / Page / Source-Surface Context

### Menu Context

当前 dossier 结论：
- `/erp/orders` 的 repo-owned menu context 已被发现，但尚未闭合成正式 mapping

evidence level:
- `Supported`

当前支撑：
- repo 已有 menu coverage support surface
- repo 已有 `/erp/orders` source line 的 planning-level source inventory baseline

当前不能推出：
- 正式 menu key
- 正式 menu title
- menu tree 位置已经固定

### Page Context

当前 dossier 结论：
- `/erp/orders` 的 repo-owned page context 已被发现，但尚未闭合成正式 mapping

evidence level:
- `Supported`

当前支撑：
- repo 已有 page research support surface
- repo 已有 `/erp/orders` source line 的 planning-level page mapping baseline

当前不能推出：
- 正式 page key
- 正式 page title
- page entry 与 endpoint 关系已经固定

### Source-Surface Context

当前 dossier 结论：
- `/erp/orders` 是 current repo 已明确命名、且已进入 formal behavior 的 source endpoint line

evidence level:
- `Confirmed`

当前支撑：
- admitted selector / readiness / first path formal docs
- current path code/tests

当前最多能说明：
- 这条 endpoint line 已经进入 repo-owned current behavior

当前不能推出：
- 整个 `/erp/orders` source surface 已经盘清
- sibling source families 已全部确认

## Request / Response / Payload Carrier Overview

### Request-Side Contract

当前 dossier 结论：
- 当前 repo 还没有 `/erp/orders` request-side contract 的 repo-owned answer

evidence level:
- `Candidate`

当前支撑：
- current repo 的 formal behavior 从 capture-side persisted payload snapshots 出发
- formal docs 没有定义 `/erp/orders` 的请求方式、认证方式、query 参数、分页参数或 response envelope contract

当前不能推出：
- request method
- auth mode
- filter / pagination / checksum rule
- external API request contract

### Response / Payload Top-Level Carrier

当前 dossier 结论：
- 当前 first path 只正式承认一种 top-level payload carrier：one JSON object with a top-level `rows` list

evidence level:
- `Confirmed`

当前支撑：
- [capture-to-sales-orders-path.md](../../capture-to-sales-orders-path.md)
- current first path code/tests

当前最多能说明：
- `source_endpoint == "/erp/orders"` 的当前参与 payload，必须能 decode 成一个包含 top-level `rows` list 的 JSON object

当前不能推出：
- top-level object 上其他 sibling keys 的正式语义
- top-level envelope 已经盘清

### Current Rows-Level Consumed Shape

当前 dossier 结论：
- 当前 formal behavior 只消费 `rows` family 中能 normalize 成 first-slice `sales_orders` facts 的 order-level rows

evidence level:
- `Confirmed`

当前 required row clues:
- `order_id`
- `paid_at`
- `paid_amount`
- `payment_status`

当前 optional row clue:
- `store_id`

当前最多能说明：
- 这是 current first `sales_orders` slice 的 rows-level consumed shape

当前不能推出：
- 这是 `/erp/orders` rows-level full field dictionary
- `rows` 下所有字段语义已确认

### Adjacent Carrier Space

当前 dossier 结论：
- 在 current `sales_orders` first slice 之外，`/erp/orders` 同一条 line 上仍有一条 rows-adjacent non-`sales_orders` family candidate

evidence level:
- `Supported`

当前支撑：
- current first path 只消费 `sales_orders` order-level facts
- source-surface baseline 已把 adjacent non-`sales_orders` family 记为待盘清对象
- adjacent payload-family baseline 已把它单独抽成 same-line candidate family

当前不能推出：
- 这条 candidate family 已等于 `sales_order_items` source family
- 它已经 contract-ready
- 它的 carrier 一定是 nested list、row sibling fields 或其他具体容器

## Evidence Matrix

| dossier statement | evidence level | repo-owned basis | current use | current limit |
| --- | --- | --- | --- | --- |
| `/erp/orders` 是 current repo 已进入 formal behavior 的 endpoint anchor | `Confirmed` | first path formal docs；current path code/tests | 允许把它写成 current source-intelligence dossier 的 primary API object | 不等于整个 source line 已盘清 |
| `/erp/orders` 有 repo-owned menu context，但 mapping 未闭合 | `Supported` | source-surface completeness baseline；menu research support surface | 允许把 menu context 记入 dossier | 不等于 menu key/title/tree 已固定 |
| `/erp/orders` 有 repo-owned page context，但 mapping 未闭合 | `Supported` | source-surface completeness baseline；page research support surface | 允许把 page context 记入 dossier | 不等于 page key/title/entry 已固定 |
| current payload carrier 是 object with top-level `rows` list | `Confirmed` | first path formal docs；current path code/tests | 允许把它写成 current top-level carrier truth | 不等于 top-level envelope 已盘清 |
| current rows-level consumed shape 只覆盖 first `sales_orders` slice | `Confirmed` | first path formal docs；`SalesOrderProjectionFact` normalization rule | 允许把当前 first-slice row shape 写入 dossier | 不等于 rows-level field dictionary 已完成 |
| `/erp/orders` 同线存在 rows-adjacent non-`sales_orders` family candidate | `Supported` | source-surface baseline；adjacent payload-family baseline；first path exclusions | 允许把同线 adjacent carrier space 记入 dossier | 不等于 candidate family 已确认 target truth |
| `/erp/orders` request-side contract 仍未形成 repo-owned answer | `Candidate` | formal docs 当前未定义 request contract | 允许把 request-side 空白显式写出来 | 不能把空白误写成默认外部 API 规则 |
| inventory line 与 broader non-orders lines 不进入本 dossier | `Deferred` | charter；current source inventory baseline | 允许显式排除不相关 scope | 不等于 inventory 不存在 |

## Source Evidence Summary

这份 dossier 当前只吸收三层 repo-owned evidence：

### `Confirmed` Evidence Anchors

- [admitted-transform-input-boundary.md](../../admitted-transform-input-boundary.md)
- [capture-to-sales-orders-path.md](../../capture-to-sales-orders-path.md)
- [sales-orders-projection-contract.md](../../sales-orders-projection-contract.md)
- `src/app/services/capture_to_sales_orders_path.py`
- `src/app/services/transform_readiness_evaluator.py`
- `tests/test_admitted_transform_input_selector.py`
- `tests/test_capture_to_sales_orders_path.py`

### `Supported` Evidence Anchors

- [source-surface-completeness-map.md](../../source-surface-completeness-map.md)
- [orders-adjacent-payload-family-baseline.md](../../orders-adjacent-payload-family-baseline.md)
- [research-support-current-surface.md](../../research-support-current-surface.md)
- [serving-projection-minimal-boundary.md](../../serving-projection-minimal-boundary.md)

### Explicitly Excluded As Current Truth Sources

- screenshot
- raw sample
- legacy runbook
- `tmp/**`
- `output/**`
- 旧仓 flat service/script 结构

这些材料如果后续要进入 dossier，只能先被重写吸收，不能直接写成 current truth。

## Current Serving Value

当前 `/erp/orders` dossier 已经带来的 serving value 很明确：

1. 它把 `/erp/orders` 固定成当前唯一已进入 formal behavior 的 source endpoint anchor。
2. 它把 current top-level carrier 固定成 `object + top-level rows list`，为后续 dossier / field dictionary / relation doc 提供稳定 API 入口。
3. 它把 current first `sales_orders` slice 的 rows-level consumed boundary 写清，避免把 first-slice normalization rule 误写成整条 source line 的 full semantics。
4. 它还能明确区分两种 downstream value：
   - `sales_orders` 已有 landed capture-to-serving path
   - `sales_order_items` 当前只有 landed persistence surface 与 downstream vocabulary neighborhood，但当前还不是 source truth，也不是 landed path

## Unresolved Questions

当前 dossier 仍明确保留以下关键问题：

1. `/erp/orders` 的正式 menu key/title/tree 是什么
2. `/erp/orders` 的正式 page key/title/entry 是什么
3. request-side contract、auth mode、query/filter/pagination/checksum 规则是什么
4. top-level `rows` 之外是否存在 repo-owned sibling carrier
5. rows-adjacent non-`sales_orders` family 的真实 carrier/container 是什么
6. source-side detail/item vocabulary 是否与当前 serving-side `sales_order_items` 命名一致
7. `sales_order_items` downstream persistence surface 是否以及如何由未来 source path 喂入

## Non-Goals

这份 dossier 当前明确不是：
- `/erp/orders` 全量 API inventory
- `/erp/orders` 字段字典
- `/erp/orders` relation baseline
- `/erp/orders` serving-readiness doc
- `sales_order_items` source truth answer
- inventory dossier
- runtime contract/path truth

它只是一份单 API、单主文档、可复用结构的 source-intelligence dossier 样板。
