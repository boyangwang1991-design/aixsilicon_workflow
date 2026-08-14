# knowledge — AIXSILICON ChipKnowledge 知识库建设规划

> 客观事实基线：2026-08-13（五层架构迁移完成、Draft 基线形成）。原文细节见 [`../archived/architecture/repo-plans/knowledge.md`](../archived/architecture/repo-plans/knowledge.md)。
> 本文件已并入 archived 原文的完整规划细节：ROADMAP（B0/B1）与参考材料规范 reference-material-spec（作为附录补入）。

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

### 5.1 ROADMAP（B0/B1）

**阶段 0：基线设计**

| ID | 任务 | 输出 | 状态 |
|---|---|---|---|
| B0-01 | 冻结一级信息架构 | 18 卷、流程、评审门、模板、案例、评测目录 | ✅ 已完成（草案） |
| B0-02 | 建立统一元数据 | 页面 Front Matter 规范与示例 | ✅ 已完成（草案） |
| B0-03 | 建立对象关系模型 | ID 规则、对象类型、核心关系、JSON Schema | ✅ 已完成（草案） |
| B0-04 | 建立页面与流程模板 | 知识页、流程页、Gate、LLD、VP、Release | ✅ 已完成（草案） |
| B0-05 | 选定首条案例链 | 参数化流水线 MAC 案例章程与结构 | ✅ 已完成（草案） |
| B0-06 | 指定 Owner/Reviewer | RACI 与领域人员名单 | ⬜ 待组织决策 |
| B0-07 | 冻结工具基线 | 仿真、Lint、综合及开源替代路径 | ⬜ 待环境盘点 |
| B0-08 | 技术评审基线 | 评审记录与问题闭环 | ⬜ 待评审 |
| B0-09 | 五层架构迁移 | knowledge/app/template-script-schema/skill/project-data 边界 | ✅ 已完成（结构迁移） |

**阶段 1：MVP**（建议第 2–3 月）：流程主线（模块研发闭环 + 需求/LLD/RTL/DV/静态/PPA Gate）；核心知识（数字基础/需求架构/RTL/功能验证/静态/PPA 的 P0 页，Technical Review 覆盖 100%）；MAC 案例（需求→LLD→RTL→SVA→参考模型→验证→约束→报告→Release，统一命令可复现、证据绑定版本与配置）；检索与评测（结构化索引样本、首批知识问答与代码任务，错误版本与无证据问题可拒答）。

### 5.2 reference-material-spec（摘要）

- **目录结构**：`reference/`（README 总索引 + `knowledge-handbook/` 按领域分类（`01-standards/`、`02-architecture/`…）+ `offline/` 离线资料）；单个资料目录 `REF-{TYPE}-{NNN}/` 含 `README.md`（VitePress 渲染）+ `metadata.yaml` + `images/` + `origin/`（原始格式文件）；
- **metadata.yaml**：基本信息（id/title/type/status）、来源（source）、分类（category）、关联（relations：knowledge_pages/volumes/prerequisites/related_refs）、文件（files：markdown/images/origin + hash）、治理（governance：source_role/version_baseline/maintenance_status/verified_by）、推荐（recommendation：level S/A/B/C、target_audience、applicable_stages、suggested_form）；
- **VitePress 配置**：`apps/handbook/.vitepress/config.mts` 新增参考资料侧边栏（`referenceSidebar`，按 `\d{2}-` 领域分组、REF- 目录排序）与 rewrites（`README.md` → `index.md`），导航栏加「参考资料」入口；
- **Reference Parser Skill**：`skills/reference-parser/`（SKILL.md + `parse_pdf/parse_docx/parse_html/parse_markdown` + templates + examples）；流程：文件分析 → 内容提取 → 图片提取 → metadata/README 生成 → 索引更新；依赖 PyMuPDF / python-docx / BeautifulSoup / PyYAML / Pillow；
- **实施计划**：阶段 1 规范制定 → 阶段 2 VitePress 配置 → 阶段 3 Skill 开发 → 阶段 4 测试验证；待确认问题：图片压缩/OCR/索引自动更新/多版本管理/权限控制。

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/knowledge.md`](../archived/architecture/repo-plans/knowledge.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/knowledge.md` ROADMAP 原文（B0 阶段 0 + 阶段 1 MVP）与 `plans/reference-material-spec.md`（§1 目录结构、§2 元数据规范、§3 VitePress 配置、§4 Reference Parser Skill、§5 实施计划）。
