# Architecture Decision Records (ADR)

本目录记录 `aixsilicon_workflow` 的关键架构决策。

## 索引

| ADR | 状态 | 决策 |
|---|---|---|
| [0001-manifest-over-submodule](0001-manifest-over-submodule.md) | 接受 | 采用 Manifest + 独立 Clone，默认不用 Git Submodule |
| [0002-schema-driven-yaml](0002-schema-driven-yaml.md) | 接受 | 所有工作区/流程/证据事实以 YAML SSOT + JSON Schema 固化 |

## 如何新增 ADR

1. 复制模板 `docs/adr/_template.md`；
2. 编号为 `NNNN-<slug>.md`；
3. 记录：状态、背景、决策、结果、备选方案。
