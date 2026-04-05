# SelSaleReport Head-Line Boundary Relation Doc

状态：source-intelligence / working relation doc

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../../README.md)
- [docs/README.md](../../README.md)
- [docs/](../../README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

这份 relation doc 是 `SelSaleReport` 这条第二样板线的第一份关系级样板。

它只做一件事：
- 把 `SelSaleReport` 在 `sales list family` 中的 head-line boundary，重写成一份可复用 relation doc

当前上游对象：
- [migration-charter.md](../migration-charter.md)
- [sales-list-selsalereport-api-dossier.md](../apis/sales-list-selsalereport-api-dossier.md)
- [selsalereport-core-field-dictionary.md](../fields/selsalereport-core-field-dictionary.md)

当前配套 serving-readiness 样板位于：
- [selsalereport-head-slice-serving-readiness.md](../serving-readiness/selsalereport-head-slice-serving-readiness.md)

当前 sibling line-side dossier 样板位于：
- [sales-list-getdiyreportdata-e004001008-2-api-dossier.md](../apis/sales-list-getdiyreportdata-e004001008-2-api-dossier.md)

这份 relation doc 不做：
- 不做 whole `sales list family` relation graph
- 不做 `GetDIYReportData(E004001008_2)` dossier
- 不做 `SelDeptSaleList` dossier
- 不做更多字段扩写
- 不在本文内做 serving-readiness judgment
- 不做 support code
- 不把 `SaleNum` 直接升级成 confirmed relation truth

## Scope Boundary

当前只覆盖四类关系：

1. `SelSaleReport` 在 `sales list family` 中的 head object position
2. `SaleNum` 作为 head-line join clue 的当前关系强度
3. `SelSaleReport` 与 line-side candidate object 的 boundary
4. `SelSaleReport` 与 reconciliation object 的 grain boundary

当前明确不覆盖：
- whole sales family relation graph
- serving-readiness
- reverse lane 的全量关系解释
- payment breakdown relation universe
- field universe beyond the current head-like core cluster

## Relation Summary Matrix

| relation statement | relation type | evidence level | current serving value | current limit |
| --- | --- | --- | --- | --- |
| `SelSaleReport` occupies the head-object position inside the current `sales list family` sample line | object-position relation | `Supported` | gives the second sample line a stable order-head anchor | does not make `SelSaleReport` current repo truth |
| `retdata[0].Data[*].SaleNum` is the strongest current head-line join clue toward the line-side candidate object | head-line join clue | `Supported` | gives later relation work one high-value key to organize around | is not yet a formalized relation rule |
| normalized `sale_no` currently behaves like a `one_to_many` head-line boundary clue | head-line cardinality clue | `Supported` | shows why head and line should be modeled as separate grains instead of one table | continuous-batch stability and rewritten repo-owned relation semantics remain open |
| `SelSaleReport` and `GetDIYReportData(E004001008_2)` belong to the same page line but different grains | same-page cross-grain boundary | `Supported` | keeps future head vs line work in the same neighborhood without collapsing them | does not settle exact line-side field mapping or join contract |
| `SelSaleReport` and `SelDeptSaleList` are not peers at the same grain; `SelDeptSaleList` remains a reconciliation object | grain-boundary relation | `Supported` | prevents reconciliation-wide rows from being mistaken for head rows | does not mean reconciliation has no value |
| exact raw path mapping from `SaleNum` to the line-side raw carrier remains unresolved | raw-carrier relation | `Candidate` | keeps the current sample honest about what is still missing | blocks any claim of confirmed field-to-field relation truth |
| reverse-lane relation beyond the head-line boundary stays outside this sample | out-of-scope relation | `Deferred` | prevents this sample from silently expanding into broader family mapping | does not mean reverse work is absent or irrelevant |

## SelSaleReport As The Head Object

### Head Position

- relation type: object-position relation
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy sales ledger explicitly writes `_1 + SelSaleReport` as the order-head candidate route
  - legacy route registry records `SelSaleReport` as `sales_documents_head`
  - legacy maturity board keeps `SelSaleReport` in the mainline-ready sales cluster, not in reconciliation-only or snapshot-only roles
- current serving value:
  - gives the second source-intelligence sample line a stable head object
  - keeps order-head discussion anchored on one endpoint object instead of a whole family-wide abstraction
- current risk / unresolved note:
  - this is still a rewritten legacy conclusion
  - current repo has not yet formalized this object position into runtime behavior, contract, or readiness truth

### Why This Position Matters

- `SelSaleReport` carries named head-like fields such as `SaleNum`, `SaleDate`, `OperMan`, `TotalSaleAmount`, `TotalSaleMoney`, and `ReceiveMoney`
- that makes it the cleanest anchor for future order-head relation work
- it also gives the later line-side work a stable sibling object instead of forcing the family to be modeled as one merged route

## SaleNum As The Current Head-Line Join Clue

### `SaleNum` -> line-side normalized `sale_no`

- relation type: head-line join clue
- evidence level: `Supported`
- source evidence / provenance note:
  - `SelSaleReport` raw responses expose `retdata[0].Data[*].SaleNum`
  - legacy line-side grid analysis exposes a line-side `零售单号` field
  - legacy sales ledger explicitly says `SaleNum/零售单号` is the highest-priority head-line join candidate
  - legacy sales evidence chain ranks normalized `sale_no` above `sale_date` and `operator`
- current serving value:
  - this is the single highest-value relation clue for later head-line boundary work
  - it gives future relation or contract work a candidate key to organize around without widening scope to the whole family
- current risk / unresolved note:
  - current repo has not rewritten `SaleNum` -> `零售单号` into a repo-owned formal relation asset
  - the clue is strong, but it is still not current formal relation truth

### Current Relation Strength

- relation type: head-line cardinality clue
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy sales evidence chain reports:
    - `document_overlap_rate = 1.0`
    - `detail_overlap_rate ≈ 0.9276`
    - `relationship = one_to_many`
    - `stable_candidate = true`
  - legacy sales ledger keeps `sale_no` as the only primary join candidate that should continue forward
- current serving value:
  - enough evidence exists to say `SaleNum` is not just a vague clue; it is the strongest current head-line boundary key
  - enough evidence exists to justify keeping head and line as separate grains
- current risk / unresolved note:
  - this still does not prove a future current repo relation contract
  - continuous-batch stability and rewritten semantics remain unclosed

### Non-Primary Join Clues

- relation type: supporting relation clue
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy sales ledger and evidence chain keep `sale_date` and `operator` out of the primary join slot
  - legacy evidence shows they do not have the same stable overlap behavior as `sale_no`
- current serving value:
  - keeps future relation work from over-fitting on weaker context fields
- current risk / unresolved note:
  - they remain supporting context only; they should not be promoted into the primary boundary key

## Boundary With The Line-Side Candidate Object

### Same Family, Different Grain

- relation type: same-page cross-grain boundary
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy page research classifies `销售清单` as `multi_grain_route`
  - legacy sales ledger distinguishes:
    - `_1 + SelSaleReport` as the head candidate route
    - `_2 + GetDIYReportData(E004001008_2)` as the line candidate route
  - legacy route registry records them as different capture roles: `sales_documents_head` vs `sales_document_lines`
- current serving value:
  - this keeps future line-side work inside the same neighborhood while still preventing grain collapse
  - it explains why one dossier and one field dictionary for `SelSaleReport` are not enough to describe the whole family
- current risk / unresolved note:
  - same-page context does not imply same-grain equivalence
  - this sample still does not define a line-side object contract

### Raw Carrier Boundary

- relation type: raw-carrier relation
- evidence level: `Candidate`
- source evidence / provenance note:
  - `SelSaleReport` returns named object rows under `retdata[0].Data[*]`
  - the line-side `GetDIYReportData(E004001008_2)` raw payload still depends on array rows plus grid metadata to recover field meaning
- current serving value:
  - makes a key boundary explicit: head-side named fields are easier to stabilize first than line-side array carriers
- current risk / unresolved note:
  - exact line-side raw path and exact field-to-field mapping remain unresolved in current repo-owned docs
  - this is why the current relation sample stops at boundary strength, not full relation truth

## Boundary With The Reconciliation Object

### `SelDeptSaleList` Is Not The Same Grain

- relation type: grain-boundary relation
- evidence level: `Supported`
- source evidence / provenance note:
  - legacy sales ledger keeps `SelDeptSaleList` as a research/reconciliation source
  - legacy maturity board marks `SelDeptSaleList` as covered and HTTP-verified, but not mainline-ready
  - legacy sales ledger further states `零售明细统计` rows are aggregated wide rows rather than order-head rows
- current serving value:
  - keeps reconciliation rows from being mistaken for either head rows or line rows
  - keeps future order-count or order-money reasoning away from the wrong grain
- current risk / unresolved note:
  - current repo still has not rewritten a dedicated reconciliation dossier
  - this boundary only says “not the same grain”; it does not fully explain the reconciliation object

### Why The Reconciliation Boundary Matters

- if `SelDeptSaleList` were mixed into the head boundary, order-count and amount reasoning would be distorted
- keeping it outside the head-line boundary preserves a narrow and more reusable relation sample

## Deferred Outside This Sample

### Reverse Lane

- relation type: out-of-scope relation
- evidence level: `Deferred`
- source evidence / provenance note:
  - legacy route registry and sales ledger keep `sales_reverse_document_lines` as research-only
- current serving value:
  - prevents this sample from becoming a full sales-family relation map
- current risk / unresolved note:
  - reverse-lane relation still exists as a later neighborhood, but it is not needed to answer the current head-line boundary question

## What This Relation Doc Makes Explicit

这份 relation doc 当前新增了四件明确的 knowledge：

1. `SelSaleReport` 这条第二样板线，已经可以在不扩 whole family map 的前提下进入关系层。
2. `SaleNum` 已经被明确收口成当前最高价值的 head-line join clue，但仍停留在 `Supported`。
3. `SelSaleReport` 与 line-side candidate 的边界已经写清：同 family、同 page line、不同 grain。
4. `SelSaleReport` 与 `SelDeptSaleList` 的 grain boundary 也已经写清：后者仍是 reconciliation object，不应混入 head-line boundary。

## What This Relation Doc Does Not Claim

这份 relation doc 不声称：
- whole `sales list family` relation graph 已完成
- `SaleNum` 已经成为 current formal join rule
- line-side exact field mapping 已经闭合
- readiness judgment 已经成立
- `SelSaleReport` 已经成为 current repo truth
