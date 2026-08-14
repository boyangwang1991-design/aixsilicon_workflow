# vip — AIXSILICON VIP Repository 建设规划

> 客观事实基线：2026-08-13（规划为主，目录/文档骨架）。原文细节见 [`../archived/architecture/repo-plans/vip.md`](../archived/architecture/repo-plans/vip.md)。
> 本文件已并入 archived 原文的完整规划细节：总体架构与六层组件（§3）、VIP 标准模板与 FuseSoC Target 规范（§5）、公共 API 与设计规范（§6）、建设清单（§7）、开源参考（§8）、准入流程（§9）、测试与 Qualification（§10）、验收与出口定义（§18–§19）及跨仓一致性修订（§20）。

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

### 5.1 建设清单与优先级（P0/P1/P2）

**P0 最小可用闭环**：VIP Common（公共配置/transaction policy/日志/结果）、Clock/Reset、Ready/Valid、APB、AXI4-Lite、Generic Memory、Interrupt —— 防止各 VIP 重复造轮子。

**P1 IP 与 SoC 主干协议**：AXI4（Burst/ID/Outstanding/乱序/窄传输/4KB/exclusive）、AXI-Stream（TLAST/TKEEP/TID/TDEST/backpressure）、AHB-Lite、UART、SPI/QSPI、I2C、JTAG/DMI、CSR Access Service（frontdoor/backdoor/mirror/RAL predictor）。

**P2 系统与功能安全**：DMA Traffic、Boot Host、Power State、ECC/Parity Fault、Bus Fault、Interrupt Fault、Fault Campaign（Fault ID/注入窗口/预期机制/覆盖与证据）。

**暂不建议自研**：PCIe/CXL、DDR/LPDDR、USB、MIPI、完整 Ethernet/TSN、CHI/ACE —— 协议复杂、标准版本多、合规测试成本高，第一阶段采用商业 VIP 或受控合作资产，内部只提供统一 adapter/traffic abstraction/结果接口。

### 5.2 开源 VIP 与参考项目（调研结论）

| 项目 | 参考内容 | 采用等级 |
|---|---|---|
| Accellera UVM Core | IEEE 1800.2 UVM 参考实现 | A |
| OpenTitan `hw/dv/sv` | CIP Base、TL/UART/SPI/I2C/JTAG Agent、push-pull、CSR utilities 与 DV 方法 | A |
| TVIP-AXI / TVIP-APB | AXI4(-Lite)/APB UVM VIP、RAL adapter/predictor | A- / B+ |
| PULP common_verification | clk/reset、timeout、ready/valid master/slave | A- |
| PULP AXI / CORE-V-VERIF / riscv-dv | AXI 对拍 DUT、SoC/CPU 环境分层、RISC-V 指令生成 | A- |
| cocotbext-axi | AXI/AXI-Lite/AXI-Stream/APB Python BFM 与 Memory Model | A- |
| ZipCPU wb2axip / Accellera OVL | 协议形式属性、通用 Assertion Checker | B+ |
| PULP uvm-components | 历史 UVM 组件与 FuseSoC 打包示例（2025-11-28 归档） | C |

采用等级：A 优先评估 / A- 高价值需适配重构或许可证审计 / B+ 局部能力与交叉验证 / C 仅历史参考。第三方来源只作对拍与参考，不直接整仓复制；`vendor/` 只保存 Manifest/锁定 commit/许可证/补丁/SBOM（A2）。

### 5.3 第三方 VIP 准入流程（G0–G5）

`候选发现 → 许可证/SBOM → 协议与代码审计 → 隔离 PoC → 双模型交叉验证 → 内部 Qualification → 正式发布`：

- **G0 来源与许可证**：记录仓库 URL/commit/tag/作者/许可证/NOTICE；生成 SBOM；GPL/AGPL/未知/仅限非商业默认不进入正式库；
- **G1 代码结构审计**：是否真正可复用 VIP（非单 DUT Testbench）、是否支持 Master/Slave/Passive、无全局变量/硬编码层次/私有语法、有可运行测试与文档；
- **G2 协议符合性审计**：协议条款—Requirement—Test—Coverage 映射，独立检查 driver 与 monitor，未覆盖功能在 compatibility metadata 中声明；
- **G3 隔离 PoC**：最小 Master—Slave loopback、至少两个独立 DUT、两个仿真器、注入已知错误确认 Checker 报错、固定种子可复现；
- **G4 交叉验证**：内部 UVM Master ↔ cocotbext/PULP 参考、TVIP ↔ 内部、SVA ↔ mutation DUT，条件允许时商业 VIP ↔ 内部；
- **G5 内部重构与发布**：适配统一 interface/config/analysis port/coverage API，形成 FuseSoC Core，补齐文档，通过 Qualification 后发布内部 VLNV，不隐去第三方版权。

### 5.4 测试、Qualification 与验收出口

**质量 Gate（V0–V4）**：V0 Prototype（单仿真器编译、禁正式项目依赖）→ V1 Alpha（Master/Slave/Passive 基本完成、单测通过）→ V2 Beta（两个 DUT、两个仿真器、基础 coverage/negative 通过）→ V3 Qualified（RTM 闭环、协议覆盖达标、mutation 通过、文档齐全）→ V4 Proven（至少两项目使用并闭环、兼容矩阵稳定）。正式 Catalog 默认只显示 Qualified 与 Proven。

**验收场景（三个穿刺对象）**：① APB 寄存器型 IP（APB/RAL/Interrupt/Clock-Reset 闭环）；② AXI/AXI-Lite 桥或 X2X 类 IP（Outstanding/位宽/异步/backpressure/error/reset）；③ PIC 或功能安全中断模块（Interrupt VIP/故障注入/Safety Checker/Fault Campaign）。

**最终出口定义**：P0 VIP 具稳定 VLNV 与 FuseSoC 依赖；APB/AXI4-Lite 等至少一个主干 VIP 达 Qualified；至少两个真实项目复用；来源/许可证/修改/SBOM 可追踪；Requirement/Test/Coverage/Evidence 闭环；多仿真器兼容；Catalog 可查能力/版本/质量/兼容；UVM Verification Skill 可自动发现并装配 VIP。

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/vip.md`](../archived/architecture/repo-plans/vip.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/vip.md` §3 总体架构（六层组件）、§5 FuseSoC Target 规范、§6 公共 API 与设计规范、§7 建设清单与优先级、§8 开源参考、§9 准入流程、§10 测试与 Qualification、§18 验收场景、§19 最终出口定义与 §20 跨仓一致性修订。
