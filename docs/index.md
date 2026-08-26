# AIXSILICON 文档中心

本页是 Workflow 控制面的文档入口。Workflow 只负责三件事：**维护 GitHub 仓库、提供工作空间、提供工作原则与指导**。各资产仓的 `README.md`/`delivery.md`/`design-reference.md` 由各自 repo 自行维护（`repos/aixsilicon_<repo>/`）。

## 1. 从这里开始

| 需求 | 阅读入口 |
|---|---|
| 初次了解 | [`README.md`](../README.md) |
| 安装与初始化工作区 | [`getting-started.md`](getting-started.md) |
| 查看仓库清单与 Profile | [`manifests/default.yaml`](../manifests/default.yaml) |
| 查看写入边界 / 归属 | [`../ownership-map.yaml`](../ownership-map.yaml)、[`workflow/ownership.md`](workflow/ownership.md) |
| 查看工作原则 / 政策 | [`policies/`](../policies) |
| 查看 Flow 定义 | [`workflows/`](../workflows) |
| 查看 Schema | [`schemas/`](../schemas) |

## 2. 文档分层

| 材料 | 唯一职责 |
|---|---|
| [`index.md`](index.md) | 导航和阅读路径 |
| [`getting-started.md`](getting-started.md) | 安装、初始化和基本操作 |
| [`governance.md`](governance.md) | 文档分层、状态规则和维护门禁 |
| [`workflow/ownership.md`](workflow/ownership.md) | Schema、仓库和工具归属 |

各资产仓文档（`README.md`/`delivery.md`/`design-reference.md`）由各自 repo 维护，不在本仓重复存放。

## 3. 工作原则与政策

Workflow 通过 [`policies/`](../policies) 提供工作原则（分支、依赖、安全、发布、兼容性、证据），通过 [`ownership-map.yaml`](../ownership-map.yaml) 约束写入边界。各 Skill（ip-development-suite / cbb-development-suite / soc-integration-suite / hwif-development-suite）负责对应领域的研发方法与流程，Workflow 只提供仓库管理与临时场地。

## 4. 机制与配置

| 材料 | 作用 |
|---|---|
| [`manifests/default.yaml`](../manifests/default.yaml) | 期望工作区：哪些仓、放在哪里、开发分支 |
| [`workflows/*.yaml`](../workflows) | Flow 定义（仓库管理/临时场地编排） |
| [`schemas/`](../schemas) | Manifest/Lock/Flow 等配置的 JSON Schema |
| [`bootstrap.py`](../bootstrap.py) / `aix` CLI | 工作区引导与仓库管理入口 |

## 5. 图示约定

- 项目图片统一保存在 [`assets/`](assets/README.md)；
- 生成式图片用于建立整体心智模型，不替代正文、表格或机器可读配置；
- 精确依赖看 Manifest，精确 Flow 看 `workflows/*.yaml`。
