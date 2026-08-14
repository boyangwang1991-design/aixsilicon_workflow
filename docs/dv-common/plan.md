# dv-common — AIXSILICON DV Common Repository 建设规划

> 客观事实基线：2026-08-13（P0 底座完成）。原文细节见 [`../archived/architecture/repo-plans/dv-common.md`](../archived/architecture/repo-plans/dv-common.md)。
> 本文件已并入 archived 原文的完整规划细节：六层组件模型（§5.1）、公共 API 设计（§8）、RAL/CSR 能力（§9）、Clock/Reset/Timeout/Watchdog（§10）、Schema 与证据（§11）、SemVer 与版本治理（§17）。

## 1. 定位与边界

**定位**：组织级、与具体协议和 DUT 无关的验证基础设施库——统一“验证环境怎样表达配置、怎样判断通过、怎样输出证据”。

| 归属本仓 | 不归本仓 |
|---|---|
| 基础类型 / 测试骨架 / 配置 / 日志状态 / 时钟复位 / Timeout-Watchdog | 协议 transaction/driver/monitor/checker → VIP |
| Sequence / RAL-CSR / Scoreboard / Compare / Memory / Coverage 基础 | AXI interface、interrupt contract → HWIF |
| Fault/Test control / 证据 Schema / 工具适配薄层 | CDC FIFO、位宽转换、桥接器 → CBB |
| | 具体 IP reference model → IP；仿真调度 → EDA Flow |

**禁止演变成万能 Base Env**：小型 service/component 按需实例化，组合优于继承，显式 config object。关键判断原则：与协议有关 → VIP；与 DUT 功能有关 → 留 IP/Subsystem/SoC 项目；负责“怎么运行”（大规模回归与 EDA 命令）→ Flow。

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

### 4.1 六层组件模型

| 层 | 名称 | 主要内容 |
|---|---|---|
| L0 | Types & Contracts | 类型、枚举、接口契约、Schema |
| L1 | Utilities | queue、ID、random、string、CRC、mask、统计工具 |
| L2 | Runtime Services | log、status、timeout、objection、config、manifest |
| L3 | Reusable Components | clk/rst、scoreboard、memory、coverage、fault control |
| L4 | UVM Framework | base test/env contract、sequence、RAL 服务、virtual sequencer |
| L5 | Integration Adapters | FuseSoC target、Flow 结果适配、Skill 模板、示例环境 |

依赖只能从上层指向下层；L0/L1 尽量避免 UVM 依赖，使部分工具可用于非 UVM 测试台。单向依赖规则：`UVM/simulator abstraction → dv_common_types → utility+service+policy → optional aggregate core → VIP/IP Env/SoC Env`。禁止 `dv-common → axi-vip`、`dv-common → concrete IP RAL model`、`dv-common → soc_top_pkg`、`dv-common → project test`、底层反向依赖聚合 package。

### 4.2 公共 API 设计规范

- **最小 Base Test**（`dv_base_test`）：创建/获取强类型 run config；安装 status/failure/timeout/manifest 服务；统一 test start/end；收集最终结果；不实例化任何具体 VIP、不假设 DUT 寄存器模型、不写项目专用 vseq 选择逻辑。
- **Service 生命周期**：`configure → start → reset_notify → quiesce → drain → finalize`；每个 service 声明是否 reset-aware、是否需 drain、是否产生最终 metric、是否影响 pass/fail、thread ownership、销毁与重复启动语义。
- **Reset Epoch**：reset assert 时 epoch 递增；transaction 记录所属 epoch；scoreboard 默认禁止跨 epoch 匹配；outstanding 按 policy flush/error/preserve；coverage 可按 epoch 分组。
- **Scoreboard API**：`write_actual/write_expected/match/flush(reason)/drain(timeout)/get_pending_count/get_statistics` + matcher/compare policy 插槽；业务层提供 transaction key、compare policy、reference model 调用、reset/错误响应的业务预期。
- **Compare Policy**：至少支持 exact、field mask、byte enable、X/Z policy、integer tolerance、float absolute/relative/ULP tolerance、unordered collection、ignored metadata、自定义 field callback；比较失败必须输出结构化 diff。
- **配置优先级**：`Schema Default < Organization Profile < Project Config < Test Config < CLI Override`，最终值记录来源。
- **Message ID 治理**：格式 `AIX_DV_<DOMAIN>_<EVENT>`（如 `AIX_DV_SB_MISMATCH`、`AIX_DV_TIMEOUT_GLOBAL`、`AIX_DV_RESET_EPOCH`），禁止用难以稳定聚类的自由文本作回归 signature。

### 4.3 RAL 与 CSR 公共能力

- 边界：SystemRDL 是寄存器事实源（归所属 IP）；PeakRDL 生成 UVM RAL 模型；DV Common 提供 RAL 基类、公共 sequence、排除/策略对象与连接辅助；VIP 提供具体总线 RAL adapter；IP Env 负责选择 map/adapter/predictor/backdoor 路径。
- **P0 CSR Sequence**：CSR smoke、HW reset value、RW access、bit-bash、access policy 检查、frontdoor/backdoor 一致性、reset 中断访问、非法地址/错误响应（由项目与 VIP 提供行为）、volatile 字段采样、shadowed/lockable 扩展钩子。
- **CSR 排除机制**：不在 sequence 中硬编码寄存器名，统一用 metadata/policy 表达（pattern/tests/reason/requirement_id），排除项必须有 reason，安全/功能安全项目建议绑定 requirement ID。

### 4.4 Clock / Reset / Timeout / Watchdog

- **Clock Generator**：周期/频率、duty cycle、phase offset、start/stop/gate、平滑/立即频率切换策略、jitter 扩展接口、多时钟命名与状态查询、结构化 metric 输出。
- **Reset Generator**：active-high/low、sync/async assertion/deassertion、pulse width、power-on/warm reset、reset during traffic、多 reset 域、reset cause、reset epoch 广播。协议性 assertion 归 HWIF/VIP checker，DV Common 只提供产生、监测与事件服务。
- **Timeout 层级**：Global / Phase / Operation / Progress / Drain；触发时必须先执行诊断 hook（打印 outstanding、scoreboard pending、objection holder、最近 heartbeat 与 reset 状态）再结束测试。

### 4.5 Schema 与证据契约

- **Test Result**：`schema_version + test(name/requirement_ids) + run(id/seed/status/exit_code/start_time/duration_s) + failure(count/primary_signature) + metrics + artifacts`。
- **Run Manifest**：仿真器与版本、UVM 版本/profile、FuseSoC/Edalize 版本、顶层 Core VLNV、所有依赖 Core VLNV 与 Git revision、编译/运行参数归一化摘要、seed 与派生 seed、配置快照及来源、RTL/VIP/DV Common/RAL 版本、容器/OS/toolchain profile、waiver/rule profile、artifact checksum。
- **Failure Signature**：`message_id + component_path_class + transaction_type + normalized_location + root_cause_tag`；动态数值/时间戳/seed/地址不直接进入 signature，作为附加 context。
- **Exit Code**：0 PASS / 1 DUT-Checker 功能失败 / 2 Testbench 基础设施失败 / 3 Compile-Elaboration / 4 Timeout-Deadlock / 5 配置-Schema 错误 / 6 Tool-License-Environment / 7 ABORT / 8 SKIP（是否视为流水线成功由 Flow 决定）。
- 结果 Schema 与 tool_repo 对齐为单一公共契约（C4），确定性实现归 `aixsilicon_tool_repo`。

### 4.6 SemVer 与版本治理

| 变更 | 版本 |
|---|---|
| 新增可选组件/方法，默认行为不变 | Minor |
| 修复 bug，不改变合法用户行为 | Patch |
| 删除/改名公共类、方法、字段；默认 compare/reset/timeout 语义变化；结果 Schema 删除/改变必选字段 | Major |
| 结果 Schema 新增可选字段 | Minor |
| 新增仿真器兼容修复 | Patch 或 Minor，视 API 而定 |

API 稳定性：`public / protected extension / internal` 三级，仅 public 进入兼容承诺；field macro、factory override、config key 也属于 API。Deprecated 流程：Minor 标记 → 提供替代 API 与迁移文档 → 至少保留一个稳定发布周期 → Major 删除 → Catalog 记录影响范围 → Skill 模板先迁移。

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

### 5.1 首批穿刺场景

- **场景 A：APB 寄存器 IP**——`SystemRDL → PeakRDL RAL → APB VIP → CSR sequence → Scoreboard/Status → Result/Manifest`，覆盖 Clock/Reset、RAL adapter/predictor、CSR smoke/reset/rw/bit-bash、timeout/非法配置 negative test、requirement ID 绑定、FuseSoC Release。
- **场景 B：X2X/AXI Bridge**——多 outstanding、乱序匹配、32～1024bit 宽度、reset during traffic、backpressure、多 Clock/异步、latency/throughput metric、scoreboard drain 与 pending 诊断。
- **场景 C：PIC 功能安全中断控制器**——pulse/level interrupt、interrupt record/clear、fault request/activation/observation、stuck/lost/duplicate 注入、reset epoch、Safety mechanism 响应时延、requirement/fault ID/test evidence 绑定。

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/dv-common.md`](../archived/architecture/repo-plans/dv-common.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/dv-common.md` §5.1 六层组件模型、§8 公共 API、§9 RAL/CSR、§10 Clock/Reset/Timeout、§11 Schema 与证据、§17 版本治理、§20 穿刺场景与 §28 跨仓一致性修订（2026-08-13）。
