# Source Intelligence 子树协作导轨

这份文档服务于 `docs/source-intelligence/**`。

它不是 formal source of truth，也不是知识主输出位。
formal truth 仍以仓库根 [README.md](../../README.md)、[docs/README.md](../README.md)、已 landed 的 formal docs，以及当前 `main` 上的 `src/app/**`、`src/migrations/**`、`tests/**` 为准。

## 子树定位

这个子树是 repo-owned source-intelligence knowledge assets 的主输出区。
它负责收口重写后的知识资产，不负责承接未重写的 legacy 碎片。

## 主输出位

当前主输出位只包括：
- [migration-charter.md](./migration-charter.md)
- [legacy-source-intelligence-inventory-baseline.md](./legacy-source-intelligence-inventory-baseline.md)
- [apis/README.md](./apis/README.md)
- [fields/README.md](./fields/README.md)
- [relations/README.md](./relations/README.md)
- [serving-readiness/README.md](./serving-readiness/README.md)

## 非输出位

[docs/reference/legacy-backend/extracts/README.md](../reference/legacy-backend/extracts/README.md) 只是输入隔离区，不是 output slot。

不要把以下材料直接升级成 truth 或主输出：
- legacy extract
- screenshot
- runbook
- raw sample

这些材料如果要进入这个子树，必须先被重写成 repo-owned knowledge asset，并写清 evidence level。

## 默认先读

默认阅读顺序：
1. [README.md](./README.md)
2. [migration-charter.md](./migration-charter.md)
3. [docs/reference/legacy-backend/README.md](../reference/legacy-backend/README.md)
4. [docs/reference/legacy-backend/extracts/README.md](../reference/legacy-backend/extracts/README.md)
5. 再进入你这次要改的具体 output slot README 或目标文档

如果这次任务属于 source-intelligence 全量迁移主线，还要先对齐：
6. [ops/full-migration-master-plan.md](./ops/full-migration-master-plan.md) 的当前 milestone / PR / next allowed step
7. `docs/source-intelligence/ops/current-main-state.md`
8. `docs/source-intelligence/ops/milestone-board.md`

## 默认三角色模式

- `ChatGPT` 负责 review：按当前 milestone / PR / gate / truth discipline 审核，不直接改写主规划，不默许扩 scope。
- `User` 默认只做 relay：复制主计划第 12 节模板和 Codex 回包；除非明确需要真实仓库状态，否则不承担结构判断和手工归纳。
- `Codex` 负责执行：必须先判断当前 milestone / PR / next allowed step，再实施本轮 allowed scope，并吸收 review 结果继续收敛。

## 执行前状态门

每次进入本子树改动前，至少先确认：
- 当前是哪个 milestone / 哪个 PR
- 当前 `status` 是什么
- 当前 `next allowed step` 是什么
- 当前 allowed files 是什么
- 这轮是推进、纠偏，还是仅状态同步

如果这些问题不能从当前文档和仓库状态中回答，就先补状态同步，不要跳 gate 开写。

## 执行后状态门

- 如果这轮改变了 `milestone / PR / status / next allowed step / review verdict / blockers` 中任一项，就必须回写主计划状态。
- 文件未变更不等于无需回写；`changed files: none` 也是有效轮次。
- 没有最新状态同步块，这轮不算闭环。

## Review 最低问题集

每次知识迁移包的 review，至少回答：
- 这次新增了什么 repo-owned knowledge
- 它是否明显提升了 contract-ready 或 serving-ready 判断能力
- 它是否只是重复搬运已有线索
- 新内容是否进入了明确 output slot，而不是停留在 extract/input lane
- 这次是否遵守当前 allowed files
- 这次是否越过当前 milestone / PR gate
- 这次是否把 `Candidate / Supported` 误写成 `Confirmed`
- 这次是否把 planning / reference 混成 landed truth

## Executor 回包合同

每轮 source-intelligence 回包至少包含：
- 完整状态同步块：按主计划第 12.2 节字段全集填写，而不是只给摘要
- 当前状态快照：milestone / PR / status / next allowed step
- 本轮定位：推进、纠偏，还是仅状态同步
- changed files
- validation
- risks
- 一段可直接转发给 ChatGPT 的 review 摘要

默认不要把用户变成二次整理者；回包应尽量可直接转发，而不是要求用户先手工浓缩 diff。回包缺少完整状态同步块时，这轮不算完成。

## Relay 最小操作原则

- 默认只需要复制主计划第 12 节模板和 Codex 当前回包。
- 新开窗口时，用户默认只复制最新状态同步块和固定启动文本，不需要自己从上一轮聊天里倒推状态。
- 只有在必须依赖真实 git/worktree truth 时，才要求用户额外贴 `git status`、`copy-pr-diff` 或 `copy-changed-files` 输出。
- 如果 reviewer 指出越 gate、truth drift 或 scope drift，应由 Codex 负责缩回最小正确范围，不把判断责任转给用户。
