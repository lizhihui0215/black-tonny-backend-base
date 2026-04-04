# Active Migration Plan

状态：planning-only / working document

这份文档不是 formal source of truth。

formal truth 仍以以下文档为准：
- [README.md](../README.md)
- [docs/README.md](./README.md)
- [docs/](./README.md) 下各 formal boundary docs

这份文档只用于长期执行规划，避免迁移路线、当前包状态和后半段执行底稿依赖聊天上下文。

当前新路线的 authoritative 起点另行记录在：
- [clean-mainline-charter.md](./clean-mainline-charter.md)

这份文档当前主要保留为：
- 旧 11 包路线记录
- 既有执行底稿
- existing planning assets / inputs 的收口说明

它不是新 milestone 路线的 authoritative 编号入口。

## 当前 11 包迁移路线

| # | Package | Status | 一句话目标 |
| --- | --- | --- | --- |
| 1 | `docs: align root readme current state` | `merged` | 对齐顶层 README 的 current state 与当前阅读路径。 |
| 2 | `feat: add analysis batches formal surface` | `merged` | `analysis_batches` 的最小 formal persistence surface 已在 main 落地。 |
| 3 | `feat: add sales projection persistence surface` | `merged` | `sales_orders` 与 `sales_order_items` 的最小 persistence surface 已在 main 落地。 |
| 4 | `feat: add inventory persistence surface` | `merged` | `inventory_current` 与 `inventory_daily_snapshot` 的最小 persistence surface 已在 main 落地。 |
| 5 | `docs+test: align expanded capture formal surface` | `merged` | 已把前面已落地的 capture 对象同步到 docs、mapping 和 guardrail tests。 |
| 6 | `docs: answer transform admission and readiness minimums` | `merged` | 已在行为代码开始前把 admitted input 与 readiness 的最小 docs truth 收紧。 |
| 7 | `docs: answer transform lifecycle transition minimums` | `merged` | 已在行为代码开始前把 transform lifecycle transition 的最小 docs truth 收紧。 |
| 8 | `feat: add admitted transform input selector` | `merged` | 已基于 formal persisted facts 增加第一条 admitted input selector。 |
| 9 | `feat: add transform readiness evaluator and batch lifecycle helper` | `merged` | 已增加第一条 readiness evaluator 与窄职责 lifecycle helper。 |
| 10 | `feat: add first serving projection contract` | `merged` | 已增加第一条最窄 slice 的 serving projection contract。 |
| 11 | `feat: add first capture-to-serving projection path` | `merged` | 已打通第一条最窄的 `capture -> transform -> serving` 正式行为链。 |

## 当前状态

当前 11 包主路线状态：
- 已完成并收口
- 当前 formal truth 已包含：
  - 第一条 `sales_orders` serving projection contract
  - 第一条最窄 `capture -> transform -> serving` path
  - 对应 rollback / failure docs guardrail

post-route planning 另行记录在：
- [post-route-mainline-planning.md](./post-route-mainline-planning.md)

当前 planning-only 结论：
- 当前 `main` 上的 11 包成果保留为 `既有行为资产`
- 它们是新路线的基线，不是新 milestone 编号的一部分
- 新 milestone 编号从 [clean-mainline-charter.md](./clean-mainline-charter.md) 定义的 `M1-PR1` 重新开始
- 新路线编号、默认顺序与 package 起点统一以 [clean-mainline-charter.md](./clean-mainline-charter.md) 为准
- 当前新路线应统一复用的 planning vocabulary 是：
  - [clean-mainline-charter.md](./clean-mainline-charter.md)
  - [formal-planning-reference-boundary-and-exploration-taxonomy.md](./formal-planning-reference-boundary-and-exploration-taxonomy.md)
- 当前 repo-owned source inventory baseline 维护在：
  - [source-surface-completeness-map.md](./source-surface-completeness-map.md)
- 当前 `/erp/orders` adjacent payload-family baseline 维护在：
  - [orders-adjacent-payload-family-baseline.md](./orders-adjacent-payload-family-baseline.md)
- 当前 `/erp/orders` adjacent payload semantics baseline 维护在：
  - [orders-adjacent-payload-semantics-baseline.md](./orders-adjacent-payload-semantics-baseline.md)
- 当前 `/erp/orders` adjacent contract-entry minimums baseline 维护在：
  - [orders-adjacent-contract-entry-minimums.md](./orders-adjacent-contract-entry-minimums.md)
- 当前 `/erp/orders` source-accuracy minimums baseline 维护在：
  - [orders-source-accuracy-minimums.md](./orders-source-accuracy-minimums.md)
- 当前 `/erp/orders` adjacent source-evidence baseline 维护在：
  - [orders-adjacent-source-evidence-baseline.md](./orders-adjacent-source-evidence-baseline.md)
- 当前 `/erp/orders` source-accuracy revisit baseline 维护在：
  - [orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md)
- 当前 `/erp/orders` adjacent single-target mapping minimums baseline 维护在：
  - [orders-adjacent-single-target-mapping-minimums.md](./orders-adjacent-single-target-mapping-minimums.md)
- 后续 source inventory、payload semantics、accuracy、migration planning 包都应复用这组 boundary / taxonomy 约束
- 这份文档不再继续拆第 11 包之后的实现包
- 第 11 包之后的新主线已改为更贴近完整迁移的 `migration-completeness mainline`
- 这条新主线拆成两条 planning 子轨：
  - `database / domain migration completeness`
  - `menu / source-surface completeness`
- `hardening-first` 不再单独作为唯一主线，而是新的 completeness 结构中的一个子轨
- 第 11 包之后的新主线候选、优先级、拆包方式与风险，统一收口到新的 post-route planning note
- 当前 post-route planning 的第一包输出是：
  - [domain-migration-completeness-map.md](./domain-migration-completeness-map.md)
- 当前 post-route planning 的第二包输出是：
  - [source-surface-completeness-map.md](./source-surface-completeness-map.md)
- 当前针对 landed first path 的 hardening planning 输出是：
  - [first-path-hardening-minimums.md](./first-path-hardening-minimums.md)
- 上述 post-route outputs 当前只保留为 existing planning assets / inputs
- 它们不是当前 milestone 路线里的已编号包序列
- 当前如需继续推进新的 milestone 路线：
  - 先从 [clean-mainline-charter.md](./clean-mainline-charter.md) 开始
  - 不再直接从这份文档续写新的 milestone 编号或 next package 编号

## 第 8-11 包最终执行底稿

这一节只服务后半段行为链执行，不覆盖 formal docs。

### 统一前提

- 以 `black-tonny-backend-base` 当前 formal docs 为 truth boundary
- 不把 legacy repo 当实现真源
- 默认第 2-7 包先完成，再进入第 8 包实现

### 第 8 包：admitted transform input selector

只允许依赖的 persisted facts：
- `capture_batches.capture_batch_id`
- `capture_batches.batch_status`
- `capture_batches.transformed_at`
- `capture_batches.error_message`
- `capture_endpoint_payloads.capture_batch_id`
- `capture_endpoint_payloads.source_endpoint`
- `capture_endpoint_payloads.payload_json`
- `capture_endpoint_payloads.checksum`
- `capture_endpoint_payloads.pulled_at`

必要时可读但不是默认真源：
- `capture_endpoint_payloads.route_kind`
- `capture_endpoint_payloads.page_cursor`
- `capture_endpoint_payloads.page_no`
- `capture_endpoint_payloads.request_params`

admitted source status 真源约束：
- 只有当第 6/7 包 docs 已正式把 `captured` 写成 admitted source status 时，第 8 包代码才允许把 `batch_status == "captured"` 当真源
- 在这条 docs truth 正式落地前，第 8 包不得从任何现有 status 值隐式推 admission truth

输入：
- `capture_batch_id`
- persisted `capture_batches` row
- linked persisted `capture_endpoint_payloads` rows

输出：
- 第一条行为链所需的 admitted input bundle / snapshot

不做什么：
- 不做 readiness 判断
- 不做 lifecycle 写入
- 不做 serving projection 写入
- 不接 route registry、maturity board、external sample、tmp/output、docs parser

依赖前置包：
- 第 5 包
- 第 6 包
- 第 7 包

### 第 9 包：transform readiness evaluator and batch lifecycle helper

最小 readiness 输入：
- 一个 admitted batch snapshot
- 该 batch 关联的 admitted payload snapshots
- 一条明确的 first-slice projection definition

最小输入字段：
- batch side:
  - `capture_batch_id`
  - `batch_status`
  - `transformed_at`
  - `error_message`
- payload side:
  - `source_endpoint`
  - `payload_json`
  - `checksum`
  - `pulled_at`

只回答：
- 当前 admitted inputs 是否足以进入第一条最窄 projection slice

第一条行为链只允许的状态迁移：
- `captured -> transformed`
  - 成功时只写：
    - `batch_status = "transformed"`
    - `transformed_at = now`
  - 成功时不清空 `error_message`
- `captured -> failed`
  - 失败时写：
    - `batch_status = "failed"`
    - `error_message` 覆盖写最新错误
  - 不写 `transformed_at`

输入：
- 第 8 包输出的 admitted input bundle

输出：
- 一个 readiness decision
- 一个窄职责 lifecycle write contract

不做什么：
- 不写 serving projection
- 不做 retry / reopen / resume
- 不做 multi-slice completeness
- 不引入 worker ownership / reservation / locking

依赖前置包：
- 第 8 包
- 第 6 包
- 第 7 包

### 第 10 包：first serving projection contract

第一条最窄 slice：
- `sales_orders` only

硬要求：
- 必须明确定义 `sales_orders` projection 的 identity / upsert key
- 必须明确定义第一条 slice 的最小去重 / 覆盖策略

输入：
- 第一条 `sales_orders` slice 的 transform-ready normalized facts

输出：
- `sales_orders` 的 serving projection contract
- 对应最小 schema / persistence contract / targeted tests
- 明确的 identity / upsert key
- 明确的最小去重 / 覆盖策略

不做什么：
- 不做 `sales_order_items`
- 不做 inventory
- 不做 dashboard summary runtime
- 不做 end-to-end orchestration

依赖前置包：
- 第 3 包
- 第 6 包
- 第 7 包
- 第 9 包

### 第 11 包：first capture-to-serving projection path

输入：
- 第 8 包 admitted selector 输出
- 第 9 包 readiness decision 与 lifecycle helper
- 第 10 包 `sales_orders` projection contract

输出：
- 第一条最窄的 `capture -> transform -> serving` projection path
- first-slice serving writes
- 允许的 batch state transition writes

不做什么：
- 不扩到 `sales_order_items`
- 不扩到 inventory
- 不扩到 dashboard summary API
- 不扩到第二条 source slice
- 不扩到 retry / resume / scheduling

依赖前置包：
- 第 3 包
- 第 8 包
- 第 9 包
- 第 10 包

## 已拍板规则

- 上面的 11 包路线是当前 active mainline
- 第 1 包可快进
- 第 2-11 包默认先 planning 再实现
- 第 2 / 3 / 4 包统一采用同一实现模板：
  - model
  - schema
  - CRUD
  - migration
  - targeted tests
  - 只有 current truth 会失真时才最小同步相关 formal docs
- 第 5 包只做收口：
  - 只同步已落地对象到 docs / mapping / tests
  - 不新增 persistence object
- 第 8-11 包的 planning 必须明确：
  - 输入是什么
  - 输出是什么
  - 不做什么
  - 依赖前面哪几包
- 当前默认协作模式是“主题包推进”，不是继续拆过小 PR

## 下一步候选

- 当前 11 包主路线已完成
  - 后续如继续推进当前 milestone 路线，先从 [clean-mainline-charter.md](./clean-mainline-charter.md) 进入
  - [post-route-mainline-planning.md](./post-route-mainline-planning.md) 当前只保留为 framing / historical context，不再单独决定 next package sequencing
  - 现有 completeness / hardening docs 仅作为 existing planning assets / inputs 使用

## 明确禁区 / 不做事项

- 不把这份文档当成 formal truth
- 不把 legacy docs 正文搬到这里
- 不整目录复制 legacy repo
- 不把 capture code 和 research support code 混到同一包
- 不把大规模 docs 重写和行为代码混在一个包里
- 第 6/7 包之前，不启动 transform behavior
- 第 8-10 包未定义完成前，不启动 serving behavior
- 不引入：
  - 第 8-11 包之外的 transform behavior
  - 第 10-11 包之外的 serving behavior
  - admissions 全量迁移
  - route registry
  - maturity board
  - evidence chain
  - tmp/output 作为 runtime input
  - docs parser 作为 runtime input
