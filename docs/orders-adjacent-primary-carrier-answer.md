# Orders-Adjacent Primary Carrier Answer

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
- `M3-PR5 | docs/plan: answer /erp/orders adjacent primary carrier answer`
- current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family 的 primary carrier answer baseline
- 后续 relation answer / detail clue answer / target-scope routing 的 planning input

这份文档不做：
- 不改 `README.md`
- 不改 `docs/README.md`
- 不改任何 formal boundary docs
- 不改 runtime / model / schema / crud / service / migration / tests
- 不把 `sales_order_items-adjacent target candidate` 升级成 confirmed first target
- 不进入 contract identity / path / behavior
- 不新增 overwrite / upsert key / capture ingress / internal entrypoint / behavior readiness
- 不把 relation answer、detail clue answer、target-lane exclusion、contract-entry revisit 混成一个大包
- 不跳去 inventory、orchestration、operator-facing evidence
- 不把 planning / reference 写成已落地 truth

## Scope

这份文档只回答 current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family 的一个问题：

- 在 `same-row substructure`、`row-sibling clue lane`、`other same-payload carrier` 之间，current repo 最多能把哪一层 carrier boundary 收口成 repo-owned planning answer

它当前只覆盖：
- current `/erp/orders` `rows` anchor family 作为 formal carrier anchor
- current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family 的 carrier alternatives
- current repo 内关于 `same-row substructure`、`row-sibling clue lane`、`other same-payload carrier` 的 planning inputs
- downgraded reference candidate lane
- 这一步之后 relation / detail clue / target-scope routing 仍最少缺什么

它当前不覆盖：
- relation answer
- source-side detail clue answer
- target-lane exclusion answer
- contract identity
- path/read shape
- behavior readiness

## Why This Package Exists

[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) 已明确：
- current source-carrier minimum 仍未满足
- `primary adjacent carrier answer gap` 仍是 current `/erp/orders` adjacent line 的第一类 blocker

[orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md) 又进一步明确：
- current `single-target mapping minimum` 仍未满足
- target candidate 还没有被 source-carrier / relation / detail clues answers 支撑成 repo-owned mapping answer

因此当前需要一份单独的 planning-only carrier answer 文档，
只回答：
- current repo 是否已经能把 carrier alternatives 缩窄到一个更小的边界
- 哪些 alternatives 现在仍然并存
- 哪些 evidence 只能继续停留在 downgraded reference candidate
- 这一步之后 relation / detail clue / target-scope routing 仍还缺什么

## Carrier Alternatives Currently Under Consideration

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| `same-row substructure` candidate | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | current repo 已能明确：如果 adjacent candidate 直接附着在 current order-level row 内部，这会是一条与 current `rows` anchor 最贴近的 carrier 候选 | 不能推出 row 内一定存在 nested detail substructure；不能推出它已经是 confirmed primary carrier | 还缺一个 repo-owned carrier answer，证明 row 内确有 adjacent facts 或至少排除主要竞争 alternatives |
| `row-sibling clue lane` candidate | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | current repo 已能明确：current formal row anchor 与 order-level clues 已存在，因此 adjacent candidate 也可能继续停留在同一 row-level clue lane，而不是 nested row internals | 不能推出 row sibling detail clues 已存在；不能推出 current order-level clues 自动承担 adjacent carrier 角色 | 还缺一个更窄的 repo-owned answer，说明 row-level sibling lane 为什么比其他 alternatives 更可复查 |
| `other same-payload carrier` candidate | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md) | current repo 已能明确：除 row-centered lanes 外，仍保留一条 residual same-payload carrier alternative | 不能推出这个 alternative 已被排除；不能推出它已经对应某个被命名的 concrete carrier | 还缺 repo-owned extract 或更窄 planning answer，说明 residual same-payload alternative 是否仍需保留 |

## Reusable Anchors Already Available

| 可复用输入 | 证据层级 | 当前允许复用成什么 | 当前仍然不能推出什么 |
| --- | --- | --- | --- |
| current `rows` anchor as formal carrier baseline | `formal truth + planning` | current primary carrier answer 的 formal comparison anchor | 不能推出 adjacent candidate 与 `rows` anchor 为同一 carrier |
| current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family | `formal truth + planning` | current carrier question 的 scope anchor | 不能推出 candidate family 已经等于 confirmed carrier lane |
| current order-level clues (`order_id` / paid-state / optional `store_id`) | `formal truth + planning` | row-centered carrier comparisons；可支撑 `row-sibling clue lane` 作为有效候选 | 不能推出这些 clues 自动成为 relation key、carrier truth 或 contract identity |
| envelope-level blank exclusion | `planning` | 排除 envelope-level family 被顺手并入 current carrier answer | 不能推出 `other same-payload carrier` 已经被完全排除 |
| downstream `sales_order_items` persistence surface | `formal truth + planning` | 只作为 target-neighborhood / vocabulary 邻接线索 | 不能反推 source-side carrier |

## Current Carrier Answer Status

| question | 证据层级 | 当前 repo 证据 | 当前结论 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- | --- |
| current repo 是否已确认 primary carrier | `planning` | [orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md)；[orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md) | `carrier answer still partial` | current repo 已能明确：primary carrier 仍未确认 | 不能推出 confirmed primary carrier；不能推出 path/read shape 已确认 | 还缺更窄的 repo-owned carrier answer |
| current repo 是否已形成 rows-centered partial carrier narrowing | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | `已形成 partial carrier answer` | current repo 已足以把 current adjacent candidate 收口到一个 `rows`-centered comparison neighborhood：`same-row substructure` 与 `row-sibling clue lane` 是一阶候选；`other same-payload carrier` 仍只保留为 residual alternative | 不能推出 residual alternative 已被排除；不能推出一阶候选中哪一个已成立 | 还缺明确排除主要 alternatives 的 repo-owned answer |
| `other same-payload carrier` 是否已被排除 | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | `not yet excluded` | current repo 只足以把它降为 residual same-payload alternative，而不是 first-order row-centered candidate | 不能推出它已经被完全排除；不能推出它已经具备独立 carrier evidence | 还缺 repo-owned extract 或更窄 evidence answer，支撑继续保留或正式排除 |

## Alternatives Not Yet Excluded

| alternative | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| `same-row substructure` | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | 当前 repo 仍把它保留为 first-order candidate | 不能推出 nested row internals 已存在 | 还缺 row-internal evidence 或排除 answer |
| `row-sibling clue lane` | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | 当前 repo 仍把它保留为 first-order candidate，且它有 current row-level anchor 可作为 comparison baseline | 不能推出 row sibling clues 已经足够形成 source-side carrier answer | 还缺 row-level sibling evidence 或排除 answer |
| `other same-payload carrier` | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md) | 当前 repo 仍未把它完全排除，但已将其压低为 residual alternative | 不能推出存在某个 concrete same-payload carrier family | 还缺 repo-owned extract 或显式 exclusion answer |

## Downgraded Reference Candidates

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若要继续进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| orders-adjacent external carrier hint lane | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md)；当前 repo 无 orders-specific carrier extract | 当前 repo 只足以说明：如果后续要消费外部 carrier hints，它们必须先被降级标注，再重写成 repo-owned planning answer | 不能推出 current repo 已有可复用的 orders-adjacent carrier extract | 还缺 orders-specific downgraded extract，或继续显式保持无 extract 状态 |

## What Still Cannot Be Concluded

在这份 primary carrier answer baseline 之后，当前 repo 仍然不能推出：

- confirmed primary carrier
- confirmed first target
- contract identity
- path/read shape
- behavior readiness
- current `/erp/orders` adjacent line 已经 contract-entry ready

这些结论之所以仍然不能推出，是因为：
- current carrier answer 仍然是 partial answer
- `same-row substructure` 与 `row-sibling clue lane` 仍并存
- `other same-payload carrier` 仍未被完全排除
- relation answer 仍未收口
- source-side detail clue answer 仍未收口
- target-scope routing 仍需要 carrier answer 的进一步支撑

## Downstream Routing After This Carrier Answer

这份 package 之后，current `/erp/orders` adjacent line 至少已经明确：

1. current primary carrier answer 现在最多只能收口到：
   - `rows`-centered comparison neighborhood
   - 其中 `same-row substructure` 与 `row-sibling clue lane` 仍是并存的一阶候选
   - `other same-payload carrier` 仍是未完全排除的 residual alternative
2. 因此后续 relation answer 仍最少缺：
   - carrier 再缩窄一级，或明确说明 relation answer 如何在 partial carrier status 下继续书写
3. 后续 source-side detail clue answer 仍最少缺：
   - 哪些 clues 与 row-centered carrier neighborhood 有 repo-owned source-side evidence
4. 后续 target-scope routing 仍最少缺：
   - 为什么 `sales_order_items-adjacent target candidate` 在 partial carrier status 下仍只是 candidate，而不是 target truth
5. 当前仍不应进入：
   - contract/path/behavior
   - confirmed target naming
   - contract identity

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

它当前不替代：
- source-evidence baseline
- source-accuracy revisit baseline
- single-target mapping minimums baseline
- relation answer baseline
- detail clue answer baseline
- formal contract docs
- formal path docs

当前 `/erp/orders` adjacent relation answer baseline 另行维护在：
- [orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md)
