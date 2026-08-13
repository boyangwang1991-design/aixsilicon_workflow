# hwif — AIXSILICON HW Interface Repository 建设规划

> 客观事实基线：2026-08-13（57 接口族建成）。原文细节见 [`../archived/architecture/repo-plans/hwif.md`](../archived/architecture/repo-plans/hwif.md)。

## 1. 定位与边界

**定位**：IP、CBB、VIP 与 SoC Integration 之间**统一、可版本化、可机器读取的硬件接口契约中心**（YAML 语义契约 SSOT + 多种确定性派生视图）。

| 归属本仓 | 不归本仓 |
|---|---|
| Interface YAML Contract / Profile / Binding / Compatibility | 协议 Driver/Monitor/Sequence → VIP |
| SV package/interface/modport/flat wrapper | 协议 SVA/Checker → VIP |
| Clock/Reset/Power/CDC 属性、Capability | 桥/同步器/位宽转换 → CBB |
| 可选 IP-XACT 交换视图（派生） | SoC 实例连接、地址/中断分配 → SoC Integration |
| FuseSoC Core | CSR 寄存器定义 → 所属 IP SystemRDL |

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

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/hwif.md`](../archived/architecture/repo-plans/hwif.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
