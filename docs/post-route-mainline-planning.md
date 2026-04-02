# Post-Route Mainline Planning

状态：planning-only / working document

这份文档不是 formal source of truth。

formal truth 仍以以下文档为准：
- [README.md](../README.md)
- [docs/README.md](./README.md)
- [docs/](./README.md) 下各 formal boundary docs

这份文档只回答：11 包主路线收口后，下一轮 mainline 应先往哪里走。

## 结论摘要

推荐的 next mainline：
- `hardening-first mainline`

推荐顺序：
1. 先收紧当前 first path 的 hardening 边界
2. 再补 PostgreSQL 和 dual-db 相关 smoke / guardrail
3. 再回答 replay / dedupe / observability minimums
4. 最后再决定是否需要正式 internal entrypoint

当前不建议直接进入：
- `sales_order_items` projection contract/path
- inventory projection contract/path
- runtime route 级触发入口
- scheduler / reservation / locking / broader orchestration

当前最自然的后续扩展候选是：
- 在 hardening mainline 收口后，再推进 `sales_order_items`

## 为什么先做 Hardening

当前 repo 已经具备第一条最窄正式行为链：
- admitted selector
- readiness evaluator
- lifecycle helper
- `sales_orders` serving projection contract
- first `capture -> transform -> serving` path

但当前第一条 path 仍有几个明显“已落地、但尚未 harden”的特点：
- 当前主验证仍以 formal-layer SQLite tests 为主
- 真实 serving/capture 目标数据库前提是 PostgreSQL
- capture side 与 serving side 仍是双库，当前成功语义不是分布式原子事务
- replay / dedupe / observability 仍只有局部 contract，没有形成 post-route 明确主线
- runtime/internal 触发入口还不存在，当前 path 仍是 repo-internal service

如果现在直接扩 `sales_order_items` 或 inventory，会把这些语义空白复制到第二条、第三条 slice。
如果现在直接补 runtime/internal entrypoint，会把当前 first path 过早抬升成更显性的操作入口，但 replay、failure semantics、observability 还没先说清。

所以更稳的顺序是：
- 先 harden 当前 first slice
- 再决定是否公开 internal trigger
- 再扩第二条 slice

## 方向排序

### 1. Hardening

推荐优先级：
- `最高`

原因：
- 当前 first path 已经是 formal behavior，值得先验证和收紧
- 风险主要集中在 dual-db semantics、数据库前提、replay / failure visibility
- 这条主线不会扩大业务面，但能降低后续每一条 slice 的复制风险

### 2. `sales_order_items`

推荐优先级：
- `第二顺位`

原因：
- 它和当前 `/erp/orders` source slice 最接近
- 已经有 persistence surface
- 未来最容易复用当前 admitted input / readiness / analysis linkage

为什么不是第一顺位：
- `sales_order_items` 还没有正式 contract
- `sales_order_items.order_id` 目前只是 non-enforced business reference
- 如果在 hardening 之前就推进，容易把 dual-db failure / replay / observability 的不确定性复制到 item slice

### 3. Runtime / Internal Entrypoint

推荐优先级：
- `第三顺位`

原因：
- repo 现在只有 sample queue/task skeleton，没有与 first path 对齐的正式 internal trigger
- 这条线最终很可能需要，但不宜先于 hardening

为什么不是第一顺位：
- 一旦出现正式入口，operator-facing 语义就会更敏感
- 当前 replay / failure / observability minimums 还没先定稿
- 太早推进容易逼出 scheduler / orchestration 讨论

### 4. Inventory

推荐优先级：
- `第四顺位`

原因：
- inventory persistence surface 已存在
- 但 inventory 不是当前 first `/erp/orders` slice 的自然延伸
- 它更可能需要新的 source completeness、snapshot/window、classification flag 解释

为什么不是第一顺位：
- 它和当前 first path 共用的 contract 较少
- 新语义面比 `sales_order_items` 更宽
- 在 current mainline 上更像“开第二条业务主线”，而不是“延长现有最窄 slice”

### 5. Broader Orchestration

推荐优先级：
- `当前不推荐进入主线`

原因：
- formal docs 现在仍明确禁止 broader orchestration
- 现在直接谈 scheduler / reservation / locking，会把 current minimal path 过早拉成 system design 题

当前建议：
- 继续保持“无 broader orchestration”
- 如果必须引入协调层，也只允许在更后面定义一层更窄的 internal coordination，而不是 scheduler-first

## 不推荐先做的方向

### 不推荐先做 `sales_order_items`

原因：
- 它是很自然的下一条 projection slice，但不是最先该补的基础能力
- 当前 first path 的 hardening 空白还没先补齐
- `order_id` 对 `sales_orders.order_id` 的关系仍只是当前 non-enforced business reference

### 不推荐先做 inventory

原因：
- inventory 需要新的 completeness / snapshot / policy 解释
- 相比 `sales_order_items`，它更不像当前 first path 的自然延长
- 会显著拉宽主线范围

### 不推荐先做 runtime route 级入口

原因：
- 这会改变当前“repo-internal path only”的操作地位
- 也会逼近 public/runtime behavior，而这不是 post-route 的第一步

### 不推荐先做 broader orchestration

原因：
- 当前 formal docs 仍没有为 scheduler / reservation / locking 提供正式入口
- 太早推进会让 path / helper / contract / runtime coordination 混层

## 推荐 Mainline 拆包

建议拆成 4 个包。

### 包 1

包名：
- `docs: answer first-path hardening minimums`

一句话目标：
- 把 current first path 的 dual-db、failure surface、non-atomic success edge、internal-only boundary 说清楚。

边界：
- docs-only
- 不新增 behavior
- 不新增 runtime/internal entrypoint
- 不新增 migration/model/schema/crud/service

输入：
- 当前 first path formal docs
- 当前 first path code / tests

输出：
- 一组明确的 hardening minimum docs truth
- 对当前 success / failure / non-goals 的显式边界

风险：
- 容易把未来 retry / orchestration 过早写死
- 需要控制在“解释 current minimum”，而不是“设计 future system”

### 包 2

包名：
- `test: add PostgreSQL migration and first-path smoke`

一句话目标：
- 让 current first path 的关键 migration/apply/path 行为至少在 PostgreSQL smoke 层面被验证一次。

边界：
- tests/tooling only
- 不改 public/runtime API
- 不扩多 slice
- 不引入 orchestration

输入：
- capture/serving migration heads
- current first path services
- current `sales_orders` contract

输出：
- PostgreSQL migration/apply smoke
- first path smoke
- 更接近真实数据库前提的 guardrail

风险：
- CI / local test harness 复杂度上升
- 容易把 test infra 变成新的次级主题

### 包 3

包名：
- `docs: answer first-path replay and observability minimums`

一句话目标：
- 收紧 current first path 的 replay、dedupe、failure visibility、minimal operator-facing evidence 规则。

边界：
- docs-only 或 docs+guardrail-only
- 不新增 scheduler
- 不新增 runtime route
- 不引入 broader retry/resume behavior

输入：
- current first path result shapes
- current `sales_orders` identity / upsert rules
- dual-db failure model

输出：
- replay minimums
- dedupe / rerun non-goals
- minimal observability / failure-trace requirements

风险：
- 容易把未来 retry / recovery policy 说得过宽
- 如果写得太细，会提前锁死后续 internal trigger 设计

### 包 4

包名：
- `feat: add first internal projection run entrypoint`

一句话目标：
- 在 hardening minimums 已明确后，增加一个 internal-only 的 first path 调用入口。

边界：
- internal-only
- 不做 public runtime API
- 不做 scheduler / reservation / locking
- 不做 multi-slice
- 不做 broader orchestration

输入：
- `capture_batch_id`
- current first path service
- current first path result shape

输出：
- 一个正式 internal trigger
- 明确的调用边界
- 可测的 run result surface

风险：
- 名字和落点如果不收敛，容易滑向 orchestration root
- 如果 replay / observability minimums 还不够清楚，这包会被迫带入额外决策

## 当前最不建议先开的实现方向

最不建议先开：
- inventory contract/path

原因：
- 它会立刻打开新的 completeness 和 classification 语义面
- 和 current first `/erp/orders` slice 复用度不如 `sales_order_items`
- 不是收紧 post-route 主线的最短路径

## Hardening Mainline 之后的首个扩展候选

如果 hardening mainline 完成，最推荐的下一条扩展线是：
- `sales_order_items`

原因：
- 同属当前 `/erp/orders` source domain
- 已有 persistence surface
- 最可能共享 current admitted input / readiness / analysis linkage

建议拆法：
1. `feat: add sales_order_items serving projection contract`
2. `feat: add first sales_order_items capture-to-serving path`

在那之前，不建议直接把 `sales_order_items` 偷带进现有 `sales_orders` path。

## 当前对 Coordination 的建议

当前建议继续保持：
- 不引入 broader orchestration

如果 future work 确实需要一层协调逻辑，建议只允许：
- single-run
- single-slice
- internal-only
- 不带 scheduler / reservation / locking

换句话说：
- 可以讨论更窄的 internal coordination
- 但当前不建议把它提升为新的 mainline

## 最推荐的下一包提示词

```text
请基于 black-tonny-backend-base 当前最新 main，只做 planning-only / docs-only 工作，推进下一轮 post-route mainline 的第一包：

包名：
docs: answer first-path hardening minimums

目标：
在不新增 behavior、runtime API、migration、model、schema、crud、service 的前提下，
把 current first capture-to-serving path 的 hardening minimums 写清楚，重点收紧：
- dual-db success/failure semantics
- current non-atomic edge
- internal-only invocation boundary
- current no-op / non-ready / failed / succeeded 的最小操作语义
- explicit non-goals

边界：
- docs-only
- 不改 formal truth 之外的 runtime behavior
- 不引入 scheduler / reservation / locking / broader orchestration
- 不提前定义 replay / retry / resume 的完整策略，除非 current minimum truth 必须说清

完成后请给出低 token planning handoff：
1. PR 基本信息
2. 一句话目标
3. 收紧了哪些 minimums
4. 仍未定稿的点
5. 风险自检
6. 一组可 pbcopy 的本地审查命令
```
