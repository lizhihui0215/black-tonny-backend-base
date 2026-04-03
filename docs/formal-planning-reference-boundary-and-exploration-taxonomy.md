# Formal / Planning / Reference Boundary And Unfinished-Exploration Taxonomy

状态：planning-only / working document

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../README.md)
- [docs/README.md](./README.md)
- [runtime-boundaries.md](./runtime-boundaries.md)
- [capture-serving-boundary.md](./capture-serving-boundary.md)
- [capture-minimal-boundary.md](./capture-minimal-boundary.md)
- [serving-projection-minimal-boundary.md](./serving-projection-minimal-boundary.md)
- [sales-orders-projection-contract.md](./sales-orders-projection-contract.md)
- [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)
- `src/app/**`
- `src/migrations/**`
- `tests/**` 中已经落地并锁定当前 formal behavior 的 guardrail tests

当前 milestone 路线的 authoritative 起点仍然是：
- [clean-mainline-charter.md](./clean-mainline-charter.md)

这份文档是：
- `M1-PR2 | docs: define formal-planning-reference boundary and unfinished-exploration taxonomy`
- 面向后续 source inventory、payload semantics、accuracy、migration planning 包的共享语言文档

这份文档不做：
- 不新增 behavior
- 不新增 capture ingress
- 不新增 contract/path
- 不新增 source inventory 细节盘点
- 不新增 payload field semantics 细节结论
- 不提前定义 scheduler / orchestration / retry / reservation / locking

## 当前仓库阅读规则

在当前 repo 里，必须同时成立以下几点：

1. 当前路线只认当前 `main` 上已经 landed 的 formal docs + code/tests/migrations。
2. planning docs 只负责 next-step ordering、open gaps、package prerequisites 和 working definitions。
3. `docs/reference/**`、legacy raw / output / tmp / screenshots / runbooks / ledgers、旧仓资料、`API-images` 这类材料都只能先作为 reference 或 planning input。
4. `src/app/services/research/**` 下已有 minimal research support skeleton 是 formal truth，但它只证明最小 research support surface 存在，不等于 source completeness 已完成。
5. “字段名已存在”不等于“字段语义已明确”。
6. “有 reference 资料”不等于“source completeness 已完成”。

## Three-Layer Boundary

### 1. Formal Truth

当前属于 formal truth 的典型对象：
- `docs/` 下已经 landed 的 formal boundary docs
- `src/app/**` 下当前已落地的 runtime / capture / serving code
- `src/migrations/**` 下当前已落地的 schema / migration facts
- `tests/**` 下已经锁定当前 formal behavior、formal docs contract、migration targets 的 tests

这一层负责回答：
- 当前 repo 已经正式落地了什么
- 当前 runtime / capture / serving boundary 是什么
- 当前 contract/path/guardrail 已经到哪一步
- 当前哪些 persisted objects、state transitions、serving outputs 已经被 repo-owned truth 固定下来

这一层不负责回答：
- 下一包先做什么
- 哪些 source 还没盘清
- 哪些字段还需要继续解释
- legacy/reference 材料应如何消费
- 未来 package sequencing 或未落地 behavior

在当前 repo 语境下，以下内容都不能单靠 formal truth 自动推出：
- `sales_order_items` 字段语义已经盘清
- inventory line 已可直接进入主线 behavior
- source completeness 已经完成
- research support skeleton 已经等于完整 research migration

### 2. Planning

当前属于 planning 的典型对象：
- [clean-mainline-charter.md](./clean-mainline-charter.md)
- 这份文档
- [active-migration-plan.md](./active-migration-plan.md)
- 后续 package-level working docs，例如 source inventory、payload semantics、accuracy matrix、hardening minimums、inventory entry conditions

这一层负责回答：
- 新路线的默认顺序是什么
- 当前 open gaps 应如何命名、分组、排序
- 某个 behavior package 开始前需要哪些前置条件
- 哪些 legacy/reference 材料可以作为候选证据
- unfinished exploration 应如何统一分类

这一层不负责回答：
- 当前 runtime truth
- 当前 schema truth
- 当前 API truth
- 当前 contract/path 已经 landed 到什么程度
- 可以跳过 formal docs、code、tests、migrations 直接宣布行为成立

planning 文档可以做的，是把问题说明白；不能做的，是把未落地的内容写成已经成立的 truth。

### 3. Reference

当前属于 reference 的典型对象：
- `docs/reference/**`
- 旧仓 docs / assets / scripts 中保留为参考的材料
- legacy raw payload samples
- `tmp/**`、`output/**`、`API-images/**`、screenshots
- runbooks、ledgers、route registry、maturity board、evidence chain
- 尚未被 repo-owned planning docs 吸收的历史 tracing / troubleshooting 材料

这一层负责：
- 提供历史输入
- 提供证据候选
- 提供探索线索
- 提供排障与人工研究的背景上下文

这一层不负责：
- 直接定义 current contract/path/runtime truth
- 直接证明 source completeness 已完成
- 直接证明字段语义已明确
- 直接决定当前 milestone 的 next package sequencing

reference 可以喂给 planning，但不能越过 planning 直接改写 formal truth。

## 什么材料只能作为 Planning Input

以下材料在当前 repo 里只能先作为 planning input 或 reference evidence，不能直接升级成 truth：

| 材料 | 当前最多能说明什么 | 当前不能直接说明什么 |
| --- | --- | --- |
| `docs/reference/**` | 历史上下文、探索线索、候选 mapping 输入 | current runtime / contract / path truth |
| legacy raw payload、`tmp/**`、`output/**`、screenshots、`API-images/**` | 某个 source 或字段可能存在，或某条页面/接口值得继续盘 | payload semantics 已明确、字段语义已确认、runtime shape 已被 current repo formal surface 固定 |
| runbooks、ledgers、route registry、maturity board、evidence chain | 业务背景、研究流程、排障线索、历史分层 | current source completeness 已完成、current package 顺序已确定 |
| `sales_order_items` / inventory 等已落地 persistence objects | 对应 persistence surface 已存在 | contract/path/hardening/field semantics 已完成 |
| minimal research support skeleton | `MenuCoverageSnapshot`、`PageResearchSnapshot`、`ERPResearchSupportSnapshot` 这类最小 research support surface 已进入 current repo minimal formal surface | menu / endpoint / payload family 已经被系统盘清 |
| payload key、列名、字段名本身 | 命名线索、候选粒度、候选 role | 具体业务含义、允许用途、跨表关系、serving contract identity |

任何材料如果要从 planning input 升级为 formal truth，后续 package 仍然必须在当前 repo 内显式落：
- formal docs
- code
- tests
- migrations

不能通过“旧仓里已经写过”“截图里看起来像这样”“字段名像是这个意思”来跳过这一步。

## Unfinished-Exploration Taxonomy

这套 taxonomy 用于统一描述当前 repo 里尚未完成的 source / payload family / field family / domain slice。

同一个对象在不同层面可以处于不同状态。
例如：
- `sales_order_items` 的 persistence surface 已 landed
- 但它的 serving contract、path、字段语义盘点并没有因此自动完成

| 分类 | 在当前 repo 语境下的含义 | 典型证据 | 还不能推出什么 |
| --- | --- | --- | --- |
| `未发现` | 当前 repo 里还没有稳定、可复查的 repo-owned 线索证明这条 source / field / slice 已被识别出来 | 没有明确 planning note，也没有稳定 reference lead 被记录进 repo-owned 语境 | 不能假设它已经存在、不能直接开 contract/path |
| `已发现但未盘清` | 已知道它存在，或已经有 legacy/reference/research 线索，但 menu / endpoint / payload family / grain / filter / field role 还没说清 | `docs/reference/**`、runbook、ledger、raw sample、screenshot、research support skeleton 提示 | 不能说 source completeness 已完成；不能说字段语义已明确 |
| `已盘清但未正式映射` | repo-owned planning 已能描述它来自哪里、主要 payload family/field family 是什么、还缺哪些证据，但还没写成正式 mapping 或 contract 前提 | planning doc、working glossary、evidence note | 不能说 runtime 已可直接消费；不能说 contract/path 前提已成立 |
| `已映射但未进入 behavior` | repo-owned planning 或 contract-prep doc 已经把它映到目标 slice / domain boundary，前置条件也基本明确，但还没有 landed behavior | mapping doc、contract-prep doc、package prerequisites | 不能说 capture ingress / transform / serving behavior 已存在 |
| `deferred` | 已明确知道这条线存在且当前不做，或被其他前置条件阻塞，原因已经写清 | planning note 中的 deferred rationale、blocked-by 说明 | 不能因为 deferred 就把它当作不存在或已经解决 |

## 这些分类在当前仓库里怎么用

后续 packages 使用这套 taxonomy 时，至少要遵守：

1. 先说明对象是什么：
   - source / menu / endpoint
   - payload family / field family
   - domain slice / serving projection
2. 再说明它当前处于哪个状态。
3. 再说明支撑这个状态的证据来自哪一层：
   - formal truth
   - planning
   - reference
4. 再说明它下一步最小需要什么：
   - 继续探索
   - 先做 field glossary
   - 先做 mapping
   - 先做 hardening
   - 或明确 deferred

在当前 repo 里，至少要避免以下误写：
- `sales_order_items` 已有表，不等于 `sales_order_items` contract 已明确
- inventory 已有 persistence surface，不等于 inventory line 已可直接进入 behavior
- 已有 legacy ledger / runbook，不等于对应 source family 已经盘清
- 已有 screenshot / raw payload，不等于字段语义或 checksum 规则已经成立
- 已有 minimal research support skeleton，不等于 source inventory 已完成

## 后续 Packages 引用 Legacy / Reference / Research Material 的约束

后续 source inventory、payload semantics、accuracy、migration planning 包在引用 legacy/reference/research material 时，必须满足：

1. 明确标注材料所在层：
   - formal truth
   - planning
   - reference
2. 明确标注材料用途：
   - 当前 truth
   - planning input
   - reference evidence candidate
3. 不能把 `docs/reference/**`、legacy raw / output / tmp / screenshots / runbooks / ledgers 直接写成 current formal truth。
4. 不能把 research support skeleton 的存在直接写成“source exploration 已完成”。
5. 不能把 payload key、列名、字段名直接写成“字段含义已明确”。
6. 如果想把某个 reference 结论升级为 formal truth，必须在后续 package 里把对应 formal docs、code/tests/migrations 一起落到当前 repo。
7. 在完成 source inventory、payload semantics、accuracy、migration 这些 planning 包之前，不提前宣布 broader orchestration、scheduler、retry、reservation、locking 进入主线。

## Reuse Rule

从 `M1-PR2` 往后：
- source inventory docs
- payload semantics docs
- accuracy / reconciliation docs
- migration completeness docs
- inventory entry-condition docs

都应复用这份文档里的三层边界和 unfinished-exploration taxonomy。

这份文档的作用不是代替后续子问题文档，
而是确保后续 package 在引用 legacy/reference/research 材料时使用同一套边界和状态语言。
