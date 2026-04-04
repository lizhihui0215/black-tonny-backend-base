# Orders-Adjacent Source-Side Detail Clue Answer Under Rows-Centered Relation Baseline

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
- `M3-PR7 | docs/plan: answer /erp/orders adjacent source-side detail clue answer under rows-centered relation baseline`
- current `/erp/orders` adjacent line 在 `rows`-centered partial carrier + partial relation baseline 下的 source-side detail clue answer baseline
- 后续 target-scope routing 判断的 planning input

这份文档不做：
- 不改 `README.md`
- 不改 `docs/README.md`
- 不改任何 formal boundary docs
- 不改 runtime / model / schema / crud / service / migration / tests
- 不把 `sales_order_items-adjacent target candidate` 升级成 confirmed first target
- 不把 detail clue answer 升级成 contract identity
- 不新增 overwrite / upsert key / path / capture ingress / internal entrypoint / behavior readiness
- 不进入 target-lane exclusion 全包
- 不进入 contract-entry revisit 全包
- 不进入 contract-prep / contract / path / behavior
- 不跳去 inventory、orchestration、operator-facing evidence
- 不把 planning / reference 写成已落地 truth

## Scope

这份文档只回答 current `/erp/orders` adjacent line 的一个问题：

- 在 `rows`-centered partial carrier + partial relation baseline 下，current repo 最多能把 source-side detail clue 收口成哪一层 repo-owned planning answer

它当前只覆盖：
- current `/erp/orders` `rows` anchor family 作为 formal comparison anchor
- current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family
- current order-level clues 作为非 detail 的 relation / anchor baseline
- current `sales_order_items` persistence surface 暴露出的 downstream detail vocabulary
- rows-centered relation neighborhood 内的 detail clue candidates
- downgraded reference candidate lane
- 这一步之后 target-scope routing 仍最少缺什么

它当前不覆盖：
- target-lane exclusion 全包
- contract-entry revisit 全包
- contract identity
- path/read shape
- behavior readiness

## Why This Package Exists

[orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md) 已把 current relation 收口到一个 `rows`-centered order-attached comparison neighborhood，
但它同时明确保留：
- `anchor reuse`
- `candidate link clue`
- `still needs extra source clue`

这三类 relation alternatives 并存时，
[orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md) 仍只能把 current target lane 写成：
- `sales_order_items-adjacent target candidate`

原因之一正是：
- source-side detail clue answer 仍未收口
- downstream vocabulary demotion 虽然已经存在，但 repo-owned 的 detail clue answer 还没有单独落成 baseline

因此当前需要一份单独的 planning-only detail clue answer 文档，
只回答：
- 哪些 clue candidates 现在仍然并存
- 哪些 naming 仍只是 downstream vocabulary
- 哪些证据只能继续停留在 downgraded reference candidate
- 这一步之后 target-scope routing 仍还缺什么

## Detail Clue Candidates Currently Under Consideration

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| `detail-attribute cluster candidate` (`sku/style/color/size`-adjacent naming neighborhood) | `planning` with formal vocabulary anchor | [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md)；`src/app/models/sales_order_item.py` | current repo 已能明确：如果 source-side detail clues 存在，最值得继续核对的一类 clue family 是一组 order-attached detail-attribute naming neighborhood，并且它只允许被保守写成 source-side candidate clue cluster | 不能推出 source payload 中已经存在 `sku_id` / `style_code` / `color_code` / `size_code` 同名字段；不能推出 attribute semantics 已确认 | 还缺 repo-owned source-side evidence，说明这组 naming neighborhood 中哪些 clues 真有 source-side anchor、哪些仍只是 downstream vocabulary |
| `quantity-like clue candidate` | `planning` with formal vocabulary anchor | [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md)；`src/app/models/sales_order_item.py` | current repo 已能明确：如果 source-side detail clues 存在，`quantity` 只允许被保守保留为 order-attached quantity-like candidate，而不是已确认 source semantics | 不能推出 source payload 一定存在 quantity-like field；不能推出 quantity 口径、单位或净额/件数含义已确认 | 还缺 repo-owned source-side evidence，说明 quantity-like clue 是否真实存在，以及它与 attribute cluster 是否同载于一组 source-side detail clues |
| `downstream vocabulary only` lane | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md)；[orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md) | current repo 已能明确：`sku/style/color/size/quantity` 目前只能作为 downstream comparison vocabulary，而不是 current source-side detail clue answer | 不能推出 vocabulary naming 本身已经等于 source-side clue existence；不能推出它已经足够支撑 target truth | 还缺一个更窄的 repo-owned answer，把 vocabulary-only naming 与 source-side candidate clue cluster 继续分开写 |
| `still needs extra source-side clue` residual alternative | `planning` | [orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | current repo 已能明确：即使 rows-centered relation neighborhood 已经形成，detail clue 仍可能需要额外 source-side evidence 才能成立 | 不能推出额外 source-side clue 已存在；不能推出 current rows-centered neighborhood 已足以关闭 detail clue gap | 还缺 repo-owned clue answer，用于继续保留或正式压低这条 residual alternative |

## Reusable Anchors Already Available

| 可复用输入 | 证据层级 | 当前允许复用成什么 | 当前仍然不能推出什么 |
| --- | --- | --- | --- |
| current `rows` anchor as formal comparison baseline | `formal truth + planning` | current detail clue answer 的 formal comparison anchor | 不能推出 adjacent detail clues 与 current row anchor 为同一 source-side structure |
| current order-level clues (`order_id` / paid-state / optional `store_id`) | `formal truth + planning` | rows-centered relation / comparison anchors；可帮助区分哪些 clues 仍是 order-level anchors，而不是 detail clues | 不能推出这些 clues 自动成为 detail clue、target identity 或 overwrite key |
| current `rows`-centered partial carrier + partial relation baseline | `planning` | current detail clue question 的上游 baseline；可把 clue 讨论限制在 order-attached comparison neighborhood 内 | 不能单独推出任何 concrete detail clue 已成立 |
| downstream `sales_order_items` persistence surface | `formal truth + planning` | downstream naming neighborhood / vocabulary demotion baseline | 不能反推 source payload 中已存在对应 detail clue |
| current `rows`-adjacent non-`sales_orders` candidate family | `formal truth + planning` | current detail clue question 的 scope anchor | 不能推出 candidate family 已经等于 confirmed detail lane |

## Current Detail Clue Answer Status

| question | 证据层级 | 当前 repo 证据 | 当前结论 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- | --- |
| current repo 是否已确认 source-side detail clue answer | `planning` | [orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md)；[orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md) | `detail clue answer still partial` | current repo 已能明确：detail clue answer 仍未确认 | 不能推出 confirmed detail clue answer；不能推出 confirmed first target | 还缺更窄的 repo-owned detail clue answer |
| current repo 是否已形成 rows-centered partial detail clue narrowing | `formal truth + planning` | [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md)；`src/app/models/sales_order_item.py` | `已形成 partial detail clue answer` | current repo 已足以把 detail clue question 收口到一个 rows-centered order-attached comparison neighborhood：`detail-attribute cluster candidate` 与 `quantity-like clue candidate` 可被保留为 source-side candidates，而 `sku/style/color/size/quantity` 仍是 vocabulary-only naming neighborhood | 不能推出两类 candidates 中任一已被 source-side 证明；不能推出 residual alternative 已被排除 | 还缺能排除主要 clue alternatives 的 repo-owned answer |
| current named detail vocabulary 是否仍是 vocabulary-only | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | `still vocabulary-only, not source-side answer` | current repo 已能明确：`sku/style/color/size/quantity` 的当前身份仍是 downstream vocabulary | 不能推出 source-side 同名字段已存在；不能推出 naming match 已经发生 | 还缺 source-side evidence，说明哪些 clues 能从 vocabulary-only 升为 source-side candidate answer |
| `still needs extra source-side clue` 是否已被排除 | `planning` | [orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | `not yet excluded` | current repo 只足以把它压低为 residual alternative，而不是 first-order rows-centered clue candidate | 不能推出 current rows-centered neighborhood 已经足以关闭 detail clue gap | 还缺 repo-owned extract 或更窄 clue answer，支撑继续保留或正式压低 |

## Clues That Are Still Only Downstream Vocabulary

| clue / naming lane | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| `sku_id` | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | 当前 repo 只足以把它当作 downstream comparison vocabulary | 不能推出 source payload 中已存在 `sku_id` clue；不能推出它已是 source-side primary detail clue | 还缺 source-side evidence 或显式保持无 evidence 状态 |
| `style_code` / `color_code` / `size_code` | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | 当前 repo 只足以把这组 naming 保留为 detail-attribute vocabulary cluster | 不能推出 source side 存在同名 attribute clues；不能推出 attribute grouping 已确认 | 还缺 source-side evidence，说明这组 naming 里是否存在真实 attribute clue cluster |
| `quantity` | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | 当前 repo 只足以把它保留为 quantity-like downstream vocabulary | 不能推出 source side 存在 quantity-like clue；不能推出 quantity semantics、单位或聚合口径 | 还缺 source-side evidence，说明 quantity-like clue 是否真实存在 |

## Downgraded Reference Candidates

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| orders-adjacent external detail clue hint lane | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md)；当前 repo 无 orders-specific detail clue extract | 当前 repo 只足以说明：如果后续要消费 external detail clue hints，它们必须先被降级标注，再重写成 repo-owned planning answer | 不能推出 current repo 已有可复用的 orders-adjacent detail clue extract | 还缺 orders-specific downgraded extract，或继续显式保持无 extract 状态 |

## Evidence Gaps Still Not Closed

| gap / blocker | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| source-side clue existence gap | `planning` | [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | 当前 repo 只能稳定表达：detail clue answer 仍未确认 | 不能推出哪组 source-side detail clues 已真实存在 | 还缺一个更窄的 repo-owned answer，说明哪些 clue candidates 真有 source-side evidence |
| vocabulary-to-source promotion gap | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | 当前 repo 已能稳定表达 vocabulary demotion | 不能推出任何 named clue 已能从 vocabulary-only 升为 source-side answer | 还缺 source-side evidence，把 vocabulary-only lane 与 source-side candidate lane 分开写清 |
| repo-local downgraded reference extract gap | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md) | 当前 repo 只能说明 reference lane 可用，但仍无 orders-specific detail clue extract | 不能推出 reference 候选已经进入 current repo-owned planning | 还缺真正进入 repo 的 downgraded candidate extract，或继续显式保持无 extract 状态 |

## What Still Cannot Be Concluded

在这份 detail clue answer baseline 之后，当前 repo 仍然不能推出：

- confirmed detail clue answer
- confirmed first target
- contract identity
- path/read shape
- behavior readiness
- current `/erp/orders` adjacent line 已经 contract-entry ready

这些结论之所以仍然不能推出，是因为：
- current detail clue answer 仍然是 partial answer
- `detail-attribute cluster candidate` 与 `quantity-like clue candidate` 仍只是 source-side candidates
- `sku/style/color/size/quantity` 仍只停留在 downstream vocabulary
- `still needs extra source-side clue` 仍未被完全排除
- target-scope routing 仍需要 detail clue answer 之后的阶段路由判断

## Downstream Routing After This Detail Clue Answer

这份 package 之后，current `/erp/orders` adjacent line 至少已经明确：

1. current detail clue answer 现在最多只能收口到：
   - `rows`-centered order-attached detail-clue comparison neighborhood
   - 其中 `detail-attribute cluster candidate` 与 `quantity-like clue candidate` 仍是并存的 source-side candidates
   - `sku/style/color/size/quantity` 仍只是 downstream vocabulary-only naming neighborhood
2. 因此后续 target-scope routing 仍最少缺：
   - 当前剩余 blocker 的阶段收益复核
   - 以及是否还需要一个更高收益的 `M3` 收口包，还是已经足够进入 `M4-PR1` 的 contract-prep 预检
3. 当前仍不应进入：
   - confirmed target naming
   - contract identity
   - contract/path/behavior
4. 做完这包后，不应默认继续机械拆更多小包：
   - 必须先重新评估剩余 blocker 的边际收益
   - 再决定是继续停留在 `M3`，还是进入 `M4-PR1`

## Relationship To Other Planning Docs

这份文档当前位于以下 planning docs 之后：
- [source-surface-completeness-map.md](./source-surface-completeness-map.md)
- [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)
- [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)
- [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)
- [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)
- [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)
- [orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md)
- [orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md)
- [orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md)
- [orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md)

它当前不替代：
- source-evidence baseline
- source-accuracy revisit baseline
- single-target mapping minimums baseline
- primary carrier answer baseline
- relation answer baseline
- target-lane exclusion baseline
- formal contract docs
- formal path docs
