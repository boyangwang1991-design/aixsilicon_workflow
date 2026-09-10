# AIXSILICON Workflow

`aixsilicon_workflow` 是 AIXSILICON 硬件工程资产体系的 **多仓工作区控制面**。它的职责刻意保持轻量，只做三件事：

1. **维护 GitHub 仓库**：按清单下载各资产仓、保持独立 Git 历史、提供 `aix repo` / `aix wf sync` 等仓库管理入口；
2. **提供工作空间**：通过 Manifest/Profile 定义开发场景，`bootstrap.py` 物化 skills，`uv` 管理统一 Python 环境；
3. **提供工作原则与指导**：`AGENT.md`（Agent 工作方法）、`README.md`、`docs/`、`policies/`、`ownership-map.yaml` 固化工作原则与写入边界。

**领域研发方法由各 Skill 负责**：IP / CBB / SoC / HWIF 的设计、验证、门禁由对应 Skill（ip-development-suite / cbb-development-suite / soc-integration-suite / hwif-development-suite）约束；Workflow 只提供仓库管理与临时场地，不在本仓维护领域流程细节。

> 统一材料入口见 [`docs/index.md`](docs/index.md)，安装与初始化见 [`docs/getting-started.md`](docs/getting-started.md)。
>
> **Skill 集中管理**：`aix` CLI 的源码/测试/脚本由私有 skill `aixsilicon-workspace-management` 统一管理；[`bootstrap.py`](bootstrap.py) 把 skills 物化到 `/<agent-dir>/skills/`（默认 `/.roo/skills/`，git 忽略）后运行。首次使用：`uv sync --locked` + `uv run python bootstrap.py --ensure`。

![AIXSILICON 项目全景：Workflow 控制面协调十个独立资产仓，并通过设计、生成、验证、证据、审批、发布和消费形成闭环](docs/assets/project-panorama.png)

全景图将项目分为控制面、十个平级资产仓和工程交付闭环：Workflow 通过 Manifest/Lock 与 Flow 组织仓库协作；各资产仓保存 SSOT 与交付物；Skill 负责领域方法。图中的连线用于解释职责和生命周期，不代替 [`manifests/default.yaml`](manifests/default.yaml)、[`ownership-map.yaml`](ownership-map.yaml) 或 [`workflows/`](workflows/) 中的精确依赖、所有权与执行定义。

## 技术形态

> **Manifest 驱动的多仓工作区 + 独立 Git Clone + 统一 Python CLI + FuseSoC 聚合配置 + GitHub Actions 协调层**

默认不采用 Git Submodule。子仓统一克隆到 `repos/`，而 `repos/` 被父仓 `.gitignore` 完整忽略；父仓只版本化 Manifest、Schema、流程定义、公共 CI、脚本、政策与文档。

## 仓库生态

| 逻辑 ID | 仓库 | 定位 | 开放性 |
|---|---|---|---|
| hwif | [`aixsilicon_hwif_repo`](https://github.com/boyangwang1991-design/aixsilicon_hwif_repo) | 接口语义契约与 HDL 多视图 | 开源 |
| cbb | [`aixsilicon_cbb_repo`](https://github.com/boyangwang1991-design/aixsilicon_cbb_repo) | 可参数化公共逻辑构件与 PPA 实现 | 开源 |
| ip | [`aixsilicon_ip_repo`](https://github.com/boyangwang1991-design/aixsilicon_ip_repo) | 可独立集成和发布的完整 IP | 开源 |
| dv-common | [`aixsilicon_dv_common`](https://github.com/boyangwang1991-design/aixsilicon_dv_common) | 协议无关验证公共底座 | 开源 |
| vip | [`aixsilicon_vip_repo`](https://github.com/boyangwang1991-design/aixsilicon_vip_repo) | 协议与系统验证组件 | 开源 |
| tools | [`aixsilicon_tool_repo`](https://github.com/boyangwang1991-design/aixsilicon_tool_repo) | 确定性生成、检查、转换、打包工具（私有；交付件随公开资产仓开源） | **私有** |
| catalog | [`aixsilicon_catalog_repo`](https://github.com/boyangwang1991-design/aixsilicon_catalog_repo) | 已发布资产索引、兼容矩阵和成熟度 | 开源 |
| soc-integration | [`aixsilicon_soc_integration`](https://github.com/boyangwang1991-design/aixsilicon_soc_integration) | 通用 SoC 集成 Schema、模板、规则 | 开源 |
| skills | [`aixsilicon_skill_repo`](https://github.com/boyangwang1991-design/aixsilicon_skill_repo) | AI 辅助研发 Skill Suite（私有） | **私有** |
| knowledge | [`aixsilicon_chipknowledge`](https://github.com/boyangwang1991-design/aixsilicon_chipknowledge) | 芯片研发知识库（方法论/术语/参考索引） | 开源 |

> 仓库布局与分支策略见 [`manifests/default.yaml`](manifests/default.yaml)；工作区环境引导（uv/git/仓库清单/skills 物化）由私有 skill `aixsilicon-workspace-management` 统一管理。

## 治理与命名规范

- **VLNV 统一 `aixsilicon:*`**：由 canonical guard [`check_vlnv_namespace.py`](repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/scripts/hooks/check_vlnv_namespace.py) 强制，policy [`dependency-policy.yaml`](policies/dependency-policy.yaml) 固化；CLI 二进制名保持 `aix`；
- **单一 CLI 入口 + 插件组 `aixsilicon.commands`**：由 canonical [`cli/registry.py`](repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/src/aixworkflow/cli/registry.py) 插件发现实现，`aix tool` 由 `aixsilicon_tool_repo` 插件提供，未安装时显式 `OPTIONAL_UNAVAILABLE`；
- **跨仓边界映射**：policy [`dependency-policy.yaml`](policies/dependency-policy.yaml) `dep-no-phantom-repo` 固化；**工具归属四类**见 [`docs/workflow/ownership.md`](docs/workflow/ownership.md)；
- **Schema、仓库与工具归属**：[`docs/workflow/ownership.md`](docs/workflow/ownership.md)。

## 快速开始

详见 [`docs/getting-started.md`](docs/getting-started.md)，核心命令：

```bash
uv sync --locked                           # 安装依赖（唯一环境根 .venv）
uv run python bootstrap.py --ensure        # 物化 skills
uv run aix wf init --profile ip-dev        # 初始化工作区
uv run aix wf sync                         # clone / fetch / checkout 全部所需仓库
uv run aix wf status                       # 查看各仓状态
uv run aix wf preflight ip-development     # Flow 执行前检查 required provider

# 单仓 Git 操作（子仓 repos/<id> 与父仓 workflow）
uv run aix repo commit vip -m "feat: ..."  # 提交前先 git add
uv run aix repo push vip
```

## 目录结构

```text
aixsilicon_workflow/
├── manifests/            # 各 Profile 工作区清单（维护仓库/工作空间核心）
├── workflows/            # Flow 定义（仓库管理/临时场地编排，薄流程）
├── schemas/              # Manifest/Lock/Flow/Profile/Evidence JSON Schema
├── policies/             # 依赖/兼容/分支/发布/证据/安全原则
├── overrides/            # 本地覆盖（local.yaml 被忽略）
├── docs/                 # Workflow 自身文档（index/getting-started/governance/ownership）
├── .github/              # Reusable workflows 与 actions
│
├── repos/                # 运行时克隆的独立 Git 仓（完整忽略）
├── build/                # 统一构建输出（完整忽略）
├── reports/              # 本地报告（完整忽略）
├── cache/                # 下载与 EDA 缓存（完整忽略）
└── .aix/                 # 本地状态与生成配置（完整忽略）
```

## 核心概念

| 对象 | 回答的问题 |
|---|---|
| [Workspace Manifest](manifests/default.yaml) | 当前工作区需要克隆哪些 Git 仓库，放在哪里，使用何种开发分支或版本策略 |
| Profile | 哪个开发场景启用哪些仓（`ip-dev` / `cbb-dev` / `soc-integration` / `minimal` / `all`） |
| Local Override | 开发者本地临时替换（`overrides/local.yaml`，被忽略） |
| Flow | 每条流程的输入、Stage、write_scope 和输出（仓库管理/临时场地编排） |
| Skill | 领域研发方法与流程（ip/cbb/soc/hwif suite，私有；required stage 缺 provider 时 Flow 阻断） |

## 文档

- [统一文档中心](docs/index.md)
- [跨仓架构与六类资产协作](docs/workflow/architecture.md)
- [仓库与 Skill 使用地图](docs/workflow/repositories-and-skills.md)
- [跨仓交付流程](docs/workflow/lifecycle.md)
- [工作区操作手册](docs/workflow/operations.md)
- [当前能力边界与已知差异](docs/workflow/current-state.md)
- [Getting Started](docs/getting-started.md)
- [文档与工作区治理](docs/governance.md)
- [归属与写入边界](docs/workflow/ownership.md)

## 许可证

Apache-2.0，详见 [`LICENSE`](LICENSE)。
