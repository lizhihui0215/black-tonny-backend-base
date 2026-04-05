# SelSaleReport Core Field Dictionary

状态：source-intelligence / working field dictionary

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../../README.md)
- [docs/README.md](../../README.md)
- [docs/](../../README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

这份 field dictionary 是 `YisEposReport/SelSaleReport` 的第一份真实字段级样板。

它只做一件事：
- 把 `SelSaleReport` 当前最有 head-grain serving 价值的一批 core fields，重写成可复用的 field dictionary 记录

当前上游对象：
- [migration-charter.md](../migration-charter.md)
- [sales-list-selsalereport-api-dossier.md](../apis/sales-list-selsalereport-api-dossier.md)

当前配套 relation doc 样板位于：
- [selsalereport-head-line-boundary-relation-doc.md](../relations/selsalereport-head-line-boundary-relation-doc.md)

当前配套 serving-readiness 样板位于：
- [selsalereport-head-slice-serving-readiness.md](../serving-readiness/selsalereport-head-slice-serving-readiness.md)

这份 field dictionary 不做：
- 不做 whole `sales list family` glossary
- 不做 `GetDIYReportData(E004001008_2)` fields
- 不做 `SelDeptSaleList` fields
- 不做 relation baseline
- 不在本文内做 serving-readiness judgment
- 不把 legacy 字段线索直接升级成 current truth

## Selection Boundary

当前只收录第一批 head-like core fields：
- `SaleNum`
- `SaleDate`
- `OperMan`
- `TotalSaleAmount`
- `TotalSaleMoney`
- `ReceiveMoney`

选择规则只有一条：
- 这些字段已经在 legacy `SelSaleReport` head 路线上反复稳定出现，且对后续 order-head relation / serving 判断最有价值

当前明确不收录：
- line-side字段
- reconciliation-side字段
- 还没有足够 serving value 的 payment breakdown fields，例如 `Cash`、`CreditCard`、`OrderMoney`、`StockMoney`
- 还没有足够收口的 context/helper fields，例如 `VipCardID`、`SaleType`、`ActiveType`

## Dictionary Summary

| field name | payload path | evidence level | current serving value | current limit |
| --- | --- | --- | --- | --- |
| `SaleNum` | `retdata[0].Data[*].SaleNum` | `Supported` | current strongest order-head identity clue; highest-value head/line join candidate | not yet a formal relation or current repo identity rule |
| `SaleDate` | `retdata[0].Data[*].SaleDate` | `Supported` | current order-head date clue; useful as context and secondary validation | not a confirmed primary join key |
| `OperMan` | `retdata[0].Data[*].OperMan` | `Supported` | current operator-at-order-grain clue; useful for order-head serving slices | encoding/normalization semantics remain open |
| `TotalSaleAmount` | `retdata[0].Data[*].TotalSaleAmount` | `Supported` | current order-head quantity-total clue | unit/return interaction semantics remain open |
| `TotalSaleMoney` | `retdata[0].Data[*].TotalSaleMoney` | `Supported` | current order-head sales-amount clue | discount/refund/rounding semantics remain open |
| `ReceiveMoney` | `retdata[0].Data[*].ReceiveMoney` | `Supported` | current order-head received-amount clue; useful for payment-summary discussion at head grain | payment breakdown and settlement semantics remain open |

## Field Records

### `SaleNum`

- field name: `SaleNum`
- payload path: `retdata[0].Data[*].SaleNum`
- meaning:
  - current legacy evidence treats this as the order-head document number clue on `SelSaleReport`
  - current legacy sales-line study also treats its normalized form `sale_no` as the strongest candidate join key between head and line branches
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw `SelSaleReport` response includes `retdata[0].Data[*].SaleNum`
  - legacy grid-1 column definition maps `SaleNum` to `销售单号`
  - legacy sales ledger explicitly states `SaleNum/零售单号` is the highest-priority head-line join candidate
- current serving value:
  - highest-value order-head identity clue in the current `SelSaleReport` sample line
  - best candidate for future order-head dedupe / grouping / relation work
- current risk / unresolved note:
  - current repo has not formalized `sale_no` as a relation asset or serving identity rule
  - this field cannot yet be upgraded from candidate join key to formal relation truth

### `SaleDate`

- field name: `SaleDate`
- payload path: `retdata[0].Data[*].SaleDate`
- meaning:
  - current legacy evidence treats this as the order-head sale date clue on `SelSaleReport`
  - it is consistently present alongside `SaleNum` on the head route
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw `SelSaleReport` response includes `retdata[0].Data[*].SaleDate`
  - legacy grid-1 column definition maps `SaleDate` to `销售日期`
  - legacy sales ledger keeps normalized `sale_date` only as context / auxiliary validation, not the primary join key
- current serving value:
  - useful as order-head time context
  - useful as a secondary validation clue when comparing head and line neighborhoods
- current risk / unresolved note:
  - current repo has not rewritten timezone, business-date, or date-boundary semantics
  - this field should not be mistaken for the primary head-line relation key

### `OperMan`

- field name: `OperMan`
- payload path: `retdata[0].Data[*].OperMan`
- meaning:
  - current legacy evidence treats this as the operator / salesperson clue on the `SelSaleReport` head route
  - it belongs to order-head context rather than line-grain item detail
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw `SelSaleReport` response includes `retdata[0].Data[*].OperMan`
  - legacy grid-1 column definition maps `OperMan` to `导购员`
  - legacy sales evidence keeps normalized `operator` as a candidate contextual join/support field, not the primary key
- current serving value:
  - useful for future order-head serving slices that need operator-at-order-grain context
  - helps keep operator semantics anchored at head grain instead of leaking into line-only interpretation
- current risk / unresolved note:
  - raw samples currently show URL-escaped encoding in some responses
  - current repo has not rewritten decoding / normalization policy for this field

### `TotalSaleAmount`

- field name: `TotalSaleAmount`
- payload path: `retdata[0].Data[*].TotalSaleAmount`
- meaning:
  - current legacy evidence treats this as the head-grain total quantity clue on `SelSaleReport`
  - grid metadata maps it to `销量`
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw `SelSaleReport` response includes `retdata[0].Data[*].TotalSaleAmount`
  - legacy grid-1 column definition marks `TotalSaleAmount` as a summed numeric column
  - legacy sales ledger repeatedly uses it as part of the document-head field cluster
- current serving value:
  - useful for future order-head quantity summaries
  - helps keep quantity discussion at document-head grain instead of confusing it with per-line quantity
- current risk / unresolved note:
  - current repo has not formalized numeric type policy, unit semantics, or return/reverse interaction
  - this field should not be assumed to equal line-count or item-row-count

### `TotalSaleMoney`

- field name: `TotalSaleMoney`
- payload path: `retdata[0].Data[*].TotalSaleMoney`
- meaning:
  - current legacy evidence treats this as the head-grain sales amount clue on `SelSaleReport`
  - grid metadata maps it to `销售金额`
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw `SelSaleReport` response includes `retdata[0].Data[*].TotalSaleMoney`
  - legacy grid-1 column definition marks `TotalSaleMoney` as a summed numeric column
  - legacy sales ledger groups it with `ReceiveMoney` and other payment-related head fields
- current serving value:
  - useful for future order-level gross sales amount judgments
  - gives the head branch a stable money field distinct from line-level amount discussion
- current risk / unresolved note:
  - current repo has not rewritten discount, reversal, refund, or rounding semantics for this field
  - this field should not yet be treated as directly interchangeable with any current formal serving amount field

### `ReceiveMoney`

- field name: `ReceiveMoney`
- payload path: `retdata[0].Data[*].ReceiveMoney`
- meaning:
  - current legacy evidence treats this as the head-grain received/settled amount clue on `SelSaleReport`
  - grid metadata maps it to `实收金额`
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw `SelSaleReport` response includes `retdata[0].Data[*].ReceiveMoney`
  - legacy grid-1 column definition marks `ReceiveMoney` as a summed numeric column
  - legacy sales ledger includes it in the order-head field cluster used to discuss payment summary at head grain
- current serving value:
  - useful for future order-head payment summary slices
  - helps distinguish sales amount from received amount before any finer payment-breakdown work begins
- current risk / unresolved note:
  - current repo has not rewritten settlement semantics or the relationship to `Cash` / `CreditCard` / `OrderMoney` / `StockMoney`
  - this field should not be treated as a formal paid-status or payment-contract truth

## Deferred / Out-Of-Scope Fields

当前明确不进入这份样板的字段，包括：

- `VipCardID`
- `SaleType`
- `ActiveType`
- `Cash`
- `CreditCard`
- `OrderMoney`
- `StockMoney`
- `TotalSaleRetailMoeny`

当前原因：
- `VipCardID` 与 `SaleType` 当前更像 context/auxiliary fields，还不在这份最窄 core-field 样板的第一优先级
- `Cash`、`CreditCard`、`OrderMoney`、`StockMoney` 虽然重要，但当前更像 payment breakdown layer，容易把范围带宽
- `TotalSaleRetailMoeny` 当前还存在 legacy spelling inconsistency 线索，不适合在第一批 core-field 样板里先收口

## What This Dictionary Makes Explicit

这份字典当前新增了三件明确的 knowledge：

1. `SelSaleReport` 的第二条样板线已经能进入字段层，而且可以只围绕 head-grain core fields 收口，不必扩成 whole family glossary。
2. `SaleNum` 已经被单独固定成 highest-value core field，但仍停留在 `Supported`，没有被偷升成 formal relation asset。
3. `SaleDate`、`OperMan`、`TotalSaleAmount`、`TotalSaleMoney`、`ReceiveMoney` 可以被稳定看作 head-like core field cluster，而不是与 line/reconciliation fields 混层。

## What This Dictionary Does Not Claim

这份字典不声称：
- `SelSaleReport` 已经成为 current repo truth
- head-line relation 已经 formalized
- `sale_no` 已经成为 current formal join rule
- whole `sales list family` field universe 已经盘清
- payment breakdown semantics 已经闭合
