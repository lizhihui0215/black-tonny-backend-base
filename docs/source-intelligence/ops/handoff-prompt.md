# Handoff Prompt

状态：source-intelligence / minimum handoff prompt

如果这组文档仍处在待 merge 的 PR 里，
下面这段只应被当成 merge target handoff，
不应被反写成 current `main` 已经拥有的事实。

把下面这段直接给新会话 / 新 Codex：

```text
总目标：
把 legacy source knowledge 持续重写成 repo-owned source-intelligence assets，先服务 serving judgment，不迁 legacy 架构。

当前主线：
当前 main 已有两条 source-intelligence 样板线；下一步只能在收益清楚的前提下补一个窄缺口，不能继续泛化扩张。

当前已完成资产：
- migration charter
- legacy inventory baseline
- source-intelligence output slots: apis / fields / relations / serving-readiness
- /erp/orders first-slice dossier + field + relation + serving-readiness
- SelSaleReport dossier + field + relation + head-slice serving-readiness
- GetDIYReportData(E004001008_2) dossier + first narrow field dictionary
- ops baseline: current-main-state / gain ledger / milestone board / handoff prompt / quality gates

当前 blocker：
- 第二条样板线还没有 repo-owned line-side relation/readiness 闭环
- SaleNum 仍只是 strongest clue，不是 confirmed rule
- 继续补 dossier 有进入低收益循环的风险

本轮允许做什么：
- 只开一个窄目标
- 优先补第二条样板线缺失的 relation 或 serving-readiness
- 明确写清新增了什么 repo-owned certainty
- 明确写清对 serving 的实际帮助

本轮明确不做什么：
- 不开 whole sales list family graph
- 不开 broader readiness map
- 不开 support code
- 不改 app/services 结构
- 不把 candidate/support 直接升级成 formal truth

何时必须重新校准 source：
- 当你发现当前包回答不了“新增了什么确定性”
- 当你发现当前包对 serving 的帮助说不硬
- 当你想并行展开第二个方向
- 当你想把 legacy board/registry/evidence 直接当 current truth
- 当你准备触碰 contract/path/runtime 判断

最小读顺序：
1. docs/source-intelligence/ops/current-main-state.md
2. docs/source-intelligence/ops/milestone-board.md
3. docs/source-intelligence/ops/quality-gates.md
4. docs/source-intelligence/migration-charter.md
5. 与当前窄目标直接相关的 dossier / field / relation / serving-readiness 样板
```
