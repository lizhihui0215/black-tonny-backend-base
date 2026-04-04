# Orders First Adjacent Contract-Prep Boundary Baseline

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
- `M4-PR2 | docs/plan: answer /erp/orders first adjacent contract-prep boundary baseline`
- current `/erp/orders` first adjacent contract-prep package 的 planning boundary baseline
- 后续真正 first adjacent contract-prep package 的 admissible-question / boundary 输入

这份文档不做：
- 不改 `README.md`
- 不改 `docs/README.md`
- 不改任何 formal boundary docs
- 不改 runtime / model / schema / crud / service / migration / tests
- 不把 `sales_order_items-adjacent target candidate` 升级成 confirmed target
- 不把 partial answers 升级成 contract identity
- 不新增 overwrite / upsert key / path / capture ingress / internal entrypoint / behavior readiness
- 不进入 formal contract/path/behavior 实现
- 不跳去 inventory、orchestration、operator-facing evidence
- 不把 planning / reference 写成已落地 truth

## Scope

这份文档只回答 current `/erp/orders` first adjacent contract-prep package 的一个问题：

- 在 `M4-PR1` preflight 已经成立之后，首个 contract-prep package 的 planning boundary 应该如何被写清

它当前只覆盖：
- first adjacent contract-prep package 允许 carry forward 的 planning inputs
- target naming 里哪些对象仍必须保持 candidate-only
- source-accuracy 里哪些 answers 仍必须保持 partial
- 哪些 exclusions 仍必须留在 contract-prep scope 外
- first contract-prep package 允许尝试回答哪些问题
- first contract-prep package 明确不能提前回答哪些问题

它当前不覆盖：
- confirmed first target
- contract identity
- overwrite / upsert key
- path/read shape
- internal entrypoint
- behavior readiness
- formal contract/path/behavior truth

## Why This Package Exists

[orders-first-adjacent-contract-prep-preflight.md](./orders-first-adjacent-contract-prep-preflight.md) 已回答：
- current `/erp/orders` adjacent line 已具备 `preflight admissible but still non-final` 的 planning-level admissibility

但 preflight 文档的职责仍然是：
- 回答这条路由能不能开始进入 contract-prep 语境

它还不等于：
- 首个 contract-prep package 的边界已经写清

因此当前需要一份单独的 boundary baseline，
只回答：
- 哪些 inputs 可以被后续 contract-prep package 继续 carry forward
- 哪些对象必须继续保持 `candidate retained, not confirmed`
- 哪些对象必须继续保持 `partial answer admitted, not finalized`
- 哪些对象必须继续保持 `still excluded from contract-prep boundary`
- 首个 contract-prep package 可以尝试回答什么、不可以尝试回答什么

## Boundary Distinction

| 对象 | 证据层级 | 当前最多能说明什么 | 当前还不能推出什么 |
| --- | --- | --- | --- |
| contract-prep admissibility | `planning` | current route 已允许进入 contract-prep planning 语境 | 不能推出 contract-prep boundary 已写清；不能推出 contract truth 已成立 |
| contract-prep boundary | `planning` | current route 可以开始定义首个 contract-prep package 允许使用哪些 inputs、允许问哪些问题 | 不能推出 contract identity、overwrite / upsert、path/read shape 或 behavior readiness |
| formal contract/path truth | `formal truth` | 只有未来独立的 formal contract/path docs 与 landed code/tests 才能回答 | 当前 planning 文档不能替代它 |

## Carry-Forward Inputs Admitted Into Contract-Prep

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入下一包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| current `rows` anchor family | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md) | current repo 已正式证明：top-level `rows` list 仍是 current `/erp/orders` line 的唯一 formal anchor | 不能推出 adjacent candidate 与 current row anchor 为同一 contract carrier | 下一包只允许把它继续当作 formal comparison anchor |
| current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family | `formal truth + planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | current repo 已足以说明：first adjacent contract-prep package 只围绕这条 candidate family 展开 | 不能推出 candidate family 已被确认命名成 target truth | 下一包只允许把它继续当作 source-side candidate family |
| `sales_order_items-adjacent target candidate` | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md)；[orders-first-adjacent-contract-prep-preflight.md](./orders-first-adjacent-contract-prep-preflight.md) | current repo 已足以说明：它是当前继续保留的 narrow downstream target candidate | 不能推出 confirmed first target；不能推出 future contract name | 下一包必须继续写成 `candidate retained, not confirmed` |
| current order-level anchor clues (`order_id` / paid-state / optional `store_id`) | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md) | current repo 已足以说明：这些 clues 可继续作为 comparison anchors 被复用 | 不能推出它们已升级成 contract identity 或 final relation key | 下一包只允许把它们继续当作 anchors / comparison clues |
| provenance / downgrade discipline | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | current repo 已有稳定的 repo-owned answer / downgraded reference / exclusion 写法 | 不能推出 downgraded reference 已升级成 truth | 下一包仍需继续复用这套 discipline |
| single-theme / single family / single narrow target slice guardrail | `planning` | [clean-mainline-charter.md](./clean-mainline-charter.md)；[orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)；[orders-first-adjacent-contract-prep-preflight.md](./orders-first-adjacent-contract-prep-preflight.md) | current repo 已明确：first adjacent contract-prep package 仍只能保持单主题、单 family、单 narrow-scope | 不能推出 current target naming 已确认 | 下一包只允许把它继续当作 route guardrail |

## Target Naming That Must Remain Candidate-Only

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入下一包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| `sales_order_items-adjacent target candidate` | `formal truth + planning` | [orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md)；[orders-first-adjacent-contract-prep-preflight.md](./orders-first-adjacent-contract-prep-preflight.md) | 当前 repo 只足以把它保留为 target candidate naming | 不能推出 confirmed first target；不能推出 target naming 已等于 contract identity | 下一包必须继续保留 `candidate retained, not confirmed` |
| current order-attached detail facts candidate | `formal truth + planning` | [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | 当前 repo 只足以说明 current route 继续围绕一条 order-attached detail facts candidate 展开 | 不能推出这条 candidate 已被正式命名成 contract family | 下一包仍需把它与 target naming 和 contract identity 分开 |

## Source-Accuracy Answers That Remain Partial

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入下一包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| current partial primary carrier answer | `planning` | [orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md) | 当前 repo 只足以把 source-side carrier 收口到 rows-centered comparison neighborhood | 不能推出 confirmed primary carrier | 下一包必须继续保留 `partial answer admitted, not finalized` |
| current partial relation answer | `formal truth + planning` | [orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md) | 当前 repo 只足以把 relation 收口到 rows-centered order-attached comparison neighborhood | 不能推出 confirmed relation answer；不能推出 final relation key | 下一包必须继续保留 `partial answer admitted, not finalized` |
| current partial detail clue answer | `planning` with formal vocabulary anchor | [orders-adjacent-detail-clue-answer.md](./orders-adjacent-detail-clue-answer.md) | 当前 repo 只足以把 detail clue question 收口到 rows-centered detail-clue comparison neighborhood，并明确 vocabulary-only lane | 不能推出 confirmed detail clue answer；不能推出 source-side clue existence 已 final | 下一包必须继续保留 `partial answer admitted, not finalized` |

## Exclusions That Must Stay Out Of Scope

| exclusion | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入下一包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| payload-envelope blank | `planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-first-adjacent-contract-prep-preflight.md](./orders-first-adjacent-contract-prep-preflight.md) | 当前 repo 已足以说明：envelope-level blank 继续不属于 first contract-prep boundary | 不能推出 envelope metadata family 存在或不存在 | 下一包只允许继续保持 `still excluded from contract-prep boundary` |
| inventory-connected lane | `planning` | [clean-mainline-charter.md](./clean-mainline-charter.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) | 当前 repo 已足以说明：inventory line 继续不进入 current first adjacent contract-prep boundary | 不能推出 inventory-connected lane 可与 first package 合包 | 下一包只允许继续保持 exclusion |
| multi-lane mixed target shape | `planning` | [orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md) | 当前 repo 已足以说明：mixed shape 会破坏 narrow-scope discipline | 不能推出 mixed target 可作为 admissible contract-prep shape | 下一包只允许继续保持 exclusion |
| downgraded reference hint lane | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | 当前 repo 已足以说明：reference lane 只能作为 downgraded candidate input | 不能推出 reference lane 已等于 current truth | 下一包只允许继续保持 `downgraded reference candidate` |

## Questions Contract-Prep May Answer

在这份 boundary baseline 之后，首个 contract-prep package 当前允许尝试回答：

1. 哪些 carry-forward inputs 会被继续复用。
2. 为什么 current route 仍只允许：
   - current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family
   - `sales_order_items-adjacent target candidate`
   - single-theme / single family / single narrow target slice
3. 哪些对象必须继续保持：
   - `carry-forward, not upgraded`
   - `candidate retained, not confirmed`
   - `partial answer admitted, not finalized`
   - `still excluded from contract-prep boundary`
4. first contract-prep package 的 planning question 应如何被继续窄化，而不把它直接写成 formal contract truth。

## Questions Contract-Prep Must Not Answer

即使在这份 boundary baseline 之后，首个 contract-prep package 仍然不应直接回答：

- confirmed first target
- contract identity
- overwrite / upsert key
- path/read shape
- internal entrypoint
- behavior readiness
- formal contract/path/behavior truth

这些对象仍需继续留给后续更窄、边界更清晰的 package，而不是在 boundary baseline 或 contract-prep 起手包里偷跑。

## Downstream Routing After This Boundary Baseline

这份 package 之后，current `/erp/orders` adjacent line 至少已经明确：

1. current route 现在可以被写成：
   - `carry-forward, not upgraded`
   - `candidate retained, not confirmed`
   - `partial answer admitted, not finalized`
   - `still excluded from contract-prep boundary`
2. current boundary baseline 已把 first contract-prep package 的 admissible-question set 收清，
   - 但它本身仍不是 formal contract/path truth
3. 做完这包后，下一步才适合再判断：
   - 是否允许进入真正的 first adjacent contract-prep docs/code package

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

它当前不替代：
- contract-entry minimums baseline
- contract-prep preflight baseline
- source-evidence baseline
- source-accuracy revisit baseline
- single-target mapping minimums baseline
- formal contract docs
- formal path docs

当前 `/erp/orders` first adjacent contract-prep candidate scope baseline 另行维护在：
- [orders-first-adjacent-contract-prep-candidate-scope.md](./orders-first-adjacent-contract-prep-candidate-scope.md)
