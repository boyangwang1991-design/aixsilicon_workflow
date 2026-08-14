# hwif — AIXSILICON HW Interface Repository 建设规划

> 客观事实基线：2026-08-13（57 接口族建成）。原文细节见 [`../archived/architecture/repo-plans/hwif.md`](../archived/architecture/repo-plans/hwif.md)。
> 本文件已并入 archived 原文的完整规划细节：三视图策略（§6）、L0–L6 接口清单（§7.1–7.7）、SemVer 契约（§16）、质量 Gate 与成熟度（§17）、27 章规划索引。

## 1. 定位与边界

**定位**：IP、CBB、VIP 与 SoC Integration 之间**统一、可版本化、可机器读取的硬件接口契约中心**（YAML 语义契约 SSOT + 多种确定性派生视图）。

| 归属本仓 | 不归本仓 |
|---|---|
| Interface YAML Contract / Profile / Binding / Compatibility | 协议 Driver/Monitor/Sequence → VIP |
| SV package/interface/modport/flat wrapper | 协议 SVA/Checker → VIP |
| Clock/Reset/Power/CDC 属性、Capability | 桥/同步器/位宽转换 → CBB |
| 可选 IP-XACT 交换视图（派生） | SoC 实例连接、地址/中断分配 → SoC Integration |
| FuseSoC Core | CSR 寄存器定义 → 所属 IP SystemRDL |

边界判断原则：描述“有哪些信号、角色、语义、约束”→ 本仓；描述“如何驱动/监测/检查”→ VIP；描述“如何转换/缓存/同步/桥接”→ CBB；描述“哪个实例连哪个”→ SoC Integration；描述“寄存器地址和字段”→ SystemRDL；描述“工艺 Macro 如何实现”→ Techlib。

## 2. 现状（客观）

- **57 接口族（L0–L6）全部建成**：Contract + RTL + `.core`；
- **工具链 6 项**落地：contract_validate / sv_consistency_check / view_generate / compatibility_check / impact_analysis / package_release；
- **测试 5 组**：schema（4/4）、compile（107 文件）、structural（7/7）、compatibility（4/4）、consumer（61/61）；
- **生成物**：56 个 SV 视图 + 56 View C flat wrapper + 112 IP-XACT XML + 56 spec + catalog/lockfile；
- **缺口**：Techlib binding；正式 IP/VIP/SoCGen 消费证据待验证；`tools/` 产品级工具待迁 tool_repo（R1）；VLNV 迁移窗口。

## 3. 依赖与角色

- **依赖**：无（依赖 DAG 底座）；
- **被依赖**：cbb、ip、vip、soc-integration；
- **IP 主线角色**：`hwif.compatibility-check` 阶段消费契约；多视图由生成器确定性派生；
- **SoC 主线角色**：为 SoC 实例提供接口契约与视图。

## 4. 契约

- **VLNV**：`aixsilicon:interface:*`（存量 `aix:interface:*` 走 deprecated 迁移窗口）；
- **Schema 所有权**：`interface-contract / profile / binding / compatibility`；
- **成熟度**：draft/reviewed/qualified/proven/deprecated（`reviewed`→`qualified` 前身）；
- **三视图**：Packed Struct（RTL 首选）/ SV Interface（VIP/TB）/ Flattened Ports（交付边界），一致性由工具校验。

### 4.1 三视图策略

SV `interface` 适合 UVM virtual interface、TB 连接、局部层级与快速原型；但作为所有可综合 IP 的唯一交付边界会遇到综合/Lint/CDC/DFT/形式工具支持差异、IP-XACT/网表偏好扁平端口等限制，因此采用三视图并存：

| 视图 | 用途 | 命名/示例 |
|---|---|---|
| View A：Packed Struct | 内部 RTL 首选，类型安全、便于参数化与 SoCGen | `aix_<if>_req_t` / `aix_<if>_rsp_t`（如 `aix_stream_req_t`） |
| View B：SV Interface/Modport | VIP、TB、局部封装；SVA 由对应 VIP Core 依赖本接口 Core 后提供 | `aix_<if>_if` + modport `source/sink/monitor` |
| View C：Flattened Ports | IP 正式交付边界、Verilog/VHDL 混合、DFT/CDC/网表、第三方 IP/Pad/Macro | `<instance_prefix>_<channel>_<signal>_<direction>`（如 `s_axi_aw_valid_i`） |

命名规范要点：package `aix_<interface>_pkg`；interface `aix_<interface>_if`；类型 `<interface>_req_t` / `<interface>_rsp_t`；clock `clk_i`；active-low reset `rst_ni`；普通输入/输出 `*_i` / `*_o`；双向物理接口拆成 `*_i` / `*_o` / `*_oe_o`（避免内部 RTL 直接 inout）；宽度参数无歧义（`AddrWidth`/`DataWidth`/`IdWidth`）。内部契约角色统一使用 `initiator/target`；端口前缀可为兼容业界保留 `m_`/`s_` 别名，但必须在 metadata 中声明 alias，不把别名当成新接口类型。

### 4.2 SemVer 契约

| 版本变化 | 典型变更 |
|---|---|
| Major | 删除/重命名必选信号；改变方向、握手、reset 或错误语义；改变 struct layout；默认行为破坏性变化 |
| Minor | 新增向后兼容的可选 Capability/Profile；新增派生视图；扩大合法参数范围 |
| Patch | 文档修正；生成器修复且不改变公开 HDL API/语义；测试和 CI 修复 |

须慎重（通常至少升 Minor）：新增 packed struct 字段（即使可选也改变 type width）、修改枚举编码、改变参数默认值/tie-off 值/clock-reset-power 属性、将可选能力变必选。SV 类型演进限制：不假设“末尾加字段”二进制兼容；生成器必须输出 type fingerprint；SoC Lockfile 记录 fingerprint 防止同名异构类型进入同一工程。

Deprecated 流程：标记 `deprecated_since` → 提供替代 Interface/Profile → 提供 Migration Guide 与必要 Adapter → 至少保留两个 Release 周期 → Catalog 默认不推荐但历史 SoC 仍可解析 → 删除仅限 Major 版本或新 Catalog 大版本。

### 4.3 质量 Gate 与成熟度判定

成熟度状态：

| 状态 | 含义 | 使用限制 |
|---|---|---|
| draft | 需求和语义讨论中 | 禁止项目依赖 |
| reviewed | 架构/协议评审完成 | 允许 PoC |
| qualified | 结构、工具、消费者测试通过 | 允许正式项目使用 |
| proven | 至少两个真实项目验证 | Catalog 默认推荐 |
| deprecated | 已有替代方案 | 禁止新项目使用 |

发布 Gate：

| Gate | 检查内容 | 证据 |
|---|---|---|
| G0 Contract | YAML Schema、稳定 ID、规范引用、Owner 完整 | Schema Report |
| G1 Semantic | role/channel/signal/clock/reset/power/能力评审 | Review Record |
| G2 HDL | package/interface/flat view 编译和一致性 | Compile/Consistency Report |
| G3 Roundtrip | struct↔interface↔flat 无信息丢失 | Roundtrip Report |
| G4 Consumer | 至少一个 IP、一个 VIP 和一个 SoCGen 示例消费 | Consumer Evidence |
| G5 Compatibility | 正向/负向/需 adapter 用例判定正确 | Compatibility Report |
| G6 Release | SemVer、Manifest、SBOM、hash、Catalog 更新 | Release Manifest |

测试类型：Schema 正/负向、参数边界与非法组合、SV 多工具编译、struct pack/unpack roundtrip、flat wrapper roundtrip、modport 方向检查、width 表达式求值、tie-off/default 生成检查、Compatibility rule 单测、旧版本 Migration、IP/VIP/SoCGen 消费者、Catalog 安装与离线构建。Qualified 需至少两种商业工具（VCS/Xcelium/Questa）之一组合验证；Verilator 仅作基础 package/struct 兼容检查，不因开源工具对完整 SV interface 支持有限而降低正式接口语义。

## 5. 建设路线（客观）

| 阶段 | 状态 |
|---|---|
| 0 立项与边界冻结 | ✅ 完成 |
| 1 公共底座（common_types/clock/reset/ready_valid/…） | ✅ 完成 |
| 2 SoC 基础接口（interrupt/error_report/reg_native/memory/fifo） | ✅ 完成 |
| 3 AMBA 与数据通路（apb/axi_lite/axi/axi_stream/credit_link） | ✅ 完成 |
| 4 外设、安全与系统接口（uart/spi/i2c/gpio/jtag/power/…） | ✅ 完成（Techlib binding 待办） |
| 5 Catalog/SoCGen/Skill 闭环 | 🔶 部分（Checker/Impact/Catalog/lockfile 完成；Skill 闭环待办） |
| 6 项目验证与运营 | ⬜ 未开始 |

### 5.1 接口建设清单（L0–L6）

**L0 基础语义接口**：`common_types`(P0)、`clock`(P0)、`reset`(P0)、`ready_valid`(P0)、`req_ack`(P0)、`event`(P0)、`status_control`(P1)。

**L1 SoC 公共控制接口**：`interrupt`(P0)、`error_report`(P0)、`alert`(P1)、`clock_control`(P1)、`reset_control`(P1)、`power_state`(P1)、`isolation`(P1)、`retention`(P2)、`lifecycle_state`(P2)。

**L2 存储与寄存器接口**：`reg_native`(P0)、`memory_1rw`(P0)、`memory_1r1w`(P0)、`memory_tdp`(P1)、`rom`(P1)、`fifo_push_pop`(P0)、`ecc_memory_sideband`(P1)、`cache_maintenance`(P2)。注：SRAM Macro 具体 pin/时序属 `hw-techlib`，本仓提供逻辑抽象接口。

**L3 片上总线与流接口**：`apb`(P0，APB4/APB5 独立 Profile)、`axi_lite`(P0，AXI4-Lite 基础 Profile)、`axi`(P0/P1，AXI4 基础 Profile，ATOP/独占/USER 作 Capability)、`axi_stream`(P0，Basic/Packet/Metadata Profile)、`ahb_lite`(P1)、`obi`(P1)、`tilelink_ul`(P2)、`credit_link`(P0)、`noc_flit`(P1)、`packet_stream`(P0)。AMBA 接口必须记录采用的规范文档标识与 Profile，不能只写“AXI”；本仓描述端点契约，不描述 Crossbar 拓扑。

**L4 外设与芯片边界接口**：`uart_pin`(P1)、`spi`(P1)、`i2c`(P1)、`gpio`(P1)、`jtag`(P1)、`riscv_dmi`(P1)、`pwm`(P2)、`pad_control`(P1)、`pll_control`(P2)。仅定义数字侧接口契约；模拟电气指标、Pad 模型与 PLL 行为模型进入工艺/AMS 相关资产库。

**L5 调试、测试、可观测性**：`trace_stream`(P1)、`performance_event`(P1)、`debug_request`(P2)、`scan_control`(P2)、`mbist_control`(P1)、`lbist_control`(P2)、`dfx_override`(P2)。

**L6 功能安全与安全扩展**：`integrity_sideband`(P1)、`safety_event`(P0)、`fault_injection_control`(P1)、`lockstep_compare`(P1)、`watchdog_service`(P1)、`domain_health`(P1)、`security_violation`(P2)。这些接口与 SafeSight、FUSA Skill Suite、PIC 和 SoCGen 保持 ID 一致，但不在接口仓实现安全机制本体。

### 5.2 27 章完整规划索引

archived 原文 `plan.md`（V1.0，2026-08-12）共 27 章 + 跨仓一致性修订，全文细节见 [`../archived/architecture/repo-plans/hwif.md`](../archived/architecture/repo-plans/hwif.md)：

1. 建设结论（接口契约中心定位与 Monorepo+Core+YAML SSOT 形态）
2. 为什么必须独立建设（散落定义导致的类型/语义/版本不一致）
3. 仓库边界（归属/不归属清单与边界判断原则）
4. 与完整硬件资产体系的关系（IFC→IP/CBB/VIP/SOC/CAT 依赖 DAG）
5. 总体技术架构（L0 Identity/L1 Semantic/L2 Configuration/L3 Realization 四层契约模型，事实与派生物）
6. HDL 表达策略（三视图并存，见 §4.1）
7. 接口分类与完整建设清单（L0–L6，见 §5.1）
8. 推荐仓库结构（schema/common/foundation/system/memory/bus/link/peripheral/dft_debug/safety_security/profiles/bindings/generated/examples/tests/tools）
9. 单个接口族标准模板（contract/rtl/binding/docs/tests/metadata/.core）
10. YAML Interface Contract 设计（稳定 ID、受限宽度表达式、from/to role、capability 分离、按族拆分）
11. 统一命名与语义规范（角色统一、RTL 命名、Reset 语义、CDC/Power 属性）
12. 参数、Capability 与 Profile 治理（Profile > Parameter > Capability > 工具宏）
13. 接口兼容性模型（Protocol/Profile/Binding 三层；DIRECT/ADAPTER_REQUIRED/INCOMPATIBLE；SoCGen 集成前检查）
14. FuseSoC 组织方式（每接口族独立 Core + target 规范 + Core 示例）
15. IP/CBB/VIP/SoC 如何声明接口（IP metadata/VIP binding/CBB adapter 声明）
16. 版本与变更治理（SemVer 规则，见 §4.2）
17. 质量 Gate 与验证体系（成熟度 + G0–G6，见 §4.3）
18. CI/CD 与自动发布（PR/Nightly/Release；发布包含 Manifest/SBOM/hash）
19. Catalog 模型（asset/protocol/profiles/views/compatibility/quality/evidence）
20. IP-XACT 定位（派生交换视图，不取代 YAML SSOT）
21. 开源参考项目与采用建议（PULP AXI/Register Interface/common_cells/OpenTitan/OpenHW OBI/Arm AMBA）
22. 实施路线图（阶段 0–6）
23. 人力与周期建议（最小 3 人 / 推荐 4–5 人 / 平台 6–8 人）
24. 首批穿刺场景（APB 寄存器 IP / X2X AXI Bridge / PIC 功能安全中断系统）
25. 首批 TODO List（P0/P1/P2）
26. 一期验收标准（YAML SSOT、三视图一致、FuseSoC 稳定、Compatibility Checker 等）
27. 最终推荐（接口类型系统/契约系统/兼容性判断系统；三条架构纪律）
28. 跨仓一致性修订（2026-08-13）：`tools/` 产品级工具迁 `aixsilicon_tool_repo`（R1/ADR-0006）；`impact_analysis`/`package_release` 与 workflow 语义区分（R5/R4）；`reference/` 不发布不进 Catalog（A2）；`hw-techlib` → 待建 `aixsilicon_techlib_repo`（A4）；VLNV 统一 `aixsilicon:interface:*`（ADR-0003）

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/hwif.md`](../archived/architecture/repo-plans/hwif.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/hwif.md` §6 三视图、§7.1–7.7 接口清单、§16 SemVer、§17 Gate、§1–§27 章节索引与 §28 跨仓一致性修订（2026-08-13）。
