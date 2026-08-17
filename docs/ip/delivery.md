# IP 交付台账

> 状态、负责人、日期和 Evidence 只在 [`../todo.md`](../todo.md) 维护。

| ID | P | 里程碑 | 任务 | 依赖 | 验收 / Evidence | Owner |
|---|---|---|---|---|---|---|
| IP-001 | P0 | M3 | 冻结 APB 寄存器 IP 规格、SystemRDL 和验收矩阵 | HWIF-001 | 需求/寄存器/测试/Gate 可追溯 | boyang wang |
| IP-002 | P0 | M3 | 确定性生成 RTL/RAL/Header/Core | IP-001、TOOL-002 | drift check、hash、正负样例 | boyang wang |
| IP-003 | P0 | M3 | 完成 APB lint/build/unit/regression | DV-002、VIP-001、WF-008 | 固定 Lock 下 G0～G6 Evidence | boyang wang |
| IP-004 | P0 | M4 | 完成发布候选、人工批准和 Catalog 登记 | IP-003、WF-010、CAT-004 | G7、Tag/Release/SBOM/RTM/Catalog PR | boyang wang |
| IP-005 | P1 | M4 | 收敛 ipkg 与 aix-core-tool/release 的边界 | IP-004 | 无重复 Core/发布事实源，兼容测试通过 | boyang wang |
| IP-006 | P2 | 扩展 | 评审 Bridge/PIC 下一切片 | APB C4、真实消费者 | 评审记录、Owner、资源和验收切片 | boyang wang |

## APB 必测负向场景

非法地址、只读写入、写掩码、reset 中访问、wait-state、error response、RAL mirror mismatch、缺 provider、脏工作区和证据缺失均必须产生可解释失败。
