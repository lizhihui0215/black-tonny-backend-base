# Post-Route Mainline Planning

状态：planning-only / working document

这份文档不是 formal source of truth。

formal truth 仍以以下文档为准：
- [README.md](../README.md)
- [docs/README.md](./README.md)
- [docs/](./README.md) 下各 formal boundary docs

这份文档只回答：11 包主路线收口后，下一轮 mainline 应如何更明确地朝“完整迁移”靠拢。

## 结论摘要

推荐的 next mainline：
- `migration-completeness mainline`

这条主线不再把 `hardening-first` 当唯一主线。
新的 post-route 结构改为两条并行规划、串行落包的子轨：
1. `database / domain migration completeness track`
2. `menu / source-surface completeness track`

`hardening-first` 的位置调整为：
- `database / domain migration completeness track` 里的一个子轨
- 它仍然重要，但不再单独代表 post-route 全局方向

## 什么叫“完整迁移”的最小定义

在当前 repo 里，“完整迁移”不等于一次性把所有 legacy runtime 全搬过来。

当前更现实的最小定义是：
- repo 已经不仅有一条最小正式行为链
- repo 还对剩余待迁移的数据库 / domain surfaces 给出明确盘点和归类
- repo 还对剩余待探索的菜单 / endpoint / payload / slice 给出明确盘点和归类
- 每一块尚未落地的内容，都被明确标成以下之一：
  - 已正式落地
  - 只到 persistence surface
  - 只到 planning / reference
  - 尚未探索完成
  - 明确 deferred / non-goal

换句话说：
- 当前 first `sales_orders` path 证明“正式行为链已经可以落地”
- 但只有当剩余 domain surfaces 和 source surfaces 也被系统性盘点、映射、排序后，repo 才开始更接近“完整迁移”

## 当前已完成的最小正式行为链

当前已完成并可作为 post-route 起点的最小正式行为链是：
- admitted transform input selector
- first-slice readiness evaluator
- narrow capture-batch lifecycle helper
- first `sales_orders` serving projection contract
- first `capture -> transform -> serving` path

它当前只覆盖：
- `/erp/orders`
- `sales_orders`

它当前不代表：
- `sales_order_items` 已迁移完成
- inventory 已迁移完成
- source surface 已盘点完成
- runtime/internal entrypoint 已定稿
- broader orchestration 已开始

## 当前缺口：两类问题

### 1. Database / Domain Migration Completeness

这一类关注的是：
- 哪些 domain surfaces 只有 persistence surface，还没有 contract/path
- 哪些已落地 contract/path 还缺 hardening
- 哪些 serving / transform / dual-db 语义还没盘点完成

当前主要缺口：
- `sales_order_items` 只有 persistence surface，没有 serving projection contract，也没有 path
- `inventory_current` / `inventory_daily_snapshot` 只有 persistence surface，没有 contract，也没有 path
- 当前 first `sales_orders` path 的 hardening 仍未形成完整 post-route 盘点
- dual-db success/failure / replay / observability 仍只覆盖局部 truth
- “数据库已落地对象”和“domain 已完成迁移对象”之间还没有一份明确 completeness map

### 2. Menu / Source Exploration Completeness

这一类关注的是：
- 上游菜单 / endpoint / payload family 是否已探索完成
- 哪些 source surfaces 已经被 current first path 吸收
- 哪些 source surfaces 只是 reference / research
- 哪些还没有进入正式 mapping

当前主要缺口：
- `/erp/orders` 之外，还没有一份 repo-owned source-surface completeness map
- 当前缺少“menu -> endpoint -> payload -> slice”系统盘点文档
- 当前 research support 只有 minimal skeleton，不等于 source exploration 已完成
- 当前 legacy reference 里有很多菜单、台账、runbook、capture 路线资料，但 repo 里还没有把它们整理成新的 completeness track

## 为什么新结构更贴近完整迁移

如果 post-route 只盯着 hardening 当前 first path，会有两个问题：
- 它会把注意力集中在“让已落地的一条链更稳”，但不会自然逼出“还有哪些 domain/source surface 没迁完”
- 它会让 `sales_order_items`、inventory、菜单盘点、payload 盘点看起来像零散 side quest，而不是完整迁移主线的一部分

改成两条子轨后：
- `database / domain migration completeness track` 负责回答“数据库与业务域还差哪些正式 contract/path”
- `menu / source-surface completeness track` 负责回答“上游菜单、endpoint、payload、slice 还有哪些没探索/没映射”

这样后续每个实现包都会更清楚自己服务的是哪一块“完整迁移缺口”，而不只是“继续补一点当前 first path”

## 新的 planning 结构

### 主线名称

- `migration-completeness mainline`

### 子轨 A：database / domain migration completeness

目标：
- 建立 repo 内“已落地 / persistence-only / contract-missing / path-missing / deferred”的 domain completeness 盘点

当前应覆盖：
- `sales_orders`
- `sales_order_items`
- `inventory_current`
- `inventory_daily_snapshot`
- current first path 的 hardening gap

### 子轨 B：menu / source-surface completeness

目标：
- 建立 repo 内“已探索 / 已映射 / reference-only / 待探索”的 source completeness 盘点

当前应覆盖：
- menu
- endpoint
- payload family
- slice mapping
- 哪些 source 只存在于 legacy reference / research support skeleton

## 下一轮 planning 先该产出什么文档

推荐先产出两份盘点 / mapping 文档，再进入新的实现包。

### 文档 1

文档名建议：
- `domain-migration-completeness-map.md`

作用：
- 盘点当前数据库 / domain surfaces 的迁移完成度

至少回答：
- 哪些对象只是 persistence surface
- 哪些对象已经有 serving projection contract
- 哪些对象已经有 capture-to-serving path
- 哪些对象已经 hardening 到什么程度
- 哪些对象明确 deferred

### 文档 2

文档名建议：
- `source-surface-completeness-map.md`

作用：
- 盘点当前 menu / endpoint / payload / slice 的探索完成度

至少回答：
- 哪些 source/menu 已被 repo-owned docs 明确记录
- 哪些 endpoint/payload family 已映射到 current slice
- 哪些 source surface 还停留在 legacy reference / research support
- 哪些 source completeness 仍然空白

## 新推荐拆包顺序

建议拆成 5 个小包。

### 包 1

包名：
- `docs: map domain migration completeness`

一句话目标：
- 先把 database / domain migration completeness 盘清楚。

边界：
- docs-only
- 不改 formal truth
- 不新增 behavior

输入：
- 当前 formal docs
- 当前已落地 model/schema/crud/service/migration surface

输出：
- 一份 domain completeness map

风险：
- 容易把 persistence surface 误写成 behavior completeness

### 包 2

包名：
- `docs: map source-surface completeness`

一句话目标：
- 把 menu / endpoint / payload / slice 的 source completeness 盘清楚。

边界：
- docs-only
- 不改 formal truth
- 不新增 behavior

输入：
- 当前 formal docs
- legacy reference index
- research support current surface

输出：
- 一份 source-surface completeness map

风险：
- 容易把 reference 资料误写成 current formal truth

### 包 3

包名：
- `docs: answer first-path hardening minimums`

一句话目标：
- 把 current first path 的 dual-db / failure / replay / observability minimums 收紧成 repo-owned truth。

边界：
- docs-only 或 docs+guardrail-only
- 不新增 behavior

输入：
- current first path docs / tests / code
- 前两份 completeness maps

输出：
- hardening minimums

风险：
- 容易提前写死 broader retry / orchestration

### 包 4

包名：
- `feat: add sales_order_items serving projection contract`

一句话目标：
- 在 completeness maps 和 hardening minimums 之后，优先推进最接近 current first slice 的下一条 domain contract。

边界：
- 只做 `sales_order_items`
- 不扩 inventory
- 不做 broader runtime/orchestration

输入：
- `/erp/orders` domain context
- existing `sales_order_items` persistence surface

输出：
- first `sales_order_items` serving projection contract

风险：
- `order_id` 与 `sales_orders` 的关系仍需收紧说明

### 包 5

包名：
- `feat: add first internal projection run entrypoint`

一句话目标：
- 在 current first path 已被 harden 且下一条 domain contract 已开局后，再引入 internal-only trigger。

边界：
- internal-only
- 不做 public runtime API
- 不做 scheduler / reservation / locking

输入：
- current first path
- hardening minimums

输出：
- 一个正式 internal entrypoint

风险：
- 如果放得太早，会把 coordination 问题提前抬上来

## 当前不推荐先做的方向

### 不推荐先直接开 inventory 主线

原因：
- inventory 更像第二条独立 domain mainline
- 它需要新的 completeness / snapshot / policy 解释
- 它不如 `sales_order_items` 那样自然延续 current `/erp/orders` slice

### 不推荐先直接开 runtime route 入口

原因：
- 当前 repo 里还没有把 source completeness 和 domain completeness 盘清楚
- 过早加入口，会让 current first path 过早承担更强的 operator-facing 语义

### 不推荐先开始 broader orchestration

原因：
- formal docs 当前仍明确限制 broader orchestration
- post-route 现在更该先盘“还有什么没迁完”，而不是先做协调层设计

## 最推荐的下一包提示词

```text
请基于 black-tonny-backend-base 当前最新 main，只做 planning-only / docs-only 工作，推进 post-route mainline 的第一包：

包名：
docs: map domain migration completeness

目标：
在不新增 behavior、runtime API、migration、model、schema、crud、service 的前提下，
盘点当前 repo 在 database / domain migration completeness 上的真实状态。

重点回答：
- 哪些对象只是 persistence surface
- 哪些对象已经有 projection contract
- 哪些对象已经有 capture-to-serving path
- 哪些对象仍缺 contract/path/hardening
- 哪些对象明确 deferred

边界：
- docs-only
- 不改 formal boundary docs
- 不把 reference / archive 材料写成 current truth

完成后请给出低 token planning handoff：
1. PR 基本信息
2. 一句话目标
3. 盘清了哪些 completeness gap
4. 仍未定稿的点
5. 风险自检
6. 一组 pbcopy 审查命令
```
