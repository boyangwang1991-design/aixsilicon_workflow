# docs/archived → docs 新材料 迁移覆盖跟踪表（COVERAGE）

> 本文档是「`docs/archived` 整理到 `docs` 新材料」工程的**单一事实源（SSOT）覆盖跟踪表**。
> 总表覆盖全部 **45 个** archived 源文件；状态统一为「已迁移」或「已合并」。
> **archived 源文件全部保留**（历史原文供追溯），**清理留待后续**。
>
> 批次说明：
> - 第一批：`docs/adr/`（8）、`docs/architecture/`（5）、`docs/getting-started.md`、`docs/workflow/` 下 9 个治理参考文件；
> - 第二批：root 规划合并进 `docs/workflow-repo-plan.md`、`docs/workflow/plan.md`、`docs/workflow/todo.md` 及 workflow 参考文件；
> - 第三批：repo-plans 11 个合并进各仓 `plan.md` / `todo.md`；
> - 第四批（本批）：索引更新、COVERAGE 生成、失效链接修正与回归验证。

## 迁移覆盖总表（45 行）

| 源文件（`docs/archived/` 下相对路径） | 目标文件 | 处理方式 | 状态 | archived 是否保留 | 备注 |
|---|---|---|---|---|---|
| README.md | `docs/index.md` | 并入归档说明（索引） | 已合并 | 是（保留） | 根级索引；归档说明并入 index.md §归档区 |
| collaboration.md | `docs/workflow/collaboration.md` | 迁入新目录 | 已迁移 | 是（保留） | 治理参考 |
| getting-started.md | `docs/getting-started.md` | 合并主本 | 已合并 | 是（保留） | 与 quickstart 合并去重 |
| global-todolist.md | `docs/workflow/todo.md`、`docs/workflow-repo-plan.md`、各仓 `todo.md` | 拆分 | 已合并 | 是（保留） | 旧全局统一 todo 拆分至各仓 |
| manifest.md | `docs/workflow/manifest.md` | 迁入新目录 | 已迁移 | 是（保留） | 治理参考 |
| maturity-model.md | `docs/workflow/maturity-model.md` | 迁入新目录 | 已迁移 | 是（保留） | 治理参考 |
| optimization-plan.md | `docs/workflow/plan.md` §工程化 | 合并 | 已合并 | 是（保留） | 代码工程化方案 |
| quickstart.md | `docs/getting-started.md` | 合并去重 | 已合并 | 是（保留） | 与 getting-started 合并 |
| release.md | `docs/workflow/release.md` | 迁入新目录 | 已迁移 | 是（保留） | 治理参考 |
| schema-ownership.md | `docs/workflow/schema-ownership.md` | 迁入新目录 | 已迁移 | 是（保留） | 治理参考 |
| tool-placement.md | `docs/workflow/tool-placement.md` | 迁入新目录 | 已迁移 | 是（保留） | 治理参考 |
| troubleshooting.md | `docs/workflow/troubleshooting.md` | 迁入新目录 | 已迁移 | 是（保留） | 治理参考 |
| COVERAGE.md | `docs/COVERAGE.md` | 空文件重建 | 已迁移 | 是（保留） | 覆盖表重建（即本文档） |
| adr/README.md | `docs/adr/README.md` | 迁入新目录 | 已迁移 | 是（保留） | ADR 索引 |
| adr/_template.md | `docs/adr/_template.md` | 迁入新目录 | 已迁移 | 是（保留） | ADR 模板 |
| adr/0001-manifest-over-submodule.md | `docs/adr/0001-manifest-over-submodule.md` | 迁入新目录 | 已迁移 | 是（保留） | — |
| adr/0002-schema-driven-yaml.md | `docs/adr/0002-schema-driven-yaml.md` | 迁入新目录 | 已迁移 | 是（保留） | — |
| adr/0003-unified-vlnv-namespace.md | `docs/adr/0003-unified-vlnv-namespace.md` | 迁入新目录 | 已迁移 | 是（保留） | — |
| adr/0004-cli-entry-and-plugin-registry.md | `docs/adr/0004-cli-entry-and-plugin-registry.md` | 迁入新目录 | 已迁移 | 是（保留） | — |
| adr/0005-cross-repo-boundary-map.md | `docs/adr/0005-cross-repo-boundary-map.md` | 迁入新目录 | 已迁移 | 是（保留） | 本批修正 `../../plan.md` 失效链接 |
| adr/0006-tool-ownership-and-migration.md | `docs/adr/0006-tool-ownership-and-migration.md` | 迁入新目录 | 已迁移 | 是（保留） | — |
| architecture/README.md | `docs/architecture/README.md` | 重建索引 | 已迁移 | 是（保留） | 架构总览索引 |
| architecture/overview.md | `docs/architecture/overview.md` | 迁入新目录 | 已迁移 | 是（保留） | 本批修正 `../../plan.md` 失效链接 |
| architecture/plan.md | `docs/architecture/README.md` | 组织说明精简并入 | 已合并 | 是（保留） | 无独立文件 |
| architecture/relationship-diagram.md | `docs/architecture/relationship-diagram.md` | 迁入新目录 | 已迁移 | 是（保留） | — |
| architecture/repos.md | `docs/architecture/repos.md` | 迁入新目录 | 已迁移 | 是（保留） | 本批修正 `repo-plans/` 链接 |
| architecture/workflows.md | `docs/architecture/workflows.md` | 迁入新目录 | 已迁移 | 是（保留） | 本批修正 `repo-plans/` 链接 |
| architecture/repo-plans/README.md | `docs/index.md` | 并入来源注记 | 已合并 | 是（保留） | 各仓 plan/todo 索引并入 index.md §各仓 Plan/Todo |
| architecture/repo-plans/hwif.md | `docs/hwif/plan.md`、`docs/hwif/todo.md` | 合并 | 已合并 | 是（保留） | — |
| architecture/repo-plans/cbb.md | `docs/cbb/plan.md`、`docs/cbb/todo.md` | 合并 | 已合并 | 是（保留） | — |
| architecture/repo-plans/ip.md | `docs/ip/plan.md`、`docs/ip/todo.md` | 合并 | 已合并 | 是（保留） | — |
| architecture/repo-plans/dv-common.md | `docs/dv-common/plan.md`、`docs/dv-common/todo.md` | 合并 | 已合并 | 是（保留） | — |
| architecture/repo-plans/vip.md | `docs/vip/plan.md`、`docs/vip/todo.md` | 合并 | 已合并 | 是（保留） | — |
| architecture/repo-plans/tools.md | `docs/tools/plan.md`、`docs/tools/todo.md` | 合并 | 已合并 | 是（保留） | — |
| architecture/repo-plans/catalog.md | `docs/catalog/plan.md`、`docs/catalog/todo.md` | 合并 | 已合并 | 是（保留） | — |
| architecture/repo-plans/soc-integration.md | `docs/soc-integration/plan.md`、`docs/soc-integration/todo.md` | 合并 | 已合并 | 是（保留） | — |
| architecture/repo-plans/skills.md | `docs/skills/plan.md`、`docs/skills/todo.md` | 合并 | 已合并 | 是（保留） | — |
| architecture/repo-plans/knowledge.md | `docs/knowledge/plan.md`、`docs/knowledge/todo.md` | 合并 | 已合并 | 是（保留） | — |
| plans/README.md | `docs/workflow/cross-repo-architecture-review.md`、`docs/workflow/cross-repo-optimization-plan.md` | 并入导语 | 已合并 | 是（保留） | 无独立文件 |
| plans/cross-repo-architecture-review.md | `docs/workflow/cross-repo-architecture-review.md` | 迁入新目录 | 已迁移 | 是（保留） | — |
| plans/cross-repo-optimization-plan.md | `docs/workflow/cross-repo-optimization-plan.md` | 迁入新目录 | 已迁移 | 是（保留） | — |
| root/README.md | `docs/index.md` | 并入归档区说明 | 已合并 | 是（保留） | 归档区说明并入 index.md |
| root/plan.md | `docs/workflow-repo-plan.md`、`docs/workflow/plan.md`、`docs/workflow/manifest.md`、`docs/workflow/collaboration.md`、`docs/workflow/release.md` | 拆分 | 已合并 | 是（保留） | 全局规划拆分合并 |
| root/todo.md | `docs/workflow/todo.md` | 合并 | 已合并 | 是（保留） | — |
| root/aixsilicon_build_todolist.md | `docs/workflow-repo-plan.md`、各仓 `todo.md` | 拆分 | 已合并 | 是（保留） | 建设待办拆分至各仓 |

## 核对结论

- 源文件计数：**根级 13 + adr 8 + architecture 6 + repo-plans 11 + plans 3 + root 4 = 45**，与任务映射一致；
- 目标文件均已在 `docs/` 下核对存在（`docs/architecture/README.md` 为重建索引、`docs/COVERAGE.md` 为本文档）；
- archived 源文件 **45 个全部保留未删除**，清理留待后续。
