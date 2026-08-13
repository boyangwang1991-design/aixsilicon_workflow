# dv-common — AIXSILICON DV Common Repository 建设规划

> 客观事实基线：2026-08-13（P0 底座完成）。原文细节见 [`../archived/architecture/repo-plans/dv-common.md`](../archived/architecture/repo-plans/dv-common.md)。

## 1. 定位与边界

**定位**：组织级、与具体协议和 DUT 无关的验证基础设施库——统一“验证环境怎样表达配置、怎样判断通过、怎样输出证据”。

| 归属本仓 | 不归本仓 |
|---|---|
| 基础类型 / 测试骨架 / 配置 / 日志状态 / 时钟复位 / Timeout-Watchdog | 协议 transaction/driver/monitor/checker → VIP |
| Sequence / RAL-CSR / Scoreboard / Compare / Memory / Coverage 基础 | AXI interface、interrupt contract → HWIF |
| Fault/Test control / 证据 Schema / 工具适配薄层 | CDC FIFO、位宽转换、桥接器 → CBB |
| | 具体 IP reference model → IP；仿真调度 → EDA Flow |

**禁止演变成万能 Base Env**：小型 service/component 按需实例化，组合优于继承，显式 config object。

## 2. 现状（客观）

- L0–L5 六层组件骨架完成（types/utils/runtime/components/uvm-ral/adapters）；
- **P0 公共底座实现**：非 UVM 单测 12/12、minimal UVM example 全链路、rtl_smoke 通过（VCS `-full64`）；
- **tools 工具层 5 件**：schema_check / dep_check / api_diff / result_check / doc_gen + `run_checks.sh`（ALL CHECKS PASSED）；
- `docs/api/` 34 份 API 文档生成；
- **缺口**：P1 RAL/CSR 正式行为、PeakRDL 接入、APB 穿刺、首个 Candidate、CI 三段。

## 3. 依赖与角色

- **依赖**：无（不反向依赖 VIP/具体 IP/SoC 项目）；
- **被依赖**：vip；
- **IP 主线角色**：为 IP 的 UVM 环境提供公共组件与 result/manifest schema；
- **SoC 主线角色**：为 SoC 级验证提供公共底座。

## 4. 契约

- **VLNV**：`aixsilicon:dv:common_*`（存量 `aix:dv:*` 走迁移窗口）；
- **Schema 所有权**：`dv-run-manifest / test-result / failure / metric`（与 tool_repo 对齐为单一公共契约，C4）；
- **成熟度**：Draft/Experimental/Candidate/Qualified/Deprecated/Retired（Candidate→qualified）；
- **UVM 基线**：双 profile（`uvm12_legacy` / `uvm1800_2`），公共子集 + `compat/` 薄层。

## 5. 建设路线（客观）

| 阶段 | 目标 | 状态 |
|---|---|---|
| 0 立项与边界冻结 | 边界/UVM/tool profile/穿刺 DUT | ✅ 完成 |
| 1 仓库与 L0/L1 底座 | types/utils/schema/minimal example | ✅ 完成 |
| 2 运行时服务 | log/status/failure/timeout/reset/config/manifest + clk/rst | ✅ 完成 |
| 3 RAL 与 APB 穿刺 | RAL base + CSR seq + PeakRDL + APB 示例 | 🔶 进行中 |
| 4 Scoreboard 与 Memory | matcher/compare/memory + AXI bridge | ⬜ |
| 5 SoC 与功能安全 | interrupt/fault/coverage + PIC | ⬜ |
| 6 Catalog/Skill/规模化 | Catalog + Skill 消费 + 多项目 | ⬜ |

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/dv-common.md`](../archived/architecture/repo-plans/dv-common.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
