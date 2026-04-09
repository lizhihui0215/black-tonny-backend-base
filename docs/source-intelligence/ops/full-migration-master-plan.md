# Black Tonny Source-Intelligence 全量迁移主计划（2026-04-07）

> Canonical path: `docs/source-intelligence/ops/full-migration-master-plan.md`
>
> workspace 根目录下的 `black_tonny_source_intelligence_master_plan_2026-04-07.md` 现在只保留跳转说明；后续状态同步、handoff、ChatGPT review、Codex 执行都以这份仓库内版本为准。

## 0. 当前执行状态（repo truth）

- `last checked`: `2026-04-09 23:16 (Asia/Shanghai)`
- `repo inspected`: `/Users/lizhihui/Workspace/black-tonny-workspace/black-tonny-backend-base`
- `current worktree branch`: `main`
- `landed baseline`: `docs: add source-intelligence ops baseline (#79)`
- `latest landed control-plane update`: `docs: require master plan status sync after each round (#80)`
- `current official milestone / PR`: `none`
- `status`: `NOT STARTED / no official active package`
- `next allowed step`: `close the repo-canonical master-plan migration round, then when execution resumes start PR-0: docs: reconcile post-merge source-intelligence ops state`
- `current main / origin main truth`: `main` 与 `origin/main` 当前都停在 `92413d6 docs: require master plan status sync after each round (#80)`
- `active package files currently modified in worktree`: `AGENTS.md`、`docs/README.md`、`docs/source-intelligence/AGENTS.md`、`docs/source-intelligence/README.md`、`docs/source-intelligence/ops/README.md`、`docs/source-intelligence/ops/full-migration-master-plan.md`、`docs/source-intelligence/ops/handoff-prompt.md`
- `local draft files detected in current worktree`: `none`

### 0.1 最新标准状态同步块

> 这是当前唯一最新实例。第 12.2 节只是字段模板；每个有效轮次结束前，必须先回填这里，再视为这轮闭环完成。

```text
当前状态同步（当前唯一最新实例）：

- checked at: 2026-04-09 23:16 (CST)
- current milestone: none
- current PR: none
- PR title: none
- status: NOT STARTED / collaboration-control hardening only
- merged baseline: docs: add source-intelligence ops baseline (#79); docs: require master plan status sync after each round (#80)
- repo truth summary: source-intelligence 正式执行主线仍未开包；本轮把全量迁移主计划迁入 backend-base 仓库 canonical 路径，并把控制面引用统一切到仓库内版本。
- allowed files in this PR: none (当前没有官方 source-intelligence migration PR 处于 active 状态)
- changed files: docs/source-intelligence/ops/full-migration-master-plan.md; AGENTS.md; docs/source-intelligence/AGENTS.md; docs/source-intelligence/ops/handoff-prompt.md; docs/source-intelligence/ops/README.md; docs/source-intelligence/README.md; docs/README.md; /Users/lizhihui/Workspace/black-tonny-workspace/black_tonny_source_intelligence_master_plan_2026-04-07.md (redirect only)
- validation: targeted text verification on the canonical master plan plus six repository control-plane/index docs; no runtime/code changes; no tests run
- blockers / open questions: PR-0 仍未正式开始；后续任何有效轮次结束前，都必须继续回写仓库内 canonical 主计划的最新状态同步块
- next allowed step: 以仓库内 canonical 主计划作为当前唯一最新实例；当正式恢复迁移执行时，从 PR-0: docs: reconcile post-merge source-intelligence ops state 开始
- review verdict: pending external review
- action requested from Codex: 新开 ChatGPT / Codex 窗口时先复用仓库内 canonical 主计划和这份最新状态同步块；不要再使用根目录旧文件作为真源
- 我这次希望你重点 review 的问题: 主计划迁入仓库后，控制面引用与新窗口恢复流程是否已经收敛到单一真源
```

### 当前 repo truth 补充说明

- 当前按“尚未开始”处理：还没有任何官方 active package 进入 worktree。
- `PR-0` 仍然是初始状态下的首包；但在真正起草前，不应把它写成 `ACTIVE`。
- `PR-1` 及其后的包都还不能按已开始计算；只有在 `PR-0` 真正 merge 进 `main` 后，才允许进入下一包。
- 当前文档默认不假设存在本地执行分支、官方 worktree 改动，或已起草但未 merge 的包。
- 当前 worktree 里的控制面文档改动只用于补协作闭环，不应被误写成 source-intelligence 官方 active package 已开始。

### 初始状态下的首包预设（尚未开始）

- `first PR title`: `docs: reconcile post-merge source-intelligence ops state`
- `首包职责`: 只做 post-merge bookkeeping 校准；不进入 backlog/protocol、family dossier、field、relation、readiness、UT、runtime、support code
- `首包允许修改`:
  - `docs/source-intelligence/ops/current-main-state.md`
  - `docs/source-intelligence/ops/review-gain-ledger.md`
  - `docs/source-intelligence/ops/milestone-board.md`
- `首包明确排除`:
  - `docs/source-intelligence/ops/quality-gates.md`
  - `docs/source-intelligence/ops/object-family-backlog.md`
  - `docs/source-intelligence/apis/receipt-confirmation-seldocconfirmlist-api-dossier.md`
  - `docs/source-intelligence/fields/receipt-confirmation-seldocconfirmlist-core-field-dictionary.md`
- `首包退出条件`:
  - 三个 PR-0 文件全部转成 merged-main truth
  - 不再出现 pre-merge 条件语气
  - 不虚构独立 `docs/tests` merge 事实

## 1. 这份文档的用途

这份文档用于在后续新会话里，快速恢复以下事实：

- 当前项目不是“把旧仓整个搬过来”，而是“把旧仓的高价值知识迁进新仓，同时保持新仓结构干净”。
- 当前主线是 `black-tonny-backend-base` 的 `docs/source-intelligence/**`，不是旧仓 `black-tonny-backend` 的运行结构。
- 当前推进方式必须是：单线程、强 gate、强纠偏、低 token、低范围漂移。
- 当前“完成迁移”的定义，不是复制旧仓所有脚本和目录，而是让旧仓所有高价值内容都进入明确归宿：
  1. 被重写成 repo-owned 主输出；或
  2. 被降级收口到 reference / extract；或
  3. 被明确标记为 dropped / deferred / not-adopted。

### 1.1 发给 ChatGPT review 时的推荐阅读顺序

建议对方按这个顺序阅读：

1. 第 3 节：先确认“完成迁移”到底是什么意思
2. 第 4 节：再确认 family 分层和默认输出合同
3. 第 6 节：再看总里程碑与 PR 拆分
4. 第 7 节和第 8 节：再看纠偏协议、truth 规则和结构边界
5. 第 0 节：最后再看当前执行状态快照
6. 第 13 节：如果需要理解执行入口，再看首包提示词样例

原因：

- 第 3 / 4 / 6 / 7 / 8 节是主计划主体，优先级高于当前状态快照。
- 第 0 节是可变的 sync snapshot，不应该反过来覆盖主计划定义。
- 第 13 节是执行样例，不是主计划本体。

### 1.2 发给 ChatGPT review 时要先说清的边界

- 这份文档的 review 对象是 `source-intelligence knowledge migration plan`，不是完整 runtime 交付计划。
- 如果 reviewer 讨论 runtime gap，应明确标记为“范围外但值得提前提示”的风险，而不是把它混进本轮 must-have。
- reviewer 优先检查的内容应该是：完成定义、PR 拆分、gate 设计、truth discipline、completion audit 是否闭环。
- reviewer 不应把“复制旧仓结构”当成默认目标；本计划的目标是把高价值知识迁成 repo-owned knowledge system。

---

## 2. 最新 sources 的结论（实物基线）

### 2.1 新仓 `black-tonny-backend-base`

当前新仓已经具备：

- 一个克制的 FastAPI dual-database base
- 很小的 runtime API 面：`/api/v1/health`、`/api/v1/ready`、`/api/v1/login`、`/api/v1/logout`、`/api/v1/users`、`/api/v1/tiers`、`/api/v1/rate_limits`、`/api/v1/tasks`
- `docs/source-intelligence/` 主输出结构：
  - `migration-charter.md`
  - `legacy-source-intelligence-inventory-baseline.md`
  - `apis/`
  - `fields/`
  - `relations/`
  - `serving-readiness/`
  - `ops/`
- 已存在的协作脚本：
  - `scripts/copy-changed-files`
  - `scripts/copy-pr-diff`
  - `scripts/copy-pr-template-draft`
  - `scripts/copy-migration-anchors`
  - `scripts/_collab_common.py`
- 已存在的最小 research support skeleton：
  - `src/app/services/research/erp_research_service.py`
  - `src/app/services/research/page_research.py`
  - `src/app/services/research/menu_coverage.py`

当前新仓已经明确的边界：

- `capture` 是 formal landing layer，不是 research evidence warehouse。
- legacy flat `app/services` / `scripts` / `tmp` / `output` 不能机械搬进来。
- `docs/source-intelligence/**` 是知识主输出位；`docs/reference/legacy-backend/extracts/**` 是 pre-rewrite 隔离区。
- `ops/` 是控制面，不是第五种正文资产类型。

### 2.2 旧仓 `black-tonny-backend`

旧仓当前是“知识矿山”，而不是目标结构。它保留了五大域、35 条路线和大量高价值知识资产：

- cross-cutting
  - `docs/erp/api-maturity-board.md`
  - `docs/erp/capture-route-registry.md`
  - `docs/erp/capture-ingestion-roadmap.md`
  - `docs/erp/page-research-runbook.md`
- research / evidence / admission
  - `app/services/research/*.py`
  - `app/services/sales_capture_admission_service.py`
  - `scripts/analyze_yeusoft_*`
- 分域路线（来自 maturity board）
  - 销售：13
  - 库存：9
  - 会员：5
  - 储值：3
  - 流水/单据：5

### 2.3 前端 `black-tonny-frontend`

前端已经明确依赖这些 backend 路径：

- `GET /api/manifest`
- `GET /api/pages/{page_key}`
- `GET /api/dashboard/summary`
- `POST /api/assistant/chat`
- `/api/auth/*`
- `/api/user/info`

这说明 runtime gap 一定要做，但不能先于 source-intelligence 全量迁移主线直接开大代码包。

---

## 3. “全量迁移完成” 的正式定义

### 3.1 本计划里的“完成”是什么意思

本计划里的“完成迁移”定义为：

1. 旧仓五大域的 35 条路线，全部进入明确 fate：
   - `main-source family`
   - `snapshot family`
   - `reconciliation-only`
   - `research-only`
   - `blocked / deferred`
   - `not-adopted`
2. 旧仓高价值知识资产（route registry、maturity board、page research、evidence/admission、ledger、runbook、analysis outputs）全部进入明确 fate：
   - 重写吸收进 `docs/source-intelligence/**`
   - 降级到 `docs/reference/legacy-backend/extracts/**`
   - 明确 dropped / 不迁
3. 对每一个值得进入 repo-owned 主输出的对象，至少有与其价值相匹配的知识资产：
   - `API dossier`
   - `field dictionary`（如适用）
   - `relation doc`（如适用）
   - `serving-readiness doc`
4. 对 snapshot / blocked / not-adopted 家族，不再强行补全四件套；而是以更窄、更真实的输出完成迁移。
5. 迁移后，新仓仍然保持当前边界，不重新变成 legacy 风格仓库。

### 3.2 不属于本计划的“完成”

以下不算本计划必须完成的事情：

- 复制旧仓全部 Python scripts
- 复制旧仓 flat `app/services`
- 复制 `tmp/**` / `output/**` 目录树
- 让所有 legacy runtime API 立刻进入 `black-tonny-backend-base`
- 把 reference / planning 直接升级成 runtime truth

### 3.3 这条定义的默认结论

因此，“把所有内容迁移完成”的正确理解是：

- **把所有高价值内容迁成可维护的 repo-owned knowledge system**
- **而不是把所有旧文件和旧结构原样搬过来**

---

## 4. 迁移对象分层（决定 PR 数量的核心规则）

### 4.1 Type A：关系丰富的主源 family

适用对象：

- `GetDIYReportData(E004001008_2)`
- `SelSaleReport`
- `SelDocConfirmList`
- `SelDocManageList`
- `SelOutInStockReport`
- `SelDeptStockWaitList`
- `SelVipInfoList`
- `SelVipReturnVisitList`
- `储值卡明细 / GetDIYReportData`
- `商品资料 / SelWareList`
- `客户资料 / SelDeptList`

默认迁移输出：

- dossier
- field dictionary
- relation doc
- serving-readiness

但如果对象已部分落地，则只补缺口。

### 4.2 Type B：snapshot / reconciliation family

适用对象：

- `SelDeptSaleList`
- `商品销售情况 / SelSaleReportData`
- `门店销售月报 / DeptMonthSalesReport`
- 三个 `SelStockAnalysisList` 变体
- `SelDeptStockAnalysis`
- `SelDeptStockSaleList`
- `SelInSalesReportByDay`
- `SelInSalesReport`
- `SelVipAnalysisReport`
- `SelVipSaleRank`
- `储值卡汇总 / GetDIYReportData`
- `储值按店汇总 / GetDIYReportData`
- `每日流水单 / SelectRetailDocPaymentSlip`

默认迁移输出：

- dossier（更窄）
- serving-readiness（明确 snapshot / reconciliation / not-for-serving）
- 如确有必要，再补 very small field note

### 4.3 Type C：blocked / deferred family

适用对象：

- `退货明细 / SelReturnStockList`
- `门店盘点单 / store_stocktaking_diff_records`
- 其他“主列表已知，但二级动作链断裂”的家族

默认迁移输出：

- blocker-oriented dossier
- relation evidence（解释断裂点）
- serving-readiness（说明 why deferred / why blocked）

### 4.4 Type D：not-adopted / config / page-baseline

适用对象：

- `参数设置 / page_baseline`
- `导购员设置 / page_baseline`
- `小票设置 / page_baseline`
- `店铺定位 / GetControlData`
- `店铺零售清单 / GetDIYReportData`
- `VIP卡折扣管理 / 待识别`

默认迁移输出：

- 不给它们补四件套
- 只在全局 backlog / completion audit 中明确：
  - 为什么不迁
  - 为什么暂缓
  - 是否需要 future revisit

---

## 5. PR 包装原则（优化 PR 数量，同时防止低效）

### 5.1 每个 PR 只允许一个主目标

允许：

- 一个 family 的 relation 缺口
- 一个 family 的 readiness 缺口
- 一个 domain cluster 的 snapshot pack
- 一个 ops/backlog/board 校准包

不允许：

- 在 docs-only PR 里顺手补 code
- 在 family PR 里横向开第二个 family
- 在 planning/backlog PR 里顺手补正文资产

### 5.2 PR 类型与目标大小

- `docs-only / control-plane`
  - 目标文件数：3–6
  - 目标：校准 current truth / board / backlog / protocol
- `docs-only / family-core`
  - 目标文件数：2–5
  - 目标：一个 family 的 dossier/field 或 relation/readiness
- `docs-only / snapshot-pack`
  - 目标文件数：2–6
  - 目标：同类 snapshot family 一次性收口
- `code-bearing / helper`
  - 目标文件数：1–4
  - 只允许非常小的协作脚本，不碰 runtime

### 5.3 输出合同（每次都一样）

Codex 每次必须输出：

1. 本包最小范围说明
2. changed files
3. 每个文件改了什么
4. validation
5. risks
6. unified diff 摘要
7. 可复制 patch / diff
8. 下一包建议（1 个，不能多）

并优先使用：

- `./scripts/copy-changed-files --mode worktree --no-clipboard`
- `./scripts/copy-pr-diff --mode worktree --no-clipboard`
- `./scripts/copy-pr-template-draft --mode worktree --no-clipboard --goal-hint "..."`

---

## 6. 优化后的总里程碑与 PR 计划

> 这是当前建议的 **26 个核心 PR + 1 个可选脚本 PR**。对于“五大域 + 35 条路线 + cross-cutting assets” 这个范围，这个数量是合理的：足够细，不会把真相混掉；也不至于拆成 40+ 个低效碎 PR。

状态图例：

- `LANDED`：已 merge，已成为 repo truth
- `ACTIVE`：当前官方 active package，已在 worktree 起草，但未 merge
- `BLOCKED`：存在前置 gate，前置 merge 前不能进入
- `NOT STARTED`：尚未进入 worktree，也不能按已开始计算

硬规则：
- `local worktree drafts do not equal merged progress`

### Milestone 0 [NOT STARTED]：校准 current truth，收紧执行协议（2 PR）

#### PR-0 [NOT STARTED]
`docs: reconcile post-merge source-intelligence ops state`

目标：
- 只校准 current main truth
- 不进入正文资产

允许修改：
- `docs/source-intelligence/ops/current-main-state.md`
- `docs/source-intelligence/ops/review-gain-ledger.md`
- `docs/source-intelligence/ops/milestone-board.md`

退出条件：
- 三者全部转成 merged-main truth
- 不再出现 pre-merge 条件语气
- 不虚构独立 merge 事实

#### PR-1 [NOT STARTED]
`docs: add source-intelligence full-migration backlog and codex execution protocol`

前置 gate：
- `PR-0` merge 后才允许进入

目标：
- 把“全量迁移”正式写成 repo-owned backlog 和执行协议
- 不再让后续 family 选择靠聊天记忆

建议范围：
- 更新 `docs/source-intelligence/ops/milestone-board.md`
- 更新 `docs/source-intelligence/ops/handoff-prompt.md`
- 更新 `docs/source-intelligence/ops/quality-gates.md`
- 新增 `docs/source-intelligence/ops/object-family-backlog.md`

退出条件：
- 35 条路线都有 fate 和 owner slot
- handoff 可以只给最小上下文
- quality gates 写入 token / scope / truth rules

---

### Milestone 1 [NOT STARTED]：把全局知识地图补齐（2 PR）

#### PR-2 [NOT STARTED]
`docs: add global interface map baseline`

目标：
- 把当前五大域 / 路线 / endpoint family / source family 映射成全局 interface map
- 解决此前明确提到的 missing baseline

建议范围：
- `docs/source-intelligence/` 下 1 个新的全局 baseline 文档
- `ops/object-family-backlog.md` 最小更新

退出条件：
- 不再只能局部看 sample family
- 可以从全局 map 选择 family

#### PR-3 [NOT STARTED]
`docs: add legacy asset fate matrix`

目标：
- 把 route registry / maturity board / ledgers / runbooks / evidence modules / analysis outputs 的 fate 写清

建议范围：
- 更新 `legacy-source-intelligence-inventory-baseline.md`
- 如有必要，补 1 个 extract/reference mapping note

退出条件：
- 每一类 legacy 高价值资产都有 fate
- 不再出现“到底迁什么、留什么、丢什么”的摇摆

---

### Milestone 2 [NOT STARTED]：完成销售清单样板闭环（4 PR）

#### PR-4 [NOT STARTED]
`docs: formalize getdiyreportdata line-side relation evidence sample`

#### PR-5 [NOT STARTED]
`docs: formalize getdiyreportdata line-side serving-readiness sample`

#### PR-6 [NOT STARTED]
`docs: tighten sales-list request-contract baselines in current dossiers`

#### PR-7 [NOT STARTED]
`docs: add sales-list family narrow boundary answer`

目标：
- 把 `SelSaleReport` / `GetDIYReportData(E004001008_2)` / `SelDeptSaleList` / `sales_reverse_document_lines` 的 head-line-reconciliation 边界彻底收口

退出条件：
- 第二条样板线形成完整闭环
- `SaleNum` 仍保持保守 truth boundary
- 不误写 whole family completion

---

### Milestone 3 [NOT STARTED]：blocked-action pattern 样板 1 —— 收货确认（3 PR）

#### PR-8 [NOT STARTED]
`docs: add receipt-confirmation dossier and field baseline`

输出：
- `SelDocConfirmList` dossier
- 最小 field baseline（主列表级，不展开伪明细）

#### PR-9 [NOT STARTED]
`docs: add receipt-confirmation blocked-detail relation evidence`

输出：
- 主列表 ready
- detail chain blocked 的 relation answer
- `receiveConfirm` / `RTM_reportTable` / `FXDATABASE` / `detailData.currentItem` 断裂点说明

#### PR-10 [NOT STARTED]
`docs: add receipt-confirmation serving-readiness`

输出：
- ready now：主列表
- blocked/deferred：二级动作链

退出条件：
- 新仓方法论能表达“main ready / detail blocked”

---

### Milestone 4 [NOT STARTED]：blocked-action pattern 样板 2 —— 门店盘点单（3 PR）

#### PR-11 [NOT STARTED]
`docs: add store-stocktaking dossier and field baseline`

#### PR-12 [NOT STARTED]
`docs: add store-stocktaking secondary-lane relation evidence`

#### PR-13 [NOT STARTED]
`docs: add store-stocktaking serving-readiness`

目标：
- 解释 `SelDocManageList` 与 `store_stocktaking_diff_records` 的关系
- 说明 secondary raw route 何时成立，何时仍只是 research-only

退出条件：
- 新仓方法论能表达“主列表 ready / secondary lane research-only or deferred”

---

### Milestone 5 [NOT STARTED]：库存主源 cluster（2 PR）

#### PR-14 [NOT STARTED]
`docs: add inventory-main-source dossiers and field baselines`

对象：
- `SelOutInStockReport`
- `SelDeptStockWaitList`

#### PR-15 [NOT STARTED]
`docs: add inventory-main-source relation and serving-readiness answers`

目标：
- 把库存域两条最强主源候选收成 repo-owned 核心知识资产

退出条件：
- inventory 主源家族完成第一轮 repo-owned closure
- 不再只停留在旧 ledger / evidence script 里

---

### Milestone 6 [NOT STARTED]：主数据 / 主列表 cluster（2 PR）

#### PR-16 [NOT STARTED]
`docs: add master-list dossiers and field baselines`

对象：
- `商品资料 / SelWareList`
- `客户资料 / SelDeptList`
- `会员中心 / SelVipInfoList`
- `会员维护 / SelVipReturnVisitList`

#### PR-17 [NOT STARTED]
`docs: add master-list relation and serving-readiness answers`

目标：
- 把低 blocker、已 admit 的实体型列表家族一次性收口

退出条件：
- 这些 family 不再悬空在 maturity board 上
- 后续可以直接服务 capture/serving research

---

### Milestone 7 [NOT STARTED]：储值主源 + blocker family（3 PR）

#### PR-18 [NOT STARTED]
`docs: add stored-value-detail dossier and field baseline`

对象：
- `储值卡明细 / GetDIYReportData`

#### PR-19 [NOT STARTED]
`docs: add stored-value-detail relation and serving-readiness`

#### PR-20 [NOT STARTED]
`docs: add return-detail blocker dossier and readiness`

对象：
- `退货明细 / SelReturnStockList`

目标：
- 让储值主源进入 repo-owned 主线
- 让退货明细从“长期模糊难点”变成“结构化 blocker family”

退出条件：
- stored-value 明细 family 已落地
- return-detail 有 repo-owned blocker truth

---

### Milestone 8 [NOT STARTED]：snapshot / reconciliation / research-only 家族收口（4 PR）

#### PR-21 [NOT STARTED]
`docs: add sales snapshot and reconciliation pack`

对象：
- `SelDeptSaleList`
- `SelSaleReportData`
- `DeptMonthSalesReport`
- `sales_reverse_document_lines`

#### PR-22 [NOT STARTED]
`docs: add inventory snapshot pack`

对象：
- 三个 `SelStockAnalysisList` 变体
- `SelDeptStockAnalysis`
- `SelDeptStockSaleList`
- `SelInSalesReportByDay`
- `SelInSalesReport`

#### PR-23 [NOT STARTED]
`docs: add member and payment snapshot pack`

对象：
- `SelVipAnalysisReport`
- `SelVipSaleRank`
- `SelectRetailDocPaymentSlip`

#### PR-24 [NOT STARTED]
`docs: add stored-value summary snapshot pack`

对象：
- `储值卡汇总 / GetDIYReportData`
- `储值按店汇总 / GetDIYReportData`

目标：
- 所有结果快照 / 对账源 / research-only lane 都有明确定位
- 不再错误追求四件套全补齐

退出条件：
- snapshot families 全部进入 repo-owned fate
- 全量 backlog 明显收缩

---

### Milestone 9 [NOT STARTED]：not-adopted / deferred 完整收口 + completion audit（2 PR）

#### PR-25 [NOT STARTED]
`docs: close not-adopted and config-page families`

对象：
- `参数设置 / page_baseline`
- `导购员设置 / page_baseline`
- `小票设置 / page_baseline`
- `店铺定位 / GetControlData`
- `店铺零售清单 / GetDIYReportData`
- `VIP卡折扣管理 / 待识别`

#### PR-26 [NOT STARTED]
`docs: add source-intelligence migration completion audit`

目标：
- 明确哪些 family 是 migrated
- 哪些是 reference-only
- 哪些是 dropped / deferred
- 哪些仍需 future revisit

退出条件：
- 35 条路线全部有 final fate
- cross-cutting legacy assets 全部有 fate
- “全量迁移完成”可以被审计，而不是口头宣布

---

### Milestone 10 [NOT STARTED]：runtime gap preflight（2 PR，可放到 knowledge 完成后）

#### PR-27 [NOT STARTED]
`docs: add backend-base vs frontend runtime contract gap baseline`

#### PR-28 [NOT STARTED]
`docs: choose first runtime migration target and preflight`

说明：
- 这两个 PR 不属于 source-intelligence “全量知识迁移完成”的必要条件
- 但属于后续 code-bearing lane 的最安全起点

---

### 可选 PR（只在你认可时开）

#### PR-X [OPTIONAL / NOT STARTED]（optional）
`chore/scripts: add source-intelligence handoff/export helpers`

目标：
- 新增：`scripts/copy-current-main-state`
- 新增：`scripts/copy-codex-handoff`
- 复用 `_collab_common.py`

意义：
- 降低 token
- 减少手工复制错误
- 不碰 runtime

---

## 7. Codex 纠偏协议（必须执行）

### 7.1 必须先过的 gate

每一轮都必须先判断：

1. 上一个 PR 是否已 merge
2. 当前要做的是哪个 milestone / 哪个 PR
3. 本轮 allowed files 是什么
4. 本轮输出类型是什么：
   - ops / backlog
   - dossier / field
   - relation
   - readiness
   - snapshot-pack
   - blocker-pack
5. 本轮 validation 是什么

### 7.2 一旦出现以下情况，立即纠偏

#### P0：范围越界

- 改了 allowed files 之外的文件
- docs-only 包顺手改 code / tests / runtime
- 一个 PR 同时开两个 family

纠偏动作：
- 停止继续扩写
- 回滚越界文件
- 只保留当前 PR 最小正确范围

#### P1：truth 越界

- 把 `Candidate / Supported` 写成 `Confirmed`
- 把 planning/reference 写成 formal/runtime truth
- 把 blocked family 写成 ready

纠偏动作：
- 降级表述
- 补 evidence level
- 把“可疑结论”改写成 blocker / open question

#### P2：结构越界

- 试图把 legacy `app/services`、scripts、tmp/output 搬进新仓
- 新增 generic services / support code
- 混写 capture / serving / runtime / research

纠偏动作：
- 删除结构性搬运
- 只保留 repo-owned knowledge output
- 如确有代码需要，改成最小 helper 或独立 future preflight

#### P3：效率低下

- PR 太大
- 只是换一种说法重复旧结论
- 为了“全量”强行给 snapshot family 补四件套
- 输出大段原始日志而不是命令式 review 结果

纠偏动作：
- 拆 PR
- 压范围
- 改用 cluster pack 或 fate closure，而不是继续扩张

### 7.3 我给 Codex 的固定输出要求

Codex 每次都必须给：

- 状态判断
- 本轮最小范围说明
- changed files
- 每个文件改了什么
- validation
- risks
- unified diff 摘要
- 可复制 patch
- 下一步建议（只许 1 个）

---

## 8. 新仓标准（迁移时不能破）

### 8.1 结构标准

- 新知识优先进入 `docs/source-intelligence/**`
- 未重写的 legacy 知识碎片先进入 `docs/reference/legacy-backend/extracts/**`
- 不新增第 5 类正文槽位
- `ops/` 只做控制面，不做内容正文
- 不复制 legacy flat `app/services`
- 不让 `services/` 再泛化成新垃圾场

### 8.2 truth 标准

- `Confirmed / Supported / Candidate / Deferred` 必须显式出现
- 不能把 screenshot/raw sample/runbook 直接升级成 current truth
- 不能把已 admit capture 自动等同于 serving ready
- 不能把 research support skeleton 当作 legacy research 已迁完

### 8.3 code 标准

- docs-only 包不碰 runtime
- code-bearing 包默认只允许 very small helper / script
- 不为迁移方便而偷开 generic service
- 不让 support code 先行、knowledge 后补

### 8.4 capture research 标准

- capture 是 formal landing layer，不是 evidence warehouse
- research 要继续推进，但知识应沉淀到 repo-owned docs，而不是继续堆到 tmp/output
- research support 继续保持 minimal skeleton，不把旧 evidence chain 直接接回 runtime

---

## 9. 保证 capture 层研究继续推进且更高效的做法

### 9.1 研究知识和 runtime 彻底分层

继续保留：
- `src/app/services/research/**` 的最小 formal skeleton

但不做：
- 直接迁 `receipt_confirmation_evidence.py`、`maturity_board.py`、`analyze_yeusoft_*` 到 runtime 主线

正确做法：
- 把它们的知识结论重写进 source-intelligence docs
- 把仍需追溯的原始知识降级放入 reference / extracts

### 9.2 用 backlog 驱动 research，而不是临时追热点

research 的新入口要改成：

1. 先看 `ops/current-main-state.md`
2. 再看 `ops/milestone-board.md`
3. 再看 `ops/object-family-backlog.md`
4. 再进入具体 family 文档

这样做的结果：
- 不会重复研究同一条线
- 不会在低价值 family 上过度消耗 token
- 不会因为会话切换丢掉之前的真相

### 9.3 研究输出统一 fate

每次 research 新发现，必须立刻决定：

- 进入 dossier / field / relation / readiness
- 还是进入 extracts
- 还是暂时 dropped

不允许第四种：
- 继续只停留在聊天记录里

---

## 10. 严格交互流程（尽量减少你参与）

### 10.0 三角色职责（固定模式）

- `ChatGPT`：作为 reviewer，严格按当前 milestone / PR / next allowed step / truth discipline 审核；默认指出结构性风险、truth drift、scope drift，但不直接重排主规划，除非明确指出存在结构性缺陷。
- `User`：作为 relay，默认只负责复制粘贴和最小状态同步；除非我明确要求，否则不承担结构判断、diff 浓缩或 review 问题重写。
- `Codex`：作为 executor，负责实施当前 allowed scope、同步状态、生成可直接转发给 ChatGPT 的 review 包，并根据 review 结果继续纠偏或推进。

### 10.1 你的默认动作只有 4 种

1. 把我给你的“下一步 Codex 提示词”粘给 Codex
2. 把 Codex 的结果贴回给我
3. 如果我明确要求，贴 `git status` / `copy-pr-diff` / `copy-changed-files` 输出
4. merge 后告诉我“已 merge”

### 10.2 我每轮负责的事情

我每轮只做这几件事：

- 判断当前结果属于通过 / 小纠偏 / 大纠偏 / 退回
- 指出违反了哪条 gate
- 给出缩回后的最小正确范围
- 给你一条下一步可直接发给 Codex 的提示词
- 不让它越 milestone
- 不让它把 pending 写成 landed
- 不让它借机扩成大杂烩

### 10.3 什么时候我才会明确叫你配合

只有以下几种情况我才会明确让你动手：

- 需要你贴当前 worktree / diff
- 需要你确认某个 PR 已 merge
- 需要你跑仓库脚本输出结果
- 需要你粘贴验证失败片段

除此之外，我默认不额外要求你做事。

### 10.4 轮次完成条件（闭环规则）

以下都算有效轮次：

- 文件改动轮
- review verdict 改变轮
- next allowed step 改变轮
- 仅状态纠偏轮

一轮不算完成，直到同时满足：

- 已输出本轮结论
- 已更新第 0 节当前执行状态快照
- 已回填第 0.1 节“最新标准状态同步块”

如果这轮只是 review / 判断，没有改文件，也必须显式写：

- `changed files: none`

---

## 11. 对这次要求的补充建议（默认采用）

### 建议 1：把“全量迁移”定义固定下来

默认采用本文件第 3 节的定义：
- 全量迁移 = 全部 legacy 高价值内容都有明确 fate
- 不等于复制全部旧脚本 / 旧结构

### 建议 2：把 runtime gap 从知识迁移里拆出去

默认采用：
- 先完成 source-intelligence 全量迁移
- 再开 runtime gap preflight

### 建议 3：只允许再新增 1 个 ops 文档

默认采用：
- 新增 `ops/object-family-backlog.md`
- 其余规则尽量写回 `milestone-board.md`、`handoff-prompt.md`、`quality-gates.md`

这样不会让 ops 再无限膨胀。

### 建议 4：snapshot family 不强求四件套

默认采用：
- snapshot / reconciliation / not-adopted family 以更窄输出完成迁移
- 这样既真实，也省 token

### 建议 5：等 backlog 稳定后，再补 1 个低风险脚本 PR

默认采用：
- 只在需要时开 `copy-current-main-state` / `copy-codex-handoff`
- 目的是减少 token 和手工复制损耗

---

## 12. 发给 ChatGPT review / 后续同步状态的最小材料

### 12.1 发给 ChatGPT 的最小前置说明

把下面这段直接贴给 ChatGPT，可以让它先按正确边界进入 review：

```text
这是 black-tonny-backend-base 的 source-intelligence 全量迁移主线，不是旧仓 black-tonny-backend 的结构迁移。目标是把旧仓高价值知识迁成 repo-owned docs，同时保持新仓结构干净。

当前正式规则：
- 单线程、一次只允许一个 active PR
- 先判断上一包是否已 merge
- 不允许把 pending 写成 landed truth
- 不允许把 legacy flat app/services、scripts、tmp/output 迁进新仓
- docs/source-intelligence/** 是主输出位
- docs/reference/legacy-backend/extracts/** 是 legacy input 隔离区
- ops/ 只做控制面，不是第五类正文资产

当前执行文档：
- docs/source-intelligence/ops/current-main-state.md
- docs/source-intelligence/ops/milestone-board.md
- docs/source-intelligence/ops/quality-gates.md
- docs/source-intelligence/ops/handoff-prompt.md
- docs/source-intelligence/ops/object-family-backlog.md（若已落地）

当前总计划以《Black Tonny Source-Intelligence 全量迁移主计划（2026-04-07）》为准。
请把第 3 / 4 / 6 / 7 / 8 节当成主计划主体，把第 0 节当成当前状态快照，把第 13 节当成执行样例，不要混为一谈。
请先判断当前处于哪个 milestone / 哪个 PR，再做 review 或下一步提示，不要跳 gate。
```

### 12.2 当前状态同步模板

当我要把当前执行状态同步给 ChatGPT 时，优先只补下面这些字段，不要再临时写一大段自由文本：

第 12.2 节是字段模板；第 0.1 节的“最新标准状态同步块”才是当前唯一最新实例。每个有效轮次结束前，必须先把第 0.1 节回填成最新值。新开 ChatGPT / Codex 窗口时，优先复制第 0.1 节，而不是手工现编。

```text
当前状态同步（填写最新值）：

- checked at:
- current milestone:
- current PR:
- PR title:
- status:
- merged baseline:
- repo truth summary:
- allowed files in this PR:
- changed files:
- validation:
- blockers / open questions:
- next allowed step:
- review verdict:
- action requested from Codex:
- 我这次希望你重点 review 的问题:
```

建议：

- 如果当前还没正式开包，就把 `current milestone` / `current PR` / `status` 写成 `none / NOT STARTED`。
- 如果已经有 worktree 草稿，也不要直接等同于 merged progress，必须单独说明。
- 如果这次只是要 reviewer 判断方向，而不是改文档，就把 `changed files` 写成 `none`。

### 12.3 建议发给 ChatGPT 的固定 review 提问模板

```text
请基于这份主计划正文 + 我补充的“当前状态同步”，重点 review 以下问题：

1. “完成迁移”的定义是否闭环，是否足以支撑最终 knowledge delivery。
2. 当前 milestone / PR 拆分是否合理，是否存在过大、过小或顺序不当的问题。
3. 当前 next allowed step 是否合理，是否有更稳的推进方式。
4. 当前计划是否还缺少关键的 acceptance criteria、completion audit、owner slot、validation 或 handoff 信息。
5. 当前文档是否存在容易导致 truth drift、scope drift、structure drift 的模糊点。

请先指出结构性风险，再给优化建议。
请额外判断：这轮是否符合当前 milestone / PR / next allowed step，不要重排主计划，除非你明确指出存在结构性缺陷。
除非我明确要求，否则不要把 runtime 交付混成本轮 source-intelligence knowledge migration 的 must-have 范围。
```

### 12.4 每轮标准交换包

每一轮默认只交换下面三种材料：

1. 发给 ChatGPT 的最小包
   - 第 12.1 节的最小前置说明
   - 第 12.2 节的当前状态同步
   - Codex 本轮回包里的 review 摘要
2. ChatGPT 回来的 review 包
   - review verdict
   - 违反了哪条 gate / 哪类 drift
   - 建议缩回到什么最小范围
   - next allowed step 是否维持不变
3. 发给 Codex 的修订包
   - 直接贴 ChatGPT 的 review 结论
   - 若有需要，再补最新 `git status` / `copy-pr-diff` / `copy-changed-files`

默认不新增第四种自由格式中间材料，避免聊天记录变成唯一状态载体。
没有第 0.1 节“最新标准状态同步块”，这轮不算闭环。

### 12.5 当只想让对方快速恢复上下文时的最小理解块

把下面这段直接贴给 ChatGPT 或后续协作 agent，就能快速恢复上下文：

```text
这是 black-tonny-backend-base 的 source-intelligence 全量迁移主线，不是旧仓 black-tonny-backend 的结构迁移。目标是把旧仓高价值知识迁成 repo-owned docs，同时保持新仓结构干净。

当前正式规则：
- 单线程、一次只允许一个 active PR
- 先判断上一包是否已 merge
- 不允许把 pending 写成 landed truth
- 不允许把 legacy flat app/services、scripts、tmp/output 迁进新仓
- docs/source-intelligence/** 是主输出位
- docs/reference/legacy-backend/extracts/** 是 legacy input 隔离区
- ops/ 只做控制面，不是第五类正文资产

当前执行文档：
- docs/source-intelligence/ops/current-main-state.md
- docs/source-intelligence/ops/milestone-board.md
- docs/source-intelligence/ops/quality-gates.md
- docs/source-intelligence/ops/handoff-prompt.md
- docs/source-intelligence/ops/object-family-backlog.md（若已落地）

当前总计划以《Black Tonny Source-Intelligence 全量迁移主计划（2026-04-07）》为准。
请先判断当前处于哪个 milestone / 哪个 PR，再做 review 或下一步提示，不要跳 gate。
```

### 12.6 新开 ChatGPT 窗口固定启动文本

```text
你现在扮演 source-intelligence migration reviewer，不是 executor。
我下一条会贴《Black Tonny Source-Intelligence 全量迁移主计划（2026-04-07）》第 0 节里的“最新标准状态同步块”。

你的固定规则：
- 先基于我贴的“最新标准状态同步块”判断当前 milestone / PR / status / next allowed step。
- 如果我还没贴这块，你只允许先向我要这一块，不要直接判断当前进度。
- 把主计划第 3 / 4 / 6 / 7 / 8 节当成主体，第 0 节当最新状态，第 13 节当 executor 样例。
- 第 13 节不等于当前最新状态；如果它与“最新标准状态同步块”冲突，以“最新标准状态同步块”为准。
- 请优先 review：是否越 gate、是否有 truth drift / scope drift / structure drift、是否需要缩回更小范围、next allowed step 是否仍成立。
- 除非我明确要求，否则不要重排主计划，也不要把 runtime gap 混成本轮 must-have。
```

### 12.7 新开 Codex 窗口固定启动文本

```text
你现在扮演 source-intelligence executor，不是 reviewer。
我下一条会贴《Black Tonny Source-Intelligence 全量迁移主计划（2026-04-07）》第 0 节里的“最新标准状态同步块”。

你的固定规则：
- 先基于“最新标准状态同步块”判断当前 milestone / PR / status / next allowed step / allowed files / round type，再决定是否执行。
- 如果我还没贴这块，你只允许先向我要这一块；只有在它仍不足以回答问题时，才索要最小 git/worktree truth。
- 第 13 节只是 executor 样例，不是当前最新状态；如果它与“最新标准状态同步块”冲突，以“最新标准状态同步块”为准。
- 每轮回包必须包含：本轮结论、最新完成版状态同步块、changed files、validation、risks、next allowed step、可直接转发给 ChatGPT 的 review 摘要。
- 如果这轮 `changed files` 是 `none`，但 `review verdict / next allowed step / blockers` 变了，仍然必须回写状态。
- 没有“最新标准状态同步块”，这轮不算闭环。
```

---

## 13. 初始状态下第一条要发给 Codex 的提示词

> 硬边界：第 13 节是给 executor 的执行样例，不是给 reviewer 的主输入；它不能替代第 12 节的 review 材料，也不应用来重排 Milestone 设计、PR 编号与顺序，或“完成迁移”的正式定义。如果第 13 节与第 0.1 节“最新标准状态同步块”冲突，以第 0.1 节为准。

> 本节是给执行代理的首包提示词样例，不是给 ChatGPT 做主计划 review 的主输入。发给 ChatGPT review 时，应优先使用第 12 节的材料。

> 这是重置到初始状态后真正该执行的第一步。先把 current truth 校准完，再继续后面的大计划。

```text
只基于 `black-tonny-backend-base` 当前真实仓库状态，执行一个极小 docs-only 包：

PR title:
`docs: reconcile post-merge source-intelligence ops state`

背景约束：
- 当前执行状态按“尚未开始；PR-0 还未起草”处理
- `docs: add source-intelligence ops baseline (#79)` 已 merge 到 current `main`
- `docs/source-intelligence/README.md`、`docs/source-intelligence/ops/README.md`、`tests/test_source_intelligence_docs_spine.py` 的 spine wiring 已 landed
- 但 bookkeeping 没跟上：
  - `current-main-state.md` 仍有 pre-merge 条件语气
  - `review-gain-ledger.md` 缺少已 merge 记录
  - `milestone-board.md` 没把 `#79` 的 landed truth 对齐完整

本包目标：
只做 post-merge bookkeeping 校准，把 current main truth、gain ledger、milestone board 对齐到真实 git 状态。

本包只允许修改：
- `docs/source-intelligence/ops/current-main-state.md`
- `docs/source-intelligence/ops/review-gain-ledger.md`
- `docs/source-intelligence/ops/milestone-board.md`

本包必须完成：
1. `current-main-state.md`
   - 去掉 pre-merge / pending package 条件语气
   - 明确 `#79` 已 merge 到 current `main`
   - 明确 source-intelligence `ops` control plane 已 landed
   - 明确 spine wiring 已 landed
   - 不要虚构独立 `docs/tests` merge 事实
2. `review-gain-ledger.md`
   - 追加一条 2026-04-07 merged entry
   - 正确描述 landed 的确定性
   - “下一步建议”必须写成 merge 后仍成立的话
3. `milestone-board.md`
   - 把 `docs: add source-intelligence ops baseline` 记入已完成 PR
   - 明确当前仓库只能证明：`#79` 已 merge，spine wiring 已 landed
   - 明确当前仓库不能证明：`docs/tests: wire ops baseline into source-intelligence spine` 曾作为独立 package / 独立 PR merge

严格不要做：
- 不修改 `docs/source-intelligence/README.md`
- 不修改 `docs/source-intelligence/ops/README.md`
- 不修改 `tests/test_source_intelligence_docs_spine.py`
- 不新增 dossier
- 不新增 field dictionary
- 不新增 relation sample
- 不新增 serving-readiness sample
- 不修 `pytest` / `fastapi` 环境问题
- 不新增 support code
- 不扩写 ops 体系

验证要求：
- `git diff --check`
- 用最小自检确认三份文件口径一致
- 可以记录 `pytest tests/test_source_intelligence_docs_spine.py` 当前环境失败，但只能作为环境事实记录，不能在本包里转去修环境

输出要求：
1. 先给出本包最小范围说明
2. 再实施改动
3. 最后输出：
   - changed files
   - 每个文件改了什么
   - validation
   - risks
   - 为什么这是 current truth 校准，而不是新内容推进
4. 必须额外输出：
   - 简洁 unified diff 摘要
   - 可直接复制的 patch / diff 文本
5. 优先使用仓库脚本给出：
   - `./scripts/copy-changed-files --mode worktree --no-clipboard`
   - `./scripts/copy-pr-diff --mode worktree --no-clipboard`
   - `./scripts/copy-pr-template-draft --mode worktree --no-clipboard --goal-hint "只做 post-merge source-intelligence ops bookkeeping 校准；不进入 relation/readiness 正文。"`

记住：
这一步完成前，不允许进入 `GetDIYReportData` relation/readiness。
这一步 merge 后，下一包才允许是：
`docs: add source-intelligence full-migration backlog and codex execution protocol`
```
