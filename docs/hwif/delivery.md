# HWIF 交付台账

> 状态、负责人、日期和 Evidence 只在 [`../todo.md`](../todo.md) 维护。

| ID | P | 里程碑 | 任务 | 依赖 | 验收 / Evidence | Owner |
|---|---|---|---|---|---|---|
| HWIF-001 | P0 | M3 | 冻结 APB Contract/Profile/Binding/兼容规则 | ADR-0007、Schema | 正负样例通过；版本与迁移规则获批 | boyang wang |
| HWIF-002 | P0 | M3 | 生成 package/interface/flat 三视图并做 drift check | tools provider | 固定输入得到稳定 hash；手改被拒绝 | boyang wang |
| HWIF-003 | P0 | M3 | 完成 APB VIP 与代表性 IP/CBB 消费者联验 | VIP-001、IP-001/CBB-002 | 精确 SHA 的编译、仿真、兼容报告 | boyang wang |
| HWIF-004 | P0 | M4 | 发布首个 qualified APB 接口资产 | WF-010、CAT-003 | SemVer/Tag/Release/Catalog PR/Evidence | boyang wang |
| HWIF-005 | P1 | M5 | 按真实需求补齐 L0/L1 公共契约 | HWIF-004 | 每项具两个消费者或批准的例外 | boyang wang |
| HWIF-006 | P2 | 决策门 | 评审 techlib 是否达到建仓条件 | 两类适配、两个消费者 | 批准 ADR 或记录继续留在 adapter/overlay | boyang wang |

状态更新规则见 [`../todo.md`](../todo.md)，组合优先级见 [`../roadmap.md`](../roadmap.md)。
