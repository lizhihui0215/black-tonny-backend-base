# GetDIYReportData(E004001008_2) Core Field Dictionary

状态：source-intelligence / working field dictionary

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../../README.md)
- [docs/README.md](../../README.md)
- [docs/](../../README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

这份 field dictionary 是 `GetDIYReportData(E004001008_2)` 的第一份 line-side 字段级样板。

它只做一件事：
- 把 `GetDIYReportData(E004001008_2)` 当前最有 line-side serving 价值的一批 core fields，重写成可复用的 field dictionary 记录

当前上游对象：
- [migration-charter.md](../migration-charter.md)
- [sales-list-getdiyreportdata-e004001008-2-api-dossier.md](../apis/sales-list-getdiyreportdata-e004001008-2-api-dossier.md)
- [sales-list-selsalereport-api-dossier.md](../apis/sales-list-selsalereport-api-dossier.md)
- [selsalereport-head-line-boundary-relation-doc.md](../relations/selsalereport-head-line-boundary-relation-doc.md)

这份 field dictionary 不做：
- 不做 whole line glossary
- 不做 relation doc
- 不做 serving-readiness
- 不做 `SelDeptSaleList` fields
- 不做 whole `sales list family` graph
- 不做 support code
- 不把 legacy 字段线索直接升级成 current truth

## Selection Boundary

当前只收录第一批最有价值的 line-side core fields：
- `零售单号`
- `明细流水`
- `款号`
- `颜色`
- `尺码`
- `数量`
- `单价`
- `金额`

选择规则只有四条：

1. 必须优先覆盖最可能承接 `sale_no / 零售单号` join clue 的字段。
2. 必须优先覆盖 line identity / item identity 候选字段。
3. 必须优先覆盖最小 quantity / price / amount cluster。
4. 必须尽量依赖当前已经稳定对齐的 `ColumnsList`、exploration preview、和 legacy ledger field ownership，而不是扩成 whole mapping。

当前明确不收录：
- whole `ColumnsList` 全量字段
- 还没收口的 context/helper fields，例如 `店铺名称`、`输入人`、`输入时间`、`班组`、`导购员`
- 还没进入第一批最小样板的 price companion fields，例如 `吊牌价`、`吊牌金额`
- reconciliation-side fields

## ColumnsList Mapping Boundary

`GetDIYReportData(E004001008_2)` 与 `SelSaleReport` 不同。

它的 line rows 当前不是 named object rows，
而是 array rows：

- `retdata.Data[*]`

字段名当前也不是直接写在每一行里，
而是通过：

- `retdata.ColumnsList[*]`

来恢复。

因此这份字典当前采用以下 working path convention：

1. `retdata.ColumnsList[index] = 字段名`
2. `retdata.Data[*][index] = 对应列值`
3. 只有当 raw response、exploration preview、legacy ledger 三层证据能稳定对齐时，当前字典才把该字段写成 `Supported`

当前这份样板只保守承认以下 mapping floor：

| column label | column index | payload path | current mapping status |
| --- | --- | --- | --- |
| `零售单号` | `0` | `retdata.Data[*][0]` | `Supported` |
| `明细流水` | `1` | `retdata.Data[*][1]` | `Supported` |
| `款号` | `4` | `retdata.Data[*][4]` | `Supported` |
| `单价` | `8` | `retdata.Data[*][8]` | `Supported` |
| `颜色` | `9` | `retdata.Data[*][9]` | `Supported` |
| `尺码` | `10` | `retdata.Data[*][10]` | `Supported` |
| `数量` | `11` | `retdata.Data[*][11]` | `Supported` |
| `金额` | `12` | `retdata.Data[*][12]` | `Supported` |

当前不能推出：
- whole `ColumnsList -> field meaning` mapping 已经完全闭合
- raw column index 已经能自动稳定映成 current repo field names

## Dictionary Summary

| field name | payload path | evidence level | current serving value | current limit |
| --- | --- | --- | --- | --- |
| `零售单号` | `retdata.Data[*][0]` | `Supported` | current strongest line-side `sale_no` clue; highest-value head-line join candidate on the line side | not yet a formal relation rule or serving identity rule |
| `明细流水` | `retdata.Data[*][1]` | `Supported` | current strongest line-identity candidate | uniqueness scope and serving identity semantics remain open |
| `款号` | `retdata.Data[*][4]` | `Supported` | current strongest item/style identity candidate in the first narrow line cluster | style-vs-sku semantics remain open |
| `颜色` | `retdata.Data[*][9]` | `Supported` | current item-variant qualifier clue | normalization and variant taxonomy remain open |
| `尺码` | `retdata.Data[*][10]` | `Supported` | current item-variant qualifier clue | normalization and size-system semantics remain open |
| `数量` | `retdata.Data[*][11]` | `Supported` | current line quantity clue | sign, return, and unit semantics remain open |
| `单价` | `retdata.Data[*][8]` | `Supported` | current line unit-price clue | discount and rounding semantics remain open |
| `金额` | `retdata.Data[*][12]` | `Supported` | current line amount clue | sign, settlement, and relation to head-side amount remain open |

## Field Records

### `零售单号`

- field name: `零售单号`
- payload path:
  - `retdata.ColumnsList[0] = 零售单号`
  - `retdata.Data[*][0]`
- meaning:
  - current legacy evidence treats this as the line-side sale document number clue on `GetDIYReportData(E004001008_2)`
  - current head-line study also treats its normalized form `sale_no` as the strongest candidate join key between head and line branches
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw response exposes `retdata.ColumnsList[0] = 零售单号`
  - legacy exploration preview repeatedly lists `零售单号` as the first core line column
  - legacy sales ledger explicitly states `SaleNum / 零售单号` is the highest-priority head-line join candidate
- current serving value:
  - highest-value line-side join clue in the current line sample
  - best candidate for future head-line relation work and line-side grouping
- current risk / unresolved note:
  - current repo has not formalized `sale_no` as a relation asset or serving identity rule
  - this field cannot yet be upgraded from strongest clue to formal relation truth

### `明细流水`

- field name: `明细流水`
- payload path:
  - `retdata.ColumnsList[1] = 明细流水`
  - `retdata.Data[*][1]`
- meaning:
  - current legacy evidence treats this as the per-line serial / line-row identity clue on the line route
  - current legacy field ownership also aligns it with normalized `detail_serial`
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw response exposes `retdata.ColumnsList[1] = 明细流水`
  - legacy exploration preview repeatedly lists `明细流水` as the second core line column
  - legacy sales ledger lists `detail_serial` among line-only ownership fields
- current serving value:
  - strongest current candidate for distinguishing one line row from another inside the same document
  - useful for later line-side dedupe or line-grain identity design
- current risk / unresolved note:
  - current repo has not proven whether this clue is globally stable, per-document stable, or batch-scoped
  - this field should not yet be treated as a confirmed serving key

### `款号`

- field name: `款号`
- payload path:
  - `retdata.ColumnsList[4] = 款号`
  - `retdata.Data[*][4]`
- meaning:
  - current legacy evidence treats this as the line-side product/style code clue
  - current legacy field ownership aligns it with normalized `style_code`
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw response exposes `retdata.ColumnsList[4] = 款号`
  - legacy exploration preview repeatedly lists `款号` in the first product-identity cluster
  - legacy sales ledger lists `style_code` among line-only ownership fields
- current serving value:
  - strongest current item/style identity candidate in the narrow line-side core cluster
  - provides the main product anchor for later item-level relation and serving work
- current risk / unresolved note:
  - current repo has not formalized whether this is style-level, sku-level, or another product-code layer
  - this field should not yet be treated as a confirmed downstream item identity

### `颜色`

- field name: `颜色`
- payload path:
  - `retdata.ColumnsList[9] = 颜色`
  - `retdata.Data[*][9]`
- meaning:
  - current legacy evidence treats this as the line-side color / variant qualifier clue
  - it refines the product identity neighborhood around `款号`
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw response exposes `retdata.ColumnsList[9] = 颜色`
  - legacy exploration preview repeatedly lists `颜色` inside the core line column cluster
  - legacy sales ledger lists `color` among line-only ownership fields
- current serving value:
  - useful for later item-variant grouping and comparison
  - helps keep variant semantics anchored at line grain instead of being collapsed into style-only interpretation
- current risk / unresolved note:
  - normalization rules for color naming are still open
  - this field should not yet be treated as a confirmed serving dimension key

### `尺码`

- field name: `尺码`
- payload path:
  - `retdata.ColumnsList[10] = 尺码`
  - `retdata.Data[*][10]`
- meaning:
  - current legacy evidence treats this as the line-side size / variant qualifier clue
  - it sits in the same variant neighborhood as `颜色`
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw response exposes `retdata.ColumnsList[10] = 尺码`
  - legacy exploration preview repeatedly lists `尺码` inside the core line column cluster
  - legacy sales ledger lists `size` among line-only ownership fields
- current serving value:
  - useful for later item-variant grouping and comparison
  - helps keep size semantics on the line side instead of leaking into head-level summaries
- current risk / unresolved note:
  - current repo has not rewritten size normalization or size-system policy
  - this field should not yet be treated as a confirmed serving dimension key

### `数量`

- field name: `数量`
- payload path:
  - `retdata.ColumnsList[11] = 数量`
  - `retdata.Data[*][11]`
- meaning:
  - current legacy evidence treats this as the line-side quantity clue
  - it belongs to the line-detail quantity layer, not the head-side total quantity layer
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw response exposes `retdata.ColumnsList[11] = 数量`
  - legacy exploration preview repeatedly lists `数量` in the core line column cluster
  - legacy sales ledger lists `quantity` among line-only ownership fields
- current serving value:
  - useful for future line-level quantity judgments
  - helps separate per-line quantity from head-side summed quantity
- current risk / unresolved note:
  - current repo has not formalized sign semantics for returns or reverse lines
  - unit semantics remain open

### `单价`

- field name: `单价`
- payload path:
  - `retdata.ColumnsList[8] = 单价`
  - `retdata.Data[*][8]`
- meaning:
  - current legacy evidence treats this as the line-side sold unit-price clue
  - it is distinct from `吊牌价`
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw response exposes `retdata.ColumnsList[8] = 单价`
  - legacy exploration preview repeatedly lists `单价` in the price cluster
  - legacy sales ledger lists `unit_price` among line-only ownership fields
- current serving value:
  - useful for later line-level price judgments
  - gives the current line sample one direct sold-price clue instead of relying only on aggregated amount
- current risk / unresolved note:
  - current repo has not rewritten discount, rounding, or promotion semantics
  - this field should not yet be assumed interchangeable with any future normalized price field

### `金额`

- field name: `金额`
- payload path:
  - `retdata.ColumnsList[12] = 金额`
  - `retdata.Data[*][12]`
- meaning:
  - current legacy evidence treats this as the line-side amount clue
  - it belongs to the per-line money layer, not the head-side amount summary layer
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy raw response exposes `retdata.ColumnsList[12] = 金额`
  - legacy exploration preview repeatedly lists `金额` in the core line column cluster
  - legacy sales ledger lists line-only money fields and keeps this route as the detail-line candidate
- current serving value:
  - useful for future line-level amount judgments
  - helps keep line amount discussion separate from head-side total sales amount
- current risk / unresolved note:
  - current repo has not formalized sign, refund, reversal, or settlement semantics
  - this field should not yet be treated as a direct serving-contract amount truth

## Deferred / Out-Of-Scope Fields

当前明确不进入这份样板的字段，包括：

- `单据类型`
- `店铺名称`
- `品名`
- `吊牌价`
- `吊牌金额`
- `输入人`
- `输入时间`
- `销售日期`
- `导购员`
- `会员卡号`

当前原因：
- `单据类型`、`店铺名称`、`输入时间`、`导购员` 更像 context fields，不是第一批 line-side identity / quantity / amount cluster 的第一优先级
- `吊牌价`、`吊牌金额` 虽然重要，但当前更像 price-companion layer，容易把样板带宽
- `销售日期` 虽然有 relation 支撑价值，但当前仍更适合保留为 supporting clue，而不是先和 `零售单号` 混成同级 primary field
- whole `ColumnsList` 其余字段当前仍只适合作为 later neighborhood

## What This Dictionary Makes Explicit

这份字典当前新增了四件明确的 knowledge：

1. `GetDIYReportData(E004001008_2)` 这条第二样板线已经能进入字段层，而且可以只围绕 line-side core fields 收口，不必扩成 whole line glossary。
2. `ColumnsList -> Data` 这条 line-side mapping floor 已经被单独写清，但仍明确保留“不是 whole mapping closure”的边界。
3. `零售单号`、`明细流水`、`款号` 已经被固定成当前最值得优先推进的 line-side identity / join / item cluster。
4. `颜色`、`尺码`、`数量`、`单价`、`金额` 可以被稳定看作当前最小 line-side core field cluster，而不是继续散在 dossier prose 里。

## What This Dictionary Does Not Claim

这份字典不声称：
- `GetDIYReportData(E004001008_2)` 已经成为 current repo truth
- whole `ColumnsList` mapping 已完成
- head-line relation 已经 formalized
- `sale_no` 已经成为 current formal join rule
- line-side readiness 已经成立
