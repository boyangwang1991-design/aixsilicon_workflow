# repo-plans — 各子仓 plan/todo 统一统筹

> 目的：把分散在各子仓的 **plan / todo / roadmap** 统一收口到 workflow 的 `docs/architecture/repo-plans/` 集中管理。
> 迁移方式：原文件已从各子仓**完整剪切**（内容零删改保留，原文件删除并在各子仓 commit）；catalog、soc-integration 原无 plan/todo，建占位文档。
> 迁移日期：2026-08-13

## 1. 迁移总览

| 仓库 | 原子仓来源文件 | 收口文档 | 状态 |
|---|---|---|---|
| hwif | `repos/aixsilicon_hwif_repo/{plan.md, todo.md}` | [`hwif.md`](hwif.md) | ✅ 已剪切 |
| cbb | `repos/aixsilicon_cbb_repo/{cbb_repo_plan.md, cbb_repo_list.md}` | [`cbb.md`](cbb.md) | ✅ 已剪切 |
| ip | `repos/aixsilicon_ip_repo/plan.md` | [`ip.md`](ip.md) | ✅ 已剪切 |
| dv-common | `repos/aixsilicon_dv_common/{plan.md, TODO.md}` | [`dv-common.md`](dv-common.md) | ✅ 已剪切 |
| vip | `repos/aixsilicon_vip_repo/plan.md` | [`vip.md`](vip.md) | ✅ 已剪切 |
| tools | `repos/aixsilicon_tool_repo/{tool_repo_plan.md, todo.md}` | [`tools.md`](tools.md) | ✅ 已剪切 |
| skills | `repos/aixsilicon_skill_repo/{skill_repo_plan.md, todo.md}` | [`skills.md`](skills.md) | ✅ 已剪切 |
| knowledge | `repos/aixsilicon_chipknowledge/{TODO.md, ROADMAP.md, plans/reference-material-spec.md}` | [`knowledge.md`](knowledge.md) | ✅ 已剪切 |
| catalog | （无独立 plan/todo） | [`catalog.md`](catalog.md) | 📄 占位待建 |
| soc-integration | （无独立 plan/todo） | [`soc-integration.md`](soc-integration.md) | 📄 占位待建 |

## 2. 管理原则

- **本目录是各仓 plan/todo 的唯一管理入口（SSOT）**，原子仓不再各自维护规划文件；
- 文档内容为原子仓原文**完整保留**（未做删改），确保与各仓实现一致；
- 未来各仓计划/待办更新**直接在本目录维护**，并同步更新 [`../repos.md`](../repos.md) / [`../workflows.md`](../workflows.md) 等索引；
- 新增仓库（techlib / model / sw / reference-soc）接入后在此补位，并在 [`../repos.md`](../repos.md) 登记。

## 3. 链接重映射说明（重要）

> 各份文档的**正文为原子仓 plan/todo 的完整原文（零删改）**，其中相对链接原本指向**原子仓内部路径**（如 `plan.md`、`schema/`、`tools/...`、`reference/...`）。

- 迁移后这些链接在 `repo-plans/` 下不再指向原子仓（`repos/` 为运行时克隆区且被父仓 `.gitignore` 忽略）；
- 如需查看对应文件：请前往 `repos/<repo-id>/<path>`（如 `repos/aixsilicon_hwif_repo/`）；
- 引用原子仓文件时请使用指向 `repos/<repo-id>` 的完整相对路径，或改用本目录/`../repos.md` 中有效的链接；
- 本目录**新增/修改**内容请使用相对本目录正确的链接，并在 [`../repos.md`](../repos.md) / [`../workflows.md`](../workflows.md) 保持同步。

## 3. 配套

- 仓库全景与依赖：**[../repos.md](../repos.md)**
- 统筹编排：**[../workflows.md](../workflows.md)**
- 关系框图：**[../relationship-diagram.md](../relationship-diagram.md)**
- 本目录规划底稿：**[../plan.md](../plan.md)**
