# Orders First Adjacent Contract-Prep Preflight

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
- `M4-PR1 | docs/plan: preflight /erp/orders first adjacent contract-prep route`
- current `/erp/orders` first adjacent contract-prep route 的 planning-only preflight baseline
- 从 `M3` source-accuracy / routing 收口切换到 `M4` contract-prep route 的 admissibility 判断

这份文档不做：
- 不改 `README.md`
- 不改 `docs/README.md`
- 不改任何 formal boundary docs
- 不改 runtime / model / schema / crud / service / migration / tests
- 不把 `sales_order_items-adjacent target candidate` 升级成 confirmed target
- 不把 candidate mapping 或 partial source-accuracy answers 升级成 contract identity
- 不新增 overwrite / upsert key / path / capture ingress / internal entrypoint / behavior readiness
- 不进入 contract/path/behavior 实现
- 不跳去 inventory、orchestration、operator-facing evidence
- 不把 planning / reference 写成已落地 truth

## Scope

这份文档只回答 current `/erp/orders` first adjacent contract-prep route 的一个问题：

- current `/erp/orders` adjacent line 在完成 `M3` source-evidence / source-accuracy / mapping minimum / carrier / relation / detail clue 这组 planning outputs 之后，是否已经具备进入 first adjacent contract-prep 的 planning-level admissibility

它当前只覆盖：
- current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family
- current `M3` outputs 哪些可以作为 carry-forward planning inputs
- 哪些对象仍必须保持 `candidate` / `partial answer` / `exclusion` / `downgraded reference`
- current route 为什么仍只允许 single-theme / single family / single narrow target slice
- current contract-prep route 允许回答什么、不允许回答什么

它当前不覆盖：
- confirmed first target
- contract identity
- overwrite / upsert key
- path/read shape
- internal entrypoint
- behavior readiness
- contract/path/behavior 实现

## Why This Preflight Exists

[orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md) 最早把 current `/erp/orders` adjacent line 的 contract-entry minimums 列清。

随后 `M3` 这组 planning outputs 又把原先四类 minimum 拆成了可复查的 repo-owned answers：
- [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)
- [orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md)
- [orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md)
- [orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md)
- [orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md)
- [orders-adjacent-detail-clue-answer.md](./orders-adjacent-detail-clue-answer.md)

在这组 `M3` 文档都已经落地之后，继续机械细拆更多 `M3` 小包的边际收益已经明显下降。

因此当前更需要一份单独的 `M4-PR1` preflight baseline，
只回答：
- 哪些 `M3` outputs 现在已经足够作为 contract-prep 的 carry-forward inputs
- 哪些对象仍必须保留为 `candidate` / `partial answer` / `exclusion`
- current route 为什么已经允许进入 contract-prep preflight，但仍然不是 contract truth

## Carry-Forward M3 Inputs Now Available

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| current `rows` anchor family | `formal truth + planning` | [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md)；[orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md) | current repo 已正式证明：top-level `rows` list 仍是 current `/erp/orders` line 唯一 formal source anchor | 不能推出 adjacent candidate 与 current row anchor 为同一 contract carrier | 后续 contract-prep 仍要把它只当作 formal comparison anchor，而不是 contract input truth |
| current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family | `formal truth + planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md) | current repo 已足以说明：current first adjacent route 只围绕这一条 adjacent candidate family 展开 | 不能推出这条 family 已被确认命名成 target truth | 后续 contract-prep 仍要把它保持为 source-side candidate family |
| `sales_order_items-adjacent target candidate` | `formal truth + planning` | `src/app/models/sales_order_item.py`；[orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md)；[orders-adjacent-detail-clue-answer.md](./orders-adjacent-detail-clue-answer.md) | current repo 已足以说明：它是 current route 中唯一继续保留的 narrow downstream target candidate | 不能推出它已是 confirmed first target；不能推出它与 future contract identity 等价 | 后续 contract-prep 仍要显式保留 `candidate retained, not confirmed` |
| current partial primary carrier answer | `planning` | [orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md) | current repo 已足以把 current source-side carrier 收口到 `rows`-centered comparison neighborhood | 不能推出 confirmed primary carrier | 后续 contract-prep 只能把它作为 `partial answer carried forward, not upgraded` |
| current partial relation answer | `formal truth + planning` | [orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md) | current repo 已足以把 current relation 收口到 `rows`-centered order-attached comparison neighborhood | 不能推出 confirmed relation answer；不能推出 `order_id` 已是 contract key | 后续 contract-prep 只能把它作为 `partial answer carried forward, not upgraded` |
| current partial detail clue answer | `planning` with formal vocabulary anchor | [orders-adjacent-detail-clue-answer.md](./orders-adjacent-detail-clue-answer.md) | current repo 已足以把 current detail clue question 收口到 rows-centered detail-clue comparison neighborhood，并明确 vocabulary demotion | 不能推出 confirmed detail clue answer；不能推出 source-side clue existence 已最终确认 | 后续 contract-prep 只能把它作为 `partial answer carried forward, not upgraded` |
| provenance / downgrade discipline | `planning` | [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)；[orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md) | current repo 已有稳定的 repo-owned answer / downgraded reference / exclusion 写法 | 不能推出 reference lane 已升级成 current truth | 后续 contract-prep 仍要继续复用这套 downgrade discipline |
| single-theme / single family / single narrow target slice route guardrail | `planning` | [clean-mainline-charter.md](./clean-mainline-charter.md)；[orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)；[orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md) | current repo 已明确：first adjacent route 只能保持单主题、单 family、单 narrow target slice | 不能推出 current target naming 已确认 | 后续 contract-prep 仍要把它只当作 route guardrail，而不是 confirmed target naming |

## Admissibility Questions For First Adjacent Contract-Prep

| question | 证据层级 | 当前 repo 证据 | 当前 preflight 结论 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- | --- |
| current route 是否已具备进入 first adjacent contract-prep 的 planning-level admissibility | `planning` | [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)；[orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md)；[orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md)；[orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md)；[orders-adjacent-detail-clue-answer.md](./orders-adjacent-detail-clue-answer.md) | `preflight admissible but still non-final` | current repo 已足以说明：`M3` outputs 已形成一组可被后续 contract-prep package 复用的 carry-forward planning inputs | 不能推出 contract truth 已确认；不能推出 actual contract package 已经完成 | 后续只缺一个真正的 contract-prep package，显式消费这些 inputs 并继续保持 downgrade 边界 |
| current route 是否已具备一个 single-theme / single family / single narrow target slice | `formal truth + planning` | [orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md)；[orders-adjacent-detail-clue-answer.md](./orders-adjacent-detail-clue-answer.md) | `已形成 planning-level answer` | current repo 已能明确：只有 `sales_order_items-adjacent target candidate` 继续被保留为 narrow target candidate，envelope / mixed / inventory lanes 继续排除在外 | 不能推出 narrow target candidate 已被确认 | 后续 contract-prep 仍要把 target candidate 与 contract identity 显式分离 |
| current partial carrier / relation / detail clue answers 是否允许被后续包继续复用 | `planning` | [orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md)；[orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md)；[orders-adjacent-detail-clue-answer.md](./orders-adjacent-detail-clue-answer.md) | `allowed as carry-forward inputs only` | current repo 已能明确：这些 partial answers 可以被后续 package 复用为 planning inputs | 不能推出这些 answers 已经升级成 contract truth | 后续 contract-prep 仍要明确写出 `partial answer carried forward, not upgraded` |
| current exclusions 是否已足够支撑 contract-prep scope 保持收敛 | `planning` | [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)；[orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) | `sufficient for preflight scope control` | current repo 已足以说明：envelope blank、inventory line、multi-lane mixed target 当前都应继续保持 exclusion | 不能推出这些 exclusions 已经回答了 contract truth | 后续 contract-prep 仍要把它们继续写成 `still excluded from contract-prep scope` |

## Candidates / Partial Answers That Must Remain Downgraded

| 对象名称 / working name | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| `sales_order_items-adjacent target candidate` | `formal truth + planning` | [orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md) | 当前 repo 只足以把它保留为 current first adjacent route 的 target candidate | 不能推出 confirmed first target；不能推出 future contract name | 后续 contract-prep 必须继续保留 `candidate retained, not confirmed` |
| current partial carrier answer | `planning` | [orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md) | 当前 repo 只足以说明 carrier 已被压缩到 rows-centered neighborhood | 不能推出 confirmed primary carrier | 后续 contract-prep 必须继续保留 `partial answer carried forward, not upgraded` |
| current partial relation answer | `formal truth + planning` | [orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md) | 当前 repo 只足以说明 relation 已被压缩到 rows-centered order-attached neighborhood | 不能推出 confirmed relation answer；不能推出 contract relation key | 后续 contract-prep 必须继续保留 `partial answer carried forward, not upgraded` |
| current partial detail clue answer | `planning` with formal vocabulary anchor | [orders-adjacent-detail-clue-answer.md](./orders-adjacent-detail-clue-answer.md) | 当前 repo 只足以说明 detail clue 已被压缩到 rows-centered detail-clue neighborhood，并明确了 vocabulary-only lane | 不能推出 confirmed detail clue answer | 后续 contract-prep 必须继续保留 `partial answer carried forward, not upgraded` |
| orders-adjacent external hint lane | `reference + planning` | [docs/reference/legacy-backend/README.md](./reference/legacy-backend/README.md)；[orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md) | 当前 repo 只足以把 external lane 保留为 downgraded reference candidate | 不能推出 external lane 已是 current truth | 后续 contract-prep 仍要把它继续保留为 downgraded reference candidate |

## Exclusions That Must Stay In Place

| exclusion | 证据层级 | 当前 repo 证据 | 当前最多能说明什么 | 当前还不能推出什么 | 若进入后续包，最小还缺什么 |
| --- | --- | --- | --- | --- | --- |
| payload-envelope blank | `planning` | [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)；[orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md) | 当前 repo 已足以说明：envelope-level blank 继续不属于 first adjacent contract-prep scope | 不能推出 envelope metadata family 存在或不存在 | 后续 contract-prep 只需继续显式保持 exclusion |
| inventory-connected lane | `planning` | [clean-mainline-charter.md](./clean-mainline-charter.md)；[orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md) | 当前 repo 已足以说明：inventory line 继续不进入 current first adjacent route | 不能推出 inventory-connected lane 可与 first adjacent package 合包 | 后续 contract-prep 只需继续显式保持 exclusion |
| multi-lane mixed target | `planning` | [orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md) | 当前 repo 已足以说明：mixed target shape 会破坏 narrow-scope discipline | 不能推出 mixed lane 可作为 admissible route | 后续 contract-prep 只需继续显式保持 exclusion |
| contract/path/behavior implementation | `planning` | [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)；[orders-first-adjacent-contract-prep-preflight.md](./orders-first-adjacent-contract-prep-preflight.md) | 当前 repo 已足以说明：当前 package 只停留在 preflight，不进入 implementation | 不能推出 implementation 已 ready | 后续仍需独立的 contract-prep / contract / path packages |

## What Contract-Prep May Now Answer

在这次 preflight 之后，后续真正的 first adjacent contract-prep package 当前允许回答：

1. 哪些 `M3` outputs 可以作为 carry-forward planning inputs 被复用。
2. 为什么 current route 只允许继续围绕：
   - current `/erp/orders` `rows`-adjacent non-`sales_orders` candidate family
   - `sales_order_items-adjacent target candidate`
   - single-theme / single family / single narrow target slice
3. 哪些对象必须在 contract-prep 中继续保持：
   - `candidate retained, not confirmed`
   - `partial answer carried forward, not upgraded`
   - `still excluded from contract-prep scope`
   - `downgraded reference candidate`
4. first adjacent contract-prep package 的 planning question 应该怎样被窄化，而不把它直接写成 contract truth。

## What Contract-Prep Still May Not Answer

即使在这次 preflight 之后，后续 contract-prep package 仍然不应直接回答：

- confirmed first target
- contract identity
- overwrite / upsert key
- path/read shape
- internal entrypoint
- behavior readiness
- contract/path/behavior implementation

这些对象仍需继续留给后续更窄、边界更清晰的 package，而不是在 preflight 或 contract-prep 起手包里偷跑。

## Downstream Routing After This Preflight

这份 package 之后，current `/erp/orders` adjacent line 至少已经明确：

1. current route 现在可以被写成：
   - `preflight admissible but still non-final`
2. 下一包允许进入：
   - first adjacent contract-prep package
3. 但下一包仍必须继续保持：
   - `sales_order_items-adjacent target candidate` 只是 target candidate
   - current carrier / relation / detail clue answers 只是 carry-forward planning inputs
   - single-theme / single family / single narrow target slice 只是 route guardrail
4. 当前仍不应进入：
   - contract/path/behavior 实现
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
- [orders-adjacent-primary-carrier-answer.md](./orders-adjacent-primary-carrier-answer.md)
- [orders-adjacent-relation-answer.md](./orders-adjacent-relation-answer.md)
- [orders-adjacent-detail-clue-answer.md](./orders-adjacent-detail-clue-answer.md)

它当前不替代：
- contract-entry minimums baseline
- source-evidence baseline
- source-accuracy revisit baseline
- single-target mapping minimums baseline
- formal contract docs
- formal path docs

当前 `/erp/orders` first adjacent contract-prep boundary baseline 另行维护在：
- [orders-first-adjacent-contract-prep-boundary-baseline.md](./orders-first-adjacent-contract-prep-boundary-baseline.md)
