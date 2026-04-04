# Orders Source-Accuracy Minimums

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
- `M3-PR1 | docs/plan: answer /erp/orders source-accuracy minimums`
- clean charter 默认顺序里 Stage 3 的首个 `/erp/orders` source-accuracy / cross-check planning 包
- 后续 `/erp/orders` adjacent contract-entry 复核前的最小 accuracy gate 定义

这份文档不做：
- 不新增 behavior
- 不改 formal docs
- 不改 runtime / model / schema / crud / service / migration / tests
- 不新增 capture ingress
- 不新增 contract identity / overwrite / upsert key 结论
- 不提前确定 path shape / internal entrypoint
- 不新增 checksum / page completeness / reconciliation 规则
- 不提前进入 inventory line
- 不把 `docs/reference/**`、raw / tmp / output / screenshots / runbooks / ledgers / research material 写成 current truth

## Why This Package Exists

[clean-mainline-charter.md](./clean-mainline-charter.md) 已把默认顺序固定为：
- 先 Stage 2：`source / payload / field semantics packages`
- 再 Stage 3：`accuracy and cross-check packages`
- 再进入 first complete vertical

[orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md) 已明确：
- current `/erp/orders` adjacent contract-entry 仍缺
  - adjacent source-carrier evidence
  - order-to-detail attachment evidence
  - source-side detail clue evidence
  - single-target mapping minimum

因此当前 next package 不能直接开 adjacent contract/path。

这份 package 当前只做一件事：
- 把上面四类缺口重新收口为 current `/erp/orders` line 的 source-accuracy minimums

这里的 `source-accuracy` 在这份文档里只表示：
- repo-owned planning 是否已经能准确回答 adjacent candidate facts 当前究竟落在 source 的哪里
- 它们与 current order-level anchor 的关系边界是什么
- 哪些 detail clues 是 source-side evidence，哪些仍只是 downstream vocabulary
- first adjacent package 是否能保持 single-target / single-theme

它当前不表示：
- contract identity 已确认
- overwrite / upsert key 已确认
- path / behavior ready
- source completeness、checksum、page completeness、operator-facing reconciliation 已完成

## Scope

这份文档只回答 current `/erp/orders` line 的一个问题：

- 在不提前进入 adjacent contract/path 的前提下，source-accuracy 至少要先回答到什么程度

它当前只覆盖以下对象：
- current `/erp/orders` `rows` anchor family
- current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family
- current order-level semantics clues：`order_id`、`paid_at`、`paid_amount`、`payment_status`、optional `store_id`
- downstream detail vocabulary 邻接线索：`sku_id` / `style_code` / `color_code` / `size_code` / `quantity`
- envelope-level blank 作为 exclusion baseline

它当前不覆盖：
- inventory line
- capture ingress
- contract identity / overwrite / upsert
- runtime/internal entrypoint
- broader orchestration / retry / reservation / locking

## Reusable Inputs Already Available For Accuracy Work

| 可复用输入 | 证据层级 | 当前允许复用成什么 | 当前仍然不能推出什么 |
| --- | --- | --- | --- |
| `/erp/orders` `rows` anchor family | `formal truth + planning` | current source-side anchor / carrier comparison baseline | 不能推出 adjacent family 也使用同一 carrier；不能推出 current `rows` 已覆盖全部 adjacent facts |
| current order-level clues (`order_id`、`paid_at`、`paid_amount`、`payment_status`、optional `store_id`) | `formal truth + planning` | current order-level cross-check anchor；用于判断哪些 clue 只是 anchor reuse、哪些可能与 adjacent relation 有关 | 不能推出这些 clues 已经是 adjacent contract identity、link key 或 field glossary |
| `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family | `formal truth + planning` | source-accuracy work 的 scope anchor；用于说明当前确有一条相邻 candidate 需要继续盘 source side | 不能推出它已经 contract-ready；不能推出它已经等于 `sales_order_items` |
| downstream detail vocabulary (`sku_id` / `style_code` / `color_code` / `size_code` / `quantity`) | `planning` | downstream comparison vocabulary；用于核对 source side 是否存在 detail-attribute clue cluster | 不能推出这些字段一定原样存在于 `/erp/orders` payload；不能推出字段业务含义已确认 |
| envelope-level blank | `planning` | first adjacent accuracy work 的 exclusion baseline | 不能推出 envelope-level metadata family 存在或不存在；不能把它顺手并入 first adjacent scope |

## Source-Accuracy Minimums Fixed By This Package

| minimum | 当前最多能复用什么 | 合格答案最少需要什么 | 当前仍然不能推出什么 |
| --- | --- | --- | --- |
| evidence-provenance minimum | 现有 formal docs、planning docs，以及可能被明确降级标注的 reference candidates | 形成一份 repo-owned planning answer / evidence note；每条结论都标清证据层级与用途，明确哪些只是 planning input、哪些只是 reference evidence candidate | 不能把 `docs/reference/**`、raw / tmp / output / screenshots / runbooks / ledgers 直接写成 current truth |
| adjacent carrier accuracy minimum | `rows` anchor family；adjacent candidate family；current first path 只消费 top-level `rows` 的 formal anchor | 至少收口出一个最窄的 adjacent carrier boundary answer，并显式排除主要 alternative carriers；这条 answer 必须说明当前是在核对 nested row substructure、row sibling clues、还是 other same-payload carrier | 不能推出 contract input shape 已 formalized；不能推出 path read shape 已确认 |
| order-to-detail relation accuracy minimum | current order-level clues；`order-to-detail attachment ambiguity` 这个已命名 blocker | 至少把 relation boundary 写清为哪一种 repo-owned answer：`current order-level anchor reuse`、`candidate link clue`、或 `仍需额外 source clue`；并显式把 relation boundary 与 future contract identity 分开 | 不能把 `order_id` 直接升级成 adjacent contract identity；不能把 relation answer 写成 overwrite / upsert key |
| source-side detail clue accuracy minimum | downstream detail vocabulary；`order-attached detail facts candidate`；existing semantics baseline | 至少把 detail clue cluster 收口成 repo-owned answer：哪些 clues 已有 source-side evidence、哪些只有 vocabulary 邻接、哪些仍属 unresolved ambiguity；并把“字段存在”与“字段含义已确认”分开写 | 不能推出 `sku/style/color/size/quantity` 已经是 current source semantics；不能推出 quantity 口径或 attribute meanings 已确认 |
| single-target mapping accuracy minimum | adjacent candidate family；single-theme / narrow-scope 规则；envelope-level exclusion baseline | 至少明确 first adjacent package 只服务一个 narrow downstream target scope；如果当前 only 能保守写成 `sales_order_items-adjacent target candidate`，也必须继续保持“mapping candidate != contract identity” | 不能推出 first adjacent contract package 就应直接命名为 `sales_order_items` contract；不能把 envelope blank、inventory 或 accuracy extras 混入同一包 |

## Cross-Check Discipline Required By These Minimums

后续任何 `/erp/orders` source-accuracy answer，至少都要遵守以下交叉核对纪律：

1. current `order_id` / paid-state / optional `store_id` clues 只能先作为 current order-level anchor 或 comparison baseline 复用，不能直接当成 adjacent contract identity。
2. landed `sales_order_items` persistence surface 只能提供 downstream vocabulary 和 target-neighborhood clues，不能反推 source-side field existence 或业务语义。
3. 如果消费 legacy/reference/raw material，输出必须先重写成 repo-owned planning answer，并显式标注证据层级；原材料本身仍停留在 reference。
4. envelope-level blank 在拿到 repo-owned evidence 之前必须保持 exclusion，不能因为 payload 是 object with `rows` 就假设还存在 metadata family。
5. inventory line 在这个包及其直接下游 accuracy work 里继续保持 exclusion，不能借 `inventory_current` / `inventory_daily_snapshot` persistence surface 抢跑。
6. 任何 source-accuracy answer 都不能顺手给出 overwrite / upsert / internal entrypoint / broader orchestration 结论。

## What This Package Makes Explicit

基于当前 `main` 与已落地 planning baseline，这份文档当前至少明确了四件事：

1. M2-PR4 剩余的四类缺口，当前都应先被视为 source-accuracy blockers，而不是 contract 包里顺手补的细节。
2. current `/erp/orders` adjacent line 进入 contract-entry 前，至少要先拿到 carrier、relation、detail clues、single-target scope 这四类 repo-owned accuracy answers。
3. current first `sales_orders` slice 提供的是 reusable anchor，不是 adjacent contract identity 的默认模板。
4. 在 source-accuracy answer 落成之前，first adjacent package 仍然不能默认写成 `sales_order_items` contract/path。

## What This Package Explicitly Does Not Do

这份文档当前明确不做：
- 不提供 source-side evidence extract
- 不回答 adjacent carrier 的最终落点
- 不回答 order-to-detail relation 的最终 link clue
- 不回答 detail clue cluster 的最终 source mapping
- 不确认 `sales_order_items` 是否就是 first adjacent contract target
- 不定义 checksum / page completeness / reconciliation
- 不定义 capture ingress / runtime entrypoint / orchestration

## Relationship To Other Planning Docs

这份文档当前位于以下 planning docs 之后：
- [source-surface-completeness-map.md](./source-surface-completeness-map.md)
- [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)
- [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)
- [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)

它当前不替代：
- source inventory baseline
- payload family baseline
- payload semantics baseline
- contract-entry baseline
- formal contract docs
- formal path docs

## Downstream Planning Use

这份 baseline 只服务后续更窄的 source-accuracy evidence / cross-check work，以及其后的 adjacent contract-entry revisit。

当前 `/erp/orders` adjacent source-evidence baseline 另行维护在：
- [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)

当前 `/erp/orders` source-accuracy revisit baseline 另行维护在：
- [orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md)

在后续 package 里，如果要声称 current `/erp/orders` adjacent line 已经满足 source-accuracy minimums，至少要显式回答：
- 哪些 source-side carriers 已被 repo-owned evidence 收口
- 哪些 order-to-detail relation answers 已从 ambiguity 收口成可复查答案
- 哪些 detail clues 已有 source-side evidence，哪些仍只是 vocabulary 邻接
- 为什么 first adjacent target scope 仍是单主题、单 family、单 target 候选

在这些答案落成之前，后续 package 仍然必须继续遵守：
- planning / reference 不是 formal truth
- payload key / field name 不等于字段语义已明确
- `sales_order_items` persistence surface 不等于 `/erp/orders` adjacent contract 已可直接 formalize
