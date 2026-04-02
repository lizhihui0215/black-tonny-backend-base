# Clean Mainline Charter

状态：planning-only / working document

这份文档不是 formal source of truth。

formal truth 仍以以下文档为准：
- [README.md](../README.md)
- [docs/README.md](./README.md)
- [runtime-boundaries.md](./runtime-boundaries.md)
- [capture-serving-boundary.md](./capture-serving-boundary.md)
- [capture-minimal-boundary.md](./capture-minimal-boundary.md)
- [serving-projection-minimal-boundary.md](./serving-projection-minimal-boundary.md)
- [sales-orders-projection-contract.md](./sales-orders-projection-contract.md)
- [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)
- [docs/](./README.md) 下其他 formal boundary docs

这份文档只做一件事：
- 以当前 `main` 为唯一真实基线，重新建立一条干净、可执行、按 milestone 推进的新路线起点

它服务的是新的 milestone 路线，不是对旧 package 编号的继续修补。

## Scope And Purpose

这份文档当前明确回答：
1. 之前“从 PR4 开始”的路线为什么作废
2. 当前 `main` 上 11 包已落地成果应该如何归位
3. 什么叫“不依赖旧仓即可运行的完整版本”
4. formal truth / planning / reference 三层边界如何分离
5. 新路线的默认顺序应该如何固定

这份文档当前不做：
- 不新增 behavior
- 不改 formal docs
- 不改 runtime / model / schema / crud / service / migration
- 不给后续每个 milestone 直接编号到实现细节
- 不继续修补旧 `PR4 / PR5 / PR6` sequencing

## Explicit Reset

从这份文档开始，当前 mainline 的 planning 入口重置为：
- `M1-PR1 | docs/plan: define clean mainline charter`

以下几点必须显式成立：

### 1. 旧路线作废

之前那条“从 PR4 开始”的路线：
- 作废
- 不再继承
- 不再作为当前 next package 的编号来源

这里的“作废”指的是：
- 作废的是那条错误对齐后的 PR 编号与 sequencing
- 不是作废当前 `main` 上已经 landed 的 formal behavior 与 formal persistence surfaces

### 2. 11 包成果保留，但不再继续编号

当前 `main` 上已经 landed 的 11 包成果：
- 保留为 `既有行为资产`
- 保留为当前 repo 的真实基线
- 不属于新 milestone 编号的一部分

因此：
- 新 milestone 编号从 `M1-PR1` 重新开始
- `M1 / M2 / M3 ...` 不是对旧 11 包的续号
- 后续新路线必须把这 11 包当作“已有前置资产”来消费，而不是继续沿用它们的 PR 编号

### 3. 当前 main 是唯一真实基线

当前新路线只允许以：
- 当前 `main`

作为真实基线。

当前不允许把以下对象当成新路线起点：
- 已删除错误 branch
- 未落地聊天约定
- 旧仓实现结构
- legacy scripts
- legacy route registry / maturity board / evidence chain 本身

## Current Main Baseline

当前 `main` 上已经明确存在的 repo-owned 资产包括：

### Formal Behavior Assets

- 第一条 `sales_orders` serving projection contract
- 第一条最窄 `capture -> transform -> serving` path
- admitted input selector
- first-slice readiness evaluator
- narrow capture-batch lifecycle helper

### Formal Persistence Assets

- capture:
  - `capture_batches`
  - `capture_endpoint_payloads`
  - `analysis_batches`
- serving:
  - `sales_orders`
  - `sales_order_items`
  - `inventory_current`
  - `inventory_daily_snapshot`

### Minimal Research Support Assets

- `MenuCoverageSnapshot`
- `PageResearchSnapshot`
- `ERPResearchSupportSnapshot`

### Existing Guardrail Assets

- formal-layer docs tests
- first `sales_orders` contract tests
- first path tests
- minimal capture / research support surface tests

这些资产说明：
- 当前 repo 不是空白基座
- 但也还不是“不依赖旧仓即可运行的完整版本”

## What Counts As A Complete Version

新路线里说的“一个不依赖旧仓即可运行的完整版本”，当前最小完成定义不是：
- 一次性把所有 legacy domain 都迁完

当前更现实、也更可执行的最小完成定义是：

### Self-Contained Vertical

repo 内至少有一条高价值 vertical 可以在不依赖旧仓 runtime、旧仓脚本、旧仓 import 的前提下完成：
- source inventory
- capture ingress
- capture persistence
- admitted / readiness
- transform normalization
- serving contract / path
- verification / reconciliation
- operator-facing minimum evidence

### Repo-Local Runability

这条 vertical 的运行与验证：
- 只依赖 `black-tonny-backend-base`
- 可以使用当前 repo 明确保留的 configuration、database、tests、docs、reference inputs
- 不需要从旧仓拉运行逻辑进来

### Remaining Gaps Stay Explicit

除了这条 complete vertical 之外，其余 domain/source lines 必须被明确分类为以下之一：
- 未发现
- 已发现但未盘清
- 已盘清但未正式映射
- 已映射但未进入 behavior
- deferred / non-goal

也就是说：
- “完整版本”当前不等于“全域已实现”
- 它等于“至少有一条完整自洽主线 + 其余缺口已被系统显式化”

## Three-Layer Boundary

新路线必须明确分开三层边界。

### 1. Formal Truth

当前属于 formal truth 的只有：
- `docs/` 下 formal boundary docs
- `src/app/**`
- `src/migrations/**`
- 当前 code/tests 已正式证明的 runtime / capture / serving behavior

formal truth 负责回答：
- 当前 repo 已经有什么
- 当前 runtime/capture/serving 边界是什么
- 当前 landed contract/path/guardrail 到哪一步

formal truth 不负责：
- 暂未落地的规划
- legacy 输入导航
- 未来假设性的 package sequencing

### 2. Planning

当前属于 planning 的包括：
- charter
- milestone 路线
- completeness map
- source inventory 规划
- payload / field semantics working docs
- accuracy / reconciliation / hardening minimums

planning 负责回答：
- 下一步应该先做什么
- 需要先盘清哪些边界
- 哪些内容已经明确 deferred
- 每个 behavior package 开始前最小需要哪些前置文档

planning 不能直接升级成：
- runtime truth
- schema truth
- API truth
- contract truth

### 3. Reference

当前属于 reference 的包括：
- `docs/reference/**`
- legacy docs / ledgers / runbooks
- legacy raw samples / screenshots / tmp / output
- route registry
- maturity board
- evidence chain

reference 负责：
- 提供探索输入
- 提供证据候选
- 提供历史上下文与排障线索

reference 不能直接定义：
- formal runtime structure
- schema / CRUD / model semantics
- current serving contract
- current next package truth

## Default Route Order

新路线默认顺序固定为：

1. `boundary and rule packages`
2. `source / payload / field semantics packages`
3. `accuracy and cross-check packages`
4. `first complete vertical packages`
5. `inventory expansion packages`

### Stage 1: Boundary And Rules

先回答：
- 新路线的 authoritative 起点是什么
- 三层边界如何分离
- 何谓完整版本
- 未完成探索如何分类
- 字段语义和证据规则如何约束

### Stage 2: Source / Payload / Field Semantics

再回答：
- 哪些 menu/page/endpoint/payload family 当前已知
- 哪些字段名字只是存在，哪些语义已经明确
- 哪些字段只是候选 grain / role，哪些已经接近 contract-ready

### Stage 3: Accuracy And Cross-Check

再推进：
- coverage completeness
- payload shape / checksum / page completeness guardrails
- field-level semantic validation
- cross-table / cross-slice / operator-facing reconciliation minimums

### Stage 4: First Complete Vertical

在前面三层打稳后，才推进第一条完整 vertical：
- repo-local capture ingress
- capture persistence
- admitted / readiness
- normalization
- serving contract / path
- smoke / rollback / reconciliation guardrails

### Stage 5: Inventory Expansion

只有在 first complete vertical 成立后，才推进：
- inventory line entry conditions
- first inventory slice
- 更广 coverage 的逐步扩展

## Package Governance Rules

新路线默认还要遵守这些 package 规则：

1. planning package 优先于对应 behavior package
2. contract 先于 path
3. accuracy / validation 不晚于该 vertical 的第二条 behavior line
4. 每条 behavior 线都必须有：
   - targeted tests
   - regression guardrails
   - docs truth 或 planning explanation
5. broader orchestration 不得早于一条 self-contained vertical 完成
6. legacy/reference 不能直接改写成 formal truth
7. 字段名存在，不等于字段语义已明确

## Relationship To Existing Planning Docs

这份文档当前是：
- 新 milestone 路线的 authoritative 起点

其他 planning docs 的角色应当这样理解：

### `active-migration-plan.md`

作用：
- 记录当前 `main` 上 11 包既有行为资产与其执行底稿

当前不再负责：
- 新 milestone 编号起点
- 当前 next package 的 authoritative 编号

### `post-route-mainline-planning.md`

作用：
- 保留“11 包收口后为什么要转向完整迁移”这一层高层 framing

当前不再负责：
- 新路线的 authoritative 编号起点
- 当前 package sequencing 的唯一真源

### 其他 completeness / hardening planning docs

作用：
- 提供某一个子问题的 planning 输入

当前不应单独承担：
- 新 mainline 的总入口

## Explicit Non-Goals

这份文档当前明确不做：
- 不定义当前 next implementation PR 的细节实现
- 不直接盘 source inventory
- 不直接抽 payload field semantics
- 不直接定义 accuracy matrix
- 不直接定义 first complete vertical 的具体实现包
- 不重写 formal boundary docs
- 不引入 scheduler / retry / resume / reservation / locking

## Authoritative Starting-Point Statement

从当前 `main` 开始，后续新的 milestone 路线应当先读取：
- [clean-mainline-charter.md](./clean-mainline-charter.md)

再继续进入：
- 新的 M1 / M2 / M3 ... planning packages

因此：
- 这份文档是后续新路线的 authoritative starting point
- 11 包成果保留为既有行为资产
- 新 milestone 编号从 `M1-PR1` 重新开始
