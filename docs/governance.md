# 文档与工作区治理

本文定义 Workflow 控制面的文档分层、单一事实源与工作原则。目标是让 Workflow 保持轻量：只维护 GitHub 仓库、提供工作空间、提供工作原则与指导；领域研发方法与流程由各 Skill 负责。

## 1. 文档分层

| 层级 | 权威材料 | 用途 |
|---|---|---|
| 导航 | [`index.md`](index.md) | 唯一入口与阅读路径 |
| 工作区初始化 | [`getting-started.md`](getting-started.md) | 安装、初始化和基本操作 |
| 归属/写入边界 | [`../ownership-map.yaml`](../ownership-map.yaml)、[`workflow/ownership.md`](workflow/ownership.md) | Schema/仓库/工具归属 |
| 跨仓协作说明 | [`workflow/architecture.md`](workflow/architecture.md)、[套件地图](workflow/repositories-and-skills.md)、[交付流程](workflow/lifecycle.md) | 解释边界与交接，不复制领域完整规范 |
| 操作与能力边界 | [操作手册](workflow/operations.md)、[当前限制](workflow/current-state.md) | 区分可执行命令、证据与待实现能力 |
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
- **提供工作空间**：通过 `manifests/`（Profile）定义开发场景；`bootstrap.py` 下载 skill repo 并物化 skills 到 `/<agent-dir>/skills/`（默认 `/.roo/skills/`）；`uv` 管理唯一 Python 环境。
- **提供原则与指导**：`AGENT.md`（Agent 工作方法）、`README.md`、`docs/`、`policies/`、`ownership-map.yaml` 固化工作原则与写入边界。
- **领域流程由 Skill 负责**：IP/CBB/SoC/HWIF 的设计、验证、门禁由对应 Skill 约束；Workflow 只提供仓库管理与临时场地。

## 4. 变更纪律

### 本地材料归置

- 一次性脚本、试验材料与历史测试残留统一放 `tmp/<任务名>/`（Git 忽略）；归档时记录原路径，便于恢复。
- 可重建缓存统一放 `cache/<工具名>/`；`make` 入口集中配置 pytest、Python 字节码、uv、pre-commit 与 coverage 的缓存位置。直接运行 Python 时可设置 `PYTHONPYCACHEPREFIX` 为工作区 `cache/pycache` 的绝对路径。
- `reports/` 保留有价值的审查报告和工程证据；单元测试必须在 pytest 临时工作目录生成报告，不能写入真实工作区。
- `.venv/`、`repos/`、`.aix/`、Agent Skill 运行目录与安装元数据按各自工具约定保留，不作为临时垃圾搬迁或删除。

### 修改与校验

- 修改 `manifests/`、`workflows/`、`schemas/`、`policies/`、`ownership-map.yaml` 时，先运行 `make check` 与 `uv run pre-commit run --all-files` 确保全绿；
- 各仓文档变更应在对应 repo 内维护，不在本仓重复存放；
- 新仓 / 新事实域需先在 `ownership-map.yaml` 与 `manifests/default.yaml` 登记，再进入开发。
- 改 Profile、provider、套件入口或发布语义时，同步更新相关导航与操作示例；架构图中的箭头必须说明是产品依赖、验证依赖还是信息流。
- `current-state.md` 记录带日期的差异，不替代各仓任务表；修复后更新记录并关联验证，不长期复制资产数量与状态。
