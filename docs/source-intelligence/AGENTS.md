# Source Intelligence 子树协作导轨

这份文档服务于 `docs/source-intelligence/**`。

它不是 formal source of truth，也不是知识主输出位。
formal truth 仍以仓库根 [README.md](../../README.md)、[docs/README.md](../README.md)、已 landed 的 formal docs，以及当前 `main` 上的 `src/app/**`、`src/migrations/**`、`tests/**` 为准。

## 子树定位

这个子树是 repo-owned source-intelligence knowledge assets 的主输出区。
它负责收口重写后的知识资产，不负责承接未重写的 legacy 碎片。

## 主输出位

当前主输出位只包括：
- [migration-charter.md](./migration-charter.md)
- [legacy-source-intelligence-inventory-baseline.md](./legacy-source-intelligence-inventory-baseline.md)
- [apis/README.md](./apis/README.md)
- [fields/README.md](./fields/README.md)
- [relations/README.md](./relations/README.md)
- [serving-readiness/README.md](./serving-readiness/README.md)

## 非输出位

[docs/reference/legacy-backend/extracts/README.md](../reference/legacy-backend/extracts/README.md) 只是输入隔离区，不是 output slot。

不要把以下材料直接升级成 truth 或主输出：
- legacy extract
- screenshot
- runbook
- raw sample

这些材料如果要进入这个子树，必须先被重写成 repo-owned knowledge asset，并写清 evidence level。

## 默认先读

默认阅读顺序：
1. [README.md](./README.md)
2. [migration-charter.md](./migration-charter.md)
3. [docs/reference/legacy-backend/README.md](../reference/legacy-backend/README.md)
4. [docs/reference/legacy-backend/extracts/README.md](../reference/legacy-backend/extracts/README.md)
5. 再进入你这次要改的具体 output slot README 或目标文档

## Review 最低问题集

每次知识迁移包的 review，至少回答：
- 这次新增了什么 repo-owned knowledge
- 它是否明显提升了 contract-ready 或 serving-ready 判断能力
- 它是否只是重复搬运已有线索
- 新内容是否进入了明确 output slot，而不是停留在 extract/input lane
