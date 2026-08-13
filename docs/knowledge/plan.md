# knowledge — AIXSILICON ChipKnowledge 知识库建设规划

> 客观事实基线：2026-08-13（五层架构迁移完成、Draft 基线形成）。原文细节见 [`../archived/architecture/repo-plans/knowledge.md`](../archived/architecture/repo-plans/knowledge.md)。

## 1. 定位与边界

**定位**：芯片研发知识库（方法论/术语/参考索引），`exports: [chip-knowledge]`；18 卷芯片设计验证知识手册。

| 本仓负责 | 不负责 |
|---|---|
| 知识手册（18 卷）、术语、参考索引 | 资产事实/源码（各资产仓） |
| 参考材料规范、检索 Skill | SSOT 替代（各仓自管） |
| 方法论沉淀 | 确定性工程执行（workflow/tools） |

## 2. 现状（客观）

- **五层架构迁移完成**（knowledge / app / template-script-schema / skill / project-data）；
- **18 卷知识手册**：卷 01 基本完成；卷 02–04/06–16 大量章节已 Draft（**待 Owner/工具验证**）；卷 05（核心领域 IP）、卷 17（AI 辅助）、卷 18（工程案例）未开始；
- **ROADMAP 阶段 0 基线**：B0-05 首条案例链（参数化流水线 MAC）完成草案、B0-09 五层架构迁移完成；B0-06 指定 Owner/Reviewer、B0-07 冻结工具基线、B0-08 技术评审 **待组织决策**；
- **缺口**：Owner/Reviewer 指定、技术评审、卷 05/17/18、MAC 案例知识链、横向资产（术语表/来源登记/评测题）。

## 3. 依赖与角色

- **依赖**：无（独立知识域）；
- **角色**：横向知识供给，为 Skill 与工程实践提供方法论/术语/参考；不参与资产依赖 DAG。

## 4. 契约

- **成熟度**：调研 → Draft → Technical Review → Engineering Verified → Released；
- **质量纪律**：未获 Owner/Reviewer/工程证据不得虚标完成；内容完成 ≠ Released。

## 5. 建设路线（客观）

| 阶段 | 目标 | 状态 |
|---|---|---|
| 0 基线设计 | 案例链、Owner、工具基线、五层架构 | 🔶 部分（架构迁移/案例草案完成；Owner/工具/评审待决策） |
| 1 MVP | 核心知识页（数字基础/需求架构/RTL/功能验证/静态/PPA）、MAC 案例可复现 | ⬜ |

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/knowledge.md`](../archived/architecture/repo-plans/knowledge.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
