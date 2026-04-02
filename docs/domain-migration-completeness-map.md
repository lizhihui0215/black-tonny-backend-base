# Domain Migration Completeness Map

状态：planning-only / working document

这份文档不是 formal source of truth。

formal truth 仍以以下文档为准：
- [README.md](../README.md)
- [docs/README.md](./README.md)
- [docs/](./README.md) 下各 formal boundary docs

这份文档只盘点当前 repo 在 database / domain migration completeness 上的真实状态。
它不回答 menu / source-surface completeness，也不替代 post-route mainline 规划。

## Scope And Purpose

这份文档当前只覆盖：
- `sales_orders`
- `sales_order_items`
- `inventory_current`
- `inventory_daily_snapshot`
- `analysis_batches` 与当前 first `sales_orders` path 的关系

这份文档的目的不是新增任何 behavior。

它只回答：
- 哪些 domain surfaces 只是 persistence surface
- 哪些已经有 formal contract
- 哪些已经有 capture-to-serving path
- 哪些仍缺 contract / path / hardening
- 哪些当前应归类为 deferred / non-goal

它还要明确：
- “数据库已落地” 不等于 “domain migration 已完成”

## Completeness Definitions

### Core Terms

`persistence surface`：
- formal models / schemas / CRUD helpers / migrations 已落地

`formal contract`：
- 当前 repo 已把该 domain surface 的 identity、upsert、overwrite、或更窄写入规则正式说清，并落到 formal docs / code / tests

`capture-to-serving path`：
- 当前 repo 已把 admitted input、readiness、lifecycle、serving contract 串成一条正式行为链

`hardening`：
- 当前 formal behavior 已存在，但 PostgreSQL、dual-db semantics、replay / dedupe / observability、或 operator-facing minimums 仍未完成 post-route 收口

### Important Distinction

下列表述必须分开：
- `database landed`
- `domain migration completed`

在当前 repo 里：
- `database landed` 只表示 persistence surface 已落地
- `domain migration completed` 至少要求：
  - persistence surface 已落地
  - 该 domain 需要的 contract 已正式落地
  - 该 domain 如果已经进入正式行为链，则 path 也已落地
  - 当前 open hardening gaps 不再阻止它被视为当前主线的已收口 domain

因此：
- 有表、不代表有 contract
- 有 contract、不代表有 path
- 有 path、也不代表当前已经 completeness-closed

### Classification Enum

当前文档只使用这一组收敛枚举：
- `landed-path`
- `landed-contract-only`
- `persistence-only`
- `hardening-needed`
- `deferred`

当前判定规则：
- 如果 surface 已有 path，但仍有明确 open hardening gaps，优先标为 `hardening-needed`
- 如果 surface 只有 persistence surface，没有 formal contract，也没有 path，标为 `persistence-only`
- 如果 surface 已知存在且已落地到 persistence，但当前 post-route 主线明确不建议优先推进，标为 `deferred`

当前这份矩阵里，暂时没有 row 落在 `landed-contract-only`。
这不是遗漏，而是表示：
- 当前 repo 还没有第二个只到 contract、尚未进入 path 的 domain surface

## Current Domain Inventory

### `sales_orders`

当前角色：
- first serving projection contract 的唯一 landed domain
- first `capture -> transform -> serving` path 的唯一 landed serving target

### `sales_order_items`

当前角色：
- 已有 serving persistence surface
- 仍未进入 current first contract/path

### `inventory_current`

当前角色：
- 已有 minimal serving persistence surface
- 当前还没有 contract/path

### `inventory_daily_snapshot`

当前角色：
- 已有 minimal serving persistence surface
- 当前还没有 contract/path

### `analysis_batches`

当前角色：
- capture-side persisted context table
- 当前 first `sales_orders` path 需要它提供 exactly-one linked `analysis_batch_id`

当前不是：
- admitted input minimum
- readiness minimum
- serving projection contract target
- 当前 first path 的独立 capture-to-serving domain line

## Per-Domain Status Matrix

| domain surface | persistence surface | contract landed | path landed | hardening status | current classification | notes / next step |
| --- | --- | --- | --- | --- | --- | --- |
| `sales_orders` | `yes` | `yes` | `yes` | `open` | `hardening-needed` | first slice only；当前已有 first contract 与 first path；下一步不是继续扩 behavior，而是先收紧 hardening minimums |
| `sales_order_items` | `yes` | `no` | `no` | `not-started` | `persistence-only` | 已有 serving persistence surface；`order_id` 仍只是 intended business reference；下一步优先补 contract，再决定是否进 path |
| `inventory_current` | `yes` | `no` | `no` | `not-started` | `deferred` | 已有 persistence surface，但当前不是最推荐的 next domain line；需要单独 inventory contract 设计 |
| `inventory_daily_snapshot` | `yes` | `no` | `no` | `not-started` | `deferred` | 已有 persistence surface，但当前不是最推荐的 next domain line；应与 inventory current 一起作为 inventory line 评估 |
| `analysis_batches` | `yes` | `no` | `no` | `context-only` | `persistence-only` | capture-side persisted context；当前 first `sales_orders` path 把它当 downstream normalization prerequisite，而不是 contract/path target |

## Hardening Gaps Vs Missing Contract/Path

### Hardening Gaps

当前明确属于 `hardening-needed` 的只有：
- `sales_orders`

原因不是 contract/path 缺失，而是：
- 当前 first path 仍有 dual-db semantics 待系统收口
- PostgreSQL smoke 仍未成为 current first path 的常规 guardrail
- replay / dedupe / observability 仍未形成 post-route completeness truth

这意味着：
- `sales_orders` 不是“缺 contract”
- 也不是“缺 path”
- 它当前缺的是 post-route hardening completeness

### Missing Contract / Path

当前明确缺 contract 或 path 的是：
- `sales_order_items`
- `inventory_current`
- `inventory_daily_snapshot`

具体区别：
- `sales_order_items` 是当前最自然的下一条 domain contract 候选
- inventory 两张表仍更像同一条后续 inventory line，而不是当前 first `/erp/orders` line 的自然延长

### Context Surface, Not Current Contract/Path Target

`analysis_batches` 当前需要单独说明：
- 它已经是 landed persistence surface
- 它当前 first path 可被读取
- 但它不是 admitted / readiness minimum proof
- 它也不是当前这条 domain map 下的 serving contract/path target

所以它当前更适合被归类为：
- capture-side persisted context
- not current contract/path target

而不是：
- missing-serving-contract bug
- next path candidate

## Deferred / Non-Goals

当前应明确标成 deferred 的 domain line：
- `inventory_current`
- `inventory_daily_snapshot`

当前 deferred 的含义不是永久不做。
这里只表示：
- 它们已经进入 domain inventory
- 但当前 post-route 主线不建议先于 `sales_order_items` 和 first-path hardening 推进

这份文档当前的 non-goals：
- 不回答 source/menu completeness
- 不回答 runtime/internal entrypoint
- 不回答 broader orchestration
- 不定义 inventory contract 的具体 identity / overwrite 规则
- 不定义 `sales_order_items` contract 的具体 identity / overwrite 规则
- 不把 legacy/reference/archive 内容写成 current truth

## Recommended Next Package Ordering

基于当前 domain completeness 盘点，推荐顺序是：

1. `docs: map source-surface completeness`
   - 先把另一条 completeness 子轨补齐，避免 domain line 先跑、source line 还空着
2. `docs: answer first-path hardening minimums`
   - 再收紧 current first `sales_orders` path 的 hardening truth
3. `feat: add sales_order_items serving projection contract`
   - 作为当前 `/erp/orders` domain 的下一条最自然 contract line
4. `feat: add first sales_order_items capture-to-serving path`
   - 在 contract 落地后，再决定是否把 item slice 接入正式行为链
5. `docs/plan: answer inventory line entry conditions`
   - 到那时再单独决定 inventory 是否进入下一条 domain mainline

当前不建议把 inventory 直接提到 `sales_order_items` 之前。

## Relationship To Post-Route Mainline

这份文档是 `migration-completeness mainline` 的第一个子包输出。

它只覆盖：
- `database / domain migration completeness`

它不覆盖：
- `menu / source-surface completeness`

后者仍应在下一包单独盘点，避免 source/menu completeness 和 current domain inventory 混层。
