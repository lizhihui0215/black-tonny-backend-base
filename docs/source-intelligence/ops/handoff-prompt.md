# Handoff Prompt

状态：source-intelligence / minimum handoff prompt

如果这组文档仍处在待 merge 的 PR 里，
下面这段只应被当成 merge target handoff，
不应被反写成 current `main` 已经拥有的事实。

把下面这段直接给新会话 / 新 ChatGPT / 新 Codex：

```text
这是 source-intelligence 当前协作控制面的动态 handoff，不是静态状态摘要。

先做这几件事：
1. 先读 `docs/source-intelligence/ops/full-migration-master-plan.md` 第 0 节的当前执行状态。
2. 再复制同一份文档第 0 节里的“最新标准状态同步块”。
3. 如果这块缺失或字段不完整，先补状态，不要继续做 review 或执行。
4. 新开 ChatGPT 窗口时，优先使用同一份文档第 12.6 节固定启动文本。
5. 新开 Codex 窗口时，优先使用同一份文档第 12.7 节固定启动文本。
6. 再读 `docs/source-intelligence/ops/current-main-state.md`。
7. 再读 `docs/source-intelligence/ops/milestone-board.md`。
8. 再读 `docs/source-intelligence/ops/quality-gates.md`。
9. 最后判断当前 milestone / PR / status / next allowed step / allowed files / round type。

硬规则：
- 第 13 节只是 executor 样例，不等于当前最新状态。
- 如果第 13 节与“最新标准状态同步块”冲突，以“最新标准状态同步块”为准。
- 如果这轮 `changed files` 是 `none`，但 `review verdict / next allowed step / blockers` 变了，仍然必须回写状态。
- 没有“最新标准状态同步块”，这次 handoff 不完整。
```
