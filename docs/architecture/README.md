# 体系架构总览

本目录汇总 `aixsilicon_workflow` 多仓工作区体系架构的**总体说明**，回答「整套体系整体怎么运转、边界在哪、Workflow 用什么机制统筹多个仓库」。

## 正文导航

| 文档 | 用途 |
|---|---|
| [overview.md](overview.md) | **总体方案**：定位、责任链（Skill→Workflow→Tool→Asset→Catalog→EDA）、L0–L5 分层、核心对象、父仓目录结构、开源/私有边界 |
| [repos.md](repos.md) | **被统筹对象**：10 个 repo 每仓一份材料（定位/职责/依赖/主线角色/Schema 所有权/工具归属）＋ 关系阐述（依赖 DAG、数据流、写入边界、Schema 所有权） |
| [workflows.md](workflows.md) | **统筹方案（核心）**：Flow DAG + 注册 action + write_scope + Gate + Evidence 五要素；IP 设计验证与 SoC 集成验证两条主线；支撑流程定位；workflow × repo 统筹矩阵；Gate 卡点 |
| [relationship-diagram.md](relationship-diagram.md) | **关系框图**：5 张 Mermaid 图（仓库依赖 DAG、责任链数据流、两条主线链路、L0–L5 分层）＋ 读法表 |

## 文档组织方式

本目录按「README 索引 → overview 总体方案 → repos 被统筹对象 → workflows 统筹方案 → relationship-diagram 关系框图」组织：overview 先给全局定位与分层，repos 为每个 repo 提供一份材料并单独成章阐述关系，workflows 是核心（两条主线 + 支撑流程 + 统筹矩阵 + Gate 卡点），relationship-diagram 用 5 张 Mermaid 图把整个体系可视化。

> 建议阅读顺序：先图（relationship-diagram）→ 总览（overview）→ repo 材料（repos）→ 统筹（workflows）→ 回图对照。

## 相关

- 架构决策记录（ADR）：[`docs/adr/`](../adr/README.md)
- 规划索引与阅读地图：[`docs/index.md`](../index.md)
