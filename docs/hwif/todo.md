# hwif — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/hwif.md`](../archived/architecture/repo-plans/hwif.md)。
> 本文件已并入 archived 原文的阶段 0–6 路线（§22）、L0–L6 接口矩阵（§7）、工具链/测试/Gate（§8/§17/§18）、变更记录。

## P0 优先

- [ ] Techlib binding（`aixsilicon_techlib_repo` 待建前以抽象接口承接，A4）
- [ ] 完成 2 个真实消费者（CBB + VIP）依赖其 core 并通过编译
- [ ] VLNV 迁移 `aix:interface:*` → `aixsilicon:interface:*`（deprecated 窗口）
- [ ] `tools/` 产品级确定性工具分阶段迁入 `aixsilicon_tool_repo`（R1 / ADR-0006）

## P1 首个季度

- [ ] G1 Semantic 架构评审（当前待评审）
- [ ] 正式 IP / VIP / SoCGen 真实消费证据（当前仅示例）
- [ ] Skill / SoCGen 消费闭环
- [ ] `reference/` 治理：排除 fusesoc 正式发现、不发布、不进 Catalog（A2）

## P2 两个季度

- [ ] 2 个 IP + 1 个 Subsystem 达到 `proven`
- [ ] 版本迁移与 Deprecated 自动检查
- [ ] 新协议/Profile 准入流程

## 阶段路线（0–6）

| 阶段 | 状态 | 关键出口 |
|---|---|---|
| 0 立项与边界冻结 | ✅ | 架构评审通过，选定穿刺接口与消费者 |
| 1 公共底座 | ✅ | CBB/VIP 依赖公共接口 Core 并通过编译（107 文件编译 + 61/61 consumer 已验证） |
| 2 SoC 基础接口 | ✅ | PIC 或 APB 寄存器 IP 穿刺，接口元数据可被 SoCGen 读取 |
| 3 AMBA 与数据通路 | ✅ | X2X/总线桥三视图与 VIP 自动装配 |
| 4 外设、安全与系统接口 | ✅（Techlib binding 待办） | 至少一个 Subsystem 完整应用接口契约体系 |
| 5 Catalog/SoCGen/Skill 闭环 | 🔶 | Compatibility/Impact/Catalog/lockfile 完成；Skill 闭环与页面待后续 |
| 6 项目验证与运营 | ⬜ | 2 IP + 1 Subsystem 达 `proven`；Deprecated 治理；PPA/工具兼容趋势 |

## L0–L6 接口矩阵（现状）

| 层级 | Interface Core | 状态 |
|---|---|---|
| L0 | common_types / clock / reset / ready_valid / req_ack / event / status_control | ✅ |
| L1 | interrupt / error_report / alert / clock_control / reset_control / power_state / isolation / retention / lifecycle_state | ✅ |
| L2 | reg_native / memory_1rw / memory_1r1w / memory_tdp / rom / fifo_push_pop / ecc_memory_sideband / cache_maintenance | ✅ |
| L3 | apb / axi_lite / axi / axi_stream / ahb_lite / obi / tilelink_ul / credit_link / noc_flit / packet_stream | ✅ |
| L4 | uart / spi / i2c / gpio / jtag_dmi / pwm / pad_control / pll_control | ✅ |
| L5 | trace_stream / performance_event / debug_request / scan_control / mbist_control / lbist_control / dfx_override | ✅ |
| L6 | safety_event / fault_injection_control / integrity_sideband / lockstep_compare / watchdog_service / domain_health / security_violation | ✅ |

Profile 现状：15 个（apb4_base/apb_csr_v1/axi4_base/axi_memory_basic_v1/axi_dma_high_bw_v1/axi_lite_csr/axi_stream_packet/axi_stream_basic_v1/ready_valid_scalar_v1/ready_valid_packet_v1/credit_link_basic/safety_event_v1/interrupt_level_v1/interrupt_pulse_v1/memory_1rw_sync_v1）。

## 工具链 / 测试 / 生成物

- **Schema**（5 件）：`interface_contract` / `interface_profile` / `binding` / `compatibility` / `release_manifest`。
- **工具链**（6 项）：`contract_validate`（全仓契约 schema 校验）、`sv_consistency_check`（SV↔契约一致性 PASS）、`compile_smoke`（拓扑 62 文件 vlogan 通过）、`view_generate`（56 视图 + `--check-only`/`--ipxact`/`--flat`/`--docs`）、`compatibility_check`（三类判定 + Profile 能力协商）、`impact_analysis` + `package_release`（Release 包/Manifest/Quality/catalog/lockfile）。
- **CI**：GitHub Actions（契约 schema 校验 + schema 正/负向 + SV 一致性 + 生成视图最新性 + compatibility + 冒烟编译）。
- **测试**（5 组）：schema（4/4）、compile（107 文件 vlogan）、structural（7/7 roundtrip）、compatibility（4/4）、consumer（61/61）。
- **生成物**（`generated/`，禁止手工修改）：56 SV 视图 + 56 View C flat wrapper + 112 IP-XACT XML + 56 interface spec + catalog 条目 + SoC lockfile。
- **示例与绑定**：APB Target 示例、VIP/IP-XACT/Legacy binding 示例。
- **第三方参考**（`reference/`，plan §21）：参考仓库已拉取并 `.gitignore`、PULP OBI 补齐 RTL 视图、许可证审计报告；OpenTitan DV/TVIP-AXI 建设 VIP 基础库待做。

## 质量 Gate（客观状态）

- G0 Contract ✅ / G1 Semantic ⬜ / G2 HDL ✅ / G3 Roundtrip ✅ / G4 Consumer ✅（示例）/ G5 Compatibility ✅ / G6 Release ✅

## 变更记录

| 日期 | 变更内容 | 作者 |
|------|---------|------|
| 2026-08-13 | 创建 todo.md，参照 plan.md V1.0 重构：阶段路线、L0–L6 矩阵、工具链/测试、P0/P1/P2 TODO、验收标准、质量 Gate | Zoo |
| 2026-08-13 | G0 门禁：`contract_validate` 跑通全仓 42 契约 schema 校验；扩展 schema 支持 apb/ahb 握手与空 channels | Zoo |
| 2026-08-13 | 参考 PULP OBI 补齐 `bus/obi` RTL 视图；整理 `reference/` 至 16 项并补 PULP 参考 | Zoo |
| 2026-08-13 | 补齐 peripheral 族与 `ahb_lite` RTL 视图；补齐剩余缺 RTL 接口（clock_control/power_state/reset_control/trace_stream/mbist_control/fault_injection_control/noc_flit） | Zoo |
| 2026-08-13 | 实现 `sv_consistency_check`、`view_generate`（含 `--check-only`）、`compatibility_check`；建立 tests/schema（4/4）与 CI/拓扑编译脚本 | Zoo |
| 2026-08-13 | 实现 `impact_analysis` 与 `package_release`（plan §8 tools/ 6 项工具全部落地） | Zoo |
| 2026-08-13 | 补齐 L0–L6 全部未建设接口（21 个，contract+rtl+core）；建立 tests/compile(107)/structural(7/7)/consumer(61/61)；扩展 IP-XACT(112)/catalog/lockfile/9 Profile | Zoo |
| 2026-08-13 | view_generate 扩展 Flat Port Wrapper（`--flat`，56 个 View C）与 Interface Spec 文档（`--docs`，56 个）；compatibility_check 增强 Profile 能力协商（4/4） | Zoo |
| 2026-08-13 | 本文件并入 archived 原文阶段路线/L0–L6 矩阵/工具链测试/变更记录（合并补充） | Zoo |

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/hwif.md`（todo 原文）§22 阶段路线、§7 L0–L6 矩阵、§8 Schema/工具链、§17.3 测试体系、§18 CI、§八 变更记录。
