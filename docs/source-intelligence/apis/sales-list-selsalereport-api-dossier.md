# SelSaleReport API Dossier

状态：source-intelligence / working dossier

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../../README.md)
- [docs/README.md](../../README.md)
- [docs/](../../README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

这份文档是 source-intelligence 主线下第二份真实 API dossier 样板。

它只做一件事：
- 把 legacy `sales list family` 中最适合做 primary object 的单一 endpoint，重写成一份可复用的 API dossier

这份 dossier 复用的主线约束以：
- [migration-charter.md](../migration-charter.md)
- [legacy-source-intelligence-inventory-baseline.md](../legacy-source-intelligence-inventory-baseline.md)
- 为准

当前同层样板包括：
- [erp-orders-api-dossier.md](./erp-orders-api-dossier.md)

当前配套字段字典样板位于：
- [selsalereport-core-field-dictionary.md](../fields/selsalereport-core-field-dictionary.md)

当前配套 relation doc 样板位于：
- [selsalereport-head-line-boundary-relation-doc.md](../relations/selsalereport-head-line-boundary-relation-doc.md)

当前配套 serving-readiness 样板位于：
- [selsalereport-head-slice-serving-readiness.md](../serving-readiness/selsalereport-head-slice-serving-readiness.md)

当前 sibling line-side dossier 样板位于：
- [sales-list-getdiyreportdata-e004001008-2-api-dossier.md](./sales-list-getdiyreportdata-e004001008-2-api-dossier.md)

这份 dossier 不做：
- 不做整个 `sales list family` 全量 dossier
- 不做字段字典
- 不做 relation baseline
- 不在本文内做 serving-readiness judgment
- 不做 support code
- 不把 legacy 线索直接升级成 current truth

## API Identity

- dossier type: `API dossier`
- primary object family: `sales list family`
- selected primary endpoint: `YisEposReport/SelSaleReport`
- short endpoint name: `SelSaleReport`
- current dossier role: legacy `sales list family` 的 single-endpoint primary object sample
- overall evidence level for this dossier object: `Supported`

当前最多能说明：
- `SelSaleReport` 是 legacy `sales list family` 里一个稳定命名、稳定出现、且 serving relevance 很高的单一 endpoint 对象

当前不能说明：
- `SelSaleReport` 已经成为 current repo formal truth
- `SelSaleReport` 已经自动进入 current repo path / contract / readiness

## Why This Endpoint Is The Primary Object For This Sample

| candidate object | current role in family | why not chosen as this package's primary object | evidence level |
| --- | --- | --- | --- |
| `YisEposReport/SelSaleReport` | head-grain primary candidate | endpoint identity最窄，不依赖 generic DIY endpoint + `menuid/gridid` 叠加语义；同时 serving relevance 明确，适合单独立 dossier | `Supported` |
| `FXDIYReport/GetDIYReportData(E004001008_2)` | line-grain primary candidate | 仍强依赖 `menuid=E004001008`、`gridid=_2` 与页面模板语义；更适合作为独立 line-side dossier 与后续 field/relation 资产，而不是第二份单一 endpoint 样板 | `Supported` |
| `YisEposReport/SelDeptSaleList` | reconciliation / research source | legacy 里已被稳定压回对账/研究角色，不适合作为 family primary object | `Supported` |

当前选择 `SelSaleReport` 的理由只有三条：

1. 它比 `GetDIYReportData(E004001008_2)` 更像单一 endpoint object，而不是页面模板驱动的复合 endpoint 用法。
2. 它比 `SelDeptSaleList` 更接近 future serving mainline value，而不是对账辅助。
3. 它仍然处在 `销售清单` 同一 page context 内，后续要补 head/line relation 时不会丢掉 sibling context。

## Menu / Page / Source-Surface Context

### Menu Context

当前 dossier 结论：
- `SelSaleReport` 当前最稳定的 menu context 不是独立菜单，而是挂在 `销售清单` 页面之下

evidence level:
- `Supported`

当前支撑：
- legacy 菜单覆盖 manifest 把 `销售清单` 固定在 `报表管理 / 零售报表 / 销售清单`
- legacy page research 规则把 `销售清单` 作为 `sales list family` 的主要页面对象

当前最多能说明：
- `SelSaleReport` 的 menu/page context 当前应写在 `销售清单` 这条页面线上

当前不能推出：
- `SelSaleReport` 拥有独立 menu node
- page open baseline 就会直接打出 `SelSaleReport`

### Page Context

当前 dossier 结论：
- `SelSaleReport` 当前应被放在 legacy `销售清单` page context 下理解；该页面自身可见 `FuncLID=E004001008`、`FuncUrl=UnhiddenSaleList`

evidence level:
- `Supported`

当前支撑：
- legacy 菜单覆盖 manifest
- legacy page research registry

当前最多能说明：
- 这是一个 page-attached endpoint object，不是脱离页面语义即可完全理解的裸接口

当前不能推出：
- current repo 已经重写了这条 page-to-endpoint mapping

### Source-Surface Context

当前 dossier 结论：
- legacy `销售清单` page 当前被稳定识别为一条 `multi_grain_route`
- `SelSaleReport` 是其中的 head-grain branch

evidence level:
- `Supported`

当前支撑：
- legacy page research logic 会在 `GetDIYReportData` 与 `SelSaleReport` 同时出现时，把该页面标成 `multi_grain_route`
- legacy sales ledger 与 maturity board 都把 `SelSaleReport` 和 `GetDIYReportData(E004001008_2)` 并列写成主源候选，但粒度不同

当前不能推出：
- family 内全部 grain relation 已被 current repo 重写吸收

## Payload / Carrier Baseline

### Request-Side Baseline

当前 dossier 结论：
- `SelSaleReport` 当前只具有 legacy-level request baseline，不具有 current repo-owned request contract

evidence level:
- `Supported`

当前已知 request clues：
- method: `POST`
- auth mode: `token`
- representative filter vocabulary: `bdate`、`edate`
- same-family page context 下还存在 `Depart`、`Operater`、`WareClause` 等上下文线索，但它们不应被自动写成 `SelSaleReport` 已确认 request contract

当前不能推出：
- request-side 完整字段表
- 当前账号下空值是否就等于全量
- current repo 已承认的 request semantics

### Response / Carrier Baseline

当前 dossier 结论：
- `SelSaleReport` 当前表现为 document-head oriented row carrier，而不是 line carrier 或 reconciliation wide table

evidence level:
- `Supported`

当前支撑：
- legacy sales ledger 把它明确写成订单头候选源
- legacy sales evidence chain 记录它在样本窗口下真实返回 `3717` 行
- 当前被反复提及的核心字段包括：
  - `SaleNum`
  - `SaleDate`
  - `OperMan`
  - `TotalSaleAmount`
  - `TotalSaleMoney`
  - `ReceiveMoney`
  - `Cash`
  - `CreditCard`
  - `OrderMoney`
  - `StockMoney`

当前最多能说明：
- `SelSaleReport` 目前最像 order-head row carrier

当前不能推出：
- 它的完整 field universe 已被收口
- response envelope 已被 current repo 重写吸收

## Grain Relation Overview

| object | current grain role | current status | evidence level | current implication |
| --- | --- | --- | --- | --- |
| `SelSaleReport` | `head` | primary object of this dossier | `Supported` | 适合作为 family 的 order-head anchor |
| `GetDIYReportData(E004001008_2)` | `line` | sibling candidate | `Supported` | 更适合作为后续 line-side source object，而不是本包 primary object |
| `SelDeptSaleList` | `reconciliation` | sibling but not mainline | `Supported` | 继续只做研究/对账辅助，不应混成 primary source |
| `sales_reverse_document_lines` | `reverse / research-only` | outside this dossier scope | `Supported` | 说明 family 里还存在逆向单据研究层，但本包不展开 |

当前 grain relation 只写到这一层：
- `SelSaleReport` = head-grain branch
- `GetDIYReportData(E004001008_2)` = line-grain branch
- `SelDeptSaleList` = reconciliation branch

当前不能推出：
- head / line relation 已经被 current repo formalized
- `sale_no` join rule 已经成为 current truth

## Current Serving Value

当前 dossier 结论：
- 在 legacy `sales list family` 内，`SelSaleReport` 是当前最值得先迁成单独 source-intelligence 对象的 order-head candidate

evidence level:
- `Supported`

当前 serving value 主要有三点：

1. 如果后续要判断 order-level serving candidates，`SelSaleReport` 是 family 内最窄的 head anchor。
2. 它能把 future `order count / order money / payment summary / operator-at-order-grain` 这类讨论固定在 head grain，而不是误混入 line 或 reconciliation grain。
3. 它为后续补 line-side dossier、field dictionary 或 relation doc 提供一个稳定 sibling anchor。

当前不能推出：
- 它已经是 current repo 的 landed serving source
- 它已经足以单独支撑 contract/path judgment

## Evidence Matrix

| dossier statement | evidence level | evidence basis | current use | current limit |
| --- | --- | --- | --- | --- |
| `SelSaleReport` 是 `sales list family` 中最适合做单一 primary object 的 endpoint | `Supported` | legacy inventory baseline；legacy sales ledger；legacy maturity board | 允许当前包先落单一 dossier，而不是扩成 whole family | 不等于 line/reconciliation 已经不重要 |
| `SelSaleReport` 绑定在 `销售清单` page context 下 | `Supported` | legacy menu coverage manifest；legacy page research rules | 允许把 menu/page context 写进 dossier | 不等于 current repo 已有 page mapping truth |
| `销售清单` 当前是 `multi_grain_route`，`SelSaleReport` 是 head branch | `Supported` | legacy page research logic；legacy sales ledger | 允许在 dossier 中写 grain relation overview | 不等于 relation 已 formalized |
| `SelSaleReport` 当前最像 order-head row carrier | `Supported` | legacy sales ledger；legacy evidence chain；legacy maturity board | 允许把 payload baseline 写成 head-oriented candidate | 不等于完整 field dictionary 已完成 |
| `SelDeptSaleList` 继续只做 reconciliation/research source | `Supported` | legacy sales ledger；legacy maturity board；legacy route registry | 允许把 reconciliation 从 primary object 排除 | 不等于该路线没有价值 |
| `GetDIYReportData(E004001008_2)` 更适合作为后续 line-side对象 | `Supported` | legacy sales ledger；legacy route registry；legacy maturity board | 允许当前先不把 dossier 扩成 whole family | 不等于 line lane 已 ready |

## Unresolved Blockers

### Request-Side Contract Still Unrewritten

current status:
- `Candidate`

当前缺口：
- current repo 还没有把 `SelSaleReport` 的 request contract 重写成 repo-owned answer
- legacy filter vocabulary 仍停留在 ledger / board / page-research knowledge 层

### Head / Line Relation Still Unformalized

current status:
- `Candidate`

当前缺口：
- legacy 已把 `sale_no` 收口成最强 join candidate
- 但 current repo 还没有把这条 join rule 重写成正式 relation asset

### Field Universe Still Open

current status:
- `Candidate`

当前缺口：
- 当前只知道一批 head-like fields
- 还没有新仓字段字典来固定 `SelSaleReport` 的字段级 meaning / exclusions / risk

## Non-Goals

这份 dossier 当前不做：
- 不写 `GetDIYReportData(E004001008_2)` dossier
- 不写 `SelDeptSaleList` dossier
- 不把 `sales list family` 一次扩成 family-wide dossier
- 不定义 head-line join contract
- 不定义 serving-readiness judgment
- 不把 legacy `capture admit` 状态误写成 current repo truth
