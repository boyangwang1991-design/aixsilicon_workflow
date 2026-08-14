# workflow — AIXSILICON Workflow Repository 建设规划

> 客观事实基线：2026-08-13。原文细节见 [`../archived/root/`](../archived/root/README.md)（旧 plan/todo/build_todolist）。

## 1. 定位与边界

**定位**：Manifest 驱动的多仓工作区控制面。
**负责**：Workspace Manifest / Lockfile / Schema / Flow / Policy / 公共 CI / 文档 / `aix` CLI。
**不负责**：不保存资产源码副本；不替代各仓 Issue/PR/Review/Release；不成为最终 SoC Top 事实源；不自动替用户提交/推送/打 Tag/发布；不在 Lockfile/日志中保存凭据。

## 2. 现状（客观）

- **CLI**：`aix` 单入口，`wf / repo / bundle / release / tool` 五域；`make check` 51 测试通过；pre-commit 全绿；
- **治理**：ADR-0001~0006 冻结；VLNV 统一 `aixsilicon:*`；标准 action 集 + 统一退出码；
- **工作区**：6 个 Manifest Profile、10 仓已同步、真实 `locks/baseline.lock.yaml`；
- **FuseSoC**：实跑 483 core、reference 排除、冲突检测；
- **Workflow**：8 条 flow YAML 真实化；`aix wf run` / `aix wf test --affected` / `aix bundle validate|status` 接入；
- **缺口**：runner 委托 `aix tool` 真实 provider 未接入；`aix release prepare/publish` 为桩；reusable workflows 仍为占位；`aix repo pr` 未实现。

## 3. CLI 功能域

| 域 | 命令 |
|---|---|
| `aix wf` | init / sync / status / doctor / lock / diff / graph / fusesoc / clean / foreach / run / test |
| `aix repo` | status / shell / branch / commit / push / diff / pr |
| `aix bundle` | create / validate / status |
| `aix release` | prepare / publish |
| `aix tool` | 由 `aixsilicon_tool_repo` 插件（`aixsilicon.commands`）提供，未安装时 `OPTIONAL_UNAVAILABLE` |

## 4. 阶段路线（客观状态）

| 阶段 | 目标 | 状态 |
|---|---|---|
| 0 契约冻结 | 边界/ADR/VLNV/Schema/所有权 | ✅ 基本达成 |
| 1 Workspace MVP | 一键建环境、子仓独立提交 | ✅ 基本达成 |
| 2 FuseSoC 与基础跨仓验证 | 固定 Lock 重建 APB 验证闭环 | 🔶 进行中 |
| 3 Change Bundle 与影响分析 | HWIF→VIP→IP 联合变更 | ⬜ 未开始 |
| 4 发布协调与 Catalog | IP 资格验证 + 人工批准 + Catalog 更新 | ⬜ 未开始 |
| 5 SoC 集成与规模化 | SoC 锁定基线可重建 | ⬜ 未开始 |

## 5. 工程化（optimization-plan S1–S6 结论）

> 依据 [`../archived/optimization-plan.md`](../archived/optimization-plan.md) 归纳：只保留结构重构结论与遗留缺陷，不迁历史执行流水。

### 5.1 结构重构结论（已完成）

- **S1/S2 CLI 拆包**：`cli.py` 单文件 463 行 → `cli/` 包（`__init__` 入口 + `context` 统一加载 + `args` 参数构建 + `wf/repo/bundle/release` handler + `registry` 命令注册装饰器）；handler 只做解析参数→调领域模块→格式化输出；`aix` 入口与命令签名向后兼容。
- **S3 Schema 单一事实源**：`schemas/`（规范源）+ `src/aixworkflow/schemas/`（包内副本）双份 → `scripts/sync_schemas.py`（`--check` 供 CI）+ `schema.py` 运行时优先读仓库 `schemas/`（开发态）否则包内副本（安装态）；`test_schema_parity` 保留为最后防线。
- **S4 统一任务入口**：新增 `Makefile`（`install/test/lint/format/check/coverage/schema`），可选 `tox.ini` 支持 3.11/3.12 矩阵。
- **S5 命令补齐（主体）**：`aix wf run`（runner + 注册 action + 前置条件 + Run Manifest/Evidence）、`aix wf test --affected`（impact.py）、`aix bundle validate/status`（bundle.py，merge_order/状态机）。
- **P0 五项缺陷修复**：lockfile `tree` 为空（`gitops.rev_parse_any`）、`aix wf lock --no-fetch`、`aix wf status` Baseline 列、`aix wf sync --lock` 按 Lockfile checkout、真实 `locks/baseline.lock.yaml`。

### 5.2 遗留缺陷

- `aix repo pr`（gh CLI 包装，S5 残余）；
- GitHub reusable workflows 真实化（S6，替换 echo 占位，固定 Tag）；
- runner 委托 `aix tool` 真实 provider 接入（依赖 tool_repo 插件）。

## 6. CLI 清单（root/plan §26）

| 域 | 命令 | 优先级 |
|---|---|---:|
| Workspace | `aix wf init/sync/status/doctor/lock/diff` | P0 |
| Workspace | `aix wf graph/clean/foreach` | P1 |
| Repository | `aix repo status/shell/branch/commit/push` | P0 |
| Repository | `aix repo pr` / `aix repo release` | P1 / P2 |
| Flow & Bundle | `aix wf run <flow>` / `aix wf test --affected` | P0 / P1 |
| Flow & Bundle | `aix bundle create/validate/status` | P1 |
| Release | `aix release prepare/publish` | P2 |

## 7. 测试策略（root/plan §27）

- **CLI 单元测试**：Manifest include/merge/override；URL 和路径安全；revision 解析；dirty/ahead/behind/diverged 检测；Lock 稳定序列化；DAG 与环检测；Git 参数转义；exit code 映射；Evidence Schema。
- **集成测试**（本地临时 Git 仓 Fixture）：初次 clone、已存在 sync、remote 错误、dirty 保护、detached HEAD、commit 不可达、并行 fetch、单仓 commit 不污染父仓、override/release 冲突、中断恢复、Lock 重建一致性。
- **端到端测试**（一期三场景）：APB 寄存器 IP、X2X/AXI Bridge、PIC。

## 8. 验收与最终推荐

**一期验收**（root/plan §31）：一条命令按 Profile 建环境；子仓位于 `repos/` 且父仓可靠忽略；子仓独立 commit/push 父仓无变化；dirty/错误 remote/不可达 SHA/override 可识别；生成完整 FuseSoC 配置；Lockfile 可重建；APB 跨仓闭环；Change Bundle 三仓联合变更；联合 CI 拉 PR HEAD；发布前人工确认；失败 Run 可定位；文档可用。

**最终推荐**（五个稳定契约）：Workspace Contract（哪些仓库/放哪/如何同步）、Dependency Contract（仓库/VLNV/接口/工具如何依赖）、Execution Contract（每条 Flow 的输入/Stage/Gate/输出）、Collaboration Contract（跨仓变更如何关联/验证/合并/发布）、Evidence Contract（任何结论如何被版本/工具/日志/报告重建）。

## 9. 关联

- 全局规划：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- Todo：[`todo.md`](todo.md)
- 工程化来源：[`../archived/optimization-plan.md`](../archived/optimization-plan.md)
- 归档原文：[`../archived/root/`](../archived/root/README.md)
