# vip — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/vip.md`](../archived/architecture/repo-plans/vip.md)。
> 本文件已并入 archived 原文的建设清单（§7）、实现路线图（§13）、首批 TODO List（§17）、测试与 Qualification（§10）、验收场景（§18）与跨仓一致性修订（§20），并追加仓级待办。

## P0 优先

- [ ] `aixsilicon:vip:common` 公共基类（config/transaction policy/日志/结果）
- [ ] Clock/Reset、Ready/Valid 基础组件
- [ ] APB VIP 达 V3 Qualified
- [ ] Generic Memory VIP、Interrupt VIP 达 V2
- [ ] CSR/RAL adapter 与 predictor
- [ ] FuseSoC Core 模板与标准 targets（default/lint/unit_sim/smoke/regression/negative/example/formal/package）
- [ ] 建立最小 CI：Schema→Compile→Smoke→Negative→Report

## P1 首个季度

- [ ] AXI4-Lite、AXI-Stream VIP（Beta）
- [ ] AHB-Lite、UART、SPI/QSPI、I2C、JTAG/DMI（按项目排序）
- [ ] 双仿真器矩阵 + cocotb 交叉验证
- [ ] 接入 UVM Verification Skill（自动发现/装配 VIP）

## P2 两个季度

- [ ] 完整 AXI4（Burst/ID/Outstanding/乱序/窄传输/4KB/exclusive）
- [ ] 功能安全故障注入（Bus/Interrupt/ECC/Clock-Reset Fault + Fault Campaign）
- [ ] DMA Traffic / Boot Host / Power State VIP
- [ ] Mutation Test 与质量趋势 Dashboard；首个 Proven 级 VIP

## 仓级待办（本批追加）

- [ ] APB VIP 达 V3 Qualified
- [ ] Clock/Reset、Generic Memory、Interrupt VIP 达 V2
- [ ] AXI4-Lite / AXI-Stream 完成 Beta
- [ ] 双仿真器矩阵 + cocotb 交叉验证；接入 UVM Verification Skill（自动发现/装配 VIP）
- [ ] 出口：主干 VIP 可被真实 IP 复用、Catalog 显示能力/兼容矩阵

## 跨仓治理

- [ ] `common/` 与 dv-common 划界：协议相关留本仓、协议无关机制归 dv-common（R6）
- [ ] `reference/` 治理：OpenTitan/PULP 等只读对拍、不发布、不进 fusesoc 正式发现（A2）
- [ ] VLNV 统一 `aixsilicon:vip:*`（C3）；第三方 VIP 准入流程（来源/许可证/协议审计/交叉验证）落地

## 变更记录

| 日期 | 变更内容 | 作者 |
|------|---------|------|
| 2026-08-13 | 创建 todo.md：P0/P1/P2 建设清单、最小 CI、跨仓治理 | Zoo |
| 2026-08-13 | 本文件并入 archived 原文建设清单、实现路线图、首批 TODO、测试与 Qualification、验收场景与跨仓一致性修订（合并补充）并追加仓级待办（出口：主干 VIP 被真实 IP 复用） | Zoo |

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/vip.md` §7 建设清单、§10 测试与 Qualification、§13 实现路线图、§17 首批 TODO List、§18 验收场景、§20 跨仓一致性修订；仓级待办为本批追加。
