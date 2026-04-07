# Milestone Board

状态：source-intelligence / milestone board

说明：
- 当前 repo 没有把 source-intelligence 历史 PR 编号统一写进这条子主线。
- 这块板用 normalized package title 记录已观察到的 merged package。
- 如果当前 PR 还没 merge，不要把它自己预写进“已完成 PR”。

## 当前 Milestone

- `source-intelligence mainline stabilization`

## 当前目标

- 把 current source-intelligence 主线稳定成一个可继续推进、可评估收益、可及时纠偏、可交接的新仓知识主线。
- 不在没有控制面的情况下继续横向补 dossier。

## 已完成 PR

- `docs: add source intelligence migration charter`
- `docs: add legacy source-intelligence inventory baseline`
- `docs: add /erp/orders first source-intelligence sample line`
- `docs: add SelSaleReport head sample line`
- `docs: add GetDIYReportData(E004001008_2) line-side object sample`

## 未完成 PR

- `docs: add GetDIYReportData(E004001008_2) line-side relation sample`
- `docs: add GetDIYReportData(E004001008_2) line-side serving-readiness sample`
- `docs: add second-sample request-contract minimum rewrite`
- `docs: choose and justify one next high-value non-duplicate object package`

## 退出条件

- 后续包的选题不再靠惯性，而是能先过 gain / correction / quality gate。
- 第二条样板线不再只停留在 head-side readiness；line-side 至少再补一个窄缺口。
- 新会话可以只靠 repo-owned docs 接手，不必回到口头记忆。
- review 可以明确回答：
  - 新增了什么确定性
  - 对 serving 有什么实际帮助
  - 是否已经该停手或纠偏

## 当前不该并行展开的方向

- 不并行开第三个 object family dossier
- 不并行开 whole `sales list family` graph
- 不并行补 broader readiness map
- 不并行补 dossier / field / relation / readiness 全家桶
- 不并行做 support code
- 不并行做仓库结构大重排
- 不并行做 `app/services` 重构
