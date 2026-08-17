# VIP 交付台账

> 状态、负责人、日期和 Evidence 只在 [`../todo.md`](../todo.md) 维护。

| ID | P | 里程碑 | 任务 | 依赖 | 验收 / Evidence | Owner |
|---|---|---|---|---|---|---|
| VIP-001 | P0 | M3 | 完成 APB VIP MVP | HWIF-001、DV-001 | driver/monitor/checker/coverage/negative/RAL 单测 | boyang wang |
| VIP-002 | P0 | M3 | 建立故意违规 DUT/transaction 负向套件 | VIP-001 | 每类协议错误被稳定捕获并分类 | boyang wang |
| VIP-003 | P0 | M3 | 在代表性 APB IP 中达到 V3 Qualified | IP-003、WF-008 | 固定 SHA/Lock 的回归、覆盖和 Evidence | boyang wang |
| VIP-004 | P1 | M4 | 发布 APB VIP 并登记兼容/能力矩阵 | WF-010、CAT-003 | Tag/Release/Catalog PR/限制说明 | boyang wang |
| VIP-005 | P1 | 扩展 | 评审 AXI4-Lite/Stream 下一 MVP | VIP-004、真实消费者 | 协议范围、Owner、维护成本和验收获批 | boyang wang |
| VIP-006 | P2 | 扩展 | 评审双 simulator/cocotb 交叉验证 | 可用 provider | 可重建矩阵且不把可选工具变 required | boyang wang |

Clock/reset 等协议无关组件不在本仓重复建设，使用 DV Common 的版本化 API。
