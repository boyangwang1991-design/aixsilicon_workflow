# Skills 交付台账

> 状态、负责人、日期和 Evidence 只在 [`../todo.md`](../todo.md) 维护。

| ID | P | 里程碑 | 任务 | 依赖 | 验收 / Evidence | Owner |
|---|---|---|---|---|---|---|
| SKILL-001 | P1 | M3 | 运行现有 Suite validator 与脚本单测 | 可复现 Python 环境 | 结构/引用/契约/测试全绿 | boyang wang |
| SKILL-002 | P1 | M3 | 对齐 Context Pack/Change Plan/Skill Result | WF-006、ownership | Schema、读写 scope、provenance 校验 | boyang wang |
| SKILL-003 | P1 | M3 | 执行 8 个端到端 Eval 和负向安全测试 | SKILL-001/002 | 评分、失败样本、注入/越权结果可审计 | boyang wang |
| SKILL-004 | P1 | M3/M4 | 用 APB Golden Path 验证 Author/Verifier 双角色 | WF-008、IP-003 | 候选变更经独立验证和 G0～G6 | boyang wang |
| SKILL-005 | P2 | M5 | 评审 CBB Suite | WF-013 稳定 | 不复制 Tool；首个真实 CBB Eval | boyang wang |
| SKILL-006 | P2 | M6 | 添加 SoC Integration Suite | WF-014 稳定 | 16 个子 skill + 配置指纹 + drawio 图生成 | boyang wang |

Skills 始终是可选增强，不加入公共流程 required closure。
