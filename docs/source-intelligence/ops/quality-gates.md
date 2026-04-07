# Quality Gates

状态：source-intelligence / review gates

## Docs-Only PR

必须同时通过：

- 索引可发现性
  - 新文档必须有明确落点。
  - 如果当前包受范围限制不能改上游 index，至少要在本子树有 local README 或 local board 可发现。
- evidence level 完整性
  - `Confirmed / Supported / Candidate / Deferred` 不能缺位。
  - 关键结论不能只写结论，不写当前证据层级。
- truth boundary 不被偷换
  - 不能把 `Candidate / Supported` 直接升成 current truth。
  - 不能把 planning/reference 线索偷换成 formal/runtime truth。
- repo-owned 确定性必须增加
  - 必须能说清新增了什么 repo-owned knowledge。
  - 如果只是换一种说法重复旧结论，应判低收益或拒绝。
- 当前目标必须窄
  - 一包只收一个主目标。
  - 不能在 docs-only 包里顺手扩成 whole family map。

## Code PR

必须同时通过：

- 代码变更有 formal boundary 对应物。
- 代码没有把 source-intelligence 的 candidate/support 当成 runtime truth 直接消费。
- 如果代码引入新的 source-side judgment，docs 必须能指出对应 repo-owned knowledge asset 或明确说明仍未成立。
- tests/migrations/contract 边界与代码改动方向一致。
- 代码没有把 knowledge gap 偷偷塞进 generic service / helper。

## Migration / Contract PR

必须同时通过：

- 目标 source object 已有足够窄、足够清楚的 repo-owned knowledge basis。
- 新 contract/path 只服务一个明确 target，不做模糊外推。
- 未解决 blocker 不能被“先实现再说”吞掉。
- source / capture / serving / runtime 四层边界没有被混写。
- 新 formal truth 与现有 source-intelligence working docs 的关系被写清：
  - 哪些升级成 formal
  - 哪些继续停留在 working layer

## 结构健康度检查

每个相关 PR 还要额外回答三件事：

- docs 是否继续四散
  - 新知识是否还在任意 `docs/` 顶层乱落
  - 是否继续绕开 `source-intelligence` 主输出位或 `ops` 控制面
- services 是否继续泛化
  - 是否又把知识判断塞回 generic `app/services` 或难以命名的 helper
  - 是否出现新的“结构先行、知识后补”倾向
- capture / serving / runtime 边界是否被弱化
  - 是否把 source-intelligence working judgment 误写成 runtime truth
  - 是否把 capture/reference/planning 直接抬成 serving/formal
  - 是否让当前 narrow target 又被偷扩成 broader truth

## Fail Fast Conditions

出现任一情况，当前包应暂停或回退：

- 说不清新增了什么 repo-owned certainty
- 说不清对 serving 的实际帮助
- 需要同时展开两个以上主方向
- 需要靠 legacy raw output 才能支撑当前核心结论
- 需要顺手做 support code、结构重排、或 `app/services` 重构才能成立
