# Legacy Source-Intelligence Inventory Baseline

状态：source-intelligence / working inventory baseline

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../README.md)
- [docs/README.md](../README.md)
- [docs/](../README.md) 下各 formal boundary docs
- 当前 `main` 上已经 landed 的 `src/app/**`、`src/migrations/**`、`tests/**`

这份文档只做一件事：
- 盘点 `black-tonny-backend` 里和 source intelligence 直接相关的高价值 legacy 知识资产，并给出第一版迁移优先级

这份 inventory baseline 服务的是：
- 在 `/erp/orders` first-slice 样板已经完整落地后，为下一批最值得迁移和研究的接口族排优先级

这份文档复用的主线约束以：
- [migration-charter.md](./migration-charter.md)
- 为准

当前新仓已存在的 source-intelligence 主输出样板包括：
- [apis/erp-orders-api-dossier.md](./apis/erp-orders-api-dossier.md)
- [fields/erp-orders-first-slice-field-dictionary.md](./fields/erp-orders-first-slice-field-dictionary.md)
- [relations/erp-orders-first-slice-relation-doc.md](./relations/erp-orders-first-slice-relation-doc.md)
- [serving-readiness/erp-orders-first-slice-serving-readiness.md](./serving-readiness/erp-orders-first-slice-serving-readiness.md)

这份 inventory baseline 不做：
- 不开始第二个 API dossier
- 不开始第二份 field dictionary
- 不开始第二份 relation sample
- 不开始 broader readiness map
- 不做 support code
- 不把 legacy 资产直接升级成 current truth

## Scope Boundary

当前只盘以下对象：

1. 能帮助判断 endpoint family、payload family、field grain、relation、readiness 的 legacy 知识资产
2. 已经在 legacy repo 中被多次复用、能稳定指向“下一批该研究谁”的资产
3. 能被重写吸收到新仓 docs 子体系的高价值知识，而不是旧仓结构本身

当前明确不盘：
- 旧仓全部文件
- 旧仓目录树本身
- 与 source intelligence 无直接关系的 runtime glue
- 任何未重写就想直接搬进新仓的 script/output/tmp truth

## Classification Rule

这份 baseline 统一使用四级迁移分类：

- `高价值优先迁`
  - 已能明显提升下一批 dossier / field dictionary / relation doc / serving-readiness 的确定性
- `中价值待定`
  - 有价值，但还需要更明确的对象选择或证据重写
- `仅参考`
  - 适合回查、交叉验证、解释冲突，不适合直接升级成 repo-owned 知识资产
- `暂不迁`
  - 主要价值停留在旧结构、旧运行方式或临时产物表达，不应进入新仓主输出位

## Inventory Summary

| legacy asset category | representative legacy assets | 资产大致是什么 | 为什么对 serving 有价值 | 适合迁成什么新仓资产 | 当前优先级 |
| --- | --- | --- | --- | --- | --- |
| API / route registry | `docs/erp/capture-route-registry.md` | 统一列出已识别路线、endpoint、capture role/status、菜单路径、阻塞项、下一步 | 能直接帮助判断哪些接口族最值得先做 dossier/readiness，而不是盲扫全域 | `API dossier` + `serving-readiness` | `高价值优先迁` |
| menu / page research | `app/services/research/page_research.py`; `docs/erp/page-research-runbook.md`; `output/playwright/yeusoft-menu-coverage/**/manifest.json` | 菜单树、页面入口、页面动作、网络请求、页面内 endpoint 候选与 UI 线索 | 能补 dossier 里的 menu/page/source-surface context，也能给 relation doc 提供页面动作链边界 | `API dossier` + `relation doc` + `only reference` | `高价值优先迁` |
| maturity board / coverage board | `docs/erp/api-maturity-board.md`; `app/services/research/maturity_board.py`; `app/services/research/menu_coverage.py` | 全域路线状态面板、覆盖状态、可信度、阻塞项、域级排序 | 能决定“先迁谁”，也能把 readiness 判断从泛印象收口成结构化优先级 | `serving-readiness` + `API dossier` | `高价值优先迁` |
| evidence / admission knowledge | `app/services/sales_capture_admission_service.py`; `app/services/research/return_detail_evidence.py`; 其他 `*_capture_admission_service.py` / `*_evidence.py` | 把 HTTP/page evidence 收成 admit 条件、blocking issues、split rule、parameter semantics 的代码化知识 | 这是 source-to-serving 边界、identity、dedupe、line/head split、blocked action chain 的直接知识源 | `relation doc` + `serving-readiness` + `field dictionary` | `高价值优先迁` |
| ledger / runbook / probe outputs | `docs/erp/sales-ledger.md`; `docs/erp/payment-and-doc-ledger.md`; `tmp/capture-samples/analysis/*.json`; `output/playwright/**/manifest.json` | 台账、运行说明、analysis JSON、playwright manifest、network/raw outputs | 适合帮助重建对象边界和 filter vocabulary，但不应直接作为 current truth | `API dossier` + `field dictionary` + `only reference` | `中价值待定` |
| relation clues | `app/services/sales_capture_admission_service.py`; `docs/erp/payment-and-doc-ledger.md`; `app/services/research/page_research.py` | 头/行/反向路线拆分、上下文字段、二级动作链、hidden context、local table / ref / injection clue | 这是后续 relation doc 最难替代的知识源，直接决定哪些关系可升级、哪些必须继续保守 | `relation doc` + `serving-readiness` | `高价值优先迁` |

## Category Detail

### 1. API / Route Registry

| asset family | representative legacy assets | 资产大致是什么 | 为什么对 serving 有价值 | 适合迁成什么新仓资产 | 当前优先级 |
| --- | --- | --- | --- | --- | --- |
| capture route registry | `docs/erp/capture-route-registry.md` | 以路线为单位记录 endpoint、来源分类、capture role、capture status、menu path、阻塞项、下一步 | 直接决定哪些接口族已经足够窄、足够稳，值得先做 source-intelligence 主输出 | `API dossier` + `serving-readiness` | `高价值优先迁` |
| route-registry build logic | `app/services/capture_route_registry_service.py` | legacy repo 中 route registry 的兼容入口；说明 registry 曾被当成统一落点使用 | 对理解 registry 的生成来源有帮助，但本身是旧结构兼容壳，不应迁移结构表达 | `only reference` | `仅参考` |

当前判断：
- `capture-route-registry` 是高价值知识资产，但只能重写吸收，不能把 legacy capture 术语原样搬进新仓 source-intelligence docs。

### 2. Menu / Page Research

| asset family | representative legacy assets | 资产大致是什么 | 为什么对 serving 有价值 | 适合迁成什么新仓资产 | 当前优先级 |
| --- | --- | --- | --- | --- | --- |
| page research registry and heuristics | `app/services/research/page_research.py` | 把页面标题、menu target、group、target path、候选 endpoint、probe target 收成结构化 registry | 能给 dossier 提供 menu/page/source-surface context，也能给 relation doc 提供页面动作边界 | `API dossier` + `relation doc` | `高价值优先迁` |
| page research runbook | `docs/erp/page-research-runbook.md` | 解释如何跑页面研究、菜单覆盖审计、单变量 probe、以及产物落点 | 有助于理解 legacy 证据怎么来的，但 runbook 本身不是 repo-owned truth | `only reference` | `仅参考` |
| menu coverage / research manifests | `output/playwright/yeusoft-menu-coverage/**/manifest.json`; `output/playwright/yeusoft-research/**/manifest.json` | 菜单项、请求指纹、页面动作、组件状态、visible controls 的原始或半结构化记录 | 能帮助重建 menu/page/source-surface context 和 blocked action chain，但不能直接升级成结论 | `only reference` | `仅参考` |

当前判断：
- page research 的结构化 registry 值得优先迁知识。
- 原始 manifest 继续只做 reference，不应进入主输出位。

### 3. Maturity Board / Coverage Board

| asset family | representative legacy assets | 资产大致是什么 | 为什么对 serving 有价值 | 适合迁成什么新仓资产 | 当前优先级 |
| --- | --- | --- | --- | --- | --- |
| API maturity board | `docs/erp/api-maturity-board.md` | 统一记录路线阶段、可信度、coverage、blocker、下一步、证据来源 | 是 legacy repo 中“先做谁、为什么”的最强汇总面板 | `serving-readiness` + `API dossier` | `高价值优先迁` |
| maturity-board assembly logic | `app/services/research/maturity_board.py` | 把 ledger、page research、menu coverage、evidence chain 汇成一块板 | 能暴露 legacy 排序逻辑和 blocker vocabulary，但代码结构本身不迁 | `only reference` | `仅参考` |
| menu coverage classification logic | `app/services/research/menu_coverage.py` | 把 covered / visible_but_untracked / visible_but_failed / container_only 分类写成可复用逻辑 | 对 dossier 的 menu/page context 与 serving-readiness 的 coverage boundary 很有帮助 | `API dossier` + `serving-readiness` | `中价值待定` |

当前判断：
- board 本身值得迁知识，但要拆成新仓里的 dossier / readiness 语义，不能继续维持 legacy 大总览写法。

### 4. Evidence / Admission Knowledge

| asset family | representative legacy assets | 资产大致是什么 | 为什么对 serving 有价值 | 适合迁成什么新仓资产 | 当前优先级 |
| --- | --- | --- | --- | --- | --- |
| admitted mainline split knowledge | `app/services/sales_capture_admission_service.py` | 把 document payload / detail payload 拆成 `head` / `line` / `reverse`，并写出 uniqueness、blocking issues、context fields | 直接携带 source-to-serving relation clue、identity boundary、grain split 和 admit 条件 | `relation doc` + `serving-readiness` + `field dictionary` | `高价值优先迁` |
| blocker-heavy evidence bundles | `app/services/research/return_detail_evidence.py`; 其他 `*_evidence.py` | 用 baseline、variant、error group、parameter semantics、blocking issues 解释为什么某条路线还不能升级 | 能帮助新仓明确 candidate/deferred 的硬原因，而不是只写“待研究” | `serving-readiness` + `relation doc` | `高价值优先迁` |
| capture admission service families | 其他 `*_capture_admission_service.py` | 用代码固定 mainline-ready 与 not-ready 的门槛 | 是 legacy repo 最接近“知识已经够硬”的地方之一 | `serving-readiness` + `relation doc` | `中价值待定` |

当前判断：
- evidence / admission knowledge 是下一批最值得系统迁的资产层，因为它最接近硬边界，而不是泛研究感想。

### 5. Ledger / Runbook / Probe Outputs

| asset family | representative legacy assets | 资产大致是什么 | 为什么对 serving 有价值 | 适合迁成什么新仓资产 | 当前优先级 |
| --- | --- | --- | --- | --- | --- |
| domain ledgers | `docs/erp/sales-ledger.md`; `docs/erp/payment-and-doc-ledger.md`; 其他 `docs/erp/*-ledger.md` | 按域整理 endpoint、method、filters、judgment、risk label、capture strategy | 能给 dossier、field dictionary、relation doc 提供高密度对象边界与 vocabulary | `API dossier` + `field dictionary` + `relation doc` | `中价值待定` |
| runbooks | `docs/erp/page-research-runbook.md` | 说明怎么跑 research / coverage / probe | 只帮助理解 legacy 证据生产方式，不应升级成 current knowledge asset | `only reference` | `仅参考` |
| analysis / probe outputs | `tmp/capture-samples/analysis/*.json`; `output/playwright/**/network/*`; `output/playwright/**/manifest.json` | 原始或后处理的 evidence outputs | 可用于冲突排查、回查和 provenance，但不应直接吸收为 repo-owned truth | `only reference` | `仅参考` |

当前判断：
- ledger 有高价值知识，但表达里混有 risk label、capture strategy、legacy 术语，需要重写吸收。
- runbook/output 只保留 reference 角色。

### 6. Relation Clues

| asset family | representative legacy assets | 资产大致是什么 | 为什么对 serving 有价值 | 适合迁成什么新仓资产 | 当前优先级 |
| --- | --- | --- | --- | --- | --- |
| sales head-line-reverse split clue | `app/services/sales_capture_admission_service.py`; `docs/erp/sales-ledger.md` | 明确 `SelSaleReport` 更像单据头、`GetDIYReportData(E004001008_2)` 更像明细行、`SelDeptSaleList` 更像对账/结果接口 | 这是最接近 source-to-serving relation doc 的现成高价值 clue cluster | `relation doc` + `field dictionary` + `serving-readiness` | `高价值优先迁` |
| secondary action-chain blockers | `docs/erp/payment-and-doc-ledger.md`; `app/services/research/page_research.py` | 收货确认、退货明细、门店盘点单这类页面里“主列表存在，但二级动作链断裂”的线索 | 能把 candidate / deferred 的 blocker 写成硬关系问题，而不是模糊“页面还没研究完” | `relation doc` + `serving-readiness` | `高价值优先迁` |
| local-table / injected-context clues | `docs/erp/payment-and-doc-ledger.md`; `output/playwright/**/manifest.json` | `FXDATABASE`、`RTM_reportTable`、`detailData.currentItem`、`menuId` 等本地表 / 注入上下文线索 | 适合解释为什么某些关系当前不能升级，但本质仍是 blocker evidence，不是当前 truth | `relation doc` + `only reference` | `中价值待定` |

当前判断：
- relation clue 是 legacy 资产里最稀缺、也最值得提前重写吸收的一层。
- 尤其是 sales 的 head/line/reconciliation split，已经足够支撑下一批 relation-oriented source-intelligence 包。

## Migration Priority Queue

### `高价值优先迁`

1. 销售清单 family
   - 代表对象：`SelSaleReport`、`GetDIYReportData(E004001008_2)`、`SelDeptSaleList`
   - 原因：legacy 已经把 head / line / reconciliation 粒度差异写得最清楚，最适合迁成新的 dossier / field dictionary / relation doc 组合

2. 收货确认主列表与二级动作链
   - 代表对象：`SelDocConfirmList` 与其 blocked detail chain
   - 原因：主列表已 admit，但 detail chain 的 blocker 非常结构化，适合做“ready / not ready”分层样板

3. 门店盘点单主列表与损溢二级数据
   - 代表对象：`SelDocManageList` 与 `store_stocktaking_diff_records`
   - 原因：main list 与 research-only secondary lane 已经分开，适合验证 source-intelligence 如何承接“主列表 ready、二级 lane deferred”

### `中价值待定`

1. 退货明细
   - 代表对象：`SelReturnStockList`、`ReturnStockBaseInfo`
   - 原因：legacy blocker 很清楚，但仍卡在服务端错误与隐藏上下文；当前更适合作为 blocker-heavy relation/readiness reference，而不是立即开 dossier 主包

2. snapshot families
   - 代表对象：`每日流水单`、`商品销售情况`、`会员消费排行` 等
   - 原因： serving 价值存在，但当前更偏 snapshot/coverage knowledge，不是最优先的 relation-rich 主线对象

### `仅参考`

- `output/playwright/**`
- `tmp/capture-samples/analysis/*.json`
- legacy runbooks

### `暂不迁`

- 旧仓 flat service 结构
- 旧仓 script 运行方式
- `tmp/**`、`output/**` 作为目录树本身
- 任何必须依赖 legacy 目录语义才能理解的结构表达

## Current Hard Conclusions

1. legacy repo 里真正高价值、值得优先迁的不是脚本运行方式，而是 route registry、maturity board、evidence/admission bundle、relation clue 这四层知识资产。
2. `/erp/orders` first-slice 样板已经证明新仓有能力承接单点 dossier/field/relation/readiness；下一步最该迁的是能显著提升对象选择与关系判断的 legacy 知识层，而不是继续横向扫 raw outputs。
3. domain ledgers 有价值，但必须重写吸收；不能把 legacy 台账、risk label、capture strategy 原样升级成新仓主输出。
4. `output/playwright/**` 和 `tmp/capture-samples/analysis/*.json` 继续是 reference layer，不应被误写成 repo-owned current truth。

## Non-Goals

这份 inventory baseline 当前不做：
- 不定义第二个 dossier 的正式内容
- 不替代 future API inventory
- 不替代 future field universe
- 不提前确认 broader target truth
- 不把 legacy 里的 admit/registry/runtime 代码结构迁入新仓
