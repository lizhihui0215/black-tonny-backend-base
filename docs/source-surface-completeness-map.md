# Source-Surface Completeness Map

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
- `M2-PR1 | docs: map repo-owned source inventory baseline`
- 当前 repo-owned `menu / page / endpoint / payload family` inventory baseline
- 后续 payload semantics / accuracy / migration completeness planning 的输入

这份文档不做：
- 不新增 behavior
- 不新增 contract/path/capture ingress
- 不新增 payload field semantics 细节结论
- 不新增 accuracy matrix、checksum 规则、cross-table reconciliation
- 不提前定义 scheduler / orchestration / retry / reservation / locking

## Scope And Reading Rule

这份文档只盘：
- 当前 repo 已知的 `menu`
- 当前 repo 已知的 `page`
- 当前 repo 已知的 `endpoint`
- 当前 repo 已知的 `payload family`

每条对象当前只用以下 taxonomy 标状态：
- `未发现`
- `已发现但未盘清`
- `已盘清但未正式映射`
- `已映射但未进入 behavior`
- `deferred`

这里的“状态”指的是：
- 当前 source inventory baseline 的完成度

它不是在说：
- formal behavior 是否已经存在
- payload field semantics 是否已经明确
- source completeness 是否已经彻底完成

因此，某些对象即使已经被 current `main` 的 formal behavior 局部吸收，
在这份 baseline 里仍可能只被标为：
- `已发现但未盘清`
- 或 `已盘清但未正式映射`

原因是：
- 这份文档要回答的是 source inventory baseline 还缺什么
- 不是把现有 behavior 直接误写成 source completeness 已完成

## Current Formal Anchors This Baseline May Reuse

在不越界升级的前提下，这份 planning baseline 当前可以直接复用的 formal anchors 只有：

1. 当前 formal behavior 只明确吸收了一条 source-adjacent line：
   - admitted payload snapshots where `source_endpoint == "/erp/orders"`
   - current first `sales_orders` slice

2. 当前 first path 只明确要求一种最窄 payload family 形状：
   - one JSON object with a top-level `rows` list

3. 当前 repo 已有 minimal research support skeleton：
   - `MenuCoverageSnapshot`
   - `PageResearchSnapshot`
   - `ERPResearchSupportSnapshot`

这些 formal anchors 当前最多只能说明：
- `/erp/orders` 是 current first path 的唯一 repo-owned endpoint anchor
- repo 已承认 menu/page research support 是一条 formal support surface

这些 formal anchors 当前还不能直接推出：
- orders line 的 menu mapping 已完成
- orders line 的 page mapping 已完成
- `/erp/orders` 的 sibling payload families 已盘清
- inventory source line 已盘清
- payload field semantics 已明确

## Evidence Layer Rule

这份文档里的每条对象都必须注明证据来自哪一层：
- `formal truth`
- `planning`
- `reference`

这里的含义必须保持稳定：

- `formal truth`
  - 只能来自 formal docs、当前 `main` 上已落地 code/tests/migrations
- `planning`
  - 只能来自当前 repo-owned planning docs
- `reference`
  - 只能来自 `docs/reference/**`、legacy reference bridge、以及当前 repo 保留的 reference navigation

如果一条对象只能被 `reference` 支撑，
就不能把它写成 current truth。

如果一条对象只有字段名、payload key、persistence surface 或 research skeleton，
也不能把它写成字段语义已明确或 source completeness 已完成。

## Repo-Owned Source Inventory Baseline

### Menu Objects

| 对象名称 | 类别 | 当前状态 | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 下一步最小需要什么 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| current `/erp/orders` line 的 repo-owned menu mapping | `menu` | `已发现但未盘清` | `formal truth + planning` | current first path formal docs；research support skeleton；本仓 planning docs | 当前 orders line 明确存在一条 repo-owned source-adjacent line，但 menu mapping 还没在 repo 里落成可复查 inventory | 不能推出正式 menu key/title/tree；不能推出 sibling menu entries；不能推出 source completeness 已完成 | 先补 repo-owned menu inventory note，把 current `/erp/orders` line 的 menu 归属线索单独落出来 |
| inventory-related repo-owned menu mapping | `menu` | `deferred` | `planning + reference` | clean charter；domain/source planning docs；legacy reference navigation | inventory 是已知存在的后续 source line，当前不应因为 persistence surface 已有就提前当成 menu mapping 已齐 | 不能推出 inventory menu key；不能推出 inventory source line ready；不能推出 inventory completeness 已完成 | 后续先回答 inventory line entry conditions，再决定是否继续盘 menu 侧证据 |
| other repo-unrecorded menu lines beyond the rows above | `menu` | `未发现` | `planning` | 当前 repo-owned inventory baseline 仍未稳定命名这些 menu lines | 当前 baseline 还没有把更多 menu lines 稳定命名进 repo-owned 语境 | 不能仅凭 reference 资料量大就假定这些 menu lines 已被 repo 发现 | 后续 source inventory passes 再显式命名并分类 |

### Page Objects

| 对象名称 | 类别 | 当前状态 | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 下一步最小需要什么 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| current `/erp/orders` line 的 repo-owned page mapping | `page` | `已发现但未盘清` | `formal truth + planning` | `research-support-current-surface.md`；`src/app/services/research/**`；current first path docs | repo 已有 page research support surface，且 current orders line 明确存在一条 source-adjacent line | 不能推出 page key、page title、页面入口、page-to-endpoint mapping 已固定 | 先补 page-level inventory note，把 current orders line 的 page 归属线索单独盘出来 |
| inventory-related repo-owned page mapping | `page` | `deferred` | `planning + reference` | clean charter；legacy reference navigation；planning docs | inventory page line 已知存在且当前不应抢跑 | 不能推出 inventory page identity；不能推出 inventory source-side completeness 已完成 | 后续先明确 inventory 进入条件，再决定 page 侧盘点深度 |
| other repo-unrecorded page lines beyond the rows above | `page` | `未发现` | `planning` | 当前 repo-owned inventory baseline 还没有稳定命名更多 page lines | 只能说明当前 baseline 对这部分仍是空白 | 不能从 generic research skeleton 直接推出这些 page lines 已被系统盘清 | 后续 source inventory passes 再显式命名并分类 |

### Endpoint Objects

| 对象名称 | 类别 | 当前状态 | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 下一步最小需要什么 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `/erp/orders` current first-path endpoint line | `endpoint` | `已盘清但未正式映射` | `formal truth + planning` | admitted selector、readiness evaluator、first path docs/code/tests | 当前 repo 已正式证明 `/erp/orders` 是 first `sales_orders` path 的唯一 endpoint anchor | 不能推出它对应的 menu/page mapping 已完成；不能推出 sibling source families 已盘清；不能推出整个 orders source line 已完成 | 先把 `/erp/orders` 放进 repo-owned source inventory baseline，并补 sibling family 边界说明 |
| inventory-related repo-owned endpoint family | `endpoint` | `deferred` | `planning + reference` | clean charter；planning docs；legacy reference navigation | inventory source line 在路线里已被明确识别，但当前不应越过 orders line 先补 endpoint 行为或细节盘点 | 不能推出 inventory endpoint path；不能推出 inventory endpoint 已 repo-owned mapped | 后续先回答 inventory entry conditions，再决定 endpoint baseline 是否展开 |
| other repo-unrecorded endpoint families beyond the rows above | `endpoint` | `未发现` | `planning` | 当前 repo-owned inventory baseline 还没有稳定命名更多 endpoint families | 只能说明 repo 当前没有形成更完整的 endpoint inventory | 不能凭 reference 里可能存在更多接口就把它们升级成 current baseline | 后续 source inventory passes 再显式命名并分类 |

### Payload Family Objects

| 对象名称 | 类别 | 当前状态 | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 下一步最小需要什么 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `/erp/orders` top-level `rows` family for the current `sales_orders` slice | `payload family` | `已盘清但未正式映射` | `formal truth + planning` | current first path docs/code/tests；admitted/readiness docs | 当前 repo 已证明 first path 读取的是一个 top-level object with `rows` list 的最窄 payload family | 不能把 `rows` 下字段名直接写成字段语义已明确；不能推出 `sales_order_items` family 已盘清；不能推出 payload glossary 已完成 | 下一包需要单独做 payload semantics / evidence 盘点，而不是在这包里偷跑字段结论 |
| `/erp/orders` adjacent non-`sales_orders` payload families | `payload family` | `已发现但未盘清` | `formal truth + planning` | current first path exclusions；`sales_order_items` persistence surface；planning docs | 当前 orders line 除了 landed `sales_orders` slice 之外，显然还存在邻近 payload family 候选 | 不能推出 item-level payload boundary；不能推出 item field semantics；不能推出可以直接接 path | 先单独回答 orders-adjacent payload family baseline，再进入 payload semantics 或 contract 工作 |
| inventory-related payload families | `payload family` | `deferred` | `planning + reference` | inventory persistence surfaces；clean charter；legacy reference navigation | inventory payload families 是已知后续对象，但当前不应因为表已存在就假装 payload family 已盘清 | 不能推出 inventory payload shape；不能推出 inventory field semantics；不能推出 inventory behavior ready | 先回答 inventory entry conditions，再决定是否盘 payload family |
| other repo-unrecorded payload families beyond the rows above | `payload family` | `未发现` | `planning` | 当前 repo-owned inventory baseline 还没有稳定命名更多 payload families | 只能说明 current baseline 仍有显式空白 | 不能从字段名、sample、截图或 generic reference 直接推出这些 payload families 已确定 | 后续 source inventory passes 再显式命名并分类 |

当前 `/erp/orders` adjacent payload-family baseline 另行维护在：
- [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)

## What This Baseline Makes Explicit

基于上面的 inventory baseline，当前至少可以明确三件事：

1. current `main` 只正式吸收了：
   - `/erp/orders`
   - current top-level `rows` family
   - current `sales_orders` slice

2. current repo 已有：
   - menu/page research support skeleton
   - 但还没有把 current orders line 的 menu/page mapping 盘成 repo-owned baseline

3. inventory 与更广 source family 虽然已被路线识别出来，
   - 但当前只能保守地维持在 `deferred` 或 `未发现`
   - 不能因为 persistence surface、reference 材料或 screenshot/raw sample 存在就升级成 source completeness 已完成

## What This Baseline Explicitly Does Not Do

这份 baseline 当前明确不做：
- 不输出 payload field semantics glossary
- 不给 `/erp/orders` 的字段名补业务含义
- 不定义 checksum / page completeness / reconciliation 规则
- 不定义 `sales_order_items` contract/path
- 不定义 inventory contract/path
- 不定义 capture ingress
- 不定义 runtime/internal entrypoint
- 不定义 broader orchestration

## Downstream Planning Use

这份 baseline 从当前 `main` 往后，主要服务三类下游 planning 包：

1. payload semantics packages
   - 只在这份 baseline 已经命名清楚的对象上继续盘字段与证据

2. accuracy / cross-check packages
   - 只在这份 baseline 已经显式暴露的 source coverage gaps 上继续补 guardrails

3. migration completeness / inventory entry packages
   - 用这份 baseline 说明哪些 source lines 仍然只能保守地标 `deferred`、`未发现` 或 `已发现但未盘清`

这份文档本身不是：
- payload semantics 包
- accuracy 包
- migration behavior 包

## Relationship To Other Planning Docs

这份文档当前应与以下两份文档一起阅读：
- [clean-mainline-charter.md](./clean-mainline-charter.md)
- [formal-planning-reference-boundary-and-exploration-taxonomy.md](./formal-planning-reference-boundary-and-exploration-taxonomy.md)

三者的分工应保持清楚：
- charter 负责路线入口与默认顺序
- boundary/taxonomy 文档负责三层边界与统一状态语言
- 这份文档负责当前 repo-owned source inventory baseline

它当前不替代：
- payload semantics docs
- accuracy docs
- domain migration completeness docs
