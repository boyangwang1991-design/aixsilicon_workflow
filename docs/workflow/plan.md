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

## 5. 工程化（客观）

- 已完成：CLI 拆包（`cli/`）、Schema 单一事实源（`scripts/sync_schemas.py`）、Makefile、统一退出码；
- 遗留：`aix repo pr`（S5）、GitHub reusable workflows 真实化（S6）、runner 真实 provider。

## 6. 关联

- 全局规划：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- Todo：[`todo.md`](todo.md)
- 归档原文：[`../archived/root/`](../archived/root/README.md)
