# Source-Intelligence Ops

状态：source-intelligence / ops control plane

这组文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../../README.md)
- [docs/README.md](../../README.md)
- [../README.md](../README.md)
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

如果这组文档仍处在待 merge 的 PR 里，
它们当前只描述 merge target 下的 source-intelligence control plane，
不应被反写成 current `main` 已经拥有的事实。

这个子体系只服务一个目标：
- 给 `docs/source-intelligence/**` 当前主线提供 repo-owned 协作控制面

它服务于五件事：
- 收益评估
- 及时纠偏
- 新会话 handoff
- 质量门
- 结构健康度检查

它不做：
- 不产出 dossier
- 不产出 field dictionary
- 不产出 relation doc
- 不产出 serving-readiness doc
- 不替代 formal boundary docs

## Boundary Against Output Slots

- [../apis/README.md](../apis/README.md)
  - 这里放 API dossier 正文
- [../fields/README.md](../fields/README.md)
  - 这里放 field dictionary 正文
- [../relations/README.md](../relations/README.md)
  - 这里放 relation doc 正文
- [../serving-readiness/README.md](../serving-readiness/README.md)
  - 这里放 serving-readiness 正文

`ops/` 的角色只有一个：
- 给这些正文输出位提供 current main state、review gain ledger、milestone tracking、handoff、quality gates

`ops/` 当前不是：
- 新的正文输出位
- 新的对象资产类型
- 替代 `apis/`、`fields/`、`relations/`、`serving-readiness/` 的第五类正文槽位
- 根目录外部工作稿的长期宿主

## File Map

- [full-migration-master-plan.md](./full-migration-master-plan.md)
  - source-intelligence 全量迁移主线的 canonical 总计划与最新状态真源
- [current-main-state.md](./current-main-state.md)
  - 当前 main 最小真相
- [review-gain-ledger.md](./review-gain-ledger.md)
  - 每个 merge 包的收益台账
- [milestone-board.md](./milestone-board.md)
  - 当前 milestone 板
- [handoff-prompt.md](./handoff-prompt.md)
  - 给新会话 / 新 Codex 的最小交接提示
- [quality-gates.md](./quality-gates.md)
  - docs-only / code / migration-contract 三类质量门

## Use Order

1. 先读 [full-migration-master-plan.md](./full-migration-master-plan.md)，确认当前 milestone / PR / 最新状态同步块。
2. 开新包前再读 [current-main-state.md](./current-main-state.md)。
3. 选题前再看 [milestone-board.md](./milestone-board.md)。
4. 开写前过一遍 [quality-gates.md](./quality-gates.md)。
5. 新会话先复用 [handoff-prompt.md](./handoff-prompt.md)。
6. merge 后追加 [review-gain-ledger.md](./review-gain-ledger.md)。

## Merge Update Rule

- 如果这次 merge 或状态纠偏轮改变了当前 milestone / PR / next allowed step，先更新 [full-migration-master-plan.md](./full-migration-master-plan.md) 第 0 节与最新状态同步块。
- 如果这次 merge 改变了 source-intelligence 当前主线状态，更新 [current-main-state.md](./current-main-state.md)。
- 每个相关 merge 后，都向 [review-gain-ledger.md](./review-gain-ledger.md) 追加一条记录。

## Current Role

当前这个 `ops/` 子树的作用不是扩张知识资产面。

当前它只负责：
- 提供仓库内唯一 canonical 的 full-migration master plan
- 让后续包知道现在 main 到了哪
- 让 review 能回答“有没有新增 repo-owned 确定性”
- 让主线在收益下降前及时停手或纠偏
- 让 source-intelligence 资产不要继续四散
