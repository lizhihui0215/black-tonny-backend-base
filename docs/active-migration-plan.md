# Active Migration Plan

状态：planning-only / working document

这份文档不是 formal source of truth。

formal truth 仍以以下文档为准：
- [README.md](../README.md)
- [docs/README.md](./README.md)
- [docs/](./README.md) 下各 formal boundary docs

这份文档只用于长期执行规划，避免迁移路线、当前包状态和后半段执行底稿依赖聊天上下文。

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
| 8 | `feat: add admitted transform input selector` | `in-progress` | 基于 formal persisted facts 增加第一条 admitted input selector。 |
| 9 | `feat: add transform readiness evaluator and batch lifecycle helper` | `planning` | 增加第一条 readiness evaluator 与窄职责 lifecycle helper。 |
| 10 | `feat: add first serving projection contract` | `planning` | 增加第一条最窄 slice 的 serving projection contract。 |
| 11 | `feat: add first capture-to-serving projection path` | `planning` | 打通第一条最窄的 `capture -> transform -> serving` 正式行为链。 |

## 当前包

当前包：
- `#8 feat: add admitted transform input selector`

目标：
- 基于前面已收紧的 docs truth，落第一条最窄 slice 的 admitted transform input selector。

边界：
- 只落 admitted transform input selector 的最小行为闭环
- 不引入 readiness evaluator
- 不引入 lifecycle executor
- 不引入 orchestration
- 不引入 serving behavior
- 不引入 route registry
- 不引入 maturity board
- 不引入 batch orchestration service

当前已拍板规则：
- 优先最小闭环，不预埋大设计
- admitted input minimums 当前只依赖已落地 persisted capture-side facts
- `analysis_batches` 当前不是 admitted transform input 的必需前置条件
- `batch_status` 本身不是 formal admission marker，`transformed_at` 不是 admission proof
- selector 当前只做 admitted input 选择，不偷带 readiness / transition / serving contract
- 不提前定义第 9/10 包之后才应定稿的 retry / overwrite / serving contract
- 只有当 current truth 会失真时，才最小同步 formal docs

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

- `#9 feat: add transform readiness evaluator and batch lifecycle helper`
  - 基于 admitted input selector 输出，增加第一条 readiness evaluator 与窄职责 lifecycle helper
  - 仍保持最窄 slice，不引入 serving projection runtime

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
