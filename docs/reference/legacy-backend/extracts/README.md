# Legacy Extracts 隔离区

状态：reference-only / input quarantine

这份文档不是 formal source of truth。

formal truth 仍以以下对象为准：
- [README.md](../../../../README.md)
- [docs/README.md](../../../README.md)
- [docs/source-intelligence/README.md](../../../source-intelligence/README.md)
- 当前 `main` 上已经 landed 的 formal docs、`src/app/**`、`src/migrations/**`、`tests/**`

这份目录只做一件事：
- 为 legacy knowledge migration 提供一个受控的“摘取隔离区”，让旧仓知识碎片在被重写成 repo-owned source-intelligence 资产之前，先有一个明确、不会污染主输出位的落点

## Extracts 是什么

这里的 extract 不是整篇 legacy 文档迁移。

这里的 extract 只应是按需摘取、按窄对象收口的 legacy 知识碎片，例如：
- 一个 endpoint family 的窄范围文字摘记
- 一个字段簇的候选语义片段
- 一个 relation clue 的去敏追溯说明
- 一个 unresolved contradiction 的最小摘录和来源指针

它的身份只能是：
- downgraded reference input
- rewrite candidate
- traceability anchor

## Extracts 允许放什么

这里允许放：
- 从旧仓 docs、runbook、研究台账中按需摘出的窄范围文字片段
- 已去敏的字段线索、对象线索、关系线索、证据线索
- 指向 legacy 路径或对象的最小追溯说明
- 为后续重写服务的冲突记录、命名歧义、范围界定说明

放置规则：
- 一个 extract 文件只收一个窄对象，不做 whole domain 或 whole family 搬运
- 文件名应按当前窄对象语义命名，不按旧仓目录树机械镜像
- 未重写的 legacy 知识碎片优先先进入这里，不直接写进 [docs/source-intelligence/](../../../source-intelligence/README.md) 的主输出位

## Extracts 不允许变成什么

这里不允许变成：
- formal truth
- API dossier / field dictionary / relation doc / serving-readiness doc 的主输出位
- serving-ready output
- runtime contract、runtime path、schema、CRUD、模型或 API 契约的替代品
- generic evidence warehouse 或 legacy 全量正文堆放区

这里也不允许放：
- 整目录复制的 legacy 正文
- 原始截图、浏览器会话、账号口令、原始导出文件
- 只能依赖旧仓运行方式才能理解的结构性搬运物

## 与 `docs/source-intelligence/**` 的关系

[docs/source-intelligence/](../../../source-intelligence/README.md) 是 repo-owned knowledge assets 的主输出子体系。

这里的 [extracts/](./README.md) 不是那个主输出子体系的一部分，它只负责输入隔离：
- extract 可以为后续 dossier / dictionary / relation / serving-readiness 重写提供输入
- extract 本身不能被写成“已完成输出”
- 真正被吸收后的内容，必须进入 `docs/source-intelligence/**` 或其它被明确批准的 repo-owned docs 位置

换句话说：
- `extracts/` 是 pre-rewrite quarantine
- `docs/source-intelligence/**` 是 post-rewrite output

## Extract 文件的最小元信息字段建议

每个 extract 文件开头建议最少写清以下字段：
- `status`: 当前生命周期状态
- `legacy_source`: 旧仓来源路径、对象名或追溯锚点
- `scope`: 本文件只覆盖的窄对象范围
- `intended_target`: 预期重写去向，例如某个 `docs/source-intelligence/**` 文档类型
- `last_reviewed`: 最近一次人工复核日期
- `notes`: 仍保留的关键降级说明、冲突或不能升级的原因

如果需要，可用最小 front matter 或最小标题块承载这些字段，但不要为了元信息再引入新的模板体系。

## 生命周期状态

当前最小生命周期状态固定为：

- `to-rewrite`
  - 已进入隔离区，允许作为后续重写输入，但尚未变成 repo-owned output
- `consumed`
  - 关键知识已被重写吸收进 repo-owned docs；原 extract 只保留追溯价值，不再充当活动输出
- `dropped`
  - 已确认不值得继续吸收，或无法稳定复核；保留时也只作为被放弃的 trace note

状态变化规则：
- 从 `to-rewrite` 升到 `consumed` 时，必须能指出被吸收后的 repo-owned 落点
- `dropped` 不等于删除 legacy 来源，只表示当前主线不再消费这份 extract

## 当前边界

本包只建立这个隔离区和放置规则：
- 不开始迁任何 legacy 正文
- 不新增 dossier / field dictionary / relation / serving-readiness 正文
- 不改变 runtime、contract、path
