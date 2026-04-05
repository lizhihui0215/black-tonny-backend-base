# Source Intelligence Migration Charter

状态：planning-only / working document

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../README.md)
- [docs/README.md](../README.md)
- [docs/](../README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

这份文档只做一件事：
- 为新的 source-intelligence 主线定义迁移目标、证据分级、资产分类、交付物类型和 review guardrails

这份文档服务的是：
- `M1-PR1 | docs: add source intelligence migration charter`

这份文档不做：
- 不新增 runtime behavior
- 不新增 contract/path
- 不新增 inventory 范围
- 不新增模板
- 不做 docs 子体系重构
- 不做代码结构重构

## Core Goal

新的 source-intelligence 主线总目标必须固定为：
- 把旧仓已经积累的知识迁移进新仓
- 不把旧仓架构迁进新仓

这里的“知识迁移”指的是：
- 可复核的 API 认识
- 可复核的字段语义
- 可复核的关系判断
- 可复核的 evidence 归档
- 可复核的 serving-ready knowledge

这里明确不是：
- 复制旧仓目录树
- 复制旧仓 flat service/script 结构
- 继承旧仓里未重写的运行方式
- 把旧仓临时产物继续堆进新仓

## Migration Objects

当前 source-intelligence 主线允许迁移的对象，必须限制在知识资产层：

1. API
- endpoint family
- request/response shape
- page-to-endpoint clues
- filter / pagination / checksum / envelope 等候选规则

2. 字段
- field name
- field role
- field grain
- field-level ambiguity
- field-level exclusions

3. 关系
- object-to-object relation
- row-to-detail relation
- source-to-serving relation
- identity / non-identity boundary

4. Evidence
- formal truth 可复用证据
- planning-level supporting evidence
- legacy/reference evidence candidate
- 明确记录的 unresolved contradiction

5. Serving-Ready Knowledge
- 哪些知识已经足以支持后续 contract/path
- 哪些知识只够支持 planning
- 哪些知识仍必须留在 deferred

## Non-Migration Objects

以下对象当前明确不是 source-intelligence 迁移对象：
- 旧仓 `app/services` 的 flat service 结构
- 旧仓 `scripts`
- 旧仓 `tmp/**`
- 旧仓 `output/**`
- 旧仓截图、raw sample、导出文件本身
- 旧仓未重写进新仓 formal/planning docs 的 runbook truth
- 旧仓目录命名、模块切分、Base 继承方式

如果某项内容只能以“旧仓里原来就是这么放的”来解释，
它就不应被作为 source-intelligence 迁移对象。

## Evidence Taxonomy

source-intelligence 主线后续所有 working docs，都应优先复用这一组 evidence taxonomy：

### `Confirmed`

定义：
- 已被当前 repo formal truth 直接锁定

允许来源：
- formal docs
- 当前 `main` 上已经 landed 的 code/tests/migrations

当前最多能说明：
- 这是 current repo 已承认的事实

### `Supported`

定义：
- 还不是 formal truth，但已被 repo-owned planning docs 或多条稳定证据支持

允许来源：
- planning docs
- formal truth 的邻近支撑事实
- 已被 repo-owned 文档稳定吸收的 reference 线索

当前最多能说明：
- 这是一个有明确支撑、可以继续向 contract-ready 判断推进的结论

### `Candidate`

定义：
- 已有线索，但仍缺关键证据、关键关系、关键字段语义或关键边界回答

允许来源：
- reference
- screenshot
- raw sample
- runbook
- 单点 planning 记录

当前最多能说明：
- 值得继续盘

当前不能说明：
- 不能直接升级成 truth
- 不能直接成为 contract/path 前提

### `Deferred`

定义：
- 已知存在，但当前主线明确不优先处理，或被更高收益前置条件阻塞

当前最多能说明：
- 当前不做，并且原因必须写清

## Legacy Asset Classification

旧仓资产进入新仓前，必须先落到以下四类之一：

### `可直接吸收`

满足条件：
- 已经能被当前 formal truth 或稳定 planning 直接复核
- 不依赖旧仓结构才能理解
- 吸收后不会把旧仓目录语义一起带进来

典型对象：
- 已稳定命名的 API dossier 片段
- 已稳定命名的 field dictionary 条目
- 已稳定命名的 relation answer

### `需重写吸收`

满足条件：
- 旧仓里有高价值知识
- 但旧表达方式混有 runbook、脚本路径、临时结构、截图依赖或口语化结论

要求：
- 必须在新仓 docs 中重写
- 必须把来源层级和证据强度写清
- 必须去掉对旧结构的依赖

### `仅参考`

满足条件：
- 对理解背景、找线索、查冲突有帮助
- 但不足以直接升级成 repo-owned 结论

典型对象：
- screenshot
- raw sample
- legacy runbook
- 历史 output

### `不迁`

满足条件：
- 主要价值只是旧架构、旧目录、旧脚本运行方式
- 迁入后只会继续污染新仓结构
- 或内容已经过期且无法稳定复核

## Deliverable Types

source-intelligence 主线后续允许优先沉淀的交付物类型只有以下四类：

1. API dossier
- 记录 endpoint family、payload family、filter/envelope/checksum 线索、证据层级和 open questions

2. field dictionary
- 记录字段名、候选语义、grain、identity relevance、allowed evidence level 和 unresolved ambiguity

3. relation doc
- 记录对象之间的 relation、identity boundary、detail boundary、serving relevance 和 exclusions

4. serving-readiness doc
- 记录哪些 knowledge 已足以支持 serving contract/path judgment，哪些仍不够

这些交付物当前是知识资产，不是运行资产。

## Guardrails

后续 source-intelligence 包必须同时满足以下 guardrails：

1. 不把 screenshot、raw sample、旧 runbook 直接升级成 truth
2. 不把 persistence surface 自动升级成 serving truth
3. 不把旧仓结构迁入新仓
4. 不让新增知识资产继续四散到任意 docs、tmp、output 或 generic code 角落
5. 不把字段名存在误写成字段语义已确认
6. 不把 relation clue 误写成 relation truth
7. 不把 serving-ready knowledge 误写成 runtime behavior 已落地

## Review Requirements

source-intelligence 主线下的每次 review，至少必须回答以下三组问题：

### 1. 收益评估

必须评估：
- 这次 review 新增了什么 repo-owned knowledge
- 它是否明显提升了 contract-ready / serving-ready 判断能力
- 它是否只是重复搬运已有线索

### 2. 低收益循环检查

必须检查：
- 是否已经连续多轮只在改写相同线索
- 是否已经在 candidate/supporting evidence 上空转
- 是否应该停止继续补同类 planning，转去更高收益交付物

### 3. 结构健康度检查

必须检查：
- 新知识是否进入了明确 docs 位置
- support code 是否开始向 generic `services` 平铺
- 是否又引入了新的模糊 `Base`、模糊 shared abstraction、模糊目录归属

如果这三组问题回答不清，就不应继续机械开下一包。

## Structure Constraints

从这份 charter 往后，source-intelligence 资产必须遵守以下结构约束：

1. source-intelligence 资产未来优先进入新的 docs 子体系
- 当前这份 charter 只定义方向，不在本包里展开子体系模板

2. 新增 support code 不应继续平铺到 generic `services`
- 如确有必要新增 support code，必须说明为什么不能留在更窄、更贴近主题的目录

3. 新代码避免继续扩散模糊 `Base`
- 不新增为了“通用”而通用的 shared base
- 不把知识处理逻辑挂到语义模糊的基础类上

4. docs 必须继续可发现
- 任何新的 source-intelligence 核心文档，都应先接入 [docs/README.md](../README.md)

## What This Charter Makes Explicit

基于以上约束，当前至少可以明确四件事：

1. 新主线迁的是 knowledge，不是旧架构
2. 后续包应优先产出 repo-owned knowledge assets，而不是继续堆 legacy 搬运
3. evidence 强度必须显式分级，不能混写
4. review 必须把收益、循环风险、结构健康度一起纳入判断

## What This Charter Does Not Do

这份 charter 当前明确不做：
- 不直接产出 API dossier
- 不直接产出 field dictionary
- 不直接产出 relation doc
- 不直接产出 serving-readiness doc
- 不直接打开 inventory line
- 不定义 runtime contract/path
- 不定义 code-level support abstraction
- 不决定未来 docs 子体系的最终目录模板
