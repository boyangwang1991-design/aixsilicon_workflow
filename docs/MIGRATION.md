# 历史材料迁移与删除记录

本表是旧 `docs/archived/` 的最终覆盖与删除凭证，并记录后续活动材料的结构收敛。历史源共 45 个文件，已于 2026-08-13 在人工批准后从工作树删除；原文可从 Git 历史恢复。`absorbed` 表示内容已进入当前材料，`verbatim-reference` 表示长篇细节已完整迁入当前设计参考且旧状态不再生效。

## 1. 覆盖结果

| 历史源（相对 `docs/archived/`） | 当前落点 | 处理 | 状态 |
|---|---|---|---|
| `README.md` | `docs/index.md`、`docs/governance.md` | 重建入口和历史退出规则 | absorbed |
| `collaboration.md` | `docs/workflow/collaboration.md` | 合并扩展 | absorbed |
| `getting-started.md` | `docs/getting-started.md` | 与 quickstart 合并 | absorbed |
| `global-todolist.md` | `docs/roadmap.md`、`docs/progress.md`、各仓 `delivery.md` | 按组合/仓拆分 | absorbed |
| `manifest.md` | `docs/workflow/manifest.md` | 合并扩展 | absorbed |
| `maturity-model.md` | `docs/workflow/release.md` | 合并到发布与资产消费治理 | absorbed |
| `optimization-plan.md` | `docs/reference/workflow-engineering-review.md`、`docs/workflow/README.md`、`delivery.md` | 完整历史参考 + 活动实施拆分 | verbatim-reference |
| `quickstart.md` | `docs/getting-started.md` | 去重合并 | absorbed |
| `release.md` | `docs/workflow/release.md` | 合并扩展 | absorbed |
| `schema-ownership.md` | `docs/workflow/ownership.md`、`ownership-map.yaml` | 文档 + 机器可读 SSOT | absorbed |
| `tool-placement.md` | `docs/workflow/ownership.md`、`ownership-map.yaml` | 与 Schema/仓库 Owner 合并为统一归属契约 | absorbed |
| `troubleshooting.md` | `docs/workflow/troubleshooting.md` | 当前正文 | absorbed |
| `COVERAGE.md` | `docs/MIGRATION.md` | 空历史文件由本表重建 | absorbed |
| `adr/README.md` | `docs/adr/README.md` | 当前索引 | absorbed |
| `adr/_template.md` | `docs/adr/_template.md` | 当前模板 | absorbed |
| `adr/0001-manifest-over-submodule.md` | `docs/adr/0001-manifest-over-submodule.md` | 当前 ADR | absorbed |
| `adr/0002-schema-driven-yaml.md` | `docs/adr/0002-schema-driven-yaml.md` | 当前 ADR | absorbed |
| `adr/0003-unified-vlnv-namespace.md` | `docs/adr/0003-unified-vlnv-namespace.md` | 当前 ADR | absorbed |
| `adr/0004-cli-entry-and-plugin-registry.md` | `docs/adr/0004-cli-entry-and-plugin-registry.md` | 当前 ADR | absorbed |
| `adr/0005-cross-repo-boundary-map.md` | `docs/adr/0005-cross-repo-boundary-map.md` | 当前 ADR | absorbed |
| `adr/0006-tool-ownership-and-migration.md` | `docs/adr/0006-tool-ownership-and-migration.md` | 当前 ADR | absorbed |
| `architecture/README.md` | `docs/architecture/README.md` | 重建索引 | absorbed |
| `architecture/overview.md` | `docs/architecture/overview.md` | 当前正文 | absorbed |
| `architecture/plan.md` | `docs/architecture/README.md`、`docs/governance.md` | 组织规则合并 | absorbed |
| `architecture/relationship-diagram.md` | `docs/architecture/overview.md`、`docs/architecture/repos.md`、`docs/architecture/workflows.md` | 分层、依赖与主线图按唯一职责拆入当前正文 | absorbed |
| `architecture/repos.md` | `docs/architecture/repos.md`、`docs/architecture/target-design.md` | 当前职责正文 + 现状评审/目标方案 | absorbed |
| `architecture/workflows.md` | `docs/architecture/workflows.md`、`roadmap.md` | 当前正文 + 执行顺序 | absorbed |
| `architecture/repo-plans/README.md` | `docs/index.md` | 统一仓级入口 | absorbed |
| `architecture/repo-plans/hwif.md` | `docs/hwif/design-reference.md`、`README.md`、`delivery.md` | 完整参考 + 活动拆分 | verbatim-reference |
| `architecture/repo-plans/cbb.md` | `docs/cbb/design-reference.md`、`README.md`、`delivery.md` | 完整参考 + 活动拆分 | verbatim-reference |
| `architecture/repo-plans/ip.md` | `docs/ip/design-reference.md`、`README.md`、`delivery.md` | 完整参考 + 活动拆分 | verbatim-reference |
| `architecture/repo-plans/dv-common.md` | `docs/dv-common/design-reference.md`、`README.md`、`delivery.md` | 完整参考 + 活动拆分 | verbatim-reference |
| `architecture/repo-plans/vip.md` | `docs/vip/design-reference.md`、`README.md`、`delivery.md` | 完整参考 + 活动拆分 | verbatim-reference |
| `architecture/repo-plans/tools.md` | `docs/tools/design-reference.md`、`README.md`、`delivery.md` | 完整参考 + 活动拆分 | verbatim-reference |
| `architecture/repo-plans/catalog.md` | `docs/catalog/design-reference.md`、`README.md`、`delivery.md` | 完整参考 + 活动拆分 | verbatim-reference |
| `architecture/repo-plans/soc-integration.md` | `docs/soc-integration/design-reference.md`、`README.md`、`delivery.md` | 完整参考 + 活动拆分 | verbatim-reference |
| `architecture/repo-plans/skills.md` | `docs/skills/design-reference.md`、`README.md`、`delivery.md` | 完整参考 + 活动拆分 | verbatim-reference |
| `architecture/repo-plans/knowledge.md` | `docs/knowledge/design-reference.md`、`README.md`、`delivery.md` | 完整参考 + 活动拆分 | verbatim-reference |
| `plans/README.md` | `docs/index.md` | 统一导航 | absorbed |
| `plans/cross-repo-architecture-review.md` | `docs/reference/cross-repo-architecture-review.md`、`docs/architecture/target-design.md` | 原评审 + 当前复审/目标方案 | absorbed |
| `plans/cross-repo-optimization-plan.md` | `docs/reference/cross-repo-optimization-plan.md`、`docs/roadmap.md` | 原规划 + 当前排序 | absorbed |
| `root/README.md` | `docs/index.md`、`docs/governance.md` | 统一入口和历史规则 | absorbed |
| `root/plan.md` | `docs/reference/workflow-requirements.md`、`docs/reference/workflow-repo-plan.md`、`docs/roadmap.md` | 完整历史参考 + 当前路线 | verbatim-reference |
| `root/todo.md` | `docs/progress.md`、`docs/workflow/delivery.md` | 组合状态 + 仓级任务 | absorbed |
| `root/aixsilicon_build_todolist.md` | `docs/roadmap.md`、各仓 `delivery.md` | 按里程碑和 Owner 拆分 | absorbed |

覆盖计数：根级 13 + ADR 8 + architecture 6 + repo-plans 11 + plans 3 + root 4 = **45/45**。

## 2. 迁移后的权威规则

- `design-reference.md` 和 `docs/reference/` 保存完整细节，但其中的旧 Todo、百分比、日期与优先级均为历史上下文；
- 当前跨仓排序只看 `roadmap.md`；
- 当前组合状态只看 `progress.md`；
- 当前仓级状态只看 `docs/<repo>/delivery.md`；
- 架构边界看 `architecture/`、ADR、Manifest 和 ownership map。

## 3. 删除检查表

- [x] 45 个历史源均有当前落点；
- [x] 10 个仓的长篇规划已完整迁入 `design-reference.md`；
- [x] Workflow 完整旧规划和工程化方案已有当前 reference；
- [x] 根 README、AGENT 和活动 docs 不再链接 `docs/archived/`；
- [x] 删除前 Markdown 本地链接检查通过（68 个活动 Markdown 文件，0 个断链）；
- [x] Ruff、Schema parity 和 51 项 Pytest 通过；
- [x] 45 个历史文件均受 Git 跟踪，可从 Git 历史恢复；
- [x] 人工评审确认并批准删除；
- [x] `docs/archived/` 已删除。

删除命令：`git rm -r -- docs/archived`。该操作删除 45 个受跟踪文件；未触及其他目录。

删除后复核：68 个当前 Markdown 文件、0 个断链、0 个旧归档链接、0 个尾随空白、0 个混合换行；JSON/YAML 解析通过；Ruff lint、6 个 Schema parity、VLNV/运行时路径 Guard 和 51 项 Pytest 通过。

已知非阻塞项：Ruff format 报告 3 个既有 Python 文件需要格式化；原统一入口仍存在 Windows `.venv/bin/python` 路径和 pre-commit 隔离环境安装超时问题。这些作为独立工程化风险保留在 [`progress.md`](progress.md) R-07，不影响历史内容覆盖与 Git 可恢复性判定。

## 4. 活动材料二次收敛

为消除根级、architecture 与 workflow 的重复，活动材料按唯一职责重新分层；长篇原文只移动和补充导航说明，不删减设计正文。

| 原活动路径 | 当前路径/落点 | 处理 |
|---|---|---|
| `docs/workflow-repo-plan.md` | `docs/reference/workflow-repo-plan.md` | 完整十仓全景移入历史参考；当前顺序改看 roadmap |
| `docs/workflow/requirements-reference.md` | `docs/reference/workflow-requirements.md` | 完整旧总体需求移动保留 |
| `docs/workflow/engineering-reference.md` | `docs/reference/workflow-engineering-review.md` | 完整工程评审移动保留 |
| `docs/workflow/cross-repo-architecture-review.md` | `docs/reference/cross-repo-architecture-review.md` | 原问题编号/依据保留；当前结论看 target-design |
| `docs/workflow/cross-repo-optimization-plan.md` | `docs/reference/cross-repo-optimization-plan.md` | 原决策背景保留；当前执行顺序看 roadmap |
| `docs/workflow/schema-ownership.md` + `tool-placement.md` | `docs/workflow/ownership.md` | 合并为 Schema、仓库和工具统一归属契约 |
| `docs/workflow/maturity-model.md` | `docs/workflow/release.md` | 成熟度并入 Gate/Evidence/Release 消费闭环 |
| `docs/workflow/plan.md` + `todo.md` | `docs/workflow/README.md` + `delivery.md` | 移除全局阶段/状态复制，只保留 Workflow 设计契约与唯一活动台账 |
| `docs/COVERAGE.md` | `docs/MIGRATION.md` | 兼容指针无独立信息，入口收敛到本表 |

当前结构：根级管理入口/治理/规划/状态，`architecture/` 管稳定结构，`workflow/` 管可执行契约和交付，`reference/` 管完整历史背景；各资产仓使用 README 设计契约 + delivery 活动台账 + design-reference 历史细节。
