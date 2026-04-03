# Orders-Adjacent Payload-Family Baseline

状态：planning-only / working document

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../README.md)
- [docs/README.md](./README.md)
- [docs/](./README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

当前 milestone 路线的 authoritative 起点仍然是：
- [clean-mainline-charter.md](./clean-mainline-charter.md)

当前 shared planning vocabulary 仍然以：
- [formal-planning-reference-boundary-and-exploration-taxonomy.md](./formal-planning-reference-boundary-and-exploration-taxonomy.md)
- 为准

这份文档当前服务的是：
- `M2-PR2 | docs: answer /erp/orders adjacent payload-family baseline`
- current `/erp/orders` line 的 adjacent payload-family planning baseline
- 后续 payload semantics 包的前置 family baseline

这份文档不做：
- 不新增 behavior
- 不新增 `sales_order_items` contract/path/behavior
- 不新增任何 contract/path/capture ingress
- 不新增 payload field semantics 细节结论
- 不新增 contract identity 结论
- 不新增 checksum / page completeness / reconciliation 规则
- 不提前进入 inventory line
- 不提前定义 scheduler / orchestration / retry / reservation / locking

## Scope

这份文档只回答 current `/erp/orders` line 上两类对象：

1. 当前已经被 landed `sales_orders` first slice 吸收的 top-level `rows` family
2. 与这个 current `rows` family 相邻、但尚未进入当前 behavior 的 payload-family candidates

这里的“adjacent”只允许按当前 repo-owned 证据保守理解为：
- same `source_endpoint == "/erp/orders"`
- same payload object，或 same `rows`-based line
- 当前 `sales_orders` first slice 之外的候选 family boundary

这份文档不把以下对象算进 current `/erp/orders` adjacent payload-family baseline：
- `source_endpoint != "/erp/orders"` 的其他 endpoint payloads
- inventory line
- field-level business semantics
- serving contract identity
- runtime orchestration assumptions

## Current Formal Anchors Reused By This Baseline

在不越界升级的前提下，这份 baseline 当前只复用以下 formal anchors：

1. current first path 只吸收：
   - `source_endpoint == "/erp/orders"` 的 admitted payload snapshots
   - one JSON object with a top-level `rows` list
   - current `sales_orders` slice

2. current readiness 只把 `/erp/orders` payload snapshots 视为当前 first `sales_orders` slice 的 readiness anchor。

3. current path 只把 `rows` list 中能 normalize 成 `SalesOrderProjectionFact` 的 row facts 写入 `sales_orders`。

4. current repo 已有：
   - `sales_order_items` persistence surface
   - 但当前 formal docs 明确还没有 `sales_order_items` contract/path

这些 formal anchors 当前最多只能说明：
- `/erp/orders` current first slice 的 payload anchor 是 top-level `rows` family
- current `sales_orders` first slice 之外还需要一个更细的 adjacent family baseline

这些 formal anchors 当前还不能直接推出：
- adjacent family 的 field-level semantics
- adjacent family 是否等于 `sales_order_items`
- adjacent family 的 contract identity
- adjacent family 的 checksum / reconciliation 规则

## Adjacency Model Used In This Package

为了避免把字段名或 persistence surface 直接误写成语义结论，这份包只采用三个保守的 working adjacency dimensions：

1. `rows-anchor family`
   - 当前 landed `sales_orders` first slice 已实际吸收的 top-level `rows` family

2. `rows-adjacent candidate family`
   - 同一 `/erp/orders` line 上，与 current `sales_orders` first slice 相邻、但还没有被 repo-owned docs 盘清的 family candidate

3. `payload-envelope-adjacent candidate family`
   - 同一 `/erp/orders` payload object 里，若存在 top-level `rows` family 之外的 sibling family，其边界目前仍未被 repo-owned 证据稳定证明

这里故意不再往下展开为：
- item-level business fields
- nested collection contract
- row identity
- overwrite policy

这些都必须留给后续 payload semantics 或 contract packages。

## Baseline Table

| family 名称 / working name | 当前状态 | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 下一步最小需要什么 |
| --- | --- | --- | --- | --- | --- | --- |
| `/erp/orders` `rows` anchor family for the current `sales_orders` slice | `已盘清但未正式映射` | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[transform-readiness-boundary.md](./transform-readiness-boundary.md)；current first path code/tests；[source-surface-completeness-map.md](./source-surface-completeness-map.md) | current repo 已证明 first slice 读取的是一个 top-level object with a `rows` list，且当前 behavior 只消费其中能 normalize 成 `SalesOrderProjectionFact` 的 order-level rows | 不能把 `rows` 下其他字段直接写成字段语义已明确；不能把 current `rows` anchor family 外推成全部 `/erp/orders` families 已盘清 | 保持它作为 boundary anchor，供下一步 adjacent family baseline 和 payload semantics 包复用 |
| `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family | `已发现但未盘清` | `formal truth + planning` | current first path 只消费 `sales_orders` order-level facts；[sales-orders-projection-contract.md](./sales-orders-projection-contract.md) 明确 `sales_order_items` 尚未定义；[source-surface-completeness-map.md](./source-surface-completeness-map.md) 已把 adjacent non-`sales_orders` families 标成待盘清；`sales_order_items` persistence surface 已 landed | current repo 已足以保守确认：同一 `/erp/orders` line 上，除了 landed `sales_orders` first slice 之外，仍存在一条邻近 family 候选，需要单独盘边界 | 不能推出这条 candidate family 就等于 `sales_order_items`；不能推出它一定是 nested list、row sibling fields 或其他具体容器；不能推出 field-level semantics、contract identity、behavior readiness | 下一步先单独回答这条 candidate family 的 boundary/evidence minimums，再进入 payload semantics 包 |
| `/erp/orders` payload-envelope-adjacent candidate family outside the current `rows` anchor | `未发现` | `planning` | current formal docs 只要求 payload 是 object with top-level `rows` list；当前 repo 还没有稳定的 repo-owned evidence 去命名 `rows` 之外的 top-level sibling family | 当前 repo 只能保守地承认这里仍有一个空白边界，不能因为 payload 是 object 就假设存在额外 top-level sibling family | 不能推出存在 top-level metadata family；不能推出不存在；不能推出 envelope-level semantics | 如后续要推进，必须先拿到 repo-owned evidence，再把它从 `未发现` 升到更具体状态 |

## What Counts As Evidence In This Package

当前这份 baseline 只接受三层证据：

- `formal truth`
  - current first path docs/code/tests
  - readiness docs/code/tests
  - landed persistence surfaces
- `planning`
  - [source-surface-completeness-map.md](./source-surface-completeness-map.md)
  - [clean-mainline-charter.md](./clean-mainline-charter.md)
  - [formal-planning-reference-boundary-and-exploration-taxonomy.md](./formal-planning-reference-boundary-and-exploration-taxonomy.md)
- `reference`
  - 当前 repo 中尚未抽成 repo-owned adjacent-family evidence 的 reference navigation

在这包里，current repo 还没有一份 orders-adjacent family 的 repo-owned `reference` 抽取物，
所以当前结论主要由：
- `formal truth`
- `planning`
- 共同保守支撑

这也意味着：
- 不能因为 legacy/reference 里可能有更多 orders 材料，就把 adjacent family 边界写成已经成立的 truth

## What This Package Explicitly Distinguishes

这包当前明确区分：

1. 已进入 current behavior 的 anchor family
   - `/erp/orders` top-level `rows` family
   - 只服务 current `sales_orders` first slice

2. 已被发现但还没盘清的 adjacent family candidate
   - same `/erp/orders` line
   - current `sales_orders` first slice 之外
   - 与后续 `sales_order_items` line 有明显邻接关系

3. 仍然没有 repo-owned evidence 的 envelope-level 空白
   - 只能保守标 `未发现`

## What This Package Explicitly Does Not Do

这份 baseline 当前明确不做：
- 不给 `rows` 下字段补业务含义
- 不定义 item-level field semantics
- 不判断 candidate family 的最终 contract target 是否就是 `sales_order_items`
- 不回答 contract identity / overwrite key
- 不回答 checksum / page completeness / reconciliation
- 不回答 capture ingress
- 不回答 runtime/internal entrypoint
- 不回答 inventory line

## Relationship To The Source Inventory Baseline

这份文档是 [source-surface-completeness-map.md](./source-surface-completeness-map.md) 的下游细化包，
只细化其中这一条：

- `/erp/orders` adjacent non-`sales_orders` payload families`
- `/erp/orders` adjacent non-`sales_orders` payload families

它不替代：
- 整体 source inventory baseline
- payload semantics docs
- accuracy docs
- domain migration completeness docs

## Downstream Planning Use

这份 baseline 只服务后续更窄的 payload semantics packages。

后续 payload semantics 包只能在这里已经命名清楚的 family 边界上继续往下走：
- `rows` anchor family
- `rows`-adjacent non-`sales_orders` candidate family
- `payload-envelope-adjacent candidate family`

但后续包仍然必须继续遵守：
- planning / reference 不是 formal truth
- payload key / field name 不等于字段语义已明确
- `sales_order_items` persistence surface 不等于 `sales_order_items` source family 已经盘清
