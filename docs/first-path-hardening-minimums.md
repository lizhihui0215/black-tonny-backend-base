# First-Path Hardening Minimums

状态：planning-only / working document

这份文档不是 formal source of truth。

formal truth 仍以以下文档为准：
- [README.md](../README.md)
- [docs/README.md](./README.md)
- [capture-serving-boundary.md](./capture-serving-boundary.md)
- [sales-orders-projection-contract.md](./sales-orders-projection-contract.md)
- [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)
- [docs/](./README.md) 下其他 formal boundary docs

这份文档只做一件事：
- 把 current first `sales_orders` `capture -> transform -> serving` path 的 hardening minimums 收紧成一份 planning-only 盘点

它不新增 behavior，也不重写 formal docs。
它只把现有 formal truth 里已经分散存在的 dual-db、rollback、result semantics、internal-only boundary 和 open hardening gaps 收口到一处，帮助 post-route planning 判断当前 first path 为什么还不能被视为 completeness-closed。

## Scope And Purpose

这份文档当前只覆盖：
- current first `sales_orders` path
- current `sales_orders` serving projection contract 的 serving-side事务语义
- current capture-side lifecycle write 与 serving-side apply 之间的 dual-db 边界

这份文档当前不覆盖：
- `sales_order_items`
- inventory
- runtime serving API
- scheduler / retry / resume / reservation / locking
- future recovery system

## Current Hardening Baseline

当前 first path 已经 landed 的最小 hardening-related truth 是：
- current path 只允许 repo-internal service invocation
- current serving-side contract apply 在一次 apply call 内保持单事务语义
- current contract apply 抛错时，会先 rollback 当前 apply call 的 serving-side writes
- current path 在 contract apply 抛错后，会再显式 cleanup serving transaction，然后才写 capture side `captured -> failed`
- current path 只把 `noop`、`non_ready`、`failed`、`succeeded` 四类结果正式收口到最小 result surface

这些 truth 已足以说明：
- current first path 不再是“完全没有 failure contract 的最小演示代码”

但这些 truth 还不足以说明：
- dual-db 行为已经 hardening-closed
- replay / recovery / observability 已经收口
- current first path 已经具备 completeness-closed 所需的最小 hardening

## Dual-DB Success/Failure Semantics

### Current Success Semantics

当前 success path 的最小顺序是：
1. admitted selector 从 capture-side persisted facts 选出 admitted input
2. readiness evaluator 只回答当前 first `sales_orders` slice 是否 ready
3. path 解析一个 linked `analysis_batches` row，并把 `/erp/orders` payload rows normalize 成 current projection facts
4. `sales_orders` projection contract 在 serving DB 内完成一次 apply call
5. 只有 serving-side contract apply 成功后，capture side 才写 `captured -> transformed`

这条 success semantics 当前已经明确保证：
- current serving writes 不会在 readiness 之前发生
- current `captured -> transformed` 不会早于 serving-side contract apply success

### Current Failure Semantics

当前 failure semantics 当前只覆盖 narrow post-readiness failure slice：
- analysis context missing
- analysis context ambiguous
- `/erp/orders` payload 无法 normalize
- downstream `sales_orders` contract apply raises

这条 failure semantics 当前已经明确保证：
- `noop` / `non_ready` 不会写 `failed`
- current `failed` 只用于 narrow post-readiness failure slice
- contract apply raises 时，会先 cleanup 当前 serving transaction，再写 capture side `captured -> failed`

当前 failure semantics 还没有扩展成：
- replay system
- resume system
- cross-db recovery system
- scheduler-driven retry policy

## Current Non-Atomic Edge

当前 first path 仍然明确存在 dual-db non-atomic edge。

当前不是一个 distributed atomic transaction：
- serving-side contract apply 和 capture-side lifecycle write 分属两个数据库
- repo 当前没有 two-phase commit
- repo 当前没有 compensating transaction framework

当前最需要明确写清的 non-atomic edge 有两条：

### Success Edge

success edge 当前是：
- serving-side contract apply 已经 commit
- 但 capture side `captured -> transformed` 仍是后续单独写入

这意味着当前仍可能存在这样一种窗口：
- `sales_orders` rows 已经落到 serving
- 但 capture batch 还没有成功标成 `transformed`

### Failure Edge

failure edge 当前是：
- serving-side contract apply failure 已被 rollback / cleanup
- 但 capture side `captured -> failed` 仍是后续单独写入

这意味着当前仍可能存在这样一种窗口：
- serving-side partial writes 已经被 cleanup
- 但 capture batch 还没有成功标成 `failed`

当前 hardening minimums 只能把这些 edge 说清。
它们还没有被消除，也还没有被提升成 broader recovery system。

## Current Rollback Semantics

### Already Guaranteed

当前 rollback semantics 已明确保证：
- one current `apply_sales_orders_projection_contract()` call 在 serving DB 内按单次事务执行
- current create/update steps 使用 `commit=False`
- 如果 apply call 中途抛错，helper 会先 `rollback()` 当前 apply call 的 serving-side writes，再把异常重新抛出
- current path 在 contract apply exception 分支里，也会再显式 `rollback(serving_db)` 一次，然后才写 capture-side `failed`
- current targeted tests 已覆盖“先部分 flush、后续失败、最终不留下 partial serving rows”

### Not Guaranteed

当前 rollback semantics 没有保证：
- capture DB 与 serving DB 之间的 distributed atomicity
- serving commit success 后如果 capture lifecycle write 失败，当前能自动补偿或自动回滚 serving-side success
- capture failed write 失败后，当前能自动建立 operator-facing recovery record
- PostgreSQL apply smoke 已经 landed

换句话说，当前 rollback semantics 已经保证了：
- one serving apply call 内部不要留下 partial serving writes

但它没有保证：
- dual-db whole-path atomicity

## Current Result Semantics

| result | current trigger boundary | serving-side minimum semantics | capture-side minimum semantics | current hardening note |
| --- | --- | --- | --- | --- |
| `noop` | admitted selector returns `None` | 不写 serving rows | 不写 lifecycle fields | 当前故意把“batch 缺失”和“payload 缺失”合并成一个 no-op surface |
| `non_ready` | admitted input exists but readiness returns `is_ready=False` | 不写 serving rows | 不写 lifecycle fields | 当前只返回 non-ready，不把它升级成 failure/retry signal |
| `failed` | readiness 之后的 narrow path failure | 如果 failure 发生在 contract apply raises 分支，则先 cleanup 当前 serving transaction；其余 current failure 分支本来就不应写 serving rows | 写 `captured -> failed` | 当前 `failed` 不是 broader recovery state，只是 narrow post-readiness failure write |
| `succeeded` | current contract apply succeeds and lifecycle write succeeds | current first-slice `sales_orders` rows 已 apply | 写 `captured -> transformed` | 当前 success 仍不是 dual-db atomic success proof，只是 current narrow path success result |

## Internal-Only Invocation Boundary

当前 first path 的 invocation boundary 仍应被明确理解为：
- repo-internal only

当前已经明确不是：
- runtime route
- public runtime API
- scheduler-owned job
- reservation / locking coordinator

这条 internal-only boundary 当前已经足以支撑：
- repo 内最小 formal behavior chain

但它还不足以回答：
- operator 以后如何稳定触发
- 触发失败后如何做 replay / reconciliation
- 是否需要更窄的一层 internal entrypoint

## Hardening Gaps That Still Block Completeness-Closed

当前至少还有以下 hardening gaps，会阻止把 current first path 直接视为 completeness-closed：

1. current dual-db non-atomic edge 只被说清，还没有更进一步的缓解或恢复最小规则
2. PostgreSQL smoke 当前还不是已落地 truth
3. replay / retry / resume / recovery minimums 仍未收口
4. observability / operator-facing reconciliation minimums 仍未收口
5. current `noop` / `non_ready` / `failed` / `succeeded` 结果虽已最小 formalized，但还没有 broader operational contract

因此当前更准确的说法是：
- first path 已经 landed
- first path 也已经有最小 failure/rollback semantics
- 但它仍然不是 hardening-complete，也不是 completeness-closed

## Explicit Non-Goals

这份文档当前明确不做：
- 不把 current path 提升成 broader orchestration engine
- 不设计 retry / replay / resume system
- 不设计 reservation / locking / scheduler
- 不把 PostgreSQL smoke 写成已落地事实
- 不把 `sales_order_items` / inventory 扩进 current first path
- 不把 internal entrypoint 直接定稿成 runtime behavior

## Relationship To Post-Route Mainline

这份文档对应 post-route planning 里的：
- `docs: answer first-path hardening minimums`

它服务的不是新的 behavior package，而是：
- 在 current first path 已经 landed 的前提下，把“为什么它还不能被视为 completeness-closed”说清楚
