# AIXSILICON 开发进度台账

更新时间：2026-08-14。本文是跨仓组合状态的唯一活动看板；任务细节以各仓 `delivery.md` 为准。

## 1. 组合状态

| 工作包 | 状态 | 完成判据 | 当前差距 | Accountable 角色 | 复审点 | 下一证据动作 |
|---|---|---|---|---|---|---|
| WP0 方案审核 | `in-progress` | 文档覆盖、目标方案、Findings 和 ADR 经人工批准 | 新组织与候选仓提案已形成，尚未批准 | workflow architect | 本次人工审核 | 逐项接受/修订 ADR-0007/0008、F-001～016 |
| WP1 Profile/依赖 v2 | `planned` | Profile exact-set 正确，typed closure/兼容测试通过 | 当前 `minimal` 启用 9 仓，主要 Profile 几乎相同 | workspace maintainer | WP0 后 | 提交 exact-set/typed DAG 测试设计 |
| WP2 Action Capability | `planned` | P0 action preflight 全部可解释，provider 被锁定 | 大量 action 未注册，FuseSoC 未实跑 | workflow runtime + tools | WP1 可并行设计 | 产出 action/provider inventory 与负向矩阵 |
| WP3 APB 穿刺 | `planned` | 固定 Lock 下 lint/编译/仿真/Evidence 可重建 | VIP、RAL/CSR、provider 尚未闭环 | APB domain owners | WP1/WP2 后 | 冻结 APB 验收矩阵和故障注入集 |
| WP4 协作和发布 | `planned` | PR HEAD 联测和 G7 发布闭环 | CI、release、Catalog PR 多为桩/占位 | release platform | WP3 G0～G6 后 | 审核 Bundle/Release/Catalog 状态机 |
| M5 CBB 产品化 | `planned` | CBB Flow + 三个示范构件 + PPA Evidence | 缺专用 Flow 与可发布闭环 | cbb owner | APB C4 后 | 冻结三示范切片和 PPA 可比字段 |
| M6 SoC 最小集成 | `planned` | 最小 SoC Golden 可生成、仿真和锁定 | Schema 骨架，生成/check action 未实现 | soc-platform | APB Catalog 后 | 审核最小 Schema/Golden/provider contract |

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
| R-00 | Profile 选择失真、依赖无类型 | 工作区过大，影响/验证闭包不准确 | 接受 ADR-0007 并完成 WP1 | workflow |
| R-01 | Flow 使用的 action 与 runner 注册表差距大 | 多数 Flow 无法真实运行 | capability registry + provider preflight | workflow/tools |
| R-02 | 工具版本/hash 未完整锁定 | Evidence 不可严格重建 | workspace lock 增加 tools 段 | workflow/tools |
| R-03 | APB VIP 与 RAL/CSR 联合闭环未完成 | 无代表性端到端验收 | WP3 全部出口通过 | dv/vip/ip |
| R-04 | Release CLI 与 CI 仍未真实化 | 无法完成 G7 和 Catalog 发布 | WP4 dry-run + 受保护环境实跑 | workflow/catalog |
| R-05 | 缺 CBB 专用 Flow | CBB 规划无法执行和验收 | 新增 Flow、Schema 和测试 | cbb/workflow |
| R-06 | SoC 验证依赖未显式表达 | 影响分析可能漏掉 dv/vip | 修订依赖模型并加 DAG 测试 | workflow/soc |
| R-07 | Windows 统一检查入口不可直接使用 | `make check` 硬编码 `.venv/bin/python`；Pytest 默认编码受 locale 影响 | Makefile/测试显式跨平台路径与 UTF-8，pre-commit 环境可离线/稳定安装 | workflow |

## 4. 决策队列

| 决策 | 建议 | 截止点 |
|---|---|---|
| ADR-0007：显式 Profile + typed dependencies | 建议接受，兼容迁移两个发布周期 | WP0 |
| ADR-0008：Action preflight + provider lock | 建议接受 | WP0 |
| dv-common / soc-integration 是否重命名 | 近期不改，以 Manifest 真实名为 canonical | M4 后复审 |
| APB 示例是否长期作为 Hello World | 建议是，作为每次 baseline/release 的最小回归 | M3 |
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

- 信息架构：Workflow + 10 个 Repo 均具有 README 设计入口和 delivery 活动台账（11/11）；Repo 的完整历史细节仍保存在 design-reference；
- 任务模型：79 个稳定任务 ID，重复 ID 0、未知依赖 0、依赖环 0；
- 候选仓：techlib/model/sw/reference-soc 共 4 份建仓前提案，均未进入 Manifest 或 required dependency；
- 文档质量：72 个 Markdown，本地断链 0、尾随空白 0、混合换行 0、缺末尾换行 0；
- 工作边界：本轮未修改脚本、Manifest、Schema、Flow YAML 或运行时代码；实现问题仅登记在 [`findings.md`](findings.md)；
- 历史迁移：45/45 覆盖保持不变，旧 `docs/archived/` 已在此前人工批准后删除，可由 Git 历史恢复；
- 既有工程门禁状态不因本轮文档整理而改变：跨平台 `make check`、离线 pre-commit 和 Ruff format 风险继续按 F-013/既有记录跟踪。
