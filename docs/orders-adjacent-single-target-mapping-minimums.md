# Orders-Adjacent Single-Target Mapping Minimums

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
- `M3-PR4 | docs/plan: answer /erp/orders adjacent single-target mapping minimums`
- current `/erp/orders` first adjacent package 的 single-target mapping minimums baseline
- 后续 adjacent contract-entry routing 判断的 planning input

这份文档不做：
- 不改 `README.md`
- 不改 `docs/README.md`
- 不改任何 formal boundary docs
- 不改 runtime / model / schema / crud / service / migration / tests
- 不把 `sales_order_items` 写成已确认 first adjacent target
- 不把 candidate mapping 直接升级成 single-target truth
- 不把 candidate mapping 直接升级成 contract identity
- 不新增 overwrite / upsert key / path / capture ingress / internal entrypoint / behavior readiness
- 不进入 contract/path/behavior
- 不跳去 inventory、orchestration、operator-facing evidence
- 不新增 accuracy matrix、checksum、page completeness、cross-table / cross-slice reconciliation
- 不把 planning / reference 写成已落地 truth

## Scope

这份文档只回答 current `/erp/orders` first adjacent package 的一个问题：

- 在不确认 contract identity 的前提下，current repo 是否已经足够把 first adjacent package 收口成一个 narrow downstream target slice

它当前只覆盖：
- current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family
- `single-theme / narrow target slice` 规则
- `sales_order_items` persistence surface 与 detail vocabulary 的 target-neighborhood 作用
- current source-accuracy blockers 对 target scope 的影响
- open ambiguity / downgraded reference candidate 对 mapping minimum 的影响

它当前不覆盖：
- inventory line
- capture ingress
- contract identity / overwrite / upsert
- runtime/internal entrypoint
- contract/path/behavior
- broader orchestration / retry / reservation / locking

## Why This Package Exists

[orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md) 已把 `single-target mapping minimum` 列为 current `/erp/orders` first adjacent package 的显式前置条件。

[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) 又把这个问题收口成 source-accuracy gate 的第四类 minimum。

[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) 则进一步明确：
- current repo 仍不能推出 single-target mapping 已定稿
- current repo 仍不能推出 `sales_order_items` 已确定为 first adjacent target

因此当前需要一份单独的 planning-only baseline，
只回答：
- current target lanes 里，哪些只是 mapping candidate
- 哪些 planning inputs 已足以支持 `single-theme / narrow target slice` 判断
- 哪些 blocker 仍然阻止 mapping minimum satisfaction
- current contract-entry routing 还不能跨过哪些边界

## Current Mapping Status Summary

| question | 证据层级 | 当前 repo 证据 | 当前结论 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- | --- |
| `single-theme / narrow target slice` 规则是否存在 | `planning` | [clean-mainline-charter.md](./clean-mainline-charter.md)；[orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md) | `已形成 planning-level answer` | current repo 已明确：first adjacent package 必须保持单主题、单 family、单 target slice | 不能仅凭规则存在就推出 target slice 已被确认 | 还缺一份更窄的 target-lane answer，把“哪一个 target lane 正在被候选”写清 |
| current `/erp/orders` 是否已有一个 narrow downstream target neighborhood | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md) | `已有部分 planning-level answer` | current repo 已暴露一个最明显的 downstream neighborhood：`sales_order_items`-adjacent lane | 不能推出这个 neighborhood 已经等于 first adjacent target truth | 还缺 source-carrier / relation / detail clue 三类 answers，支撑它从 candidate 进入 repo-owned mapping answer |
| current `single-target mapping minimum` 是否已满足 | `planning` | [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | `mapping minimum not yet satisfied` | current repo 只足以把 first adjacent package 收口为一个 target-scope question，而不是 target truth | 不能推出 `sales_order_items` 已确认为 first adjacent target；不能推出 contract-entry ready | 还缺更窄的 repo-owned carrier / relation / detail clue answers，以及 target-lane exclusion answer |

## Current Target Lanes Under Consideration

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| `sales_order_items`-adjacent target candidate | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | current repo 已足以说明：在已 landed 的 downstream surfaces 里，只有一条与 current `/erp/orders` adjacent line 明显邻接、且足够窄的 target neighborhood 候选 | 不能推出它已经是 confirmed first adjacent target；不能推出这个 candidate 已经具有 contract identity | 还缺一份 repo-owned mapping answer，说明为什么 current adjacent candidate 只服务这个 narrow target lane，而不是更宽的 mixed lane |
| broader order-detail mixed lane | `planning` | [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) | current repo 已能明确：如果 first adjacent package 同时承接多条 detail slices，就会违反 `single-theme / narrow target slice` 规则 | 不能推出 mixed lane 可作为 first adjacent package 的 target scope | 继续把它保持为 not-yet-allowed shape，不在本包里扩写其内部对象 |
| payload-envelope-adjacent lane | `planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | current repo 已能明确：envelope-level blank 仍是 exclusion，不属于 current first adjacent target-lane 候选 | 不能推出 envelope-level metadata family 存在或不存在；不能推出它可与 first adjacent package 合包 | 继续保持 exclusion，而不是把它提升为 target lane |
| inventory-connected lane | `planning` | [clean-mainline-charter.md](./clean-mainline-charter.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) | current repo 已能明确：inventory line 当前仍不应进入 `/erp/orders` first adjacent package 的 target-scope 判断 | 不能推出 inventory-connected slice 可作为 same-package target lane | 继续保持 explicit exclusion |

## Reusable Planning Inputs Already Available

| 可复用输入 | 证据层级 | 当前允许复用成什么 | 当前仍然不能推出什么 |
| --- | --- | --- | --- |
| current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family | `formal truth + planning` | current first adjacent package 的 scope anchor | 不能推出 candidate family 已经等于 target truth |
| current `sales_order_items` persistence surface | `formal truth` | downstream target-neighborhood clue；可用于说明 repo 内存在一条 item-like downstream slice | 不能反推 source-side carrier、relation、detail clue 或 contract identity |
| detail vocabulary (`sku_id` / `style_code` / `color_code` / `size_code` / `quantity`) | `formal truth + planning` | downstream persistence vocabulary；可用于说明当前 target candidate 的命名邻接 | 不能推出 source payload 具有同名字段；不能推出 target truth 已被确认 |
| `single-theme / narrow target slice` 规则 | `planning` | first adjacent package 的 routing discipline | 不能单独证明哪个 target lane 已经成立 |
| source-accuracy revisit baseline | `planning` | 当前 source-accuracy blockers 的最新 repo-owned cross-check 输入 | 不能把未满足的 carrier / relation / detail clue minimums 自动视为已经收口 |

## Target-Scope Candidates

| candidate | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| `sales_order_items-adjacent target candidate` | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | 当前 repo 已足以把它命名为一个 `target scope candidate`：它与 current order-attached detail facts candidate、detail vocabulary、下游 persistence surface 形成稳定邻接 | 不能推出它已被确认是 first adjacent target；不能推出 `sales_order_items-adjacent target candidate` 与 future contract identity 等价 | 还缺一份 repo-owned narrow-scope answer，说明这条 candidate lane 之所以被保留，是因为它是 current repo 中唯一不违反 single-theme 的 target candidate |
| `downstream vocabulary only` lane | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | 当前 repo 已能明确：`sku/style/color/size/quantity` 目前只能作为 downstream vocabulary，而不是 target truth | 不能推出 vocabulary lane 本身已经等于 target-lane answer | 还缺 source-side detail clue answer，把 vocabulary demotion 与 target candidate 保持分离 |
| `multi-lane mixed target` candidate | `planning` | [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) | 当前 repo 已能明确：把多个 unresolved lanes 混成 first adjacent package 会破坏 narrow target discipline | 不能推出 mixed target candidate 可以作为 admissible mapping answer | 继续保持 explicit exclusion，不进入 contract-entry routing |

## Blockers That Still Prevent Mapping Minimum Satisfaction

| blocker | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| primary adjacent carrier answer gap | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | 当前 repo 只能命名 carrier alternatives | 不能推出 target candidate 对应的 source-side carrier 已经收口 | 还缺排除主要 carrier alternatives 的 repo-owned answer |
| order-to-detail relation answer gap | `formal truth + planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | 当前 repo 已能明确 relation boundary 仍是 blocker | 不能推出 `order_id` 已是 target lane 的 relation key；不能推出 target scope 与 contract identity 可合并回答 | 还缺一个更窄的 relation answer，说明当前到底是 `anchor reuse`、`candidate link clue` 还是 `仍需额外 source clue` |
| source-side detail clue existence gap | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | 当前 repo 只能把 detail vocabulary 保持为 downstream comparison clue | 不能推出 target candidate 已有足够 source-side detail clue support | 还缺一个更窄的 clue existence / grouping answer |
| target-lane exclusion answer gap | `planning` | [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) | 当前 repo 已要求 first adjacent package 只服务一个 narrow target slice | 不能推出为什么其他 adjacent lanes 现在都不该进入 first package | 还缺一份显式的 repo-owned exclusion answer，说明 envelope / mixed / inventory lanes 为什么继续留在外面 |

## Open Ambiguities / Downgraded Reference Candidates

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| `sales_order_items-adjacent target candidate` vs future contract identity | `planning` | [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) | 当前 repo 已能稳定区分：target candidate 只回答 routing / target-scope，不回答 contract identity | 不能推出 target candidate 命名已经等于 future contract name | 还缺后续 contract-prep / contract package 的独立回答 |
| orders-adjacent external mapping hint lane | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md)；当前 repo 无 orders-specific mapping extract | 当前 repo 只足以说明：如果后续要借外部材料收口 target lane，它必须先降级标注，再重写成 repo-owned planning answer | 不能推出 external hint 已经提供 current target-lane truth | 还缺 orders-specific downgraded extract，或继续显式保持无 extract 状态 |
| downstream vocabulary-to-target ambiguity | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | 当前 repo 已能明确：persistence vocabulary 只提供 target-neighborhood clue | 不能推出 vocabulary 已经足以确认 target scope | 还缺 source-side clue answer 与 target-lane exclusion answer 的组合收口 |

## What Still Cannot Be Concluded

在这份 mapping minimums baseline 之后，当前 repo 仍然不能推出：

- `sales_order_items` 已确认是 first adjacent target
- single-target mapping 已定稿
- contract identity 已确认
- overwrite / upsert key 已确认
- path / internal entrypoint 已确认
- behavior readiness 已确认
- current `/erp/orders` adjacent line 已经 contract-entry ready

这些结论之所以仍然不能推出，是因为：
- current target lane 仍停留在 `sales_order_items-adjacent target candidate`
- source-carrier answer 仍未收口
- order-to-detail relation answer 仍未收口
- source-side detail clue answer 仍未收口
- target-lane exclusion answer 仍未收口

## Downstream Routing After This Package

这份 package 之后，current `/erp/orders` adjacent line 至少已经明确：

1. first adjacent package 必须继续保持：
   - single-theme
   - single family
   - single narrow target slice
2. current repo 中，唯一值得继续保留的 narrow downstream target neighborhood 只有：
   - `sales_order_items-adjacent target candidate`
3. 但 current mapping minimum 仍未满足，
   - 因为 target candidate 还没有被 source-carrier / relation / detail clues answers 支撑成 repo-owned mapping answer
4. 因此后续 contract-entry routing 仍不能直接进入：
   - contract/path/behavior
   - confirmed target naming
   - contract identity
5. 当前更合适的后续包，仍应继续围绕：
   - remaining source-accuracy blockers 的更窄回答
   - 或 contract-entry revisit 所需的 target-lane exclusion answer

## Relationship To Other Planning Docs

这份文档当前位于以下 planning docs 之后：
- [source-surface-completeness-map.md](./source-surface-completeness-map.md)
- [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)
- [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)
- [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)
- [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)
- [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)
- [orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md)

它当前不替代：
- source-accuracy minimums baseline
- source-evidence baseline
- source-accuracy revisit baseline
- contract-entry minimums baseline
- formal contract docs
- formal path docs

