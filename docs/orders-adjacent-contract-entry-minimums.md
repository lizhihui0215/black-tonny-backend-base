# Orders-Adjacent Contract-Entry Minimums

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
- `M2-PR4 | docs/plan: answer /erp/orders adjacent contract-entry minimums`
- current `/erp/orders` line 的 adjacent contract-entry minimums baseline
- 后续首个 adjacent contract/path 包的前置 planning baseline

这份文档不做：
- 不新增 behavior
- 不新增 capture ingress
- 不新增任何 contract identity / overwrite / upsert key 结论
- 不提前确定 path shape
- 不提前确定 internal entrypoint
- 不新增 checksum / page completeness / reconciliation 规则
- 不提前进入 inventory line
- 不提前定义 scheduler / orchestration / retry / reservation / locking

## Scope

这份文档只回答 current `/erp/orders` line 的一个问题：

- 什么时候才允许开首个 adjacent contract/path 包

这里的 `contract-entry` 指的是：
- 一个后续 package 是否已经拥有足够明确、足够窄、且 repo-owned 的前置条件
- 使它可以开始回答单个 adjacent family 的 contract/path 问题

这里不是在说：
- contract identity 已确认
- overwrite / upsert key 已确认
- path shape 已确认
- behavior readiness 已确认

## Reusable Inputs Already Available

以下对象当前已经可以作为后续 adjacent contract/path 包的 planning inputs，
但它们还不是 contract truth：

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入 contract/path 包前，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| `/erp/orders` `rows` anchor family | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[source-surface-completeness-map.md](./source-surface-completeness-map.md)；[orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md) | current repo 已正式证明 first slice 只消费 top-level `rows` list 里的 order-level rows | 不能推出 adjacent family 也采用同一 carrier；不能推出 `rows` anchor 已覆盖所有 adjacent source facts | 需要明确 adjacent candidate family 的 source-side carrier evidence |
| current order-level semantics clues (`order_id`, `paid_at`, `paid_amount`, `payment_status`, optional `store_id`) | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[sales-orders-projection-contract.md](./sales-orders-projection-contract.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | 这些字段当前已被 current `sales_orders` first slice 作为最窄 row-level clues 实际消费 | 不能推出这些 clues 就是 adjacent family 的 contract identity、link key 或 field glossary | 需要明确哪些 clues 只能作为复用 anchor，哪些能进入 adjacent contract-prep mapping |
| `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family | `formal truth + planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；current first path exclusions | current repo 已足以保守确认：current `/erp/orders` line 上存在一条值得单独进入后续 contract/path planning 的 adjacent family candidate | 不能推出它已经等于 `sales_order_items` source family；不能推出它已经 contract-ready | 需要补一份 repo-owned source-side evidence，把 candidate carrier / attachment / target mapping 说清到足以进入单包 contract 工作 |
| detail-attribute candidate vocabulary (`sku_id` / `style_code` / `color_code` / `size_code` / `quantity`) | `planning` | [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；`sales_order_items` persistence surface | 当前 repo 只足以把这组命名当作后续核对 source-side detail clues 的 vocabulary | 不能推出这些字段一定原样存在于 `/erp/orders` payload；不能推出它们的业务含义、口径或允许用途已明确 | 需要 repo-owned payload evidence 或明确降级的 reference candidate，证明 source-side 是否存在对应 clue cluster |
| envelope-level exclusion baseline | `planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | 当前 repo 已保守承认：`rows` 之外若存在 envelope-level family，也仍是空白边界 | 不能推出 envelope-level metadata family 存在或不存在 | 需要在 contract-entry 前显式保持这条线为 exclusion，而不是顺手并入 adjacent contract package |

## Evidence Minimums Still Missing

以下 minimums 当前如果不先补齐，就不应进入首个 adjacent contract/path 包：

| 缺失 minimum | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 合格的最小补齐方式 |
| --- | --- | --- | --- | --- | --- |
| adjacent source-carrier evidence | `planning` with possible `reference` input | current repo 只知道存在 adjacent family candidate，但还不知道它实际承载在 nested rows、row sibling fields 还是其他 family | 当前只能说明“需要单独盘”，不能说明“可以直接开 contract” | 不能推出 contract input shape；不能推出 path 读取边界 | 形成一份 repo-owned evidence note，明确 candidate family 的最窄 carrier 边界，且显式标注证据层级 |
| order-to-detail attachment evidence | `planning` with possible `reference` input | [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) 仍把 order-to-detail attachment 标为 `未解决歧义` | 当前只能说明 adjacent detail candidate 与 current order-level anchor 有关联需求 | 不能推出 link clue、join clue、contract identity 或 input grain | 先把 attachment shape 收口成一条 repo-owned mapping question，并拿到足以排除主要替代解释的 evidence |
| source-side detail clue evidence | `planning` with possible `reference` input | 目前只有 persistence vocabulary 和候选语义，没有 repo-owned source extract 证明 detail clue cluster 的存在方式 | 当前只能说明后续应重点核对这组 clues | 不能推出 `sku/style/color/size/quantity` 已是 source semantics | 形成最小 evidence extract，说明 source side 是不是存在 detail-attribute cluster，以及仍有哪些字段语义待证实 |
| single-target mapping minimum | `planning` | current repo 只有 adjacent family candidate 与 downstream `sales_order_items` vocabulary 邻接关系 | 当前最多只能说明 downstream likely needs one narrow target slice | 不能推出 first adjacent contract package 就应直接命名为 `sales_order_items` contract | 先显式回答 first adjacent package 的 target boundary 是否只服务一个 narrow downstream slice，并把“不是 contract identity”的边界写清 |

## Boundary Questions That Must Be Answered First

以下问题在 contract-entry 前必须先有 repo-owned planning answer：

| 必答 boundary question | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 进入 contract/path 包前最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| adjacent family 的 carrier boundary 是什么 | `formal truth + planning` | current first path 只证明 top-level `rows` anchor；family baseline 只证明有 adjacent candidate | 已知必须单独回答 carrier boundary | 不能跳过 carrier boundary 直接写 contract input | 一条明确的 carrier boundary answer，至少排除主要 alternative carriers |
| adjacent family 与 current `rows` anchor 的 relation boundary 是什么 | `formal truth + planning` | order-level clues 已存在，但 attachment ambiguity 仍未解决 | 已知 relation boundary 是 blocker | 不能直接把 `order_id` 升级成 adjacent contract identity | 一条 relation-boundary answer，明确它是 anchor reuse、candidate link clue，还是仍需额外 source clue |
| first adjacent package 的 target scope 是否足够单主题 | `planning` | clean charter、family baseline、semantics baseline 都要求单主题 narrow package | 已知后续包不能同时回答多个 families / slices | 不能把 adjacent contract/path 与 inventory、accuracy、broader orchestration 混在一包里 | 明确 first adjacent package 只回答一个 family、一个 target slice、一个 single-theme question |
| envelope-level blank 是否保持 exclusion | `planning` | envelope-level line 仍在 `未发现 / ambiguity` | 已知它不应被顺手塞进 first adjacent package | 不能因为 payload 是 object 就把 envelope metadata 并入 contract-entry | 在 contract-entry doc 里显式写清 exclusion，并把它保留给后续独立探索 |

## Ambiguities That Block Contract Entry

以下歧义如果不先收口，就不应开首个 adjacent contract/path 包：

| blocker / ambiguity | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要解除 blocker，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| adjacent family carrier ambiguity | `planning` | current repo 尚未证明 adjacent candidate 是 nested list、row sibling fields、还是其他 carrier | 只能保守承认 candidate family exists | 不能推出 contract input shape 或 path read shape | 一份 repo-owned carrier evidence answer |
| order-to-detail attachment ambiguity | `formal truth + planning` | semantics baseline 明确把它列为 `未解决歧义` | 只能说明 detail candidate 需要某种 attachment clue | 不能推出 `order_id` 即最终 link key；不能推出无须额外 mapping | 一份 repo-owned relation / mapping answer |
| vocabulary-to-source ambiguity | `planning` | `sales_order_items` persistence 字段名存在，但 source-side detail clue 还未被 repo-owned 证据证明 | 只能把这些名称当作 candidate vocabulary | 不能推出 source payload 也使用同名字段；不能推出 business semantics 已确认 | 一份 source-side detail clue extract 或严格降级标注的 reference evidence |
| target-slice ambiguity | `planning` | 当前只有 downstream persistence 邻接关系，没有 repo-owned contract target answer | 只能说明 first adjacent package 应保持单目标 | 不能推出 first adjacent package 必须直接 formalize `sales_order_items` contract | 一条 narrow target-scope answer，且不把 target scope 误写成 contract identity |

## Allowed Next-Step Shape

在以上 minimums 被补齐之后，允许的下一包形状只能是：

1. 单主题、单 family 的 adjacent contract-prep / contract package。
2. 只围绕 current `/erp/orders` line。
3. 只服务一个 narrow downstream target scope。
4. 明确把 reusable planning inputs、missing minimums 已补齐项、以及仍保留的 exclusions 写清。
5. 在 contract 包里仍然保持：
   - candidate semantics 不自动升级成 contract identity
   - reference/research material 不自动升级成 current truth

## Not-Yet-Allowed Shape

当前仍然不允许的下一包形状包括：

- contract + path + behavior 一起上
- contract + capture ingress 一起上
- contract + inventory 一起上
- contract + accuracy / reconciliation 一起上
- 直接用 persistence 字段名推导 contract identity
- 直接用 current `sales_orders` identity 模式外推 adjacent contract identity
- 提前定义 overwrite / upsert key
- 提前定义 internal entrypoint 或 broader orchestration

## Relationship To Other Planning Docs

这份文档是以下 planning docs 的下游 contract-entry 收口包：
- [source-surface-completeness-map.md](./source-surface-completeness-map.md)
- [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)
- [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)

它当前不替代：
- payload semantics baseline
- formal contract docs
- formal path docs
- accuracy docs

## Downstream Planning Use

这份 baseline 只服务后续首个 adjacent contract/path 包。

当前 `/erp/orders` source-accuracy minimums baseline 另行维护在：
- [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)

后续包在进入 contract/path 之前，至少要显式回答：
- 哪些 reusable inputs 已足够复用
- 哪些 evidence minimums 已被补齐
- 哪些 boundary questions 已被回答
- 哪些 ambiguities 仍然是 blockers
- 为什么当前 next-step shape 仍保持 single-theme / narrow scope

但后续包仍然必须继续遵守：
- planning / reference 不是 formal truth
- 候选语义不等于已确认 contract identity
- `sales_order_items` persistence surface 不等于 adjacent contract 已可直接 formalize
