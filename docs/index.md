# AIXSILICON Workflow / Repo 规划体系索引

> 本目录是 AIXSILICON 多仓工作区（`aixsilicon_workflow` 控制面 + 10 个资产仓）规划与建设的统一入口。
> 每个 repo 及 workflow 均拥有**独立的 Plan 与 Todo**；旧版规划材料已整体归档至 [`archived/`](archived/README.md)。

## 1. 全局规划

| 文档 | 内容 |
|---|---|
| [`workflow-repo-plan.md`](workflow-repo-plan.md) | **全局建设规划**：定位与责任链、仓库全景与依赖、两条主线、核心机制、治理契约、G0–G7、分阶段路线、风险与验收 |

## 2. 各仓 Plan / Todo

| 仓 | Plan | Todo | 类型 |
|---|---|---|---|
| workflow（控制面） | [`workflow/plan.md`](workflow/plan.md) | [`workflow/todo.md`](workflow/todo.md) | workflow |
| hwif | [`hwif/plan.md`](hwif/plan.md) | [`hwif/todo.md`](hwif/todo.md) | hw-interface |
| cbb | [`cbb/plan.md`](cbb/plan.md) | [`cbb/todo.md`](cbb/todo.md) | cbb |
| ip | [`ip/plan.md`](ip/plan.md) | [`ip/todo.md`](ip/todo.md) | ip |
| dv-common | [`dv-common/plan.md`](dv-common/plan.md) | [`dv-common/todo.md`](dv-common/todo.md) | dv-common |
| vip | [`vip/plan.md`](vip/plan.md) | [`vip/todo.md`](vip/todo.md) | vip |
| tools | [`tools/plan.md`](tools/plan.md) | [`tools/todo.md`](tools/todo.md) | tool |
| catalog | [`catalog/plan.md`](catalog/plan.md) | [`catalog/todo.md`](catalog/todo.md) | catalog |
| soc-integration | [`soc-integration/plan.md`](soc-integration/plan.md) | [`soc-integration/todo.md`](soc-integration/todo.md) | soc-integration |
| skills | [`skills/plan.md`](skills/plan.md) | [`skills/todo.md`](skills/todo.md) | skill（私有） |
| knowledge | [`knowledge/plan.md`](knowledge/plan.md) | [`knowledge/todo.md`](knowledge/todo.md) | other |

## 3. 归档区

| 文档 | 内容 |
|---|---|
| [`archived/README.md`](archived/README.md) | 归档索引 |
| [`archived/root/`](archived/root/README.md) | 旧版根 plan / todo / build_todolist |
| [`archived/adr/`](archived/adr/README.md) | ADR-0001~0006 |
| [`archived/architecture/`](archived/architecture/README.md) | 旧方案说明 / 关系框图 / 各仓 plan-todo 收口 |
| [`archived/plans/`](archived/plans/README.md) | 跨仓架构评审 / 跨仓优化规划 |
| [`archived/global-todolist.md`](archived/global-todolist.md) | 旧全局统一 todo（已拆分至各仓 todo） |

## 4. 快速阅读

1. 全局：阅读 [`workflow-repo-plan.md`](workflow-repo-plan.md) 了解体系与路线；
2. 单仓：进入对应 `docs/<repo>/` 查看 plan + todo；
3. 回溯：历史决议与细节进入 [`archived/`](archived/README.md)。

## 5. 一句话

> **Skill 理解辅助 → Workflow 顺序与 Gate → Tool 确定性执行 → 资产仓 SSOT/交付 → Catalog 发布/发现 → EDA 工程证据**；Manifest 驱动、独立 Clone、统一 CLI（`aix`）、FuseSoC 聚合、Change Bundle 协调。
