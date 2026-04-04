# Orders-Adjacent Payload Semantics Baseline

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
- `M2-PR3 | docs: answer /erp/orders adjacent payload semantics baseline`
- current `/erp/orders` line 已命名 payload families 的 planning-level semantics baseline
- 后续 contract/path planning 的前置 semantics baseline

这份文档不做：
- 不新增 behavior
- 不新增任何 contract identity / contract/path/capture ingress
- 不新增 overwrite / upsert key 结论
- 不新增 checksum / page completeness / reconciliation 规则
- 不把 payload key / field name 直接写成字段语义已明确
- 不把 `rows`-adjacent candidate 直接定性为 `sales_order_items`
- 不提前进入 inventory line
- 不提前定义 scheduler / orchestration / retry / reservation / locking

## Scope

这份文档只回答 current `/erp/orders` line 上已经在 repo-owned planning 里命名清楚的三个 families：

1. `rows` anchor family
2. `rows`-adjacent non-`sales_orders` candidate family
3. `payload-envelope-adjacent candidate family`

这份文档只盘这些 families 里的 semantics baseline：
- candidate semantics
- pending semantics
- unresolved ambiguities

它不把以下内容提前写成结论：
- 字段业务含义已最终确认
- contract identity
- overwrite / upsert key
- behavior readiness
- accuracy / reconciliation rules

## Semantics Status Language Used In This Package

这份 package 里的语义状态，不替代 [formal-planning-reference-boundary-and-exploration-taxonomy.md](./formal-planning-reference-boundary-and-exploration-taxonomy.md) 的主 taxonomy；
它只是补充说明 current `/erp/orders` named families 内部的语义成熟度：

- `候选语义`
  - 当前 repo 证据足以命名一个可能的字段角色或语义分组
  - 但还不够把它写成已确认业务含义
- `待证实语义`
  - current formal behavior 已经以最窄方式消费这条线索
  - 但 broader business meaning 仍未被 repo-owned 证据正式盘清
- `未解决歧义`
  - 当前 repo 还不能在多个合理解释之间稳定落点
  - 只能把歧义显式保留给后续包

## Current Formal Anchors Reused By This Baseline

在不越界升级的前提下，这份 baseline 当前只复用以下 formal anchors：

1. current first path 只消费：
   - `source_endpoint == "/erp/orders"` 的 admitted payload snapshots
   - one JSON object with a top-level `rows` list
   - current `sales_orders` slice
2. current `/erp/orders` normalization 只要求当前 row 提供：
   - `order_id`
   - `paid_at`
   - `paid_amount`
   - `payment_status`
   - optional `store_id`
3. current repo 已有 `sales_order_items` persistence surface，
   - 但 formal docs 仍未定义对应 source family、contract 或 path

这些 formal anchors 当前最多只能说明：
- current `rows` anchor family 已有一条被 behavior 实际消费的最窄语义线索
- current `/erp/orders` line 之外仍有一条邻近 candidate family 需要单独盘语义

这些 formal anchors 当前还不能直接推出：
- `rows` 下字段的最终业务定义
- `rows`-adjacent candidate 就等于 `sales_order_items`
- adjacent family 的 contract identity
- adjacent family 的 overwrite / reconciliation 规则

## Rows Anchor Family Semantics Clues

| 语义对象名称 / working name | 所属 family | 当前状态 | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 进入后续 contract/path 包前最小还缺什么 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| order-level row anchor candidate (`order_id`) | `/erp/orders` `rows` anchor family | `待证实语义` | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md) 明确当前 row 必须提供 `order_id`；current path code/tests 把它作为 `SalesOrderProjectionFact.order_id` 输入；[orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md) 已把 `rows` family 定位为 current anchor | current repo 已正式证明：`order_id` 是 current `sales_orders` first slice 里最窄的 row-level anchor clue | 不能推出它在 legacy/reference 语境中的业务含义已最终确认；不能把它外推成 adjacent family 的 link key；不能把它直接升级成 future contract identity | 需要 repo-owned payload evidence 去核对它与 adjacent candidate 的关系，以及在后续 contract 包前回答它是否只服务 current `sales_orders` slice |
| paid-state event cluster candidate (`paid_at` / `paid_amount` / `payment_status`) | `/erp/orders` `rows` anchor family | `待证实语义` | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md) 明确当前 row 必须提供这三个字段；current path code/tests 把它们写入 `SalesOrderProjectionFact`；[sales-orders-projection-contract.md](./sales-orders-projection-contract.md) 说明这些字段进入 current `sales_orders` contract input | current repo 已正式证明：这三个字段共同构成了 current first slice 会消费的一组 order-level paid-state / paid-value clues | 不能推出 `paid_at` 的业务时间定义已最终确认；不能推出 `paid_amount` 的币种、折扣口径或净额口径；不能推出 `payment_status` 枚举已盘清 | 需要 repo-owned payload samples 或更细 planning evidence 去拆分时间、金额、状态这三条线各自的候选语义和明显歧义 |
| optional store context candidate (`store_id`) | `/erp/orders` `rows` anchor family | `待证实语义` | `formal truth + planning` | current path code/tests 与 [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md) 都只把 `store_id` 视为 optional row input；current `SalesOrderProjectionFact` 也只把它保守承接为 optional context field | current repo 已正式证明：`store_id` 当前只是一条 optional context clue，会被 current first slice 保守带入 serving fact | 不能推出它一定是门店主键、店铺维度、渠道维度或组织维度；不能推出缺失时的业务语义 | 需要 repo-owned evidence 去确认它在 source side 的稳定 role，以及它是否只服务 order-level context 而不参与 adjacent family 语义 |

## Adjacent Candidate Family Semantics Baseline

| 语义对象名称 / working name | 所属 family | 当前状态 | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 进入后续 contract/path 包前最小还缺什么 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| order-attached detail facts candidate | `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family | `候选语义` | `formal truth + planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md) 已明确存在一条与 current `sales_orders` slice 相邻的 candidate family；current formal docs 明确 `sales_order_items` 尚未定义；current repo 已有 `sales_order_items` persistence surface | current repo 已足以保守说明：同一 `/erp/orders` line 上，除了 order-level rows 之外，还值得单独盘一条“订单附属明细事实”候选语义带 | 不能推出这条带就等于 `sales_order_items`；不能推出它一定是 item list、row sibling fields 或其他具体容器；不能推出 behavior readiness | 需要 repo-owned payload evidence 去命名这条 candidate family 的实际载体，并判断它是 nested rows、row-level substructure 还是其他 family |
| detail-attribute cluster candidate (`sku_id` / `style_code` / `color_code` / `size_code` / `quantity`) | `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family | `候选语义` | `formal truth + planning` | current repo 的 `sales_order_items` persistence surface 已存在这些字段名；[orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md) 已明确这条 family 还没盘清 | 当前 repo 最多只能说明：后续 semantics pass 应重点核对是否存在一组 detail-attribute clues，与 `sku/style/color/size/quantity` 这类下游字段 vocabulary 相关 | 不能推出这些字段一定真实存在于 `/erp/orders` payload；不能推出命名完全一致；不能推出 quantity 的业务口径或 sku/style/color/size 的 source semantics 已明确 | 需要 repo-owned payload extracts 或 reference candidates 被明确降级标注后，再判断 source side 是否存在这组 attribute clues |
| order-to-detail attachment ambiguity | `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family | `未解决歧义` | `formal truth + planning` | current first path 只证明 top-level `rows` list 里存在 order-level rows；current repo 没有 repo-owned evidence 证明 adjacent candidate 是 nested under row、row sibling fields、还是 separate family | 当前 repo 只能保守承认：order-level anchor 与 adjacent detail candidate 之间存在 attachment ambiguity，需要显式保留 | 不能推出是 `order_id` 直连；不能推出是 position-based relation；不能推出无须额外 family extraction | 需要 repo-owned payload evidence 去确认 attachment shape，并把 link clue 与 contract identity 保持分离 |
| payload-envelope metadata candidate ambiguity | `/erp/orders` `payload-envelope-adjacent candidate family` | `未解决歧义` | `planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md) 已把 `rows` 外的 envelope-level sibling family 保守标成 `未发现`；current formal docs 只证明 payload 是 object with top-level `rows` list | 当前 repo 最多只能说明：如果 envelope-level metadata family 存在，它也还没进入 repo-owned semantics baseline | 不能推出存在 top-level totals、paging、summary 或 other metadata family；不能推出不存在 | 如后续要推进，必须先拿到 repo-owned payload evidence，再把它从 envelope-level 空白升级成更具体的 semantics 对象 |

## Reference Role In This Package

当前 repo 中，`docs/reference/**` 还没有一份 orders-adjacent semantics 的 repo-owned 抽取文档。

这意味着在这包里：
- `reference`
  - 仍然只算 candidate evidence source
- 当前结论主要由：
  - `formal truth`
  - `planning`
  - 保守支撑

因此这包明确不能写成：
- legacy/reference 已经确认了 item-level 业务含义
- raw / tmp / output / screenshots 已经把 adjacent semantics 盘清
- persistence 字段名已经等于 source-side semantics

## What This Package Explicitly Distinguishes

这包当前明确区分：

1. current behavior 已实际消费的最窄语义线索
   - `order_id`
   - `paid_at / paid_amount / payment_status`
   - optional `store_id`
2. 与 current `sales_orders` slice 相邻、但仍未进入 behavior 的 candidate semantics
   - order-attached detail facts
   - possible detail-attribute cluster
3. 当前还无法稳定落点的未决歧义
   - order-to-detail attachment shape
   - envelope-level metadata existence

## What This Package Explicitly Does Not Do

这份 baseline 当前明确不做：
- 不把字段业务含义写成已最终确认
- 不输出全域 field glossary
- 不判断 candidate family 的最终 contract target
- 不回答 contract identity / overwrite key
- 不回答 checksum / page completeness / reconciliation
- 不回答 capture ingress
- 不回答 runtime/internal entrypoint
- 不回答 inventory line

## Relationship To Other Planning Docs

这份文档是以下两份 planning docs 的下游语义细化包：
- [source-surface-completeness-map.md](./source-surface-completeness-map.md)
- [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)

它当前不替代：
- source inventory baseline
- family baseline
- accuracy docs
- contract / path docs

## Downstream Planning Use

这份 baseline 只服务后续更窄的 contract/path planning。

后续 packages 只能在这里已经保守命名的语义对象上继续往下走：
- `order-level row anchor candidate`
- `paid-state event cluster candidate`
- `optional store context candidate`
- `order-attached detail facts candidate`
- `detail-attribute cluster candidate`
- `order-to-detail attachment ambiguity`
- `payload-envelope metadata candidate ambiguity`

但后续包仍然必须继续遵守：
- planning / reference 不是 formal truth
- payload key / field name 不等于字段语义已明确
- `sales_order_items` persistence surface 不等于 `/erp/orders` source semantics 已经盘清
