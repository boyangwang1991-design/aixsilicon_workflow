# AIXSILICON Workflow / Repo 规划体系索引

> 本目录是 AIXSILICON 多仓工作区（`aixsilicon_workflow` 控制面 + 10 个资产仓）规划与建设的统一入口。
> 每个 repo 及 workflow 均拥有**独立的 Plan 与 Todo**。

## 1. 快速入口

| 文档 | 内容 |
|---|---|
| [`getting-started.md`](getting-started.md) | **入门指南**：环境准备、初始化、开发与验证流程 |
| [`workflow-repo-plan.md`](workflow-repo-plan.md) | **全局建设规划**：定位与责任链、仓库全景与依赖、两条主线、核心机制、治理契约、G0–G7、分阶段路线、风险与验收 |
| [`adr/README.md`](adr/README.md) | **ADR 索引**：ADR-0001~0006（Manifest / 契约 / 命名 / CLI / 边界 / 工具归属） |
| [`architecture/README.md`](architecture/README.md) | **架构总览**：六层架构、责任链、关系框图、被统筹仓库、Workflow 编排 |
| [`COVERAGE.md`](COVERAGE.md) | **迁移覆盖**：`docs/archived/` → `docs/` 新材料迁移跟踪表（45 个源文件） |

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

## 3. 归档区（历史原文，仅供追溯）

> `docs/archived/` 的内容已并入新结构，**历史原文仍完整保留**在 `docs/archived/` 供追溯，**清理留待后续**。

| 归档原文 | 已并入新结构 |
|---|---|
| [`archived/README.md`](archived/README.md)（根级） | [`index.md`](index.md)（归档说明并入；索引） |
| [`archived/adr/`](archived/adr/README.md)（README、_template、0001–0006） | [`adr/`](adr/README.md)（同名迁移，迁入新目录） |
| [`archived/architecture/`](archived/architecture/README.md)（overview / plan / relationship / repos / workflows） | [`architecture/`](architecture/README.md)（overview / relationship / repos / workflows 迁入；plan 组织说明精简并入 README） |
| [`archived/architecture/repo-plans/`](archived/architecture/repo-plans/README.md)（11 个仓计划） | 对应仓 [`plan.md` / `todo.md`](#2-各仓-plan--todo)（hwif/cbb/ip/dv-common/vip/tools/catalog/soc-integration/skills/knowledge） |
| [`archived/plans/`](archived/plans/README.md)（跨仓架构评审 / 跨仓优化规划） | [`workflow/cross-repo-architecture-review.md`](workflow/cross-repo-architecture-review.md)、[`workflow/cross-repo-optimization-plan.md`](workflow/cross-repo-optimization-plan.md) |
| [`archived/root/`](archived/root/README.md)（旧版 plan / todo / build_todolist） | [`workflow-repo-plan.md`](workflow-repo-plan.md)、[`workflow/plan.md`](workflow/plan.md)、[`workflow/todo.md`](workflow/todo.md) |
| [`archived/`](archived/README.md)（治理参考：collaboration / manifest / maturity-model / optimization-plan / release / schema-ownership / tool-placement / troubleshooting / getting-started / quickstart / global-todolist / COVERAGE） | [`workflow/`](workflow/manifest.md) 各治理参考、[`getting-started.md`](getting-started.md)、[`workflow/todo.md`](workflow/todo.md)、[`COVERAGE.md`](COVERAGE.md) |

## 4. 快速阅读

1. 全局：阅读 [`workflow-repo-plan.md`](workflow-repo-plan.md) 了解体系与路线；
2. 入门：阅读 [`getting-started.md`](getting-started.md)；
3. 单仓：进入对应 `docs/<repo>/` 查看 plan + todo；
4. 回溯：历史决议与细节进入 [`archived/`](archived/README.md)。

## 5. 一句话

> **Skill 理解辅助 → Workflow 顺序与 Gate → Tool 确定性执行 → 资产仓 SSOT/交付 → Catalog 发布/发现 → EDA 工程证据**；Manifest 驱动、独立 Clone、统一 CLI（`aix`）、FuseSoC 聚合、Change Bundle 协调。
