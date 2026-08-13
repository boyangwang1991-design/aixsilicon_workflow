# vip — AIXSILICON VIP Repository 建设规划

> 客观事实基线：2026-08-13（规划为主，目录/文档骨架）。原文细节见 [`../archived/architecture/repo-plans/vip.md`](../archived/architecture/repo-plans/vip.md)。

## 1. 定位与边界

**定位**：可版本化、可组合、可验证、可发布的验证资产平台——**一个 VIP Monorepo + 每个 VIP 独立 FuseSoC Core + 统一公共基类 + 统一 Release Catalog 索引**。

**六层组件**：Interface（虚接口/clocking/modport）/ Transaction（事务/约束/compare）/ Agent（sequencer/driver/monitor/responder）/ Service（memory/RAL/interrupt/fault）/ Checking（checker/scoreboard/SVA/coverage）/ Packaging（core/metadata/测试/文档）。

| 归属本仓 | 不归本仓 |
|---|---|
| 协议 Agent、Transaction、BFM、Monitor、Checker、Coverage、Sequence | 通用 UVM 基类/Scoreboard 框架 → dv-common |
| 协议 SVA / Protocol Checker | SV interface/typedef/modport 语义 → hwif |
| RAL adapter / predictory | 项目专用 Env/Testcase → IP/SoC 项目 |
| 商业 VIP adapter（受控） | CSR 定义 → IP SystemRDL |

## 2. 现状（客观）

- 目录/文档骨架就绪：protocol/peripheral/system/safety/adapters/formal/schema/docs；
- **缺口**：无正式 VIP 落地（规划为主）；`common/` 与 dv-common 边界需对齐（R6）。

## 3. 依赖与角色

- **依赖**：`[hwif, dv-common]`；
- **被依赖**：ip 验证、soc-integration 系统验证；
- **IP 主线角色**：`vip-development` 维护验证组件；IP 验证环境消费 VIP Agent/Checker/Coverage；
- **SoC 主线角色**：SoC 级系统验证（boot smoke、系统抽查）复用 VIP。

## 4. 契约

- **VLNV**：`aixsilicon:vip:*`（存量 `aix:vip:*` 走迁移窗口）；
- **Schema 所有权**：`vip-metadata / testplan / coverage / release-manifest`；
- **成熟度**：V0 Prototype … V4 Proven（V0→draft；V1–V3→qualified；V4→proven）；
- **公共 API**：统一 Agent 模式（ACTIVE_MASTER/ACTIVE_SLAVE/PASSIVE/DISABLED）、统一 analysis port（transaction/request/response/error/performance）、统一能力清单（14 项）。

## 5. 建设路线（客观）

| 阶段 | 目标 | 状态 |
|---|---|---|
| 0 立项与技术选型 | Charter/边界/Schema/开源候选/APB PoC | 🔶 骨架就绪，实现待做 |
| 1 公共底座 | vip:common + FuseSoC target + Clock/Reset/Ready-Valid | ⬜ |
| 2 APB 与系统基础 VIP | APB/Memory/Interrupt + CSR-RAL adapter | ⬜ |
| 3 AXI4-Lite / AXI-Stream | 协议 check + 交叉验证 + 多仿真器 | ⬜ |
| 4 完整 AXI4 | Burst/ID/Outstanding/乱序/窄传输 | ⬜ |
| 5 外设与 SoC 服务 VIP | UART/SPI/I2C/JTAG/Boot/Power | ⬜ |
| 6 功能安全与规模化 | 故障注入、Fault Campaign、Skill 装配 | ⬜ |

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/vip.md`](../archived/architecture/repo-plans/vip.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
