# Orders-Adjacent Relation Answer Under Rows-Centered Carrier Baseline

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
- `M3-PR6 | docs/plan: answer /erp/orders adjacent relation answer under rows-centered carrier baseline`
- current `/erp/orders` adjacent line 在 `rows`-centered partial carrier baseline 下的 relation answer baseline
- 后续 detail clue / target-scope routing 判断的 planning input

这份文档不做：
- 不改 `README.md`
- 不改 `docs/README.md`
- 不改任何 formal boundary docs
- 不改 runtime / model / schema / crud / service / migration / tests
- 不把 `sales_order_items-adjacent target candidate` 升级成 confirmed first target
- 不把 relation answer 升级成 contract identity
- 不新增 overwrite / upsert key / path / capture ingress / internal entrypoint / behavior readiness
- 不进入 detail clue answer 全包
- 不进入 target-lane exclusion 全包
- 不进入 contract-entry revisit 全包
- 不进入 contract/path/behavior
- 不跳去 inventory、orchestration、operator-facing evidence
- 不把 planning / reference 写成已落地 truth

## Scope

这份文档只回答 current `/erp/orders` adjacent line 的一个问题：

- 在 `rows`-centered partial carrier baseline 下，current repo 最多能把 order-to-detail relation 收口成 `anchor reuse`、`candidate link clue`、还是 `still needs extra source clue` 中的哪一层 repo-owned planning answer

它当前只覆盖：
- current `/erp/orders` `rows` anchor family 作为 formal relation comparison anchor
- current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family 的 relation alternatives
- current repo 内关于 `anchor reuse`、`candidate link clue`、`still needs extra source clue` 的 planning inputs
- downgraded reference candidate lane
- 这一步之后 detail clue / target-scope routing 仍最少缺什么

它当前不覆盖：
- detail clue answer 全包
- target-lane exclusion answer 全包
- contract-entry revisit 全包
- contract identity
- path/read shape
- behavior readiness

## Why This Package Exists

[orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md) 已把 current adjacent carrier 收口到一个 `rows`-centered partial carrier baseline。

[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) 与 [orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md) 又共同明确：
- relation answer 仍未收口
- target candidate 还没有被 carrier / relation / detail clues answers 支撑成 repo-owned mapping answer

因此当前需要一份单独的 planning-only relation answer 文档，
只回答：
- current repo 是否已经能把 relation alternatives 缩窄到一个更小的边界
- 哪些 alternatives 现在仍然并存
- 哪些 evidence 只能继续停留在 downgraded reference candidate
- 这一步之后 detail clue / target-scope routing 仍还缺什么

## Relation Alternatives Currently Under Consideration

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| `anchor reuse` candidate | `formal truth + planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md)；[orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md) | current repo 已能明确：如果 adjacent facts 最终落在 same-row substructure，这条 relation 可能直接复用 current order-level row anchor | 不能推出 current relation 已经是纯 `anchor reuse`；不能推出 `order_id` 已可被写成 final relation key | 还缺 row-internal evidence 或更窄 relation answer，支撑 `anchor reuse` 超过其他 alternatives |
| `candidate link clue` candidate | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md) | current repo 已能明确：如果 adjacent facts 保持在 row-sibling clue lane，relation 可能需要依赖 current row-level clues 作为 candidate link clue，而不是直接复用 same-row substructure | 不能推出 link clue 已经被确认；不能推出 `order_id`、paid-state、optional `store_id` 中任一 clue 已被提升成 relation truth | 还缺更窄的 repo-owned answer，说明哪些 row-level clues 只是 comparison anchor，哪些可继续保留为 candidate link clue |
| `still needs extra source clue` candidate | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md) | current repo 已能明确：由于 `other same-payload carrier` 仍未完全排除，relation answer 仍可能需要额外 source clue 才能成立 | 不能推出 extra source clue 已经存在；不能推出 relation 已经脱离 row-centered comparison baseline | 还缺 repo-owned extract 或更窄 evidence answer，说明 extra clue 仍需保留还是可以继续被压低 |

## Reusable Anchors Already Available

| 可复用输入 | 证据层级 | 当前允许复用成什么 | 当前仍然不能推出什么 |
| --- | --- | --- | --- |
| current `rows` anchor as formal relation baseline | `formal truth + planning` | current relation answer 的 formal comparison anchor | 不能推出 adjacent relation 已经与 current row anchor 等价 |
| current order-level clues (`order_id` / paid-state / optional `store_id`) | `formal truth + planning` | rows-centered relation comparisons；可支撑 `anchor reuse` 与 `candidate link clue` 作为有效 candidates | 不能推出这些 clues 自动成为 relation key、contract identity 或 overwrite key |
| current `rows`-adjacent non-`sales_orders` candidate family | `formal truth + planning` | current relation question 的 scope anchor | 不能推出 candidate family 已经等于 confirmed relation lane |
| current `rows`-centered partial carrier answer | `planning` | relation answer 的上游 baseline；可把 relation 缩窄到 rows-centered neighborhood 内讨论 | 不能单独推出哪一种 relation alternative 已经成立 |
| downstream `sales_order_items` persistence surface | `formal truth + planning` | 只作为 target-neighborhood / vocabulary 邻接线索 | 不能反推 relation answer |

## Current Relation Answer Status

| question | 证据层级 | 当前 repo 证据 | 当前结论 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- | --- |
| current repo 是否已确认 relation answer | `planning` | [orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md)；[orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md) | `relation answer still partial` | current repo 已能明确：relation 仍未确认 | 不能推出 confirmed relation answer；不能推出 contract identity 或 path/read shape 已确认 | 还缺更窄的 repo-owned relation answer |
| current repo 是否已形成 rows-centered partial relation narrowing | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)；[orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md) | `已形成 partial relation answer` | current repo 已足以把 relation 收口到一个 `rows`-centered order-attached comparison neighborhood：`anchor reuse` 与 `candidate link clue` 是一阶候选；`still needs extra source clue` 仍只保留为 residual alternative | 不能推出 residual alternative 已被排除；不能推出一阶候选中哪一个已成立 | 还缺明确排除主要 alternatives 的 repo-owned answer |
| `still needs extra source clue` 是否已被排除 | `planning` | [orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | `not yet excluded` | current repo 只足以把它降为 residual relation alternative，而不是 first-order rows-centered candidate | 不能推出 extra source clue 已经不再需要；不能推出当前 relation 已经可以脱离 residual alternative | 还缺 repo-owned extract 或更窄 relation evidence answer，支撑继续保留或正式排除 |

## Alternatives Not Yet Excluded

| alternative | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| `anchor reuse` | `formal truth + planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md) | 当前 repo 仍把它保留为 first-order candidate | 不能推出 current relation 已经只靠 current row anchor 即可成立 | 还缺 row-internal relation evidence 或排除 answer |
| `candidate link clue` | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md) | 当前 repo 仍把它保留为 first-order candidate，且它有 current row-level clues 作为 comparison baseline | 不能推出哪条 clue 已经成为 confirmed link clue | 还缺更窄的 clue-role answer 或排除 answer |
| `still needs extra source clue` | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md) | 当前 repo 仍未把它完全排除，但已将其压低为 residual alternative | 不能推出存在某个 concrete extra source clue；不能推出无需额外 clue | 还缺 repo-owned extract 或显式 exclusion answer |

## Downgraded Reference Candidates

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| orders-adjacent external relation hint lane | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md)；当前 repo 无 orders-specific relation extract | 当前 repo 只足以说明：如果后续要消费外部 relation hints，它们必须先被降级标注，再重写成 repo-owned planning answer | 不能推出 current repo 已有可复用的 orders-adjacent relation extract | 还缺 orders-specific downgraded extract，或继续显式保持无 extract 状态 |

## What Still Cannot Be Concluded

在这份 relation answer baseline 之后，当前 repo 仍然不能推出：

- confirmed relation answer
- confirmed first target
- contract identity
- path/read shape
- behavior readiness
- current `/erp/orders` adjacent line 已经 contract-entry ready

这些结论之所以仍然不能推出，是因为：
- current relation answer 仍然是 partial answer
- `anchor reuse` 与 `candidate link clue` 仍并存
- `still needs extra source clue` 仍未被完全排除
- source-side detail clue answer 仍未收口
- target-scope routing 仍需要 relation answer 的进一步支撑

## Downstream Routing After This Relation Answer

这份 package 之后，current `/erp/orders` adjacent line 至少已经明确：

1. current relation answer 现在最多只能收口到：
   - `rows`-centered order-attached comparison neighborhood
   - 其中 `anchor reuse` 与 `candidate link clue` 仍是并存的一阶候选
   - `still needs extra source clue` 仍是未完全排除的 residual alternative
2. 因此后续 detail clue answer 仍最少缺：
   - 哪些 clues 在 rows-centered relation neighborhood 内已有 repo-owned source-side evidence
3. 后续 target-scope routing 仍最少缺：
   - 为什么 `sales_order_items-adjacent target candidate` 在 partial relation status 下仍只是 candidate，而不是 target truth
4. 当前仍不应进入：
   - contract/path/behavior
   - confirmed target naming
   - contract identity
5. 做完这包后，不应默认继续机械拆小包：
   - 必须先重新评估剩余 blocker 的边际收益
   - 再决定是继续停留在 `M3`，还是进入 `M4-PR1` 的 contract-prep 预检

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

它当前不替代：
- source-evidence baseline
- source-accuracy revisit baseline
- single-target mapping minimums baseline
- primary carrier answer baseline
- detail clue answer baseline
- formal contract docs
- formal path docs

当前 `/erp/orders` adjacent source-side detail clue answer baseline 另行维护在：
- [orders-adjacent-detail-clue-answer.md](./orders-adjacent-detail-clue-answer.md)
