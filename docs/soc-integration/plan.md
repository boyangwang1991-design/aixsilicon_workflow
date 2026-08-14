# soc-integration — AIXSILICON SoC Integration Repository 建设规划

> 客观事实基线：2026-08-13（骨架：soc-config schema + 2 示例）。原文细节见 [`../archived/architecture/repo-plans/soc-integration.md`](../archived/architecture/repo-plans/soc-integration.md)。
> 本文件已并入 archived 原文的现状与待补充规划：SoC 配置 Schema（instance/address/irq/crg/power/connect 事实域）、examples 参考配置、边界（通用能力 vs 具体产品 Top）与 tools/workflow 契约。

## 1. 定位与边界

**定位**：通用 SoC 集成 Schema、模板与规则（实例/地址/中断/CRG/Power/连接）的 SSOT；**不是具体产品 Top**。

| 归属本仓 | 不归本仓 |
|---|---|
| 通用 SoC 配置 Schema（instance/address/irq/crg/power/connect） | 具体芯片 SoC YAML SSOT/Top → 私有 `chip_<project>_soc_repo` |
| 集成模板、规则、参考配置（`examples/`） | 生成器实现（地址/中断/CRG/TopGen）→ tools |
| 集成级 Assertion / Connectivity 规则 | 各资产实现事实 → hwif/cbb/ip |

**分工公式**：Schema 与规则归本仓 → 生成器实现归 tools → 流程 DAG 归 workflow → 具体芯片配置归私有项目仓。

## 2. 现状（客观）

- `schema/soc-config.schema.json`：SoC 配置 Schema（单一事实域 Owner）；
- `examples/`：`minimal-soc.yaml`、`hac-accel-soc.yaml` 参考配置；
- **缺口**：完整 Schema 集（address/irq/crg/power/connect 分域）、配合 tool 的 Checker 接入、最小 SoC Golden。

## 3. 依赖与角色

- **依赖**：`[hwif, cbb, ip, catalog, tools]`（聚合度最高）；
- **被依赖**：无（聚合终点）；
- **SoC 主线角色**：**核心消费/配置方**——`soc.schema-check` 校验 SoC 配置；提供实例化/地址/中断/CRG/Power 规则；
- **IP 主线角色**：基本不参与（IP 粒度）。

## 4. 契约

- **Schema 所有权**：`soc-config（instance/address/irq/crg/power/connect）`；
- **生成实现**：地址/中断/CRG/TopGen 等确定性生成由 `aixsilicon_tool_repo` 提供；
- **VLNV**：`aixsilicon:*` 统一命名空间。

## 5. 建设路线（客观）

| 阶段 | 目标 | 状态 |
|---|---|---|
| 骨架 | soc-config schema + 示例 | ✅ 完成 |
| 完整化 | 完整 Schema 集 + 最小 SoC Golden（出口：SoC YAML 可通过地址/中断/连接检查） | ⬜ |
| 检查接入 | Address/IRQ/CRG/Connect Checker（配合 tool） | ⬜ |
| 规模化 | 集成基线、跨项目复用 | ⬜ |

## 6. 仓级待办（本批追加）

- [ ] 完整 Schema 集（address / irq / crg / power / connect 分域，单一事实域 Owner）
- [ ] 配合 tool 的 Address / IRQ / CRG Checker 接入（生成器由 `aixsilicon_tool_repo` 提供）
- [ ] 最小 SoC Golden 示例（出口：SoC YAML 可通过地址/中断/连接检查）

## 7. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/soc-integration.md`](../archived/architecture/repo-plans/soc-integration.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/soc-integration.md` 现状（soc-config schema / examples）与待补充规划（边界、tools 契约、workflow 衔接）；仓级待办为本批追加。
