# AIXSILICON Workflow / Repo 体系架构说明

> 用途：**整体方案框架讨论与评审底稿**。本目录从「Workflow 如何统筹 10 个子仓，完成 IP 设计验证、SoC 集成与验证」的视角，完整说明体系定位、仓库职责、流程编排与门禁关系，并以关系框图辅助理解；同时把各子仓的 plan/todo **统一收口**到 `repo-plans/` 集中管理。
> 数据来源：本仓 `manifests/`、`workflows/`、`policies/`、`ownership-map.yaml`、`docs/`、`src/aixworkflow/` 及各子仓内容（截至 2026-08-13）。
> 对象：芯片研发工程师、验证工程师、架构师、AI/EDA 工具链负责人、方案评审人。

## 1. 目录导航

| 文档 | 内容 | 用于讨论什么 |
|---|---|---|
| [`overview.md`](overview.md) | 体系定位、责任链、六层架构（L0–L5）、核心对象、父仓目录结构、开源/私有边界 | “这套体系整体怎么运转、边界在哪” |
| [`repos.md`](repos.md) | 10 个子仓作为**被统筹对象**：每个 repo 一份材料（定位/内容/边界/依赖/两主线角色/归属）+ 关系阐述 | “每个仓该放什么、谁拥有什么、依赖是否合理” |
| [`workflows.md`](workflows.md) | **整体方案框架**：Workflow 如何统筹各 repo 完成「IP 设计验证」与「SoC 集成验证」两条主线；支撑流程定位；workflow×repo 统筹矩阵、Gate 卡点 | “流程怎么统筹资产仓、门禁怎么卡点、端到端怎么串起来” |
| [`repo-plans/`](repo-plans/README.md) | **各子仓 plan/todo 统一收口**：每仓一份整合文档（含 catalog / soc-integration 占位） | “各仓接下来做什么、里程碑与待办如何统筹” |
| [`relationship-diagram.md`](relationship-diagram.md) | 5 张 Mermaid 关系框图：仓库依赖 DAG、责任链数据流、IP 主线链路、SoC 主线链路、L0–L5 分层 | “一眼看懂整体拓扑与数据流向” |
| [`plan.md`](plan.md) | 本目录规划底稿（原 `plans/architecture-docs-outline.md`，已从根目录收口至此） | “本目录当初如何规划、后续如何维护” |

## 2. 建议阅读顺序

1. **先看关系图**：[`relationship-diagram.md`](relationship-diagram.md) —— 建立整体印象（仓库拓扑 + 两条主线链路）；
2. **再看总览**：[`overview.md`](overview.md) —— 明确定位、责任链、边界；
3. **看被统筹对象**：[`repos.md`](repos.md) —— 确认每个仓的职责与依赖；
4. **看统筹方式**：[`workflows.md`](workflows.md) —— 确认 Workflow 如何编排 IP 设计与 SoC 集成验证两条主线；
5. **看各仓计划**：[`repo-plans/`](repo-plans/README.md) —— 确认各仓下一步建设与统筹；
6. **回到关系图**：对照图中每个节点在 `repos.md` / `workflows.md` 找到详细说明。

## 3. 一句话速览

> **Manifest 驱动的多仓工作区 + 独立 Git Clone + 统一 Python CLI（`aix`）+ FuseSoC 聚合配置 + Change Bundle + GitHub Actions 协调层**；
> 责任链：**Skill 决定“如何理解与辅助”→ Workflow 决定“顺序与 Gate”→ Tool 负责“确定性执行”→ 资产仓保存 SSOT/交付 → Catalog 发布合格资产 → EDA 提供工程证据**。

## 4. 两条主线速览

| 主线 | 入口 Workflow | 统筹的仓库 | 最终产出 |
|---|---|---|---|
| **IP 设计验证** | `ip-development` → `ip-verification` → `release-train` | hwif / cbb / ip / dv-common / vip / tools / catalog | 可发布的 IP（RTL/CSR/验证/文档 + Catalog 条目 + Evidence） |
| **SoC 集成验证** | `soc-integration`（消费已发布资产） | catalog / soc-integration / tools / hwif / cbb / ip / dv-common / vip | SoC Top、软件派生、集成验证结果与基线 |

> 支撑性流程（hwif-change、vip-development、cross-repo-qualification）维护主线上游的“能力/契约”与“跨仓联合验证”，详见 [`workflows.md`](workflows.md)。

## 5. 术语速查

| 术语 | 含义 | 出处 |
|---|---|---|
| Manifest | 描述“期望工作区”：哪些仓库、放哪、用哪个分支 | [`docs/manifest.md`](../manifest.md) |
| Lockfile | 描述“本次实际解析到的 SHA/VLNV/工具版本” | [`locks/`](../../locks) |
| Override | 本地临时替换（本地生效，不入库） | [`overrides/`](../../overrides) |
| Change Bundle | 一次跨仓变更的 PR/分支集合与合并顺序 | [`changesets/`](../../changesets) |
| Flow | 输入→Stage→Gate→输出的 DAG 流程定义 | [`workflows/`](../../workflows) |
| Evidence | 让结论可重建的结构化证据（Run Manifest / Log / Report / Hash） | [`schemas/evidence-index.schema.json`](../../schemas/evidence-index.schema.json) |
| VLNV | 统一资产命名 `aixsilicon:<type>:<name>:<version>` | [`docs/adr/0003-unified-vlnv-namespace.md`](../adr/0003-unified-vlnv-namespace.md) |
| Gate | 质量门禁 G0–G7，由证据驱动而非目录存在 | [`README.md`](../../README.md) §质量 Gate |
