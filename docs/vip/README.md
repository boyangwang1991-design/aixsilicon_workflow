# VIP 仓设计契约

VIP 仓保存协议相关的 driver、monitor、checker、coverage、sequence 和 adapter。Owner 为 `dv-platform`；IP/SoC 验证是消费者。

## 范围与边界

- 协议相关行为归 VIP；协议无关 runtime、RAL 通用机制和 Result Schema 归 DV Common；
- 产品专用 Env、scoreboard/reference model 留在产品仓；
- 第三方 VIP 必须经过来源/许可证、结构、协议符合性、隔离 PoC、交叉验证和内部发布门禁；
- 暂不自研完整复杂 AXI4/PCIe/USB 等，除非真实项目和维护能力共同触发。

## APB MVP

APB VIP 必须同时具备主动/被动模式、driver、monitor、protocol checker、coverage、negative sequence、RAL adapter/predictor 和标准 Result；以故意违规 DUT/transaction 证明 checker 不会 false green。

## 成熟度与出口

- V1 Draft：结构与 Schema 可校验；V2 Usable：单元/Smoke/负向通过；
- V3 Qualified：真实 IP 复用、交叉检查、覆盖目标和 Evidence 完整；
- V4 Proven：多个项目/工具矩阵长期稳定。当前 APB 只承诺到 V3；
- 发布物固定 VLNV/SemVer、能力矩阵、支持工具、已知限制和许可证。

活动交付见 [`delivery.md`](delivery.md)，完整 VIP 地图、准入流程和测试体系见 [`design-reference.md`](design-reference.md)。
