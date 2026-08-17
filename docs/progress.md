# AIXSILICON 开发进度台账

更新时间：2026-08-17。本文只汇总跨仓里程碑状态、组合风险和决策队列；任务状态、负责人、日期和 Evidence 以 [`todo.md`](todo.md) 为准，任务定义与验收条件以各仓 `delivery.md` 为准。

## 1. 组合里程碑状态

完成度采用 [`roadmap.md`](roadmap.md) 的 C0 Designed、C1 Runnable、C2 Integrated、C3 Qualified、C4 Released、C5 Proven。`当前等级` 只写已有证据，不按文件数量推断。

| 里程碑 | 窗口 | 状态 | 当前等级 | 目标等级/出口 | Accountable 角色 | 下一证据动作 |
|---|---|---|---|---|---|---|
| M0 方案/决策冻结 | W0～W2 | `in-progress` | C0（ADR+Findings 部分） | C0：ADR、Findings、Owner/验收获批 | boyang wang | ADR-0007/0008 已接受、Findings 审核已完成（2026-08-17）；剩余：APB profile 获批 |
| M1 控制面安全底座 | W2～W6 | `in-progress` | C1（核心机制） | C2：exact Profile、typed deps、preflight、fail-closed、Lock/Evidence | boyang wang | WF-002/004/005/006/007/011/012 及 TOOL-001/003/004 已实现（2026-08-17，95 项测试全绿，pre-commit 11/11）；下一步：M2 APB 穿刺 |
| M2 APB 最短穿刺 | W5～W10 | `planned` | C0 draft | C1：真实 Contract→生成→compile/smoke | boyang wang | 冻结 APB profile、SystemRDL 和最小验收矩阵 |
| M3 APB 完整资格 | W9～W15 | `planned` | not started | C3：负向/边界/影响与固定 Lock G0～G6 | boyang wang | 审核故障注入、coverage 和 Evidence 矩阵 |
| M4 协作与发布 | W13～W19 | `planned` | contract draft | C4：PR HEAD 联验、G7、Release、Catalog PR | boyang wang | 冻结 Bundle/Release/Catalog 状态机与幂等键 |
| M5 CBB 产品化 | W20～W27 | `planned` | C0 draft | C4：三示范参数/PPA 闭环，至少一项发布 | boyang wang | 冻结 arbiter/pipeline/FIFO 切片和 PPA 可比字段 |
| M6 最小 SoC | W24～W33 | `planned` | C0 draft | C3：Golden 生成/负向/compile/sim/boot/baseline | boyang wang | 审核最小 Schema、Golden 和 provider contract |
| M7 规模化运营 | W33+ | `deferred` | not started | C5：第二消费者、兼容矩阵、候选仓决策 | boyang wang | M6 出口后复审激活 |

## 2. 已验证基线

- 10 个仓库均已同步到 `main`，工作树 clean，remote 状态 sync；
- Workspace CLI 已具备 `wf/repo/bundle/release/tool` 命令框架；
- Manifest 提供 7 个 Profile，仓库级 DAG 当前无环；
- 8 条 Flow YAML 已存在；
- ADR-0001～0006、Schema Owner 和工具四类归属已形成；
- Lock、FuseSoC 配置生成、Flow runner 和 Evidence 基础结构已经存在。

“文件存在”只表示基线已建立，不表示端到端能力完成。

## 3. P0 阻塞与风险

| ID | 问题 | 影响 | 解除条件 | Owner |
|---|---|---|---|---|
| R-00 | Profile 选择失真、依赖无类型 | 工作区过大，影响/验证闭包不准确 | ✅ 已解除（2026-08-17）：ADR-0007 accepted + WF-002 实现 exact Profile/typed deps/DAG/closure（65 项测试全绿） | workflow |
| R-01 | Flow 使用的 action 与 runner 注册表差距大 | 多数 Flow 无法真实运行 | ✅ 已解除（2026-08-17）：capability registry + preflight 实现（6 态 + fail-closed 阻断） | workflow/tools |
| R-02 | 工具版本/hash 未完整锁定 | Evidence 不可严格重建 | ✅ 已解除（2026-08-17）：Lock tools 段 + Run Manifest environment/provider/hash 字段 | workflow/tools |
| R-03 | APB VIP 与 RAL/CSR 联合闭环未完成 | 无代表性端到端验收 | WP3 全部出口通过 | dv/vip/ip |
| R-04 | Release CLI 与 CI 仍未真实化 | 无法完成 G7 和 Catalog 发布 | WP4 dry-run + 受保护环境实跑 | workflow/catalog |
| R-05 | 缺 CBB 专用 Flow | CBB 规划无法执行和验收 | 新增 Flow、Schema 和测试 | cbb/workflow |
| R-06 | SoC 验证依赖未显式表达 | 影响分析可能漏掉 dv/vip | ✅ 已解除（2026-08-17）：soc-integration typed deps（verification: dv-common/vip）在 WF-002 落地 | workflow/soc |
| R-07 | Windows 统一检查入口不可直接使用 | `make check` 硬编码 `.venv/bin/python`；Pytest 默认编码受 locale 影响 | ✅ 已解除（2026-08-17）：Makefile/pre-commit 跨平台入口（uv run python）+ 测试显式 UTF-8；`make check` 与 pre-commit 11/11 全绿 | workflow |

## 4. 决策队列

| 决策 | 建议 | 截止点 |
|---|---|---|
| ADR-0007：显式 Profile + typed dependencies | ✅ 已接受（2026-08-17，REV-1/REV-2） | M0 |
| ADR-0008：Action preflight + provider lock | ✅ 已接受（2026-08-17，REV-1/REV-2/REV-3） | M0 |
| dv-common / soc-integration 是否重命名 | 近期不改，以 Manifest 真实名为 canonical | M4 后复审 |
| APB 示例是否长期作为 Hello World | 建议是，作为每次 baseline/release 的最小回归 | M2/M3 |
| techlib 是否建仓 | 等两个真实适配消费者出现 | M5 |

## 5. 更新模板

每次状态更新追加或修改以下信息：

```text
日期：YYYY-MM-DD
工作包/仓：
状态：planned | in-progress | blocked | done | deferred
本次完成：
证据：PR / SHA / run-id / report
下一动作：
阻塞与解除条件：
Accountable 角色/负责人：
目标日期或复审点：
```

禁止仅以任务数量或文档篇幅报告百分比；优先报告里程碑出口和可重建证据。

## 6. 本轮验证记录

- **2026-08-17 WF-001/WF-003 决策完成**：ADR-0007/ADR-0008 均接受并写入修订点；产出 [`evidence/action-inventory.md`](evidence/action-inventory.md)（46 个 action：注册 6、缺口 40，量化 F-004）与 [`evidence/profile-diff.md`](evidence/profile-diff.md)（5 个开发 Profile 实测完全相同，量化 F-010）；M0 进入 C0（ADR 部分），R-00/R-01 解除条件已就绪；
- **2026-08-17 WF-002（M1）实现完成**：exact Profile（`include_repositories`/`optional_repositories`）+ typed dependencies（product/verification/tooling/discovery/context）+ typed DAG/closure 落地；default.yaml 迁移为精确 Profile；新增 14 项测试（共 65 项全绿）；R-00 解除；M1 进入 C1（Profile 部分）；
- **2026-08-17 M0 Findings 审核完成**：F-001～F-013 已逐项确认 Owner、关闭阶段与关联任务（见 [`findings.md`](findings.md) §6）；M0 进入 C0（ADR+Findings 部分）；
- **2026-08-17 M1 核心实现完成**：WF-004（capability registry + preflight 6 态）、WF-005（runner fail-closed/required 阻断/timeout/retry/write_scope/Gate 判定）、WF-006/TOOL-003（Run Manifest environment/provider/hash + Lock tools 段）、WF-007/TOOL-004（退出码分段契约 + 参数/路径安全）、WF-011（Makefile/pre-commit 跨平台入口 + UTF-8，F-013 解除，pre-commit 11/11 全绿）、WF-012（事件循环 guard/secret redaction/force-push 拒绝）落地；新增 capability/runner/security/pr 测试，**95 项测试全绿**；R-01/R-02/R-06/R-07 解除；
- **2026-08-17 已实现 Finding 关闭**：F-001/002/004/005/006/007/008/012 由 `open → resolved`（机制级实现 + 测试证据）；连同 F-010/F-013，共 10 项已关闭；仍 open：F-003/F-009（M4）、F-011（M3/M4，accepted）；
- 信息架构：Workflow + 10 个 Repo 均具有 README 设计入口和 delivery 任务定义（11/11）；Repo 的完整历史细节仍保存在 design-reference；
- 任务模型：79 个稳定任务 ID 全部进入统一 [`todo.md`](todo.md)（79/79），delivery 状态列 0、重复 ID 0、未知依赖 0、依赖环 0；
- 候选仓：techlib/model/sw/reference-soc 共 4 份建仓前提案，均未进入 Manifest 或 required dependency；
- 文档质量：73 个 Markdown，本地断链 0、尾随空白 0、混合换行 0、缺末尾换行 0；
- 工作边界：本轮未修改脚本、Manifest、Schema、Flow YAML 或运行时代码；实现问题仅登记在 [`findings.md`](findings.md)；
- 历史迁移：45/45 覆盖保持不变，旧 `docs/archived/` 已在此前人工批准后删除，可由 Git 历史恢复；
- 既有工程门禁状态不因本轮文档整理而改变：跨平台 `make check`、离线 pre-commit 和 Ruff format 风险继续按 F-013/既有记录跟踪。
