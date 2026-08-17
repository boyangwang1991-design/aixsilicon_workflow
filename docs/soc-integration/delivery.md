# SoC Integration 交付台账

> 状态、负责人、日期和 Evidence 只在 [`../todo.md`](../todo.md) 维护。

| ID | P | 里程碑 | 任务 | 依赖 | 验收 / Evidence | Owner |
|---|---|---|---|---|---|---|
| SOC-001 | P1 | M6 | 冻结最小 instance/address/IRQ/CRG/connect Schema | M3/M4 契约 | 正负样例、版本和 Owner 审核 | boyang wang |
| SOC-002 | P1 | M6 | 建立只含已发布 APB 资产的最小 Golden | CAT-005、IP-004 | 配置可解析，版本/接口无歧义 | boyang wang |
| SOC-003 | P1 | M6 | 定义 socgen/connect provider 输入输出契约 | SOC-001 | 生成区/手写区、Result/Artifact/路径约束 | boyang wang |
| SOC-004 | P1 | M6 | 完成地址/IRQ/连接/接口负向检查 | SOC-003、TOOL-006、HWIF-004 | 冲突/缺端点/不兼容稳定失败 | boyang wang |
| SOC-005 | P1 | M6 | 完成 compile/sim/boot smoke/baseline | SOC-002～004、WF-014 | 固定 Lock 的 G0～G6 Evidence | boyang wang |
| SOC-006 | P2 | 决策门 | 评审独立 sw 仓 | SOC-005 | 独立生命周期/Owner/两个消费者或批准例外 | boyang wang |
| SOC-007 | P2 | 决策门 | 评审 reference-soc 建仓 | 稳定 Golden、独立发布需求 | 批准 ADR 或继续作为本仓示例 | boyang wang |

M6 前允许设计 Schema 与 provider contract，不提前把候选仓或大规模生成器列为 required。
