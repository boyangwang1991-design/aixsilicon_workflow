# 当前能力边界与已知差异

核对日期：2026-09-10。依据为当前本地 Manifest、Flow、runtime 实现、仓内 README/Core 和 suite 入口。
本页是有日期的检查记录，不是长期维护的资产状态总表；仓库变化后应重新核查。

## 已核实的控制面行为

- `aix wf doctor` 本次通过：10 仓依赖图无环、所检查仓库 remote 正常；不代表领域 EDA 可用或资产合格。
- 三条 Flow 的 preflight 均阻断：`skill.ip.design`、`skill.cbb.design`、`skill.soc.integration` 为 `unimplemented`。Skill 已物化不等于这些 provider 已注册。
- `workspace-prepare` 实际调用 `workspace.resolve`，检查所选必选仓是否缺失/dirty 并生成 FuseSoC 聚合配置；没有据此证明隔离工作树自动分配。
- `aix release publish` 当前仅经工作区 guard 后记录本地发布状态；不自动执行远端发布，也不能替代可审计的人工批准记录。

实现依据：[actions.py](../../repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/src/aixworkflow/actions.py)、[capability.py](../../repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/src/aixworkflow/capability.py)、[release CLI](../../repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/src/aixworkflow/cli/extras.py)。

## 跨仓文档与契约差异

| 发现 | 当前处理原则 | 后续 owner |
|---|---|---|
| ownership map 的 CBB `cbb/`、DV `common/`、VIP 顶层路径与实际资产布局不一致 | 本文说明实际布局但不扩大机器授权；涉及写入时先确认精确 owner/路径，修复映射后再执行自动流程 | Workflow + 资产 owner |
| DV Common 的实际 `.core` 仍使用历史 vendor，与统一 `aixsilicon:*` 政策不一致 | 不宣称命名迁移已完成；消费前核查实际 VLNV，迁移需更新消费者及锁 | DV Common + 消费者 |
| HWIF README 指向已不存在的 workflow 域文档/任务表 | 新导航直接链接仓内指南与 suite，不恢复第二份领域规范或中央任务表 | HWIF 文档 owner |
| VIP README 仍提及 `vip-repo-maintainer`，实际主入口是 `vip-development-suite` | 以当前存在的套件及子 skill 为入口；registry 与套件生命周期状态不能机械等同 | VIP + Skill owner |
| IP README 部分历史段落说 planned 无目录，与当前允许开发目录的校验不一致 | planned 目录不代表 implemented；按当前校验和交接契约处理 | IP owner |
| SoC/VIP 独立工作区示例列出局部 `.venv` | 在本多仓 workflow 内仍统一用根 uv 环境；独立工程示例不能直接套入本地多仓布局 | Skill owner |
| Tool 归属政策与部分套件自带确定性脚本并存 | 先使用实际已实现入口，不宣称所有能力已迁到 `aix tool` | Tools + Skill owner |
| IP SEC-015 的 registry 名称/版本与工作区包身份不同 | 保留 planned 告警；交付前由 owner 决定对齐还是拆分，不能自动重命名或升级状态 | IP owner |

这些差异不在本次文档任务中修改实现；本文不构成对历史路径、缺失 provider 或发布能力的授权豁免。

## 使用这些文档时的判断顺序

先查当前机器配置与源码，再查所属 suite 的 artifact contract 和子 skill，最后读本层说明。
若来源冲突，保留 finding，暂停会受冲突影响的写入/发布，交给 owner 澄清；不要仅挑选最宽松的描述执行。
资产是否可用应逐项查看 registry、具体包身份、支持矩阵、质量证据及消费者验证，而不是引用规划条目数量。
