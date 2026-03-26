# 旧后端文档盘点与迁移映射（PR-1）

## 1. 本次目标

本 PR 只做文档盘点、映射、分类和边界说明，不做正式业务迁移。

本次要完成的事情：
- 盘点旧仓库 `black-tonny-backend` 的文档资产
- 按“可吸收为正式真源的候选文档 / 研究参考文档 / 历史归档文档”分类
- 输出旧路径 -> 新路径映射表
- 输出 capture 相关迁移范围清单
- 输出 research 相关“仅保留 reference、不进入 runtime”的清单
- 为新仓库补齐迁移索引和迁移边界说明

## 2. 明确边界

当前唯一真源是 `black-tonny-backend-base`。

本 PR 明确不做：
- 不迁旧仓库 `app/services`
- 不迁旧仓库 `scripts`
- 不接入 `capture` runtime
- 不接入 `research` runtime
- 不修改对外 API 行为
- 不整块复制旧仓库目录

## 3. 盘点范围

本次共盘点旧仓库自写 Markdown 文档 37 份：
- 根目录入口文档 8 份
- 兼容适配文档 1 份
- `docs/` 主题文档 26 份
- `tmp/capture-samples/` 样本文档 2 份

本次不纳入盘点：
- `.venv/`、`.pytest_cache/` 等第三方或缓存文档
- `.github/` workflow 或模板文件
- 脚本、源码、截图、JSON 样本本身

## 4. 分类口径

### 4.1 可吸收为正式真源的候选文档

仍然能为新仓库提供长期结构边界、双库职责边界或正式契约基线的文档。

处理原则：
- 可以被改写吸收到新仓库真源
- 不能原样继承旧 runtime 叙事

### 4.2 研究参考文档

只用于帮助理解上游 ERP、capture 准入、字段映射、tooling 或研究流程的文档。

处理原则：
- 只保留为 reference
- 不进入 runtime
- 不作为模型、CRUD、API 或模块结构真源

### 4.3 历史归档文档

描述旧 split runtime、旧业务 API、旧协作适配或旧样本状态的文档。

处理原则：
- 只保留历史上下文
- 不作为新仓库当前实现依据

## 5. 分类结果与旧路径 -> 新路径映射

分类汇总：
- 可吸收为正式真源的候选文档：5 份
- 研究参考文档：16 份
- 历史归档文档：16 份

### 5.1 可吸收为正式真源的候选文档

| 旧路径 | 新路径 | 本次动作 | 说明 |
| --- | --- | --- | --- |
| `docs/README.md` | `docs/README.md` | 已改写为新仓库 docs 索引 | 旧索引结构不直接复用，改成 base 真源入口 |
| `docs/backend-boilerplate-alignment.md` | `docs/legacy-backend-migration-mapping.md` | 已吸收关键结构边界 | 保留“不新增扁平化大 service 层”的迁移约束 |
| `docs/backend-boilerplate-migration-roadmap.md` | `docs/legacy-backend-migration-mapping.md` | 已吸收阶段顺序和 capture 优先级 | 作为下一阶段范围定义输入，而不是直接复制旧路线图 |
| `docs/two-database-architecture.md` | `README.md` 和 `docs/legacy-backend-migration-mapping.md` | 已补充边界说明 | 明确业务 API 只读 `serving`，不直读 `capture` |
| `docs/api-response-standard.md` | `docs/legacy-backend-migration-mapping.md` | 记入后续 formal contract 输入 | 本 PR 不复制旧业务 API 文档，但保留 envelope 约束来源 |

### 5.2 研究参考文档

| 旧路径 | 新路径 | 本次动作 | 说明 |
| --- | --- | --- | --- |
| `docs/dashboard/summary-capture-mapping.md` | `docs/reference/legacy-backend/README.md` | 建 reference 目标目录，不复制正文 | 只作为未来 serving 投影迁移的参考输入 |
| `docs/erp/README.md` | `docs/reference/legacy-backend/README.md` | 建 reference 目标目录，不复制正文 | ERP 研究总览只能保留为 reference |
| `docs/erp/api-maturity-board.md` | `docs/reference/legacy-backend/README.md` | 建 reference 目标目录，不复制正文 | 成熟度面板帮助判断准入，不定义 runtime |
| `docs/erp/capture-ingestion-roadmap.md` | `docs/reference/legacy-backend/README.md` | 建 reference 目标目录，不复制正文 | 只保留为 capture 准入顺序参考 |
| `docs/erp/capture-route-registry.md` | `docs/reference/legacy-backend/README.md` | 建 reference 目标目录，不复制正文 | 注册表只能辅助 admission 设计 |
| `docs/erp/sales-ledger.md`、`docs/erp/inventory-ledger.md`、`docs/erp/member-ledger.md`、`docs/erp/stored-value-ledger.md`、`docs/erp/payment-and-doc-ledger.md`、`docs/erp/cost-visibility-audit.md` | `docs/reference/legacy-backend/README.md` | 建 reference 目标目录，不复制正文 | 这些台账只保留为业务源研究资料 |
| `docs/erp/page-research-runbook.md` | `docs/reference/legacy-backend/README.md` | 建 reference 目标目录，不复制正文 | 浏览器研究流程只保留 reference |
| `docs/tooling/README.md`、`docs/tooling/ai-token-playbook.md`、`docs/tooling/browser-research-tools.md`、`docs/tooling/mcp-guide.md` | `docs/reference/legacy-backend/README.md` | 建 reference 目标目录，不复制正文 | tooling 说明不能反向定义新仓库架构 |

### 5.3 历史归档文档

| 旧路径 | 新路径 | 本次动作 | 说明 |
| --- | --- | --- | --- |
| `README.md`、`ARCHITECTURE.md` | `docs/archive/legacy-runtime/README.md` | 建 archive 目标目录，不复制正文 | 旧 runtime 叙事与当前 base 已脱钩 |
| `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`.claude/CLAUDE.md` | `docs/archive/legacy-runtime/README.md` | 建 archive 目标目录，不复制正文 | 旧仓库协作入口不再作为新仓库真源 |
| `CONTRIBUTING.md`、`SECURITY.md`、`CHANGELOG.md` | `docs/archive/legacy-runtime/README.md` | 建 archive 目标目录，不复制正文 | 先归档，后续按新仓库需要重写 |
| `docs/frontend-auth-api.md`、`docs/frontend-backend-boundary.md`、`docs/assistant/chat-api.md` | `docs/archive/legacy-runtime/README.md` | 建 archive 目标目录，不复制正文 | 这些文档描述的是旧业务 runtime 契约，不是当前 base 真源 |
| `docs/dashboard/summary-api.md`、`docs/dashboard/evolution-index.md` | `docs/archive/legacy-runtime/README.md` | 建 archive 目标目录，不复制正文 | 旧 Dashboard API 与演进叙事不应直接迁入 base |
| `tmp/capture-samples/README.md`、`tmp/capture-samples/report_api_samples.md` | `docs/archive/legacy-runtime/README.md` | 建 archive 目标目录，不复制正文 | 原始样本、临时说明和操作性内容只保留历史上下文 |

## 6. capture 相关迁移范围清单

以下内容只作为下一阶段准备范围，不在本 PR 实施：

### 6.1 先迁契约和边界，不先搬旧实现

下一阶段优先围绕这些对象定义新仓库正式契约：
- `capture_batches`
- `capture_endpoint_payloads`
- `analysis_batches`
- `sales_orders`
- `sales_order_items`
- `inventory_current`
- `inventory_daily_snapshot`

### 6.2 旧仓库中值得按需阅读的 capture 输入

这些文件只作为下一阶段“按需摘取”的候选输入：
- 这些候选输入文件只允许用于阅读、职责提炼和边界确认。
- 不允许以“复制加改名”的方式直接迁入 `src/app`、`src/scripts` 或其他正式运行目录。
- `app/services/capture/contracts.py`
- `app/services/capture/route_registry.py`
- `app/services/capture/batch_lifecycle.py`
- `app/services/capture/persist_helpers.py`
- `app/crud/capture_batches.py`
- `app/crud/analysis_batches.py`
- `app/crud/serving_projections.py`
- `app/services/serving/transform.py`
- `app/services/serving/summary_projection.py`

### 6.3 新仓库的建议落点

这里继续保持同一条限制：候选输入文件只允许用于阅读、职责提炼和边界确认，不允许以“复制加改名”的方式直接迁入正式运行目录。

未来正式迁入时，优先落到：
- `src/app/models/`
- `src/app/crud/`
- 必要时再引入窄职责的 `src/app/services/capture/` 或 `src/app/services/serving/`

禁止回到旧式做法：
- 禁止恢复 flat `app/services/*.py` 大型编排层
- 禁止业务 API 直接读取 `capture`
- 禁止把 admit、registry、transform 和 research 混成一个目录主线

### 6.4 当前明确不在下一阶段首批范围中的内容

以下内容不属于首批 capture 迁移对象：
- 旧 flat `app/services/*_capture_admission_service.py`
- `app/services/capture_route_registry_service.py` 这类兼容壳
- 旧仓库 `scripts/admit_*`
- 旧仓库 `scripts/transform_capture_batch.py`

## 7. research 相关仅保留 reference、不进入 runtime 的清单

以下内容后续即使保留，也只能停留在 reference 层：
- `docs/erp/**`
- `docs/tooling/**`
- `docs/dashboard/summary-capture-mapping.md`
- `app/services/research/**`
- `scripts/*_research.py`
- `scripts/analyze_*_evidence_chain.py`
- `scripts/probe_*.py`
- `scripts/run_yeusoft_page_research.py`
- `scripts/run_yeusoft_menu_coverage_audit.py`
- `scripts/build_erp_api_maturity_board.py`
- `scripts/build_erp_capture_route_registry.py`
- `tmp/capture-samples/**`

保持 reference-only 的理由：
- 它们帮助判断上游接口是否可信、字段是否稳定、路线是否可以准入
- 它们不能直接成为 runtime import、router、schema、CRUD、模型或 API 契约
- 它们不能反向定义新仓库模块结构

## 8. 哪些内容明确不迁，为什么

- 不迁旧 `app/services`
  - 旧目录混合 runtime、capture、research、compat shim，和当前 base 的长期结构冲突
- 不迁旧 `scripts`
  - 本阶段只做盘点与映射，且大量脚本属于 admit/probe/research runner
- 不迁旧业务 API 文档正文
  - 它们描述的是旧 runtime 表面，不应直接继承为新仓库真源
- 不迁 `tmp/capture-samples/**` 原始样本
  - 操作性强、时效性高，且不适合作为正式仓库文档主线

## 9. 风险点

- 旧仓库有不少文档同时混有“当前事实”和“过渡态叙事”，下一阶段真正迁代码时仍需回看原文，不应只看这份映射表
- ERP 研究文档和样本可能持续变化，reference 区只能辅助判断，不能替代新仓库正式契约
- 本 PR 只建立目标目录和映射规则，尚未迁入任何旧正文；后续若要补正文，必须逐份挑选，不能整目录复制

## 10. 本 PR 如何验证没有影响 runtime

- 变更只允许出现在 `README.md` 和 `docs/**`
- 不改 `src/app/**`
- 不改 `src/scripts/**`
- 不改 `src/migrations/**`
- 不改测试、CI、Docker、依赖或环境配置

本 PR 结束时应通过以下检查：
- `git diff --name-only` 只出现文档文件
- 新增 Markdown 链接可打开
- README 与 docs 中的迁移边界表述一致
