# Source-Surface Completeness Map

状态：planning-only / working document

这份文档不是 formal source of truth。

formal truth 仍以以下文档为准：
- [README.md](../README.md)
- [docs/README.md](./README.md)
- [docs/](./README.md) 下各 formal boundary docs

这份文档只盘点当前 repo 在 menu / endpoint / payload / slice 维度上的 source-surface completeness。
它不替代 post-route mainline 规划，也不替代 domain migration completeness 盘点。

## Scope And Purpose

这份文档当前只回答：
- 当前 repo-owned formal behavior 实际吸收了哪些 source surface
- 哪些 menu / endpoint / payload family 已进入 current `sales_orders` first path
- 哪些 source 目前只存在于 legacy reference 或 research support skeleton
- 哪些 source/menu 还没有被系统盘点
- 哪些 source completeness gap 会影响后续 `sales_order_items`、inventory、internal entrypoint 的推进顺序

这份文档当前不回答：
- 新的 runtime behavior
- 新的 contract / path / orchestration
- domain migration completeness
- inventory 或 `sales_order_items` 的具体 contract 细节

它还要明确：
- source completeness 和 domain completeness 不是同一张表
- legacy/reference/research material 可以作为盘点输入，但不是 current formal truth

## Completeness Definitions

### Core Terms

`menu surface`：
- 上游 ERP 的菜单、页面入口或 page/menu 归属线索

`endpoint`：
- 当前 capture-side persisted payload 上可识别的 `source_endpoint`
- 或 legacy/reference 中可识别的上游接口路径

`payload family`：
- 同一条 endpoint 之下、可被认为属于同一类结构的 payload shape

`slice mapping`：
- 某条 source surface 当前是否已被 repo-owned formal behavior 吸收进更窄的 transform / serving slice

### Important Distinction

下列表述必须分开：
- `source evidence exists`
- `source completeness mapped`
- `mapped to current behavior`

在当前 repo 里：
- `source evidence exists` 只表示 repo 里能找到参考资料、research skeleton、或当前代码读取线索
- `source completeness mapped` 表示 repo 已把 menu / endpoint / payload family / slice 的关系盘点成可追踪结构
- `mapped to current behavior` 则要求这条 source surface 已被当前 formal behavior 真正吸收

因此：
- 有 reference，不代表有 repo-owned mapping
- 有 research skeleton，不代表 source exploration 已完成
- 有 persistence surface，也不代表 source-side completeness 已完成

### Classification Enum

当前文档只使用这一组收敛枚举：
- `mapped-to-current-behavior`
- `mapped-to-persistence-only`
- `reference-only`
- `partially-explored`
- `unexplored`
- `deferred`

当前判定规则：
- 只有当 source surface 已进入 current formal behavior，才标 `mapped-to-current-behavior`
- 如果已知存在下游 persistence surface，但 source-side contract/path 仍未正式映射，标 `mapped-to-persistence-only`
- 如果 repo 里只有 research support skeleton 或局部探查接口，没有完整 mapping，标 `partially-explored`
- 如果当前只存在于 legacy/reference 输入，标 `reference-only`
- 如果 repo 里连稳定的 menu / endpoint / payload family inventory 都还没有，标 `unexplored`
- 如果 source line 已知存在，但当前主线不建议优先推进，标 `deferred`

## Current Source Inventory

### Current First-Path Source Surface

当前 repo-owned formal behavior 只明确吸收了一条 source surface：
- endpoint: `/erp/orders`
- payload family: one JSON object with a top-level `rows` list
- current slice mapping: `sales_orders`

当前已明确进入 first path 的 only current source rule 是：
- 只有 `source_endpoint == "/erp/orders"` 的 admitted payload snapshots 会参与当前 first path

当前还没有 repo-owned formal menu mapping 去回答：
- `/erp/orders` 对应哪个正式 menu line
- 同一菜单线下还有哪些 sibling endpoints / payload families

所以：
- current first path 已吸收 endpoint/payload/slice 关系
- 但 menu-side completeness 仍未收口

### Repo-Owned Research Skeleton

当前 repo 已有最小 research support skeleton：
- `MenuCoverageSnapshot`
- `PageResearchSnapshot`
- `ERPResearchSupportSnapshot`

这些 skeleton 说明：
- repo 已承认 menu/page research 是一条独立 planning 输入
- repo 能记录 `stub` / `noted` / `partial` / `collected` 这类最小研究状态

但这不表示：
- menu inventory 已经盘完
- endpoint family 已经盘完
- source completeness 已经 formalized

### Legacy Reference Source Inputs

当前 legacy/reference 里已经明确保留为盘点输入的 source-side 材料包括：
- ERP 台账类文档
- API maturity board
- capture ingestion roadmap
- capture route registry
- page research runbook

它们当前只能作为：
- source completeness 的 planning 输入
- 后续 source inventory 的参考来源

它们当前不能作为：
- repo-owned current truth
- 新 contract / path 的自动真源

## Menu -> Endpoint -> Payload Family -> Slice Mapping Matrix

| menu surface | endpoint | payload family | slice mapping | current repo evidence | current classification | notes / next step |
| --- | --- | --- | --- | --- | --- | --- |
| repo-owned menu mapping not yet landed for the current orders line | `/erp/orders` | one JSON object with a top-level `rows` list for current order-level rows | `sales_orders` | current first path docs and readiness docs | `mapped-to-current-behavior` | 当前 formal behavior 只吸收这条 endpoint/payload/slice 关系；menu 层仍未成为 repo-owned mapping |
| current orders line beyond the landed `sales_orders` first slice | `/erp/orders` | adjacent non-`sales_orders` facts on the same orders line | none yet | current first path exclusions plus landed `sales_order_items` persistence surface | `mapped-to-persistence-only` | `sales_order_items` 在 domain 上最接近，但 source-side completeness 仍未正式盘清 |
| repo-owned menu/page research skeleton | none yet | snapshot-only menu/page research metadata | none | `research-support-current-surface.md` and `src/app/services/research/` | `partially-explored` | 当前只有 skeleton，不等于 menu -> endpoint -> payload family inventory 已建立 |
| legacy ERP source research line | multiple legacy-only or not yet repo-owned | ledger / registry / runbook / maturity-board families | none | `docs/reference/legacy-backend/README.md` and `docs/legacy-backend-migration-mapping.md` | `reference-only` | 这些资料可以喂给 planning，但不能直接升级为 current truth |
| inventory-related source family | not yet repo-owned | inventory current / snapshot families not yet mapped in repo-owned docs | none | landed inventory persistence surfaces plus legacy reference inputs | `deferred` | inventory 不能因为已有 persistence surface 就假装 source exploration 已完成 |
| menus/endpoints/payload families beyond the rows above | unknown | unknown | none | no repo-owned completeness map yet | `unexplored` | 这部分空白正是当前包要显式暴露出来的 completeness gap |

## Mapped Vs Reference-Only Vs Unexplored

### Mapped To Current Behavior

当前只有一条 source surface 明确进入 current formal behavior：
- `/erp/orders`
- 当前 order-level `rows` payload family
- `sales_orders` first slice

这条映射已经足以支撑：
- admitted selector 之后的 first readiness evaluator
- first `capture -> transform -> serving` path

但它仍然不表示：
- menu completeness 已完成
- `sales_order_items` source completeness 已完成
- inventory source completeness 已完成

### Reference-Only

当前 legacy/reference 输入可以说明：
- 上游还有更多 menu / ledger / route / runbook 资料
- source completeness 不能只靠 current first path 推断

但 reference-only 仍然只是：
- planning 输入
- 研究导航

而不是：
- current runtime truth
- 当前 formal contract

### Partially-Explored

当前 repo-owned research support 只证明：
- menu/page research 有了最小 skeleton
- repo 可以记录“看过 / noted / partial”的状态

它没有证明：
- source family inventory 已经建立
- menu -> endpoint -> payload family -> slice 的系统 mapping 已经落地

所以：
- `research support current surface != source exploration completed`

### Unexplored

当前仍未被系统盘点清楚的包括：
- `/erp/orders` 当前 first slice 之外的 sibling source families
- inventory line 的 repo-owned endpoints / payload families
- 其他 menu / endpoint / payload families 的优先级和 completeness 状态

这类空白如果不先盘清：
- 后续 `sales_order_items` contract/path 容易只沿 domain 猜
- inventory line 容易被 persistence surface 误导成“来源面也差不多齐了”
- internal entrypoint 也会缺少“到底在触发哪一类 source line”的 planning 约束

## Current Gaps Blocking Fuller Migration Completeness

当前会阻塞 fuller migration completeness 的 source-side 缺口主要有四类：

1. current first path 只有 endpoint/payload/slice mapping，没有 repo-owned menu mapping
2. `sales_order_items` 虽然是最近的下一条 domain line，但 source-side completeness 仍未正式盘清
3. inventory 只有 persistence surfaces，没有 repo-owned source family mapping
4. repo 还缺一份系统 source inventory，去说明哪些 line 是 mapped、reference-only、partially-explored、unexplored

这意味着：
- 下一步不能只看 domain 表面就直接开实现
- 也不能把 legacy research/reference 误当作“已经完成 source mapping”

## Deferred / Non-Goals

当前明确标成 deferred 的 source line：
- inventory-related source family

当前 deferred 的含义不是永久不做。
这里只表示：
- inventory 是已知存在的一条 source line
- 但当前不建议在 `sales_order_items` source completeness 和 first-path hardening 之前优先推进

这份文档当前的 non-goals：
- 不定义新的 contract / path
- 不回答 domain completeness
- 不定义 runtime/internal entrypoint
- 不定义 broader orchestration
- 不把 legacy/reference/archive 内容改写成 formal truth

## Recommended Next Package Ordering

基于当前 source-surface completeness 盘点，推荐顺序是：

1. `docs: answer first-path hardening minimums`
   - 先把当前唯一 landed first path 的 hardening truth 收口
2. `feat: add sales_order_items serving projection contract`
   - 前提是承认 source-side completeness 仍未收口，只先推进最接近的 domain contract line
3. `docs/plan: answer sales_order_items source admission and mapping minimums`
   - 在 item slice 真正接 path 前，把 source-side 假设单独收口
4. `docs/plan: answer inventory line entry conditions`
   - 单独回答 inventory source line 何时进入下一条 mainline
5. `feat: add first internal projection run entrypoint`
   - 放在更后面，避免在 source completeness 还模糊时提前固定入口

## Relationship To Post-Route Mainline Planning

这份文档是 `migration-completeness mainline` 的第二个 planning 子包输出。

它只覆盖：
- `menu / source-surface completeness track`

它不覆盖：
- `database / domain migration completeness track`
- current first path hardening minimums

## Relationship To Domain Migration Completeness Map

这份文档和 [domain-migration-completeness-map.md](./domain-migration-completeness-map.md) 是并列关系。

两者的分工必须保持清楚：
- `domain-migration-completeness-map.md` 回答“哪些表面已有 persistence / contract / path”
- 这份文档回答“哪些上游 source line 已被系统探索、映射、吸收或仍然空白”

因此：
- `sales_order_items` 在 domain 上可以是下一条自然 contract 候选
- 但 source-side completeness 仍然未盘清

这正是为什么：
- source completeness 和 domain completeness 不能混成同一张表
