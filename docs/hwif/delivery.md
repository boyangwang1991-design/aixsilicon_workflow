# HWIF 交付台账

| ID | P | 里程碑 | 任务 | 依赖 | 验收 / Evidence | Owner | 状态 |
|---|---|---|---|---|---|---|---|
| HWIF-001 | P0 | M3 | 冻结 APB Contract/Profile/Binding/兼容规则 | ADR-0007、Schema | 正负样例通过；版本与迁移规则获批 | hw-platform | `planned` |
| HWIF-002 | P0 | M3 | 生成 package/interface/flat 三视图并做 drift check | tools provider | 固定输入得到稳定 hash；手改被拒绝 | hwif + tools | `planned` |
| HWIF-003 | P0 | M3 | 完成 APB VIP 与代表性 IP/CBB 消费者联验 | VIP-001、IP-001/CBB-002 | 精确 SHA 的编译、仿真、兼容报告 | hw-platform | `planned` |
| HWIF-004 | P0 | M4 | 发布首个 qualified APB 接口资产 | WF-010、CAT-003 | SemVer/Tag/Release/Catalog PR/Evidence | hw-platform | `planned` |
| HWIF-005 | P1 | M5 | 按真实需求补齐 L0/L1 公共契约 | HWIF-004 | 每项具两个消费者或批准的例外 | hw-platform | `deferred` |
| HWIF-006 | P2 | 决策门 | 评审 techlib 是否达到建仓条件 | 两类适配、两个消费者 | 批准 ADR 或记录继续留在 adapter/overlay | architecture board | `deferred` |

进入 `in-progress` 前补齐具体负责人、目标日期和 PR/分支。组合优先级见 [`../roadmap.md`](../roadmap.md)。
