# Current Main State

状态：source-intelligence / current-main minimum truth

如果这份文档仍处在待 merge 的 PR 里，
它当前只描述 merge target 下应固定的最小状态，
不应被反写成 current `main` 已经拥有的事实。

来源锚点：
- [migration-charter.md](../migration-charter.md)
- [legacy-source-intelligence-inventory-baseline.md](../legacy-source-intelligence-inventory-baseline.md)
- [../README.md](../README.md)
- [apis/README.md](../apis/README.md)
- [fields/README.md](../fields/README.md)
- [relations/README.md](../relations/README.md)
- [serving-readiness/README.md](../serving-readiness/README.md)

## 当前主目标

- 持续把 legacy source knowledge 重写成 repo-owned knowledge assets。
- 先服务 serving judgment。
- 不把 legacy 架构、script、tmp、output 迁进新仓。

## 当前已完成资产

- 主线规则已落地：
  - charter
  - evidence taxonomy
  - deliverable types
  - review guardrails
- 主输出位已落地：
  - `apis/`
  - `fields/`
  - `relations/`
  - `serving-readiness/`
- `/erp/orders` first slice 已有一套闭环样板：
  - dossier
  - field dictionary
  - relation doc
  - serving-readiness
- `sales list family` 第二条样板线已落地：
  - `SelSaleReport` dossier
  - `SelSaleReport` core field dictionary
  - `SelSaleReport` head-line boundary relation doc
  - `SelSaleReport` head-slice serving-readiness
  - `GetDIYReportData(E004001008_2)` dossier
  - `GetDIYReportData(E004001008_2)` first narrow field dictionary
- legacy inventory baseline 已落地。
- 当前 `ops` 控制面已落地。

## 当前未完成资产

- `GetDIYReportData(E004001008_2)` line-side relation doc
- `GetDIYReportData(E004001008_2)` line-side serving-readiness doc
- 第二条样板线的 exact head-line relation contract answer
- 第二条样板线的 request-contract rewriting
- whole `sales list family` relation/readiness answer
- 下一批高价值 legacy knowledge 的正式选题结果

## 当前 blocker

- 第二条样板线还没有 repo-owned line-side relation/readiness 闭环。
- `SaleNum` 仍只是 strongest clue，不是 confirmed rule。
- `Supported / Candidate / Deferred` 还不能直接升级成 path / contract truth。
- 如果继续无控制地补 dossier，很容易进入低收益循环。

## 当前下一步候选

- 先做一个窄的 line-side relation 包。
- 或先做一个窄的 line-side serving-readiness 包。
- 或在继续扩样板前，先用当前 inventory baseline 明确下一批只开一个高价值对象。

## 当前明确不该假设的事

- 不该假设 `SelSaleReport` 已有 landed runtime path。
- 不该假设 `SelSaleReport` 已有 formal serving contract。
- 不该假设 `SaleNum` 已经是 confirmed head-line relation rule。
- 不该假设 whole `sales list family` 已 ready。
- 不该假设 legacy registry / board / evidence code 已经被重写成 current repo-owned truth。
- 不该假设 candidate/support 可以直接喂给 formal contract 或 runtime code。
