# GetDIYReportData(E004001008_2) API Dossier

状态：source-intelligence / working dossier

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../../README.md)
- [docs/README.md](../../README.md)
- [docs/](../../README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

这份文档是 source-intelligence 主线下第三份真实 API dossier 样板，
也是 `sales list family` 第二条样板线里的第一份 line-side object answer。

它只做一件事：
- 把 `FXDIYReport/GetDIYReportData(menuid=E004001008, gridid=E004001008_2)` 重写成一份可复用的 line-side API dossier

这份 dossier 复用的主线约束以：
- [migration-charter.md](../migration-charter.md)
- [legacy-source-intelligence-inventory-baseline.md](../legacy-source-intelligence-inventory-baseline.md)
- [sales-list-selsalereport-api-dossier.md](./sales-list-selsalereport-api-dossier.md)
- [selsalereport-head-line-boundary-relation-doc.md](../relations/selsalereport-head-line-boundary-relation-doc.md)
- [selsalereport-head-slice-serving-readiness.md](../serving-readiness/selsalereport-head-slice-serving-readiness.md)
- 为准

当前同层样板包括：
- [erp-orders-api-dossier.md](./erp-orders-api-dossier.md)
- [sales-list-selsalereport-api-dossier.md](./sales-list-selsalereport-api-dossier.md)

当前配套字段字典样板位于：
- [sales-list-getdiyreportdata-e004001008-2-core-field-dictionary.md](../fields/sales-list-getdiyreportdata-e004001008-2-core-field-dictionary.md)

这份 dossier 不做：
- 不做 relation doc
- 不在本文内做 serving-readiness judgment
- 不做 `SelDeptSaleList` dossier
- 不做 whole `sales list family` graph
- 不做 support code
- 不把 legacy 线索直接升级成 current truth

## API Identity

- dossier type: `API dossier`
- object family: `sales list family`
- selected line-side object: `FXDIYReport/GetDIYReportData(menuid=E004001008, gridid=E004001008_2)`
- short object name: `GetDIYReportData(E004001008_2)`
- current dossier role: current second sample line 的 line-side object sample
- overall evidence level for this dossier object: `Supported`

当前最多能说明：
- `GetDIYReportData(E004001008_2)` 是 legacy `销售清单` 页面上一个稳定可命名、稳定附着在 page context 上、并且更像 order-line / detail-line grain 的对象

当前不能说明：
- 它已经成为 current repo formal truth
- 它已经自动进入 current repo path / contract / readiness
- 它已经足以代表 whole `sales list family`

## Why This Is The Current Missing Line-Side Object To Fill

| candidate object | current role | why this package chooses or skips it | evidence level |
| --- | --- | --- | --- |
| `GetDIYReportData(E004001008_2)` | line-side object | 当前最直接决定 head-line boundary 能否继续推进的 sibling object；如果没有单独 dossier，第二条样板线会一直停在“head 已收口、line 只有名字”的状态 | `Supported` |
| `SelSaleReport` | head-side object | 已经有 dossier / field dictionary / relation doc / serving-readiness 闭环，不是当前最缺的对象位 | `Supported` |
| `SelDeptSaleList` | reconciliation object | 粒度更宽，当前只需要被稳定压回 reconciliation / research side，不适合作为这包 primary object | `Supported` |

当前选择 `GetDIYReportData(E004001008_2)` 的理由只有三条：

1. 它是 `SelSaleReport` 同页同 family 的直接 sibling object，也是当前第二条样板线最明显的 line-side 缺口。
2. legacy 证据已经稳定把它写成 `明细行候选源`，因此 current repo 需要先把 line-side object answer 独立写清，后续 field/relation work 才不会继续悬空。
3. 它的 object identity 比 `SelDeptSaleList` 更直接服务 head-line boundary，而不是对账/宽表边界。

## Menu / Page / Source-Surface Context

### Menu Context

当前 dossier 结论：
- `GetDIYReportData(E004001008_2)` 当前最稳定的 menu context 不是独立菜单，而是挂在 `销售清单` 页面之下

evidence level:
- `Supported`

当前支撑：
- legacy 页面 manifest 把 `销售清单` 固定在 `报表管理 / 零售报表 / 销售清单`
- legacy exploration 与 maturity board 都把 `GetDIYReportData(E004001008_2)` 绑在这条页面线上

当前最多能说明：
- 这是 `销售清单` page-attached object，不是脱离 page 语义即可单独理解的裸接口

当前不能推出：
- `GetDIYReportData(E004001008_2)` 拥有独立 menu node

### Page Context

当前 dossier 结论：
- `GetDIYReportData(E004001008_2)` 当前应被放在 legacy `销售清单` page context 下理解；该页面可见 `FuncLID=E004001008`、`FuncUrl=UnhiddenSaleList`

evidence level:
- `Supported`

当前支撑：
- legacy 页面 manifest
- legacy exploration metadata
- legacy maturity board

当前最多能说明：
- 这是由 `销售清单` page + `gridid=_2` 共同限定的 object identity

当前不能推出：
- current repo 已经重写了这条 page-to-object mapping

### Source-Surface Context

当前 dossier 结论：
- legacy `销售清单` page 当前被稳定识别为 `multi_grain_route`
- `GetDIYReportData(E004001008_2)` 是其中的 line-side branch

evidence level:
- `Supported`

当前支撑：
- legacy page research 把该页面标成 `multi_grain_route`
- legacy sales ledger 把 `_2 + 销售清单` 写成订单行候选路线
- legacy maturity board 把它写成 `明细行路线`

当前不能推出：
- family 内全部 grain relation 已被 current repo 重写吸收

## Why This Belongs To The Line-Side Object Slot

当前 dossier 结论：
- `GetDIYReportData(E004001008_2)` 当前更像 line-detail / order-line grain object，而不是 head object 或 reconciliation object

evidence level:
- `Supported`

当前支撑：
- request 绑定了 `menuid=E004001008` 与 `gridid=E004001008_2`
- legacy exploration 在 base case 下返回：
  - `response_shape = retdata.ColumnsList+Data`
  - `row_count = 9843`
  - `column_count = 52`
  - columns preview 包括：
    - `零售单号`
    - `明细流水`
    - `款号`
    - `颜色`
    - `尺码`
    - `数量`
    - `金额`
- legacy raw response显示 `retdata.Data[*]` 是 array rows，而不是 named object rows
- legacy sales ledger 稳定区分：
  - `_1 + SelSaleReport` = head route
  - `_2 + 销售清单` = line route
  - `SelDeptSaleList` = reconciliation route

当前最多能说明：
- 这是当前第二条样板线里最直接的 line-side object

当前不能推出：
- line-side field mapping 已闭合
- 它已经形成 current repo formal serving object

## Payload / Carrier Baseline

### Request-Side Baseline

当前 dossier 结论：
- `GetDIYReportData(E004001008_2)` 当前只有 legacy-level request baseline，不具有 current repo-owned request contract

evidence level:
- `Supported`

当前已知 request clues：
- method: `POST`
- auth mode: `token`
- fixed page binding:
  - `menuid = E004001008`
  - `gridid = E004001008_2`
- representative parameter vocabulary:
  - `parameter.BeginDate`
  - `parameter.EndDate`
  - `parameter.Depart`
  - `parameter.Operater`
  - `parameter.Tiem`
  - `parameter.WareClause`

当前参数语义只到这一层：
- `parameter.Tiem`
  - `Supported`
  - current legacy evidence shows `0 / 1 / 2` 在当前账号下属于 `same_dataset`
- `parameter.BeginDate`
  - `Supported`
  - current legacy evidence shows `scope_or_date_boundary`
- `parameter.EndDate`
  - `Supported`
  - current legacy evidence shows `scope_or_date_boundary`
- `parameter.Depart`
  - `Supported`
  - current legacy evidence shows `scope_or_date_boundary`

当前不能推出：
- request-side 完整字段表
- 当前账号下现有参数语义就是 future current repo truth
- `Tiem` 已经完全不重要

### Response / Carrier Baseline

当前 dossier 结论：
- `GetDIYReportData(E004001008_2)` 当前表现为 `ColumnsList + Data` 的 array/grid carrier，而不是 head-side named object carrier

evidence level:
- `Supported`

当前支撑：
- legacy raw response 顶层结构是：
  - `errcode`
  - `retdata`
- line rows 当前挂在：
  - `retdata.Data[*]`
- field meaning 当前需要通过：
  - `retdata.ColumnsList[*]`
  - grid metadata
  来恢复
- 当前 raw response 已显示 `ColumnsList` 包含：
  - `零售单号`
  - `明细流水`
  - `款号`
  - `数量`

当前最多能说明：
- 这是一个比 head-side 更依赖 grid metadata 的 line carrier
- 这也是为什么 line-side object answer 必须先独立成 dossier，不能直接拿 head dossier 代替

当前不能推出：
- line-side full field dictionary 已完成
- raw column index 已经能自动稳定映成 current repo field names

## Current Evidence Level

| dossier statement | evidence level | evidence basis | current use | current limit |
| --- | --- | --- | --- | --- |
| `GetDIYReportData(E004001008_2)` 是 `销售清单` page 上稳定的 line-side object | `Supported` | legacy exploration；legacy maturity board；legacy sales ledger | 允许 current repo 先落单一 line-side dossier | 不等于 current repo truth |
| `销售清单` 当前是 `multi_grain_route`，而 `_2` 是 line branch | `Supported` | legacy page research；legacy sales ledger；legacy maturity board | 允许把它写成 head sibling，而不是独立 family | 不等于 whole family relation 已 formalized |
| `GetDIYReportData(E004001008_2)` 当前最像明细行候选源 | `Supported` | legacy sales ledger；exploration row/column evidence；raw response shape | 允许把 current serving value 收口到 line-side object 层 | 不等于 line-side readiness 已成立 |
| line carrier 当前依赖 `ColumnsList + Data` array/grid 语义 | `Supported` | legacy exploration；raw response | 允许明确指出 line-side 的 object difficulty 高于 head-side | 不等于 field dictionary 已完成 |
| legacy board 已把它写成 `已HTTP回证`、`capture_admission_ready=true`、但 `mainline_ready=false` | `Supported` | legacy api-maturity-board | 允许 current dossier 保守承认它是高价值对象，但仍不越界到 current repo mainline judgment | 不等于 current repo 已接纳 capture/path |

## Current Serving Value

当前 dossier 结论：
- 在 `sales list family` 当前第二条样板线里，`GetDIYReportData(E004001008_2)` 是最有必要先独立沉淀的 line-side object

evidence level:
- `Supported`

当前 serving value 主要有三点：

1. 它补上了 `SelSaleReport` head 闭环之后最明显的 line-side object 缺口。
2. 它为后续 line-side field dictionary 与 head-line relation answer 提供了单独 object anchor。
3. 它把 line grain 与 `SelSaleReport` head grain、`SelDeptSaleList` reconciliation grain 明确拆开，避免 whole family 混层。

当前不能推出：
- 它已经是 current repo 的 landed serving source
- 它已经足以单独支撑 contract/path judgment
- reverse lane 已经被这份 dossier 一起解释完成

## Unresolved Blockers

### Request Semantics Still Unrewritten

current status:
- `Candidate`

当前缺口：
- current repo 还没有把 `menuid/gridid/parameter.*` 重写成 repo-owned request contract
- `Tiem`、`Depart` 等参数仍停留在 legacy exploration 语义层

### Field Recovery Still Depends On Grid Metadata

current status:
- `Candidate`

当前缺口：
- current repo 虽然已经有第一份 narrow line-side field dictionary，但 `ColumnsList -> field meaning` 当前仍只收口到一小批 core fields
- line rows 当前仍依赖 array index + grid metadata，不是 named field payload

### Head-Line Relation Still Outside This Dossier

current status:
- `Candidate`

当前缺口：
- `sale_no / 零售单号` 虽然已经是 strongest join clue，但 relation rule 仍未 formalized
- exact field-to-field mapping 仍不应在这份 dossier 里偷写成 truth

### Reverse / Reconciliation Boundaries Stay Outside

current status:
- `Deferred`

当前缺口：
- `sales_reverse_document_lines` 仍是 later neighborhood
- `SelDeptSaleList` 仍是 reconciliation object
- 这份 dossier 当前只回答 line-side object identity，不回答这些 wider boundaries

## Non-Goals

这份 dossier 当前不做：
- 不写 `GetDIYReportData(E004001008_2)` 的字段字典
- 不写 head-line relation doc
- 不写 serving-readiness
- 不写 `SelDeptSaleList` dossier
- 不把 `sales list family` 一次扩成 family-wide graph
