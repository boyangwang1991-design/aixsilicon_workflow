# AIXSILICON 完整建设路线图

本文是跨仓建设顺序、里程碑出口和组合级优先级的唯一活动规划。全部任务状态、负责人和 Evidence 在 [`todo.md`](todo.md)，组合状态与决策队列在 [`progress.md`](progress.md)，实现缺陷与关闭证据在 [`findings.md`](findings.md)。目标架构见 [`architecture/target-design.md`](architecture/target-design.md)。

计划基线：2026-08-14。相对周次以方案/ADR 获批后的首个工作日为 `T0`；下文日历窗口按建议 `T0 = 2026-08-17` 估算，人工审核晚于该日时整体顺延，不压缩验证时间。

## 1. 路线图目标

建设顺序不是“把所有 Repo 同时补全”，而是：

1. 先建立 fail-closed 的控制面和可重建证据底座；
2. 用一个 APB 寄存器 IP 做最短穿刺，证明真实 provider 能运行；
3. 在同一切片上补齐负向、边界、影响分析和 G0～G6，形成完整实现；
4. 再补 Change Bundle、人工批准、G7、Release 和 Catalog；
5. 复用已经验证的控制面建设 CBB 三个示范闭环；
6. 最后建设最小 SoC Golden，再评审是否拆分新仓；
7. 规模化、更多协议/IP、私有 EDA/Skill 和多环境矩阵均在核心闭环稳定后展开。

## 2. 完成度定义

同一能力统一使用 C0～C5，避免把“文件存在”误报为“完成”：

| 等级 | 名称 | 必须证明 | 不足以达到该等级的内容 |
|---|---|---|---|
| C0 Designed | 方案已冻结 | Owner、边界、Schema/契约、依赖、验收和风险获批 | 只有 README/YAML 草案 |
| C1 Runnable | 最短穿刺可运行 | 真实 provider 在 clean workspace 完成一条 happy path | mock、手工拼接、required stage 被 skip |
| C2 Integrated | 完整实现已接通 | 正向/负向/边界、失败传播、Lock/Result/Artifact 全部接通 | 仅“退出码 0”或单元测试 |
| C3 Qualified | 可重建资格通过 | 固定 Lock 的 G0～G6、影响集合、Evidence Index 和故障注入 | registry 中手写 `pass` |
| C4 Released | 可正式消费 | 人工批准、G7、Tag/Release、SBOM/RTM、Catalog PR | candidate、开发分支或本地包 |
| C5 Proven | 已规模复用 | 至少两个独立真实消费者/场景和持续兼容证据 | 两个示例引用同一未发布分支 |

“穿刺完成”对应 C1；“完整实现”至少对应 C2；“资格完成”对应 C3；只有 C4 才能作为后续阶段的正式发布依赖。

## 3. 关键路径与允许并行

```mermaid
flowchart LR
    M0["M0 方案与决策冻结"] --> M1["M1 控制面安全底座"]
    M1 --> M2["M2 APB 最短穿刺 C1"]
    M2 --> M3["M3 APB 完整实现与资格 C3"]
    M3 --> M4["M4 协作与发布 C4"]
    M4 --> M5["M5 CBB 三示范闭环 C4"]
    M4 --> M6A["M6 SoC Schema/Golden 设计"]
    M5 --> M6B["M6 最小 SoC 资格 C3"]
    M6A --> M6B
    M6B --> M7["M7 规模化与候选仓复审"]

    M1 -.并行准备.-> D["APB domain contracts"]
    D -.进入.-> M2
    M3 -.并行设计.-> R["Release/Catalog contracts"]
    R -.进入.-> M4
```

允许的并行只有四条工作流：

| Lane | 主责 | 可并行范围 | 不能越过的门 |
|---|---|---|---|
| A 控制面 | workflow + tools | Profile/依赖、provider、runner、Evidence、安全 | M2 前必须达到 C2；未 fail-closed 不准实跑资格 |
| B APB 资产 | hwif + ip + dv-common + vip | Contract、SystemRDL、VIP/DV 最小能力 | 只能在 M1 契约上设计；M2 前不宣称 qualified |
| C 发布发现 | release + catalog | Schema、Catalog diff/PR、审批/幂等设计 | M3 G0～G6 前不执行正式 G7/Release |
| D 可选增强 | skills + knowledge | 文档、Eval、知识路径 | 不进入 required closure，不阻塞 A/B/C |

推荐至少配置 Lane A、Lane B、Lane C 三个稳定责任组；若只有 1～2 个执行组，计划工期按 1.3～1.5 倍评估，禁止靠删减负向测试追回日期。

## 4. 总体里程碑与建议窗口

| 里程碑 | 相对窗口 | 建议日历 | 目标等级 | 主要出口 | 状态 |
|---|---|---|---|---|---|
| M0 方案/决策冻结 | W0～W2 | 2026-08-17～08-28 | C0 | ADR-0007/0008、Findings 处置、Owner/验收批准 | `in-progress` |
| M1 控制面安全底座 | W2～W6 | 2026-08-31～09-25 | C2 | exact Profile、typed deps、preflight、fail-closed runner、Lock/Evidence | `planned` |
| M2 APB 最短穿刺 | W5～W10 | 2026-09-21～10-23 | C1 | Contract→SystemRDL→RTL/RAL/Header→compile/smoke 的真实链 | `planned` |
| M3 APB 完整资格 | W9～W15 | 2026-10-19～11-27 | C3 | 负向/边界/coverage/影响分析与固定 Lock G0～G6 | `planned` |
| M4 协作与发布 | W13～W19 | 2026-11-16～12-25 | C4 | PR HEAD 联验、审批/G7、Tag/Release、Catalog PR | `planned` |
| M5 CBB 产品化 | W20～W27 | 2027-01-04～02-19 | C4 | arbiter/pipeline/FIFO 参数/PPA 三闭环与发布 | `planned` |
| M6 最小 SoC | W24～W33 | 2027-02-01～04-02 | C3 | 已发布 APB 资产组成 Golden，生成/检查/boot smoke/baseline | `planned` |
| M7 规模化运营 | W33+ | 2027-04-05 起 | C5 | 第二消费者、Nightly/兼容矩阵、候选仓决策、运营指标 | `deferred` |

M5 跨年安排从 2027-01-04 起正式执行，避免把年末低可用周期写成虚假的连续交付。M6 的 Schema/Golden 设计可在 M4 后半段开始，但正式 build/smoke 必须消费 C4 资产和稳定 Catalog resolve。

## 5. M0：方案与决策冻结

### 5.1 目标

把“建议方案”变为可执行承诺，确定哪些问题现在解决、哪些延后、谁负责以及用什么证据关闭。

### 5.2 工作范围

| 任务 | 内容 |
|---|---|
| WF-001 | 接受或修订 ADR-0007：exact Profile + typed dependencies |
| WF-003 | 接受或修订 ADR-0008：Action/Provider/Preflight |
| WP0 审核 | 审核目标架构、11 个域设计契约、79 个 Delivery 任务和候选仓激活门 |
| Findings 审核 | 对 F-001～F-013 逐项确定 severity、Owner、关闭阶段和 Evidence |

### 5.3 出口与停止条件

出口：ADR 状态明确；M1/M2 的 Accountable 与首个 PR/测试设计明确；APB profile、公开 simulator/provider 和最小 IP 范围获批。

停止条件：ADR-0007/0008 未决、APB profile 不明确或没有 Lane A/B Owner 时，不进入实现；允许继续做只读审计和设计，不允许并行铺开 CBB/SoC。

## 6. M1：控制面安全底座（先于业务穿刺）

### 6.1 实现顺序

1. WF-002：exact Profile、typed dependency、v1 兼容和 DAG/closure 测试；
2. TOOL-001 + WF-004：provider metadata、capability registry、preflight；
3. WF-005：required/needs/timeout/retry/on_failure/gate/write_scope fail-closed；
4. WF-006 + TOOL-003：Lock、Run Manifest、Evidence、provider/tool/env/hash；
5. TOOL-004 + WF-007：安全参数、路径、退出码和失败分类；
6. WF-011/WF-012：跨平台检查入口、受控 PR、secret/权限负向测试。

### 6.2 必测负向矩阵

未注册 action、provider unavailable、required stage skipped/blocked、dirty repo、unlocked revision、local override、越界 write scope、命令/路径注入、超时、重试耗尽、依赖失败、缺 Evidence、错误 Gate 顺序和 Windows/POSIX 编码差异。

### 6.3 里程碑出口

- `minimal/ip-dev/cbb-dev/dv-dev/soc-integration/release` 得到可解释的精确仓集；
- preflight 对每个 required/optional action 给出 provider/version/availability；
- required 能力缺失时运行前失败，运行中失败不会汇总成 pass；
- Lock/Evidence Schema 可校验并能重放一个最小虚拟 Flow；
- F-001/F-002/F-004～F-008/F-010/F-012 至少完成机制级测试，最终关闭仍以 M3 真实 APB Evidence 为准。

## 7. M2：APB 最短穿刺（C1 Runnable）

### 7.1 目标切片

只实现一个最小 APB 寄存器 IP：一个明确 APB profile、一个 SystemRDL addrmap、一个可观察功能/中断、一个公开 simulator 路径。穿刺的目标是证明链路，不在此阶段追求多协议、多工具或完整性能签核。

### 7.2 任务顺序与并行关系

| 子阶段 | 任务 | 可并行 | 出口 |
|---|---|---|---|
| 契约 | HWIF-001、IP-001、DV-001 | Catalog/Knowledge Schema 设计 | APB/CSR/Result/验收矩阵冻结 |
| 公共验证 | DV-002、DV-003、VIP-001、VIP-002 | HWIF 生成视图 | RAL/CSR/clock/reset + APB checker/negative 可单测 |
| 确定性生成 | HWIF-002、TOOL-002、IP-002 | VIP/DV 单测 | RTL/RAL/Header/Core 可重建，drift 被拒绝 |
| 首次组装 | DV-004、WF-008（先进入 in-progress） | Knowledge/Skill 可选对齐 | clean workspace 完成 compile + 最小 smoke |

### 7.3 C1 出口

- 真实 provider 完成 `resolve → preflight → generate → lint/build → smoke → Result`；
- 生成物与输入/工具版本有 hash；
- 至少一次故意缺 provider、破坏寄存器或协议错误能被稳定捕获；
- 允许部分完整回归/coverage 尚未关闭，但缺项必须明确显示为未完成，不能显示 pass。

若 C1 连续两个迭代仍依赖手工步骤，应停止增加功能，先把手工步骤转成 Action/Provider 或明确移出公共流程。

## 8. M3：APB 完整实现与资格（C2→C3）

### 8.1 完整实现范围

- HWIF-003：APB Contract 被 VIP、IP 和至少一个 CBB/等价消费者联合消费；
- IP-003：lint/build/unit/smoke/regression、CSR 一致性、coverage 和限制说明；
- VIP-003：APB VIP 达 V3 Qualified，故意违规 DUT/transaction 全部命中；
- WF-008：APB Flow 的 action/Gate/write scope/Evidence 完整，G0～G6 顺序正确；
- DV-005：在第二消费者上验证 DV Common API/SemVer（可在 M3 后半段完成）；
- KNOW-004、SKILL-003/004：只作为可选质量增强，不阻塞公共资格。

### 8.2 必须覆盖的失败场景

非法/未对齐地址、RO 写入、reserved 位、write mask、reset 中访问、wait-state、error response、RAL mirror mismatch、协议时序违规、超时、随机 seed 重放、脏/未锁工作区、required stage skip、证据缺字段和跨仓 PR SHA 不一致。

### 8.3 C3 出口

- 固定 Lock 从 clean workspace 可重复完成 G0～G6；
- Run Manifest/Evidence Index 能定位 repo SHA、stage、provider/tool/env、seed、artifact hash 和 Failure Signature；
- 负向/边界/恢复测试全部有预期失败类别；
- Qualification 不产生 G7，不创建正式 Tag/Catalog 条目；
- F-001/F-002/F-004/F-007/F-008/F-011 只有在真实 APB Evidence 通过后才能关闭。

## 9. M4：跨仓协作与正式发布（C4）

### 9.1 设计准备（可与 M3 后半段并行）

CAT-001/003/004：Catalog Schema、APB 条目模板、Catalog diff/PR 契约；WF-009：Change Bundle 状态机和 PR HEAD checkout 设计。

### 9.2 实现顺序

1. WF-009：多 PR HEAD、影响集合、联合 CI、merge order 和最终 SHA；
2. CAT-002：现有条目来源/Evidence 清查，不能把历史 `pass` 当证明；
3. WF-010：candidate → approval → G7 → Tag/Release → Catalog PR；
4. IP-004/005：IP 发布、ipkg/Core 边界、legacy VLNV 迁移；
5. HWIF-004、VIP-004：发布 APB Contract/VIP 及兼容矩阵；
6. CAT-005/006：resolve/compatibility 与 Release→Catalog 端到端验收。

### 9.3 C4 出口

- Change Bundle 联验的每个结果绑定精确 PR HEAD；
- clean/locked/no-override 和 G0～G6 合格后才可请求人工批准；
- G7、Tag/Release、SBOM、RTM、Release Manifest 和 Catalog PR 完整；
- 重复 publish 幂等，并发发布互斥，中途失败可从明确状态恢复；
- APB IP/HWIF/VIP 可由 Catalog + Lock 在新工作区重建；
- F-003/F-006/F-009/F-011 完成关闭证据。

M4 未完成前，不把 APB 方案复制到第二类完整 IP，也不把 CBB/SoC 标为正式可消费。

## 10. M5：CBB 三个示范闭环

### 10.1 顺序

1. CBB-001：metadata/params/result/PPA Schema 和成熟度；
2. CBB-002/003/004：arbiter、ready/valid pipeline、FIFO 三个独立示范；
3. CBB-005：从三示范中提炼 Action/Flow 领域验收契约；
4. TOOL-005 + WF-013：param-matrix/PPA provider 与 CBB qualification Flow；
5. CBB-006：三个构件完成 G0～G7、Release 和 Catalog；
6. HWIF-005/SKILL-005 只有在真实需求出现时启动。

### 10.2 三示范各自证明

| 构件 | 必须证明 |
|---|---|
| arbiter | 公平/优先级属性、请求边界、形式或随机验证、实现变体 |
| ready/valid pipeline | latency/throughput/backpressure 契约、长链切分、PPA sweep |
| FIFO | depth/width/阈值边界、overflow/underflow、memory mapping 和 CDC 适用性 |

### 10.3 出口

三个示范均达到 C3，至少一个达到 C4；PPA 数据绑定工艺/库/约束/tool/RTL SHA/参数；真实 IP/SoC 消费至少一个构件。未达到这些条件前不批量实现 15 个种子构件；CBB-007 保持 deferred。

## 11. M6：最小 SoC Golden

### 11.1 前置条件

APB IP/HWIF/VIP 已达到 C4；Catalog resolve 稳定；SoC 只消费已发布版本；M5 至少一个 CBB 可消费或明确记录本次不使用 CBB 的理由。

### 11.2 实现顺序

1. SOC-001：冻结 instance/address/IRQ/CRG/connect 最小 Schema；
2. SOC-002：从 Catalog 选择发布资产，建立最小 Golden；
3. SOC-003：先冻结 socgen/connect provider 输入输出和生成区边界；
4. TOOL-006：按已冻结契约实现 socgen/connect 最小 provider；
5. SOC-004：基于真实 provider 完成地址冲突、缺端点、接口/clock/reset 不兼容负向检查；
6. WF-014 + SOC-005：compile/sim/boot smoke/baseline Lock/G0～G6；
7. SKILL-006 可做可选 Eval，不进入 required Gate。

### 11.3 出口

- Catalog → SoC config → address/IRQ/CRG/Top/software view → compile/sim/boot smoke 可重建；
- 生成区与手写区隔离，非法连接稳定失败；
- baseline Lock 和 Evidence 可用于新工作区复现；
- 达到 C3 后再决定是否对参考 SoC 做独立 G7/Release。

SOC-006/007 只在出口后评审 `sw`/`reference-soc` 候选仓，不提前建空仓。

## 12. M7：规模化、第二消费者与候选仓

### 12.1 C5 工作

- APB/HWIF/VIP/DV 在第二个独立 IP/项目验证兼容性；
- CBB-007 按真实消费者扩种子池；
- VIP-005/006 按需求引入 AXI4-Lite/Stream 和第二 simulator；
- DV-006、TOOL-007、KNOW-005～007 按证据驱动扩展；
- CAT-007 建立 deprecated/yanked/替代与周期审计；
- Nightly、baseline train、容量/失败指标、blue/red zone 和兼容矩阵运营化。

### 12.2 候选仓复审

| 候选 | 复审任务/阶段 | 激活条件 |
|---|---|---|
| techlib | HWIF-006 / M5 后 | 两类真实适配、两个消费者、独立版本与公共/私有边界 |
| model | 按需 | 两个 IP 共享同一模型且需要独立发布 |
| sw | SOC-006 / M6 后 | 两个目标共享 BSP/Boot/HAL 且生命周期独立 |
| reference-soc | SOC-007 / M6 后 | Golden 稳定、存在外部消费者和独立 Release 需求 |

详细提案见 [`proposals/repositories/`](proposals/repositories/README.md)。未满足门禁时继续留在现有 Owner 仓或私有 Overlay。

## 13. 任务覆盖与阶段归属

| 阶段 | 必需任务 | 可选/后置任务 |
|---|---|---|
| M0 | WF-001、WF-003 | — |
| M1 | WF-002、WF-004、WF-005、WF-006、WF-007、WF-011、WF-012、TOOL-001、TOOL-003、TOOL-004 | SKILL-001、SKILL-002、KNOW-001、KNOW-002、KNOW-003 |
| M2 | HWIF-001、HWIF-002、IP-001、IP-002、DV-001、DV-002、DV-003、DV-004、VIP-001、VIP-002、TOOL-002、WF-008（启动） | CAT-001、CAT-003、CAT-004、KNOW-004 |
| M3 | HWIF-003、IP-003、VIP-003、WF-008（完成）、DV-005 | SKILL-003、SKILL-004 |
| M4 | WF-009、WF-010、CAT-002、CAT-005、CAT-006、IP-004、IP-005、HWIF-004、VIP-004 | — |
| M5 | CBB-001、CBB-002、CBB-003、CBB-004、CBB-005、CBB-006、TOOL-005、WF-013 | HWIF-005、SKILL-005 |
| M6 | SOC-001、SOC-002、SOC-003、SOC-004、SOC-005、TOOL-006、WF-014 | SKILL-006 |
| M7 | CBB-007、DV-006、VIP-005、VIP-006、TOOL-007、CAT-007、IP-006、KNOW-005、KNOW-006、KNOW-007、HWIF-006、SOC-006、SOC-007 | 新候选仓任务需另经 ADR |

任务只在一个阶段拥有主要完成出口；跨阶段出现的 WF-008 等仅表示“启动/完成”两个检查点，不复制任务状态。全部任务的最新状态始终以 [`todo.md`](todo.md) 为准。

## 14. 进度管理机制

### 14.1 每周更新

每个 `in-progress` 任务必须更新：Accountable 人、目标日期、当前分支/PR、上次 Evidence、下一证据动作、阻塞及解除条件。没有 PR/测试/运行记录的任务不得长期保持 `in-progress`。

### 14.2 里程碑评审

每两周或里程碑出口前举行一次评审，只接受以下进度证据：

- 合并的 ADR/Schema/契约；
- 绑定 SHA 的 PR/CI；
- 固定 Lock 的 run-id/Evidence Index；
- 负向/故障注入结果；
- Tag/Release/Catalog PR；
- 经批准的延期、降级或 wont-fix 决策。

禁止用代码行数、文档数、完成任务百分比或“YAML 已存在”替代出口证据。

### 14.3 状态与健康度

| 状态 | 使用条件 | 组合动作 |
|---|---|---|
| `planned` | Owner/依赖/出口已明确，尚未启动 | 保持优先级，不占 WIP |
| `in-progress` | 有 Accountable、目标日期和活动 PR/Evidence | 每周更新下一证据动作 |
| `blocked` | 外部依赖/决策阻止继续 | 记录解除 Owner 和最晚复审日 |
| `done` | Gate/出口证据完整 | 从活动台账移出，保留 Git/Evidence 引用 |
| `deferred` | 未满足触发条件或资源明确后置 | 到指定里程碑复审，不暗中启动 |

组合健康度使用里程碑出口：绿色=出口已通过；黄色=仍可在窗口内完成但存在已分配风险；红色=关键路径阻塞或退出证据不成立。不得按任务数量计算绿色。

## 15. WIP、顺序和停止规则

- 每个 Lane 同时最多 2 个主要 `in-progress` 任务；跨仓联合任务计入双方 WIP；
- 优先关闭关键路径 blocker，再开始新的 P1/P2；
- 同一失败连续两个迭代无实质进展时，暂停功能扩展，进行最小复现/设计复审；
- required provider 不可用时，不用 mock/skip 继续资格；
- APB 未 C4 前不启动第二个完整 IP；CBB 三示范未过 C3 前不扩种子池；SoC 未过 C3 前不拆 reference-soc/sw；
- 安全、许可证、数据损坏或 false-green 风险可以立即停止里程碑，即使排期受影响。

## 16. 风险燃尽顺序

| 顺序 | Findings/风险 | 最晚关闭点 | 未关闭的后果 |
|---|---|---|---|
| 1 | F-001/F-002/F-004/F-005/F-007 | M1 机制完成，M3 真实关闭 | 禁止将任何 Flow 结果用于资格 |
| 2 | F-006/F-008/F-010/F-012/F-013 | M1/M2 | 无法证明安全、影响闭包和可重建性 |
| 3 | F-011 | M3 | Qualification 不得声称 G7 |
| 4 | F-003/F-009 | M4 | 禁止正式 Release/Catalog |
| 5 | APB VIP/RAL/CSR/负向闭环 | M3 | 禁止扩第二 IP/CBB/SoC |
| 6 | PPA 可比性与参数空间 | M5 | 禁止批量扩 CBB |
| 7 | SoC 生成边界/连接负向/boot smoke | M6 | 禁止独立 reference-soc/sw |

## 17. 组合级 Definition of Done

项目第一阶段可宣布“核心平台完成”，必须同时满足：

1. M0～M6 出口全部有批准记录和可重建 Evidence；
2. APB IP/HWIF/VIP 达 C4，DV Common/Tools/Workflow 至少达支撑该 Release 的 C3；
3. 三个 CBB 示范达到 C3 且至少一个 C4；
4. 最小 SoC Golden 达 C3；
5. required action/provider inventory 无未解释缺口；
6. false-green、写入越界、Lock/Evidence、Change Bundle、G7/幂等发布等 P0 Findings 已关闭；
7. 新成员能在 clean Windows/POSIX 环境按文档重建最小 APB 和 SoC Evidence；
8. Catalog 能解析精确发布资产和兼容关系，且不把 candidate/legacy-unverified 当作 qualified；
9. 候选仓均有明确的“建立/不建立”评审结果，没有口头依赖。

达到上述出口后，M7 才从 `deferred` 转为活动运营路线图。
