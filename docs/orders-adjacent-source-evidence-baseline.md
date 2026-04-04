# Orders-Adjacent Source-Evidence Baseline

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
- `M3-PR2 | docs/plan: answer /erp/orders adjacent source-evidence baseline`
- current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family 的 source-evidence planning baseline
- 后续 source-accuracy revisit 与 adjacent contract-entry revisit 的前置 evidence baseline

这份文档不做：
- 不新增 behavior
- 不改 `README.md`
- 不改 `docs/README.md`
- 不改任何 formal boundary docs
- 不改 runtime / model / schema / crud / service / migration / tests
- 不把 candidate family 直接命名成 `sales_order_items` contract
- 不新增 contract identity / overwrite / upsert key / path / capture ingress / internal entrypoint
- 不进入 single-target mapping 结论
- 不新增 accuracy matrix、checksum、page completeness、cross-table / cross-slice reconciliation
- 不提前进入 inventory line
- 不提前进入 scheduler / orchestration / retry / reservation / locking
- 不把 `docs/reference/**`、raw / tmp / output / screenshots / runbooks / ledgers / research material 写成 current truth
- 不把 candidate semantics / candidate mapping 直接升级成 landed truth

## Scope

这份文档只回答 current `/erp/orders` line 的一个问题：

- current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family 的 repo-owned source-side evidence baseline，应先被收口成什么形状

它当前只覆盖：
- current `/erp/orders` `rows` anchor family 作为对照 anchor
- current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family
- current order-level anchor clues：`order_id`、`paid_at`、`paid_amount`、`payment_status`、optional `store_id`
- downstream persistence vocabulary：`sales_order_items` surface 上的 `sku_id` / `style_code` / `color_code` / `size_code` / `quantity`
- `docs/reference/**` 当前可复查的 reference lane 状态
- envelope-level blank 与 inventory exclusion

它当前不覆盖：
- contract identity
- single-target mapping 结论
- overwrite / upsert key
- path/read shape 已确认
- behavior readiness
- capture ingress
- runtime/internal entrypoint
- inventory line

## Why This Package Exists

[orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md) 已明确 current `/erp/orders` adjacent contract-entry 仍缺：
- adjacent source-carrier evidence
- order-to-detail attachment evidence
- source-side detail clue evidence
- single-target mapping minimum

[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) 又把其中前三类缺口重新收口成 current `/erp/orders` line 的 source-accuracy gate，
但它当前明确不提供 source-side evidence extract。

同时，当前 repo 里：
- formal truth 只正式证明了 `/erp/orders` top-level `rows` anchor 如何服务 current `sales_orders` first slice
- 在这包落地前，current repo 还没有一份 orders-adjacent source-evidence 的 repo-owned planning extract
- `docs/reference/**` 当前只有 reference 区说明文档，没有 orders-adjacent source-evidence 抽取物

因此，这包当前只做一件事：
- 先把 current `/erp/orders` adjacent candidate 的 source-evidence baseline 作为 repo-owned planning answer 落下来

它不是：
- contract-prep 包
- contract/path 包
- behavior 包

## Reusable Evidence Anchors Already Available

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 |
| --- | --- | --- | --- | --- |
| `/erp/orders` top-level `rows` anchor carrier | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；`src/app/services/capture_to_sales_orders_path.py`；[source-surface-completeness-map.md](./source-surface-completeness-map.md) | current repo 已正式证明：current first path 只消费 object-with-`rows` 的 `/erp/orders` payload，并且只把 order-level rows normalize 进 `sales_orders` first slice | 不能推出 adjacent candidate 也由同一 carrier 承载；不能推出 `rows` 已覆盖全部 adjacent source facts |
| current order-level anchor clues (`order_id`、`paid_at`、`paid_amount`、`payment_status`、optional `store_id`) | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；current first path code/tests | current repo 已正式证明：这些 clues 当前只作为 `sales_orders` first slice 的最窄 row-level anchor / paid-state / optional context clues 被实际消费 | 不能推出它们已是 adjacent family 的 link key、field glossary 或 contract identity |
| `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family | `formal truth + planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md) | current repo 已足以保守确认：current `/erp/orders` line 上存在一条值得继续盘 source-evidence 的 adjacent candidate family | 不能推出它已经 contract-ready；不能推出它已经等于 `sales_order_items` source family |
| downstream persistence vocabulary from `sales_order_items` surface | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | current repo 已正式证明 downstream persistence surface 存在，并可把 `sku/style/color/size/quantity` 这组名称当作 comparison vocabulary | 不能推出这些字段一定原样存在于 `/erp/orders` payload；不能推出 source-side detail semantics 已确认 |
| current repo-local reference lane for orders-adjacent evidence | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md)；当前 `docs/reference/**` 文件状态 | 当前 repo 只足以说明：reference lane 被保留为候选输入通道，但还没有一份 orders-adjacent source-evidence extract 进入 current repo | 不能推出 legacy/reference 已经给出 current repo-owned evidence answer；不能把 reference lane 直接写成 current truth |
| envelope-level blank / inventory exclusion baseline | `planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) | 当前 repo 已保守承认：`rows` 外 envelope-level family 仍是空白边界，inventory line 当前继续排除在外 | 不能推出 envelope metadata family 存在或不存在；不能把 inventory 抢跑并入 adjacent source-evidence baseline |

## Source-Carrier Evidence Question

这部分当前只回答：
- current adjacent candidate 的 source-side carrier evidence 应如何被 repo-owned 地记录

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 合格的 repo-owned evidence answer 最少需要什么 |
| --- | --- | --- | --- | --- | --- |
| current `rows` carrier anchor | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；`src/app/services/capture_to_sales_orders_path.py`；`tests/test_capture_to_sales_orders_path.py` | current repo 已正式证明：top-level `rows` list 是 current `sales_orders` first slice 的 carrier anchor | 不能推出 adjacent candidate 与 `rows` anchor 是同一 carrier；不能推出 adjacent facts 一定 nested under row | 后续 evidence answer 需要明确 adjacent candidate 与 current `rows` anchor 的 relation 是 `same-row substructure`、`row-sibling clue lane`、还是 `other same-payload carrier` |
| adjacent carrier alternatives baseline | `planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) | current repo 已保守暴露三类相互竞争的 carrier 方向：nested row substructure、row sibling clue lane、other same-payload carrier | 不能推出哪一种已经成立；不能推出 path/read shape 已确认 | 合格答案至少要收口一个 primary carrier answer，并显式排除主要 alternative carriers |
| repo-local reference candidate lane for carrier evidence | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md)；当前 `docs/reference/**` 无 orders-adjacent extract | 当前 repo 只足以说明：如果后续要消费 legacy/reference 线索，必须先作为 downgraded reference candidate 被引入 planning answer | 不能推出 reference lane 里已经存在可直接复用的 current repo-owned carrier evidence | 合格答案至少要把任何外部候选材料先重写为 repo-owned evidence note，并标清 `reference evidence candidate` 身份 |

## Order-To-Detail Attachment Evidence Question

这部分当前只回答：
- current order-level anchor 与 adjacent detail candidate 的 relation evidence 应如何被 repo-owned 地记录

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 合格的 repo-owned evidence answer 最少需要什么 |
| --- | --- | --- | --- | --- | --- |
| current order-level anchor clues | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | current repo 已正式证明：`order_id` 与 paid-state / optional store clues 当前只服务 order-level rows anchor | 不能推出这些 clues 自动成为 adjacent relation key；不能推出 `order_id` 已是 future contract identity | 合格答案至少要说明这些 clues 哪些只是 comparison anchor，哪些可能参与 relation evidence |
| order-attached detail facts candidate | `formal truth + planning` | [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | current repo 已保守命名：adjacent candidate 需要某种 order-to-detail attachment 才能成立为 source-side evidence answer | 不能推出 attachment shape 已确认；不能推出 relation grain 已确认 | 合格答案至少要给出一个 repo-owned relation answer 类型：`anchor reuse`、`candidate link clue`、或 `仍需额外 source clue` |
| order-to-detail attachment ambiguity | `formal truth + planning` | [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) | current repo 已明确：attachment ambiguity 仍是 blocker，不能跳过 | 不能推出 `order_id` 直连、position-based relation 或无须额外 family extraction | 合格答案至少要排除主要替代解释，并把 relation answer 与 future contract identity 显式分离 |

## Source-Side Detail Clue Evidence Question

这部分当前只回答：
- source-side detail clue cluster 应如何被 repo-owned 地记录

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 合格的 repo-owned evidence answer 最少需要什么 |
| --- | --- | --- | --- | --- | --- |
| downstream detail vocabulary (`sku_id` / `style_code` / `color_code` / `size_code` / `quantity`) | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | 当前 repo 只足以把这组字段名当作 downstream comparison vocabulary | 不能推出 source payload 也使用同名字段；不能推出这些字段的业务口径已确认 | 合格答案至少要把 `vocabulary match` 与 `source-side evidence` 分开写 |
| source-side detail clue evidence gap | `planning` | [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) | 当前 repo 已明确：source-side detail clue evidence 仍是一个显式缺口 | 不能推出 `sku/style/color/size/quantity` 已经是 current source semantics | 合格答案至少要说明哪些 clues 已有 source-side evidence、哪些只有 vocabulary 邻接、哪些仍是 open ambiguity |
| repo-local downgraded reference candidate lane for detail clues | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md)；当前 repo 没有 orders-adjacent detail clue extract | 当前 repo 只足以说明：如果后续从 legacy/reference 引入 detail clue 线索，它们必须先被降级标注并重写成 repo-owned planning answer | 不能推出外部截图、raw sample、runbook 已经等于 current repo evidence | 合格答案至少要记录 candidate source、downgrade status、以及它被吸收后仍保留的未决歧义 |

## Evidence Provenance And Downgrade Rule

后续任何 current `/erp/orders` adjacent source-evidence answer，至少都要遵守：

1. current first path formal docs / code / tests 只能证明 `rows` anchor 如何服务 `sales_orders` first slice，不能自动证明 adjacent carrier / attachment / detail clue。
2. planning 文档可以把 repo 内可复查材料重写成 evidence answer，但必须显式标注：
   - `repo-owned evidence answer`
   - `planning input`
   - `reference evidence candidate`
   - `open ambiguity / exclusion`
3. `docs/reference/**` 当前只证明 reference lane 存在，不证明 orders-adjacent evidence 已被抽取进 current repo。
4. raw / tmp / output / screenshots / runbooks / ledgers / 旧仓材料 如果要被后续 package 消费，必须先降级标注，再被重写成 repo-owned planning answer。
5. landed persistence vocabulary 只能作为 comparison vocabulary，不得反推 source-side field existence 或 business semantics。
6. minimal research support skeleton 的存在不等于 orders-adjacent source-evidence extract 已完成。

## Exclusions And Open Ambiguities

这份 baseline 当前明确保持以下 exclusions / ambiguities：

- envelope-level blank 继续保持 exclusion
- inventory line 继续保持 exclusion
- single-target mapping 继续不回答
- contract identity 继续不回答
- overwrite / upsert key 继续不回答
- path/read shape 继续不回答
- behavior readiness 继续不回答
- order-to-detail attachment 若无新增 repo-owned evidence，继续保持 open ambiguity
- source-side detail clue cluster 若只有 downstream vocabulary，继续保持 evidence gap

## Source-Evidence Minimum Answer Shape

后续 package 如果要声称 current `/erp/orders` adjacent source-evidence 已经回答到可复查程度，至少要给出一份 repo-owned answer，明确包含：

1. 一个被命名的 evidence question：
   - source-carrier
   - order-to-detail attachment
   - source-side detail clue cluster
2. 每条 answer 的证据层级：
   - formal truth
   - planning
   - reference evidence candidate
3. 每条 answer 当前最多能说明什么。
4. 每条 answer 当前还不能推出什么。
5. 哪些替代解释仍未被排除。
6. 哪些 exclusion 仍然保持不变。

如果这些要素缺任一项，当前都应保守写成：
- evidence gap
- downgraded reference candidate
- open ambiguity

而不是提前写成 contract-prep truth。

## Relationship To Other Planning Docs

这份文档当前位于以下 planning docs 之后：
- [source-surface-completeness-map.md](./source-surface-completeness-map.md)
- [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)
- [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)
- [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)
- [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)

它当前不替代：
- source inventory baseline
- payload family baseline
- payload semantics baseline
- source-accuracy minimums baseline
- contract-entry minimums baseline
- formal contract docs
- formal path docs

## Downstream Use

这份 baseline 只服务：
- 后续 source-accuracy revisit
- 后续 adjacent contract-entry revisit

它当前不直接服务：
- single-target mapping 定稿
- contract/path/behavior 落地

后续包如果要消费这份 baseline，至少要显式回答：
- 哪些 source-carrier answers 已经从 open ambiguity 收口成 repo-owned evidence answer
- 哪些 order-to-detail relation answers 仍只是 candidate link clue
- 哪些 detail clues 已有 source-side evidence，哪些仍只是 downstream vocabulary
- 哪些 reference materials 仍只停留在 downgraded candidate 层
- 为什么 envelope-level blank / inventory exclusion 仍保持不变

在这些 answers 明确之前，后续包仍然必须继续遵守：
- planning / reference 不是 formal truth
- candidate semantics / candidate mapping 不等于 landed truth
- `sales_order_items` persistence surface 不等于 first adjacent target 已经确定
