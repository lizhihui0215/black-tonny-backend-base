# Orders First Adjacent Contract-Prep Candidate Scope

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
- `M4-PR3 | docs/plan: shape /erp/orders first adjacent contract-prep candidate scope`
- current `/erp/orders` first adjacent contract-prep package 的 candidate-scope baseline
- 后续更窄 contract docs 的非最终化 planning 输入

这份文档不做：
- 不改 `README.md`
- 不改 `docs/README.md`
- 不改任何 formal boundary docs
- 不改 runtime / model / schema / crud / service / migration / tests
- 不把 `sales_order_items-adjacent target candidate` 升级成 confirmed target
- 不把 candidate mapping / partial answers 升级成 contract identity
- 不新增 overwrite / upsert key / path / capture ingress / internal entrypoint / behavior readiness
- 不进入 formal contract/path/behavior 实现
- 不再写一个纯 meta 的 admissibility / boundary baseline 包
- 不跳去 inventory、orchestration、operator-facing evidence
- 不把 planning / reference 写成已落地 truth

## Scope

这份文档只回答 current `/erp/orders` first adjacent contract-prep package 的一个问题：

- first adjacent contract-prep package 现在应围绕什么 candidate scope 展开

它当前只覆盖：
- current contract-prep package 预备围绕哪个 candidate target / candidate family / candidate question 展开
- 这包允许消费哪些 carry-forward inputs
- 哪些 naming 仍必须保持 non-final
- 哪些 partial answers 允许被带入但不能升级
- 哪些 exclusions 仍必须保持在 scope 外
- 这包允许产出哪些非最终化中间结果
- 这包明确不能提前产出哪些结果

它当前不覆盖：
- confirmed first target
- contract identity
- overwrite / upsert key
- path/read shape
- internal entrypoint
- behavior readiness
- formal contract/path truth

## Candidate Scope Being Shaped

这包当前只把 first adjacent contract-prep package 收口为一个 candidate scope：

1. source-side family scope：
   - current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family
2. downstream target scope：
   - `sales_order_items-adjacent target candidate`
3. package question scope：
   - 如何把 current adjacent line 的 candidate target、candidate family 与 current partial source-accuracy answers 组织成一条可继续收窄的 contract-prep question

这包当前不把上述 scope 升级成：
- confirmed first target
- contract identity
- formal contract package truth

## Carry-Forward Inputs Used By This Package

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入下一包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| current `rows` anchor family | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md) | current repo 已正式证明：top-level `rows` list 仍是 current `/erp/orders` line 唯一 formal anchor | 不能推出 adjacent candidate 与 current row anchor 为同一 contract carrier | 下一包只允许继续把它当作 formal comparison anchor |
| current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family | `formal truth + planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | current repo 已足以说明：candidate scope 应只围绕这一条 adjacent family 展开 | 不能推出 candidate family 已被确认命名成 target truth | 下一包仍只能把它当作 candidate family |
| `sales_order_items-adjacent target candidate` | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md)；[orders-first-adjacent-contract-prep-boundary-baseline.md](./orders-first-adjacent-contract-prep-boundary-baseline.md) | current repo 已足以说明：candidate scope 应围绕这条 narrow downstream target candidate 展开 | 不能推出 confirmed first target；不能推出 future contract name | 下一包仍必须保持 `candidate scope shaped, not confirmed` |
| current order-level anchor clues (`order_id` / paid-state / optional `store_id`) | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md) | current repo 已足以说明：它们仍可作为 comparison anchors 被复用进 candidate scope | 不能推出它们已升级成 contract identity 或 final relation key | 下一包仍只能把它们当作 anchors / comparison clues |
| current `carry-forward, not upgraded` discipline | `planning` | [orders-first-adjacent-contract-prep-boundary-baseline.md](./orders-first-adjacent-contract-prep-boundary-baseline.md) | current repo 已能明确：这包允许消费 carry-forward inputs，但不允许升级它们 | 不能推出 carry-forward inputs 已被 final 化 | 下一包仍需继续复用这条 discipline |

## Candidate Naming That Remains Non-Final

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入下一包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| `sales_order_items-adjacent target candidate` | `formal truth + planning` | [orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md)；[orders-first-adjacent-contract-prep-boundary-baseline.md](./orders-first-adjacent-contract-prep-boundary-baseline.md) | 当前 repo 只足以把它写成 current candidate scope 的 target naming | 不能推出 confirmed first target；不能推出 target naming 已等于 contract identity | 下一包必须继续保留 `candidate retained, not confirmed` |
| current order-attached detail facts candidate | `formal truth + planning` | [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | 当前 repo 只足以说明：candidate scope 继续围绕 order-attached detail facts candidate 展开 | 不能推出这条 candidate 已被正式命名成 contract family | 下一包仍需把它与 contract identity 分开 |

## Partial Answers Admitted Into This Package

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入下一包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| current partial primary carrier answer | `planning` | [orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md) | 当前 repo 只足以说明：candidate scope 可继续复用 rows-centered carrier neighborhood | 不能推出 confirmed primary carrier | 下一包必须继续保留 `partial inputs admitted, not upgraded` |
| current partial relation answer | `formal truth + planning` | [orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md) | 当前 repo 只足以说明：candidate scope 可继续复用 rows-centered relation neighborhood | 不能推出 confirmed relation answer；不能推出 final relation key | 下一包必须继续保留 `partial inputs admitted, not upgraded` |
| current partial detail clue answer | `planning` with formal vocabulary anchor | [orders-adjacent-detail-clue-answer.md](./orders-adjacent-detail-clue-answer.md) | 当前 repo 只足以说明：candidate scope 可继续复用 rows-centered detail-clue neighborhood，并继续保持 vocabulary-only lane | 不能推出 confirmed detail clue answer；不能推出 source-side clue existence 已 final | 下一包必须继续保留 `partial inputs admitted, not upgraded` |

## Exclusions That Remain Out Of Scope

| exclusion | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入下一包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| payload-envelope blank | `planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-first-adjacent-contract-prep-boundary-baseline.md](./orders-first-adjacent-contract-prep-boundary-baseline.md) | 当前 repo 已足以说明：envelope-level blank 继续不属于 current candidate scope | 不能推出 envelope metadata family 存在或不存在 | 下一包只允许继续保持 `still excluded from this package` |
| inventory-connected lane | `planning` | [clean-mainline-charter.md](./clean-mainline-charter.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) | 当前 repo 已足以说明：inventory line 继续不进入 current candidate scope | 不能推出 inventory-connected lane 可与 current package 合包 | 下一包只允许继续保持 exclusion |
| multi-lane mixed target shape | `planning` | [orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md) | 当前 repo 已足以说明：mixed shape 会破坏 single-theme / narrow-scope | 不能推出 mixed target 可进入 current package | 下一包只允许继续保持 exclusion |
| downgraded reference hint lane | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | 当前 repo 已足以说明：reference lane 只能作为 downgraded candidate input 保留 | 不能推出 reference lane 已等于 current truth | 下一包只允许继续保持 `downgraded reference candidate` |

## Outputs This Contract-Prep Package Is Allowed To Produce

| output / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入下一包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| candidate package question statement | `planning` | [orders-first-adjacent-contract-prep-boundary-baseline.md](./orders-first-adjacent-contract-prep-boundary-baseline.md) | 当前 repo 已足以允许：把首个 contract-prep package 的问题进一步收窄成一个 candidate package question | 不能推出 formal contract question 已最终确定 | 下一包仍需继续保持 non-final wording |
| carry-forward input set for first contract-prep package | `planning` | [orders-first-adjacent-contract-prep-boundary-baseline.md](./orders-first-adjacent-contract-prep-boundary-baseline.md) | 当前 repo 已足以允许：明确这包会消费哪些 planning inputs | 不能推出这些 inputs 已升级成 truth | 下一包仍需继续标注 `carry-forward, not upgraded` |
| deferred-output list for later formal contract/path packages | `planning` | [orders-first-adjacent-contract-prep-boundary-baseline.md](./orders-first-adjacent-contract-prep-boundary-baseline.md) | 当前 repo 已足以允许：显式列出哪些问题继续 deferred 给后续 formal contract/path packages | 不能推出 deferred items 已被回答 | 下一包仍需保持 defer list 显式存在 |
| scope-locked exclusion note | `planning` | [orders-first-adjacent-contract-prep-boundary-baseline.md](./orders-first-adjacent-contract-prep-boundary-baseline.md) | 当前 repo 已足以允许：明确把 envelope / inventory / mixed target 继续排除在当前 package 外 | 不能推出 exclusions 已消失 | 下一包仍需保持 exclusion note |

## Outputs It Must Not Yet Produce

首个 contract-prep package 当前明确不能提前产出：

- confirmed first target
- contract identity
- overwrite / upsert key
- path/read shape
- internal entrypoint
- behavior readiness
- formal contract/path truth

这些对象仍需留给后续更窄、边界更清晰的 formal contract docs 或 docs+code package，而不是在 current candidate scope package 里偷跑。

## Downstream Routing After This Package

这份 package 之后，current `/erp/orders` adjacent line 至少已经明确：

1. first adjacent contract-prep package 现在应围绕一个被写清的 candidate scope 展开，而不是再回头重做 preflight / boundary 抽象包。
2. current route 当前只允许把这包写成：
   - `candidate scope shaped, not confirmed`
   - `intermediate output allowed, not final contract truth`
   - `partial inputs admitted, not upgraded`
   - `still excluded from this package`
3. 做完这包后，下一步才适合再判断：
   - 是否允许进入真正的 first adjacent contract-prep formal docs 或 docs+code package

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
- [orders-adjacent-detail-clue-answer.md](./orders-adjacent-detail-clue-answer.md)
- [orders-first-adjacent-contract-prep-preflight.md](./orders-first-adjacent-contract-prep-preflight.md)
- [orders-first-adjacent-contract-prep-boundary-baseline.md](./orders-first-adjacent-contract-prep-boundary-baseline.md)

它当前不替代：
- contract-prep preflight baseline
- contract-prep boundary baseline
- formal contract docs
- formal path docs
