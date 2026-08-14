# Architecture Decision Records (ADR)

本目录记录 `aixsilicon_workflow` 的关键架构决策。

## 索引

| ADR | 状态 | 决策 |
|---|---|---|
| [0001-manifest-over-submodule](0001-manifest-over-submodule.md) | 接受 | 采用 Manifest + 独立 Clone，默认不用 Git Submodule |
| [0002-schema-driven-yaml](0002-schema-driven-yaml.md) | 接受 | 所有工作区/流程/证据事实以 YAML SSOT + JSON Schema 固化 |
| [0003-unified-vlnv-namespace](0003-unified-vlnv-namespace.md) | 接受 | 全组织统一 VLNV 命名空间 `aixsilicon:*` |
| [0004-cli-entry-and-plugin-registry](0004-cli-entry-and-plugin-registry.md) | 接受 | 统一 CLI 入口 `aix` 与插件注册组 `aixsilicon.commands` |
| [0005-cross-repo-boundary-map](0005-cross-repo-boundary-map.md) | 接受 | 跨仓边界映射（幽灵仓库收敛） |
| [0006-tool-ownership-and-migration](0006-tool-ownership-and-migration.md) | 接受 | 确定性工具归属四类与分阶段迁移路径 |

## 如何新增 ADR

1. 复制模板 `docs/adr/_template.md`；
2. 编号为 `NNNN-<slug>.md`；
3. 记录：状态、背景、决策、结果、备选方案。
