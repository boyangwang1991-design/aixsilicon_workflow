# Tools 交付台账

| ID | P | 里程碑 | 任务 | 依赖 | 验收 / Evidence | Owner | 状态 |
|---|---|---|---|---|---|---|---|
| TOOL-001 | P0 | M2 | 为现有公共包补齐 provider metadata/capability | WF-003 | inventory 与 preflight 全覆盖 | engineering-platform | `planned` |
| TOOL-002 | P0 | M2/M3 | 接通 schema/hwif/reg/core 到 APB Flow | TOOL-001、WF-004 | 真实 provider 调用、稳定 Result/Artifact | tools + workflow | `planned` |
| TOOL-003 | P0 | M2 | 锁定包、外部工具、容器/EDA 版本与 hash | WF-006 | Lock/Evidence Schema 与重放通过 | tools + workflow | `planned` |
| TOOL-004 | P0 | M2 | 统一工具侧退出码、安全参数和路径边界 | WF-003/004 | 注入/越界/缺依赖负向测试 | engineering-platform | `planned` |
| TOOL-005 | P1 | M5 | 建设 param-matrix/PPA provider 最小集 | CBB-001～004 | 三个 CBB 示范闭环可重建 | tools + cbb | `deferred` |
| TOOL-006 | P1 | M6 | 建设 socgen/connect 最小 provider 集 | SOC-001～004 | Golden 地址/IRQ/CRG/Top/连接检查 | tools + soc | `deferred` |
| TOOL-007 | P2 | 扩展 | 按消费者评审 report/rtm/package/catalog 工具 | APB C4 或 M5/M6 需求 | 无重复能力；首个 PR 带真实消费者测试 | engineering-platform | `deferred` |

已完成包的实现明细保留在 Git 和设计参考，不在活动台账重复。
