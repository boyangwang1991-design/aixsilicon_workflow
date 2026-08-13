# docs/architecture/ 文档大纲（v3 最终，供执行）

> 目标：在 `docs/architecture/` 下产出一份**用于方案讨论**的完整说明，核心回答：
> **Workflow 如何统筹 10 个 repo，完成 IP 设计验证与 SoC 集成验证两条主线**；为**每个 repo 构建一份材料**并**阐述 repo 之间的关系**；**把各子仓 plan/todo 剪切到 repo-plans/ 统一处理**；绘制整个 workflow/repo 的关系框图。
> 原则：聚焦整体方案框架，不做 hwif-change 等子流程的 stage 级罗列；支撑流程只讲“在框架中的位置”。

## 文档组织（5 篇 + repo-plans/ 目录）

```
docs/architecture/
├── README.md                 # 索引与阅读地图
├── overview.md               # 总体方案：定位 / 责任链 / 分层 / 对象 / 边界
├── repos.md                  # 每个 repo 一份材料 + 关系阐述
├── workflows.md              # 核心：统筹方案（两条主线 + 支撑流程 + 统筹矩阵 + Gate 卡点）
├── relationship-diagram.md   # 关系框图（5 张 Mermaid）
└── repo-plans/               # 各仓 plan/todo 统一搬移整合（每仓一份）
    ├── README.md             # 统筹总览：原则、导航、状态
    ├── hwif.md
    ├── cbb.md
    ├── ip.md
    ├── dv-common.md
    ├── vip.md
    ├── tools.md
    ├── catalog.md
    ├── soc-integration.md
    ├── skills.md
    └── knowledge.md
```

---

## 1. README.md（索引，薄）

- 用途与对象
- 目录导航表（5 篇 + repo-plans/ 每篇“用于讨论什么”）
- 建议阅读顺序：先图 → 总览 → repo 材料 → 统筹 → 各仓计划 → 回图
- 两条主线速览表（IP 设计验证 / SoC 集成验证：入口 workflow、统筹仓、产出）
- 术语速查（Manifest/Lockfile/Override/Change Bundle/Flow/Evidence/VLNV/Gate）

## 2. overview.md（总体方案）

1. 为什么需要独立的 Workflow 仓 —— 统一回答的 7 类问题
2. 体系定位与核心主张 —— 技术形态一句话 + ADR 支撑（0001/0004）
3. 责任链 —— Skill→Workflow→Tool→Asset→Catalog→EDA（每环“回答什么问题、归属哪里”）
4. 六层架构 L0–L5 —— 每层内容与主要输出
5. 核心对象 —— Manifest / Lockfile / Override / Change Bundle / Flow / Evidence
6. 父仓目录结构 —— 谁放在哪（manifests/workflows/schemas/policies/… + repos 忽略区）
7. Workflow 统筹机制原理 —— init/sync → Flow DAG → 注册 action → Gate → Evidence（一段话讲清）
8. 开源/私有边界 —— 公共底座开源、Skill/项目/Foundry 私有；公共流程不依赖私有 Skill

## 3. repos.md（核心细化：每个 repo 一份材料 + 关系阐述）

### 3.0 关系总览
- 10 仓全景表：逻辑 ID / 仓库 / 类型 / 定位 / 开放度 / 当前内容状态
- 仓库依赖 DAG（`depends_on` 推导，附 Mermaid）
- 四域分组：接口/设计域、验证域、集成/发布域、执行/知识域

### 3.1 每个 repo 的材料（10 节，统一模板）
模板：定位 / 当前内容 / 职责与边界 / 依赖关系 / IP 主线角色 / SoC 主线角色 / Schema 所有权 / 工具归属 / 关系阐述。
按序：hwif、cbb、ip、dv-common、vip、tools、catalog、soc-integration、skills、knowledge。

### 3.2 关系阐述（单独成章）
1. 依赖关系推导表（hwif 为底座；cbb←ip；vip←hwif+dv-common；soc-integration 聚合 hwif/cbb/ip/catalog/tools）
2. 数据流关系（契约流 / 验证流 / 发布流 / 执行流）
3. 写入边界关系（`ownership-map.yaml` 摘要）
4. Schema 所有权关系（单一 Owner）
5. 命名与状态备注（dv-common/soc-integration 无 `_repo` 后缀；待填充状态）

## 4. repo-plans/（各仓 plan/todo 剪切统一处理）

> 定位：**把各子仓 plan/todo/roadmap 物理搬移到本目录统一处理**，每仓一份整合文档；原子仓文件删除并 commit（完整剪切）。

1. **`repo-plans/README.md`** —— 统筹总览
   - 统筹原则：plan/todo 统一收口到父仓 `docs/architecture/repo-plans/`，单一事实源；
   - 导航表（10 份文档 ↔ 原子仓路径）；
   - 迁移状态标注（已剪切 / 无独立 plan 新增占位 / 待补充）。
2. **每仓一份整合文档**（10 份，文件名 `<repo-id>.md`）
   - 汇总该仓原 `plan.md` / `todo.md` / `TODO.md` / `*_plan.md` / `ROADMAP.md` / `plans/*` 的要点，按统一小节组织：
     - 现状与目标、关键里程碑、待办事项、依赖与风险、与本体系其他仓的衔接；
   - catalog、soc-integration 无独立 plan：新建占位文档并标注“待建立”。
3. **子仓原文件剪切清单（执行时删除 + 各仓 commit）**
   - hwif：`plan.md`、`todo.md`
   - cbb：`cbb_repo_plan.md`、`cbb_repo_list.md`
   - ip：`plan.md`
   - dv-common：`plan.md`、`TODO.md`
   - vip：`plan.md`
   - tools：`todo.md`、`tool_repo_plan.md`
   - skills：`todo.md`、`skill_repo_plan.md`
   - knowledge：`TODO.md`、`ROADMAP.md`、`MIGRATION.md`、`PROJECT_ORGANIZATION.md`、`plans/reference-material-spec.md`
   - catalog、soc-integration：无原文件，无需删除

## 5. workflows.md（核心：统筹方案）

1. 统筹模型总述 —— Flow DAG + 注册 action + write_scope + Gate + Evidence 五要素
2. 主线一：IP 设计验证端到端（目标/输入输出、阶段编排、各阶段统筹的仓、Gate 卡点、产物与证据链）
3. 主线二：SoC 集成验证端到端（同上）
4. 支撑流程定位：hwif-change、vip-development、cross-repo-qualification、release-train
5. workflow × repo 统筹矩阵（一张表：流程在哪些仓读/写、产出、卡哪个 Gate）
6. 主线之间的衔接（IP 发布进 Catalog → SoC 选型；跨仓改动走 Change Bundle）
7. 方案讨论要点（命名不统一、工具迁移阶段、私有 overlay 接入点等）

## 6. relationship-diagram.md（关系框图，5 张 Mermaid）

1. 图 1：仓库依赖 DAG（10 仓，depends_on）
2. 图 2：责任链数据流（Skill→Workflow→Tool→Asset→Catalog→EDA）
3. 图 3：主线一 IP 设计验证链路（stage → repo 读写 → gate → evidence → catalog）
4. 图 4：主线二 SoC 集成验证链路（同上）
5. 图 5：L0–L5 分层图（六层 + 资产仓/流程映射）

> Mermaid 约束：节点方括号 `[]` 内不使用双引号与圆括号，避免解析错误。
