# catalog — AIXSILICON Catalog Repository 建设规划

> 客观事实基线：2026-08-13（骨架：index + 7 资产条目 + schema）。原文细节见 [`../archived/architecture/repo-plans/catalog.md`](../archived/architecture/repo-plans/catalog.md)。
> 本文件已并入 archived 原文的现状与待补充规划：资产条目索引（`catalog/index.yaml` + `catalog/assets/` + `schemas/catalog-asset.schema.json`）、定位/生命周期/发布更新流程与发布流对接。

## 1. 定位与边界

**定位**：已发布资产索引、兼容矩阵与成熟度——被所有消费者共享的“发布资产目录”，生命周期不同于流程代码。

| 归属本仓 | 不归本仓 |
|---|---|
| 资产条目（VLNV / Git URL / Tag / SHA / SemVer / 依赖 / License / Owner / Evidence） | 资产源码/交付物 |
| 兼容矩阵、成熟度映射 | 本地开发 Manifest / Lockfile（Workflow 管） |
| `catalog-asset.schema.json`（Schema 所有权） | 生成器实现（tools） |

**边界纪律**：Catalog **只索引正式发布资产**，不存开发分支 RTL；与 Workspace Manifest **不重复**——Manifest 描述工作区，Catalog 描述已发布可复用资产。

## 2. 现状（客观）

- `catalog/index.yaml`：资产索引入口；
- `catalog/assets/`：首批 7 条资产（cbb-hac-adapters / dv-common-types / hwif-apb / hwif-hac-if / ip-hac-aes / ip-uart / vip-hac-if）；
- `schemas/catalog-asset.schema.json`：资产条目 Schema（已定义）；
- **缺口**：条目随各仓 release 持续填充；兼容矩阵与成熟度映射落地；与 `release-train` 更新 PR 对接。

## 3. 依赖与角色

- **依赖**：无；
- **被依赖**：soc-integration（`catalog.resolve` 选型）、workflow（`catalog.update` / `catalog.update-pr`）；
- **IP 主线角色**：IP 发布后 `catalog.update` 写入资产条目；
- **SoC 主线角色**：SoC 集成起步 `catalog.resolve` 做资产选型。

## 4. 契约

- **Schema 所有权**：`catalog-asset`；
- **成熟度**：统一外部尺度 `draft / qualified / proven / deprecated`（各仓内部词汇映射）；
- **更新方式**：生成草案 + PR，不自动 merge；配合 `release-train` 的 `catalog.update-pr`。

## 5. 建设路线（客观）

| 阶段 | 目标 | 状态 |
|---|---|---|
| 骨架 | index + assets + schema | ✅ 完成 |
| 首轮填充 | 首批 `qualified` 条目（出口：覆盖 IP/CBB/VIP/HWIF/DV-Common 至少各 1 个） | ⬜（随各仓 release） |
| 完善 | 兼容矩阵、成熟度映射、自动更新 | ⬜ |

## 6. 仓级待办（本批追加）

- [ ] 首批 `qualified` 资产条目：IP / HWIF / DV-Common 各至少 1（出口：覆盖 IP/CBB/VIP/HWIF/DV-Common 至少各 1 个 `qualified`）
- [ ] 兼容矩阵与成熟度映射落地（各仓内部词汇 → `draft/qualified/proven/deprecated`）
- [ ] 随各仓 release 自动/受控更新（`aix release publish` → Catalog PR，不自动 merge）

## 7. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/catalog.md`](../archived/architecture/repo-plans/catalog.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/catalog.md` 现状（index/assets/schema）与待补充规划（定位/生命周期、发布更新流程、发布流对接）；仓级待办为本批追加。
