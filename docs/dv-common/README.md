# DV Common 仓设计契约

DV Common 是协议无关验证基础设施、运行时服务、RAL 公共机制和标准结果模型的唯一 Owner。Owner 为 `dv-platform`；VIP、IP 和 SoC 验证是消费者。

## 范围与边界

- 负责：基础类型、配置、clock/reset/timeout/watchdog、scoreboard policy、RAL base/CSR sequence、Run/Test/Failure Schema；
- 不负责：APB/AXI 等协议 driver/monitor/checker、产品 Env/DUT、Flow 编排和 EDA adapter；
- 采用组合优于继承，禁止演变成万能 Base Env；公共 API 必须小、显式、可版本化；
- `rtl/` 只容纳验证辅助 RTL，DPI 限定在无法用标准 SV 表达且有可移植替代方案的场景。

## 首个切片

围绕 APB 寄存器 IP 提供 RAL base、标准 CSR sequence、reset epoch、timeout 和统一 Test Result/Failure Signature；与 APB VIP 分工明确，并由两个消费者验证 API 稳定性。

## 验收出口

- Schema 具正负样例、版本和兼容策略；
- 组件单测覆盖正常、超时、reset 并发、compare policy 和失败聚类；
- 同一结果在不同 simulator adapter 下保持字段语义一致；
- 公共能力被 APB IP 与至少一个独立样例复用，不依赖私有 Skill；
- 发布前完成 G0～G6 所需结果/Evidence 对接。

活动交付见 [`delivery.md`](delivery.md)，完整六层模型、API 和迁移策略见 [`design-reference.md`](design-reference.md)。
