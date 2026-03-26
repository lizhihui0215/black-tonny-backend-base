## PR Goal
一句话说明本次 PR 只做什么，不做什么。

示例：
- 只补文档映射，不迁业务代码
- 只迁 capture 最小模型，不接入 runtime
- 只修正 README 和 docs 引用，不改 API 行为

## Changed Files
列出本次实际修改的文件或目录，只写与本次目标直接相关的内容。

示例：
- README.md
- docs/legacy-backend-migration-mapping.md
- docs/README.md

## Boundary Check
请直接填写“是”或“否”：

- 是否涉及 research：
- 是否涉及 capture：
- 是否涉及 serving：
- 是否涉及 runtime：
- 是否改动对外 API 行为：

如果有“是”，请补一句说明改动边界。

## Not Migrated
明确写出这次没有迁入的新旧仓库内容，以及原因。

示例：
- 未迁旧仓库 app/services：避免把旧的扁平 service 结构带入新仓库
- 未迁 scripts：避免把研究/一次性脚本引入正式运行面
- 未迁 research runtime：仅保留为参考资料，不进入正式链路

## Risks
只写 1 到 3 个真实风险点，不要写空话。

示例：
- 文档路径虽然更新，但后续仍可能被误读为代码实现真源
- capture 边界已定义，但正式模型尚未完全落位
- 旧仓库候选输入若被直接复制，仍有污染新结构的风险

## Validation
写清楚这次如何验证。

至少回答这 3 件事：
- 如何验证没有破坏 runtime
- 如何验证没有把 research 混入正式链路
- 如何验证文档与代码现状一致

示例：
- 本次仅修改 docs 和 README，未改 src/app，因此 runtime 行为不变
- 未新增 router、worker、scheduler、service import，不存在 research 接入正式链路
- 已逐项检查文档中的目录、职责和迁移边界与当前仓库现状一致