# soc-integration — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/soc-integration.md`](../archived/architecture/repo-plans/soc-integration.md)。
> 本文件已并入 archived 原文的现状与待补充规划（合并补充），并追加仓级待办。

## 已完成

- [x] `schema/soc-config.schema.json`（SoC 配置 Schema 单一 Owner）
- [x] `examples/minimal-soc.yaml`、`examples/hac-accel-soc.yaml`

## P0 优先

- [ ] 完整 Schema 集（instance / address / irq / crg / power / connect 分域）
- [ ] 最小 SoC Golden 示例（出口：SoC YAML 可通过地址/中断/连接检查）
- [ ] 定义通用能力 vs 具体产品 Top 的边界（后者归私有 `chip_<project>_soc_repo`）

## P1 首个季度

- [ ] Address / IRQ / CRG Checker 接入（配合 tool 生成器）
- [ ] Connectivity 检查与集成级 Assertion 规则
- [ ] SoC YAML 可通过地址/中断/连接检查

## P2 两个季度

- [ ] 集成规则（Tie-off/Default Slave/Timeout/CDC-RDC）
- [ ] 规模化基线重建（配合 workflow `soc.baseline`）
- [ ] 参考 SoC（`aixsilicon_reference_soc_repo` 待建）联动

## 治理

- [ ] 生成实现归 tool_repo、流程 DAG 归 workflow（C4）
- [ ] techlib 引用统一 `aixsilicon_techlib_repo`（A4）

## 仓级待办（本批追加）

- [ ] 完整 Schema 集（address / irq / crg / power / connect 分域）
- [ ] 配合 tool 的 Address / IRQ / CRG Checker 接入
- [ ] 最小 SoC Golden 示例（出口：SoC YAML 可通过地址/中断/连接检查）

## 变更记录

| 日期 | 变更内容 | 作者 |
|------|---------|------|
| 2026-08-13 | 本文件并入 archived 原文现状与待补充规划（合并补充）并追加仓级待办（完整 Schema 集 / Checker 接入 / 最小 SoC Golden） | Zoo |

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/soc-integration.md` 现状（soc-config schema / examples）与待补充规划（边界、tools 契约、workflow 衔接）；仓级待办为本批追加。
