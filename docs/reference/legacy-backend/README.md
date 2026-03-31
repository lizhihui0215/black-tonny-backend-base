# 旧后端参考资料区

这个目录预留给从 `black-tonny-backend` 选择性保留的 reference 资料。

当前正式文档请先看 [docs/README.md](../../README.md)。

关于 research support，当前阅读顺序应先看：
- [docs/research-support-current-surface.md](../../research-support-current-surface.md)
- [docs/legacy-research-bridge-note.md](../../legacy-research-bridge-note.md)

这里的 reference 区不是 legacy research 全量正文迁移区。
旧仓 `black-tonny-backend` 中的 legacy research docs / assets 仍然是当前参考真源。

关于 capture，当前阅读顺序应先看：
- [docs/capture-minimal-boundary.md](../../capture-minimal-boundary.md)
- 如需双库职责边界，再看 [docs/capture-serving-boundary.md](../../capture-serving-boundary.md)

这里的 reference 区不是 legacy capture 全量正文迁移区。
旧仓 `black-tonny-backend` 中的 legacy capture docs / assets 仍然是当前参考来源之一。

这里可以放：
- ERP 台账、成熟度面板、capture 路线注册表
- 页面研究 runbook、tooling 说明
- capture 到 serving 的字段映射草案
- 追溯说明、样本清单、排障模板、研究记录

这里不能变成：
- 新仓库 runtime 的正式真源
- app import 入口
- router 挂载入口
- schema、CRUD、模型或 API 契约的替代品
- capture 正式契约的长期归属地

迁移规则：
- 只允许按需挑选，不允许整目录复制
- 原始截图、凭证、账号口令、浏览器会话、临时样本不进入这里
- 研究资料只能辅助准入判断，不能反向定义 runtime 结构

PR-1 只建立这个 reference 目标目录，不复制旧文档正文。
