# Orders Source-Accuracy Revisit After Source-Evidence Baseline

状态：planning-only / working document

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../README.md)
- [docs/README.md](./README.md)
- [docs/](./README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

当前 milestone 路线的 authoritative 起点仍然是：
- [clean-mainline-charter.md](./clean-mainline-charter.md)

当前 shared planning vocabulary 仍然以：
- [formal-planning-reference-boundary-and-exploration-taxonomy.md](./formal-planning-reference-boundary-and-exploration-taxonomy.md)
- 为准

这份文档当前服务的是：
- `M3-PR3 | docs/plan: revisit /erp/orders source-accuracy after source-evidence baseline`
- current `/erp/orders` adjacent line 的 source-accuracy revisit / cross-check baseline
- 后续 current `/erp/orders` line 的路由判断输入

这份文档不做：
- 不改 `README.md`
- 不改 `docs/README.md`
- 不改任何 formal boundary docs
- 不改 runtime / model / schema / crud / service / migration / tests
- 不进入 single-target mapping 定稿
- 不把 candidate mapping 直接升级成 single-target truth
- 不新增 contract identity / overwrite / upsert key / path / capture ingress / internal entrypoint
- 不进入 contract/path/behavior
- 不新增 accuracy matrix、checksum、page completeness、cross-table / cross-slice reconciliation
- 不提前进入 inventory line
- 不提前进入 scheduler / orchestration / retry / reservation / locking
- 不把 planning / reference 写成已落地 truth

## Scope

这份文档只回答 current `/erp/orders` adjacent line 的一个问题：

- 在 [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) 已经落地之后，current source-accuracy minimums 现在被回答到了哪一步

它当前只复核：
- current `/erp/orders` `rows` anchor family
- current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family
- `source-carrier`
- `order-to-detail relation`
- `source-side detail clues`
- 这些问题当前对应的 planning-level evidence answers、remaining evidence gaps、remaining open ambiguities、downgraded reference candidates

它当前不复核：
- single-target mapping 定稿
- `sales_order_items` 是否已确定为 first adjacent target
- contract identity
- path/read shape 已确认
- behavior readiness

## Why This Revisit Exists

[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) 先定义了 current `/erp/orders` adjacent line 的 source-accuracy gate。

[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) 再把：
- source-carrier evidence
- order-to-detail attachment evidence
- source-side detail clue evidence

这三类问题先收口成 repo-owned source-evidence baseline。

这两份文档的职责不同：
- source-accuracy minimums 文档负责定义 minimum gate
- source-evidence baseline 文档负责定义 evidence baseline 与 downgrade discipline

因此当前仍需要一份单独的 revisit / cross-check 文档，
回答：
- 哪些 minimum 现在已经有 planning-level evidence answer
- 哪些 minimum 仍未满足
- 哪些对象仍应保持 `evidence gap`、`open ambiguity`、`downgraded reference candidate`
- 当前 revisit 之后仍不能推出什么

## Source-Accuracy Minimums Being Revisited

| minimum / question | 证据层级 | 当前 repo 证据 | 当前 revisit 结论 | 现在最多能说明什么 | 现在仍不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- | --- |
| evidence-provenance minimum | `planning` | [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[formal-planning-reference-boundary-and-exploration-taxonomy.md](./formal-planning-reference-boundary-and-exploration-taxonomy.md) | `已形成 planning-level answer` | current repo 已经有一套 repo-owned provenance / downgrade discipline，可把 `repo-owned evidence answer`、`planning input`、`reference evidence candidate`、`open ambiguity / exclusion` 分开写 | 不能推出任何 reference 材料已经自动升级成 truth | 后续包只需在这套 discipline 下继续补更窄 evidence answers，不必重复定义 provenance 规则 |
| source-carrier accuracy minimum | `formal truth + planning` | [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；`src/app/services/capture_to_sales_orders_path.py`；`tests/test_capture_to_sales_orders_path.py` | `已有部分 planning-level answer，但 minimum 仍未满足` | current repo 已能明确：`rows` anchor 是唯一 formal carrier anchor；adjacent candidate 的主要 carrier alternatives 也已被 repo-owned planning 命名出来 | 不能推出 primary adjacent carrier 已确认；不能推出 path/read shape 已确认 | 至少还缺一个更窄的 repo-owned carrier answer，用于收口 primary carrier 并排除主要替代 carriers |
| order-to-detail relation accuracy minimum | `formal truth + planning` | [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | `已有部分 planning-level answer，但 minimum 仍未满足` | current repo 已能明确：order-level clues 当前只作为 comparison anchor；relation answer 必须与 future contract identity 分开；attachment ambiguity 仍是显式 blocker | 不能推出 `order_id` 已是 relation key；不能推出 attachment shape 已确认；不能推出 relation grain 已确认 | 至少还缺一个更窄的 repo-owned relation answer，用于说明是 `anchor reuse`、`candidate link clue` 还是仍需额外 source clue |
| source-side detail clue accuracy minimum | `planning` with formal vocabulary anchor | [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；`src/app/models/sales_order_item.py` | `已有部分 planning-level answer，但 minimum 仍未满足` | current repo 已能明确：`sales_order_items` surface 只提供 downstream comparison vocabulary，不能反推 source-side detail clue existence 或 semantics | 不能推出 source-side detail clues 已被证明存在；不能推出 `sku/style/color/size/quantity` 已是 current source semantics | 至少还缺一个更窄的 repo-owned answer，用于说明哪些 detail clues 已有 source-side evidence、哪些仍只是 vocabulary 邻接 |
| single-target mapping accuracy minimum | `planning` | [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)；[orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md) | `本包不复核，仍未满足` | current repo 只足以说明 single-target mapping 仍是后续独立问题 | 不能推出 `sales_order_items` 已确定为 first adjacent target；不能推出 target boundary 已经收口 | 后续只有在 source-carrier / relation / detail clues 的更窄答案继续收口后，才适合另开更窄 mapping package |

## Evidence Answers Now Available

### Source-Carrier

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 现在最多能说明什么 | 现在仍不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| current `rows` anchor as formal carrier baseline | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；`src/app/services/capture_to_sales_orders_path.py`；`tests/test_capture_to_sales_orders_path.py` | current repo 已正式证明：top-level `rows` list 是 current `sales_orders` first slice 的唯一 formal carrier anchor | 不能推出 adjacent candidate 与 `rows` anchor 为同一 carrier | 还缺 adjacent candidate 的 primary carrier answer |
| adjacent carrier alternatives as repo-owned planning answer | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | current repo 已能用 repo-owned planning 语言稳定表达：adjacent candidate 目前只在 `same-row substructure`、`row-sibling clue lane`、`other same-payload carrier` 之间竞争 | 不能推出三者之一已经成立 | 还缺排除主要 alternatives 的 evidence answer |

### Order-To-Detail Relation

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 现在最多能说明什么 | 现在仍不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| order-level clues as relation comparison anchors | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | current repo 已能明确：`order_id` 与 paid-state / optional `store_id` clues 当前只服务 relation comparison / anchor reuse 判断 | 不能推出这些 clues 自动成为 relation key 或 contract identity | 还缺 relation answer 的更窄收口 |
| relation-answer shape as repo-owned planning answer | `planning` | [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | current repo 已能明确：relation answer 只能先写成 `anchor reuse`、`candidate link clue` 或 `仍需额外 source clue` | 不能推出当前三者中哪一种已成立 | 还缺可以排除主要替代解释的 repo-owned relation answer |

### Source-Side Detail Clues

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 现在最多能说明什么 | 现在仍不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| downstream vocabulary demotion answer | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | current repo 已能明确：`sku/style/color/size/quantity` 目前只是 downstream comparison vocabulary，不是 current source-side evidence answer | 不能推出 source payload 中存在同名字段；不能推出字段 semantics 已确认 | 还缺 source-side detail clue existence / non-existence 的更窄 evidence answer |
| reference lane downgrade answer | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | current repo 已能明确：任何 future detail clue 外部材料都必须先降级标注，再重写进 planning answer | 不能推出 current repo 已有 orders-specific downgraded detail clue extract | 还缺真实的 repo-owned candidate extract 或继续保持 gap |

## Remaining Evidence Gaps

当前 revisit 之后，仍然没有被满足的 source-accuracy minimums 包括：

| gap / blocker | 证据层级 | 当前 repo 证据 | 现在最多能说明什么 | 现在仍不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| primary adjacent carrier answer gap | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | 当前 repo 只能稳定表达 carrier alternatives baseline | 不能推出 primary carrier 已确认；不能推出 path/read shape 已确认 | 还缺一个排除主要替代 carrier 的 repo-owned answer |
| source-side detail clue existence gap | `planning` | [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | 当前 repo 只能稳定表达 downstream vocabulary demotion | 不能推出哪组 detail clues 已经被 source-side 证明 | 还缺一个更窄的 clue existence / grouping answer |
| repo-local downgraded reference extract gap | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md) | 当前 repo 只能说明 reference lane 可用，但仍无 orders-specific extract | 不能推出 reference 候选已经进入 current repo-owned planning | 还缺真正进入 repo 的 downgraded candidate extract，或继续显式保持无 extract 状态 |

## Remaining Open Ambiguities

当前 revisit 之后，仍应显式保留的 open ambiguities 包括：

| ambiguity | 证据层级 | 当前 repo 证据 | 现在最多能说明什么 | 现在仍不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| order-to-detail attachment ambiguity | `formal truth + planning` | [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | 当前 repo 已能把它稳定保持为显式 ambiguity，并要求 relation answer 与 contract identity 分开 | 不能推出 `order_id` 已是 relation key；不能推出无需额外 source clue | 还缺一个更窄的 relation answer |
| carrier-choice ambiguity among adjacent alternatives | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | 当前 repo 已能稳定命名主要 carrier alternatives | 不能推出哪一种 carrier 已成立 | 还缺更窄 carrier evidence answer |
| envelope-level blank | `planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | 当前 repo 已能稳定保持 envelope-level blank 为 exclusion | 不能推出 envelope-level metadata 存在或不存在 | 仍应保持 exclusion，而不是在本包里继续扩写 |

## Downgraded Reference Candidates

当前 revisit 后，可以明确写成 downgraded reference candidate 状态的只有：

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 现在最多能说明什么 | 现在仍不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| orders-adjacent external evidence lane | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md) | 当前 repo 只足以说明：external lane 可作为 future candidate source，但当前仓库还没有 orders-specific extract | 不能推出 external lane 已经提供 current repo-owned answer | 若后续要消费，必须先把 candidate extract 降级标注并写入 repo-owned planning answer |

## What Still Cannot Be Concluded

在这次 revisit 之后，当前 repo 仍然不能推出：

- single-target mapping 已定稿
- `sales_order_items` 已确定为 first adjacent target
- contract identity 已确认
- path/read shape 已确认
- behavior readiness 已确认
- current `/erp/orders` adjacent line 已经 contract-entry ready

这些结论之所以仍然不能推出，是因为：
- source-carrier minimum 仍未满足
- order-to-detail relation minimum 仍未满足
- source-side detail clue minimum 仍未满足
- single-target mapping 当前仍不在这包范围内

## Downstream Routing After This Revisit

这次 revisit 之后，当前最明确的路由判断是：

1. `source-accuracy` 这条线现在已经有：
   - provenance / downgrade discipline
   - anchor demotion answer
   - vocabulary demotion answer
   - exclusions baseline
2. 但它还没有：
   - primary carrier answer
   - relation answer
   - source-side detail clue answer
3. 因此当前仍不应进入：
   - single-target mapping 定稿
   - contract/path/behavior
4. 当前更合适的下一包，仍应停留在 current `/erp/orders` adjacent line 的 source-accuracy / cross-check lane，
   - 继续把 remaining blockers 收口成更窄的 repo-owned answers
   - 而不是把 evidence baseline 直接升级成 contract-entry ready

## Relationship To Other Planning Docs

这份文档当前位于以下 planning docs 之后：
- [source-surface-completeness-map.md](./source-surface-completeness-map.md)
- [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)
- [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)
- [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)
- [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)
- [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)

它当前不替代：
- source-accuracy minimums baseline
- source-evidence baseline
- contract-entry minimums baseline
- formal contract docs
- formal path docs

当前 `/erp/orders` adjacent single-target mapping minimums baseline 另行维护在：
- [orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md)
