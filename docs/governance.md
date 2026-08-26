# 文档与工作区治理

本文定义 Workflow 控制面的文档分层、单一事实源与工作原则。目标是让 Workflow 保持轻量：只维护 GitHub 仓库、提供工作空间、提供工作原则与指导；领域研发方法与流程由各 Skill 负责。

## 1. 文档分层

| 层级 | 权威材料 | 用途 |
|---|---|---|
| 导航 | [`index.md`](index.md) | 唯一入口与阅读路径 |
| 工作区初始化 | [`getting-started.md`](getting-started.md) | 安装、初始化和基本操作 |
| 归属/写入边界 | [`../ownership-map.yaml`](../ownership-map.yaml)、[`workflow/ownership.md`](workflow/ownership.md) | Schema/仓库/工具归属 |
| 工作原则/政策 | [`policies/`](../policies) | 分支、依赖、安全、发布、兼容性、证据原则 |
| 各仓文档 | `repos/aixsilicon_<repo>/` | 单仓定位、边界、契约、任务与历史（各仓自行维护） |

## 2. 单一事实源

- 仓库清单与依赖：`manifests/default.yaml`，文档只解释，不复制为可编辑事实；
- 写入边界与 Schema Owner：`ownership-map.yaml`；
- Flow 定义：`workflows/*.yaml`；
- 配置 Schema：`schemas/`；
- 工作原则：`policies/`；
- 各仓任务定义与状态：由各 repo 自身维护。

## 3. 工作原则

- **维护仓库**：通过 `aix` CLI（`aix wf sync` / `aix repo status|commit|push`）管理 `repos/` 下的各子仓；`repos/` 被 `.gitignore` 完整忽略，子仓保持独立 Git 历史。
- **提供工作空间**：通过 `manifests/`（Profile）定义开发场景；`bootstrap.py` 下载 skill repo 并物化 skills 到 `/.roo/skills/`；`uv` 管理唯一 Python 环境。
- **提供原则与指导**：`AGENT.md`（Agent 工作方法）、`README.md`、`docs/`、`policies/`、`ownership-map.yaml` 固化工作原则与写入边界。
- **领域流程由 Skill 负责**：IP/CBB/SoC/HWIF 的设计、验证、门禁由对应 Skill 约束；Workflow 只提供仓库管理与临时场地。

## 4. 变更纪律

- 修改 `manifests/`、`workflows/`、`schemas/`、`policies/`、`ownership-map.yaml` 时，先运行 `make check` 与 `uv run pre-commit run --all-files` 确保全绿；
- 各仓文档变更应在对应 repo 内维护，不在本仓重复存放；
- 新仓 / 新事实域需先在 `ownership-map.yaml` 与 `manifests/default.yaml` 登记，再进入开发。
