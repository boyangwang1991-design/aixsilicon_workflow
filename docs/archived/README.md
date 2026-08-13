# AIXSILICON 归档区（历史规划材料）

> 本目录保存旧版规划材料，**仅作历史参考**；当前规划与建设入口见 [`../index.md`](../index.md) 与 [`../workflow-repo-plan.md`](../workflow-repo-plan.md)。
> 归档日期：2026-08-13（docs 体系重构）。

## 目录结构

| 路径 | 内容 |
|---|---|
| [`adr/`](adr/README.md) | ADR-0001~0006（Manifest 选型 / Schema 驱动 / VLNV 统一 / CLI 插件 / 跨仓边界 / 工具归属） |
| [`architecture/`](architecture/README.md) | 旧方案说明（overview / repos / workflows / relationship-diagram）+ 各仓 plan-todo 收口（[`repo-plans/`](architecture/repo-plans/README.md)） |
| [`plans/`](plans/README.md) | 跨仓架构评审（R/A/C 决议）、跨仓优化规划（D1–D5） |
| [`root/`](root/README.md) | 旧根 `plan.md` / `todo.md` / `aixsilicon_build_todolist.md` |
| [`global-todolist.md`](global-todolist.md) | 旧全局统一 todo（已拆分至各仓独立 todo） |
| 顶层 `.md` | 旧 `manifest / maturity-model / optimization-plan / schema-ownership / tool-placement / release / collaboration / getting-started / quickstart / troubleshooting` |

## 使用建议

- 需要**历史决议**（ADR、跨仓评审 R/A/C、优化 D1–D5）→ 读 `adr/`、`plans/`；
- 需要**各仓 plan/todo 原文**（完整细节）→ 读 `architecture/repo-plans/<id>.md`；
- 需要**旧版根规划全貌** → 读 `root/`；
- 需要**成熟度映射 / Schema 所有权 / 工具归属**等治理事实 → 读顶层对应 `.md`。

> 新规划 / 新待办一律写入 [`../index.md`](../index.md) 索引下的各仓 `plan.md` / `todo.md`，归档区不再作为活动依据。
