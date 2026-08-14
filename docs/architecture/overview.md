# 总体方案：AIXSILICON Workflow / Repo 体系（overview）

> 本页回答：**这套体系整体怎么运转、边界在哪、Workflow 用什么机制统筹多个仓库。**

## 1. 为什么需要独立的 Workflow 仓

各资产仓只回答“资产本身是什么”（IP 的 RTL、HWIF 的契约、VIP 的协议组件……）。但整条研发链仍缺一个**统一答案**：

| 问题 | 由谁统一回答 |
|---|---|
| 新成员如何一次得到完整、正确的开发环境？ | Manifest / Lockfile |
| 哪些版本的 HWIF、DV Common、VIP、IP 可以一起用？ | 依赖图 + Catalog 兼容矩阵 |
| 本地未合入的 HWIF 如何临时给 VIP/IP 用？ | Local Override |
| 一次跨仓功能改动由哪些分支/PR 组成、按什么顺序合？ | Change Bundle |
| 某个 IP 发布前要跑哪些跨仓验证、凭什么判定通过？ | Flow + Gate + Evidence |
| SoC 项目如何重建某个历史集成基线？ | 锁定 SHA 的 Lockfile + Release |
| Skill / 工具从哪里读输入、写到哪、用哪个版本？ | 统一执行环境（`aix` CLI + action） |

**`aixsilicon_workflow` 就是这些问题的统一答案**：它是一个“多仓工作区控制面”，不是源码汇总仓，也不替代任何资产仓的 Issue/PR/Review/Release。

## 2. 体系定位与核心主张

> **Manifest 驱动的多仓工作区 + 独立 Git Clone + 统一 Python CLI（`aix`）+ FuseSoC 聚合配置 + Change Bundle + GitHub Actions 协调层**

- **Manifest + 独立 Clone**（[ADR-0001](../adr/0001-manifest-over-submodule.md)）：子仓统一克隆到 `repos/`，父仓 `.gitignore` 完整忽略；每个子仓保持独立 Git 历史、分支、PR、Tag、Release。
- **父仓只版本化**：Manifest、Lockfile、Schema、流程定义、公共 CI、脚本、文档。
- **CLI 单入口 `aix`**（[ADR-0004](../adr/0004-cli-entry-and-plugin-registry.md)）：`aix wf / aix repo / aix bundle / aix release / aix tool`；`aix tool` 由 `aixsilicon_tool_repo` 插件（`aixsilicon.commands`）提供，未安装时显式 `OPTIONAL_UNAVAILABLE`。

## 3. 责任链（谁决定什么）

> **Skill 决定“如何理解与辅助”→ Workflow 决定“顺序与 Gate”→ Tool 负责“确定性执行”→ 资产仓保存 SSOT/交付 → Catalog 发布合格资产 → EDA 提供工程证据。**

```text
Skill(理解/辅助) ──指导──▶ Workflow(顺序/Gate) ──编排──▶ Tool(确定性执行)
                                                              │
     Catalog(发布/发现) ◀── Release ── 资产仓(SSOT/交付) ◀────┘
                                                              │
                                                     EDA(工程证据: sim/syn/ppa)
```

| 角色 | 回答的问题 | 归属 |
|---|---|---|
| **Skill** | 如何理解需求、生成/解释设计、选择流程 | `aixsilicon_skill_repo`（私有） |
| **Workflow** | 先跑什么、后跑什么、什么算通过 | `aixsilicon_workflow`（本仓 `workflows/`） |
| **Tool** | 如何确定性生成/检查（CSR、HWIF、Core、Top…） | `aixsilicon_tool_repo`（T1） |
| **Asset Repo** | 事实、源码、正式交付物（SSOT） | hwif / cbb / ip / dv-common / vip / soc-integration |
| **Catalog** | 已发布哪些资产、版本、VLNV、兼容性、成熟度 | `aixsilicon_catalog_repo` |
| **EDA** | 仿真/综合/PPA 等工程证据 | EDA Provider（公开流程不硬编码私有路径） |

> 核心纪律：**派生视图一律由 Tool 确定性生成，不手工维护**（ADR-0002 / ADR-0006）；质量门禁基于**证据 + 哈希**，不只检查目录存在。

## 4. 六层架构（L0–L5）

| 层 | 内容 | 主要输出 |
|---|---|---|
| **L0 工作区层** | 目录、clone、sync、状态、缓存 | 本地一致工作区（`repos/`） |
| **L1 配置层** | Manifest、Profile、Lock、Override | 可解析依赖基线 |
| **L2 资产发现层** | FuseSoC roots、VLNV、Catalog | 可构建资产图 |
| **L3 流程编排层** | develop / verify / integrate / release | 标准化任务 DAG |
| **L4 质量与证据层** | Gate、RTM、报告、Hash、SBOM | 结构化判定证据 |
| **L5 协作与发布层** | PR、Change Bundle、Release Train | 可审计多仓协作 |

## 5. 核心对象

| 对象 | 回答的问题 | 载体 |
|---|---|---|
| **Workspace Manifest** | 需要克隆哪些仓、放哪、用哪个分支 | [`manifests/default.yaml`](../../manifests/default.yaml) |
| **Workspace Lockfile** | 本次实际解析到的 SHA / VLNV / 工具版本 | [`locks/`](../../locks) |
| **Local Override** | 本地临时替换 | [`overrides/`](../../overrides) |
| **Change Bundle** | 跨仓变更的分支/PR 与合并顺序 | [`changesets/`](../../changesets) |
| **Flow** | 输入→Stage→Gate→输出的 DAG | [`workflows/`](../../workflows) |
| **Evidence** | 结论如何被版本/工具/日志/报告重建 | Run Manifest + Evidence Index |

## 6. 父仓目录结构（谁放在哪）

```text
aixsilicon_workflow/
├── manifests/            # 各 Profile 工作区清单
├── locks/                # baseline 与 release 锁文件
├── overrides/            # 本地覆盖（local.yaml 被忽略）
├── schemas/              # Manifest/Lock/Bundle/Flow/Profile/Evidence JSON Schema
├── workflows/            # 跨仓 Flow 定义（统筹编排）
├── changesets/           # Change Bundle 目录
├── policies/             # 依赖/兼容/分支/发布/证据/安全策略
├── toolchains/           # 工具链 Profile 与容器定义
├── templates/            # 元数据、Bundle、Release、PR 模板
├── src/aixworkflow/      # aix Python CLI
├── tests/                # 单元 / 集成 / fixtures / golden
├── docs/                 # 文档与 ADR
├── .github/              # Reusable workflows 与 actions
│
├── repos/                # 运行时克隆的独立 Git 仓（完整忽略）
├── build/ / reports/ / cache/ / .aix/   # 构建输出与本地状态（完整忽略）
```

## 7. Workflow 统筹仓库的机制（一句话原理）

1. **`aix wf init/sync`** 按 Manifest 把所需仓库放到 `repos/`，并锁定到 Lockfile SHA；
2. **Flow（YAML DAG）** 声明 Stage 顺序、每个 Stage 用哪个注册 action、写哪个仓的哪些路径（`write_scope`）；
3. **注册 action**（[`src/aixworkflow/actions.py`](../../src/aixworkflow/actions.py)）是确定性执行单元：调用 `aix tool` 插件，或迁移窗口内回退到仓内脚本，**绝不执行 Flow YAML 里的任意 Shell**；
4. **Gate** 卡在关键节点，由证据（Run Manifest/Log/Report/Hash）驱动；
5. 端到端证据汇入 **Evidence Index**，合格资产经 Release 进 **Catalog**。

> 详细编排见 [`workflows.md`](workflows.md)，被统筹的仓库见 [`repos.md`](repos.md)，可视化见 [`relationship-diagram.md`](relationship-diagram.md)。

## 8. 开源 / 私有边界

| 内容 | 默认属性 | 原因 |
|---|---|---|
| HWIF / CBB / 公共 IP / VIP / DV Common | 开源 | 形成可复用硬件与验证生态 |
| Workflow / Tool / Catalog / 通用 SoC 集成框架 | 开源 | 工程链条可复现、可贡献 |
| `aixsilicon_skill_repo` | **私有** | 核心 Prompt、方法论、Agent 编排 |
| 具体商业芯片 SoC 项目仓 | **私有** | 产品配置、未公开 IP、项目进度 |
| Foundry / PDK / Memory Macro 适配、商业 EDA License/路径 | **私有 Overlay** | NDA 与许可证约束 |

> 原则：公共 Workflow **必须能在没有私有 Skill 的情况下**运行确定性基础流程；私有 Skill 是能力增强层，不能成为开源仓构建/测试/发布验证的隐藏必需依赖。

## 9. 本页相关

- 被统筹的仓库清单与依赖：**[repos.md](repos.md)**
- 两条主线编排（IP 设计验证 / SoC 集成验证）：**[workflows.md](workflows.md)**
- 关系框图：**[relationship-diagram.md](relationship-diagram.md)**
- 完整规划：**[workflow-repo-plan.md](../workflow-repo-plan.md)**；ADR 索引：**[docs/adr/](../adr/README.md)**
