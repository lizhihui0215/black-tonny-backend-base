# Source Intelligence Docs

状态：working index / output structure

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../README.md)
- [docs/README.md](../README.md)
- [docs/](../README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

这份文档只做两件事：
- 说明 source-intelligence docs 的当前主输出结构
- 明确哪些旧 docs 继续作为输入参考，哪些位置是新的主输出位

这个子树的最小协作导轨见 [AGENTS.md](./AGENTS.md)。
它服务于 `docs/source-intelligence/**`，但它不是主输出位。
当前 review / handoff / milestone / quality-gate 的默认控制面入口见 [ops/README.md](./ops/README.md)。

## Current Output Structure

当前 source-intelligence 主输出位收口到：

- [migration-charter.md](./migration-charter.md)
  - 当前主线 charter
- [legacy-source-intelligence-inventory-baseline.md](./legacy-source-intelligence-inventory-baseline.md)
  - legacy source-intelligence 高价值资产 inventory baseline
- [apis/README.md](./apis/README.md)
  - API dossier 主输出位
- [fields/README.md](./fields/README.md)
  - field dictionary 主输出位
- [relations/README.md](./relations/README.md)
  - relation docs 主输出位
- [serving-readiness/README.md](./serving-readiness/README.md)
  - serving-readiness docs 主输出位

当前 source-intelligence 协作控制面入口收口到：

- [ops/README.md](./ops/README.md)
  - current main state / review gain ledger / milestone tracking / handoff / quality gates 的默认入口
  - 不是新的 dossier / field dictionary / relation / serving-readiness 正文输出位
- [ops/full-migration-master-plan.md](./ops/full-migration-master-plan.md)
  - source-intelligence 全量迁移主线的 canonical 总计划与当前状态真源

当前已经落在这套结构里的资产只有：

- [migration-charter.md](./migration-charter.md)
- [legacy-source-intelligence-inventory-baseline.md](./legacy-source-intelligence-inventory-baseline.md)
- [apis/erp-orders-api-dossier.md](./apis/erp-orders-api-dossier.md)
- [apis/sales-list-selsalereport-api-dossier.md](./apis/sales-list-selsalereport-api-dossier.md)
- [apis/sales-list-getdiyreportdata-e004001008-2-api-dossier.md](./apis/sales-list-getdiyreportdata-e004001008-2-api-dossier.md)
- [fields/erp-orders-first-slice-field-dictionary.md](./fields/erp-orders-first-slice-field-dictionary.md)
- [fields/selsalereport-core-field-dictionary.md](./fields/selsalereport-core-field-dictionary.md)
- [fields/sales-list-getdiyreportdata-e004001008-2-core-field-dictionary.md](./fields/sales-list-getdiyreportdata-e004001008-2-core-field-dictionary.md)
- [relations/erp-orders-first-slice-relation-doc.md](./relations/erp-orders-first-slice-relation-doc.md)
- [relations/selsalereport-head-line-boundary-relation-doc.md](./relations/selsalereport-head-line-boundary-relation-doc.md)
- [serving-readiness/erp-orders-first-slice-serving-readiness.md](./serving-readiness/erp-orders-first-slice-serving-readiness.md)
- [serving-readiness/selsalereport-head-slice-serving-readiness.md](./serving-readiness/selsalereport-head-slice-serving-readiness.md)

## Current Output Rule

从当前包往后：

1. API dossier 优先进入 [apis/](./apis/README.md)
2. field dictionary 优先进入 [fields/](./fields/README.md)
3. relation docs 优先进入 [relations/](./relations/README.md)
4. serving-readiness docs 优先进入 [serving-readiness/](./serving-readiness/README.md)
5. source-intelligence 主线 charter 继续留在这个子体系根下
6. legacy source-intelligence inventory baseline 继续留在这个子体系根下，作为后续对象选择入口
7. current main state / review gain ledger / milestone tracking / handoff / quality gates 优先进入 [ops/](./ops/README.md)
8. `ops/` 不能承载 dossier / field dictionary / relation / serving-readiness 正文资产

当前不应再把这些资产平铺回 `docs/` 顶层：
- dossier
- field dictionary
- relation doc
- serving-readiness doc

当前也不应把未重写的 legacy extract 直接写进这些主输出位。
未重写的 legacy 知识碎片，应先进入 [../reference/legacy-backend/extracts/README.md](../reference/legacy-backend/extracts/README.md) 定义的隔离区。

## Upstream Input Docs That Remain Outside This Subtree

以下旧 docs 当前仍然是 source-intelligence 输入参考，
但它们不是新的 source-intelligence 主输出位：

- [../reference/legacy-backend/extracts/README.md](../reference/legacy-backend/extracts/README.md)
- [source-surface-completeness-map.md](../source-surface-completeness-map.md)
- [orders-adjacent-payload-family-baseline.md](../orders-adjacent-payload-family-baseline.md)
- [orders-adjacent-payload-semantics-baseline.md](../orders-adjacent-payload-semantics-baseline.md)
- [orders-adjacent-contract-entry-minimums.md](../orders-adjacent-contract-entry-minimums.md)
- [research-support-current-surface.md](../research-support-current-surface.md)
- [capture-to-sales-orders-path.md](../capture-to-sales-orders-path.md)
- [sales-orders-projection-contract.md](../sales-orders-projection-contract.md)

这些文档当前可作为：
- formal truth anchor
- planning input
- adjacent evidence input

当前 repo 不存在单独的 `sales-order-items-projection-contract.md` formal doc。
任何 `sales_order_items` 邻接判断，仍应回到已有 landed 的 formal docs、planning docs 与 code/tests 组合复核。

其中 [../reference/legacy-backend/extracts/README.md](../reference/legacy-backend/extracts/README.md) 额外承担：
- legacy knowledge fragment 的 quarantine / downgraded input lane
- 在重写前承接窄范围 extract 的落点

它们当前不应被误写成：
- source-intelligence 主输出位
- 已重写完成的 dossier / relation / serving-readiness asset

[../reference/legacy-backend/extracts/README.md](../reference/legacy-backend/extracts/README.md) 下的 extract 文件同样不应被误写成：
- formal truth
- dossier / field dictionary / relation / serving-readiness output
- serving-ready output

## Non-Goals

这份结构索引当前不做：
- 不做全量 dossier 扩张
- 不做 whole field universe
- 不做 whole relation universe
- 不做 whole serving-readiness map
- 不做 docs 全量重组
