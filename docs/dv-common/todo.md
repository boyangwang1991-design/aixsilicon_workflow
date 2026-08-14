# dv-common — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/dv-common.md`](../archived/architecture/repo-plans/dv-common.md)。
> 本文件已并入 archived 原文的阶段 0–6 路线（§21）、P0 已完成明细（TODO 原文）、跨仓一致性修订（§28）与变更记录。

## P0 优先

- [ ] RAL base 与 CSR sequence 正式行为（smoke/reset/rw/bit-bash）
- [ ] PeakRDL UVM RAL 输出链接入
- [ ] APB 寄存器 IP 示例（`examples/apb_csr_ip`）全链路可运行
- [ ] 发布首个 Candidate + Catalog 接入
- [ ] 冻结 result/manifest/failure Schema V0.1（与 tool_repo 对齐，C4）

## P1 首个季度

- [ ] in-order scoreboard 业务装配（matcher/flush/drain/pending）
- [ ] memory mirror / backdoor contract 完整化
- [ ] UVM Verification Skill 改为消费公共组件
- [ ] CI 三段接入（PR/Nightly/Release，可挂 `tools/run_checks.sh`）

## P1/P2 两个季度

- [ ] out-of-order matcher、reset epoch 与跨 reset 策略
- [ ] latency/outstanding 统计
- [ ] AXI/X2X 穿刺（`examples/axi_bridge`）
- [ ] interrupt/fault control 正式行为；PIC 功能安全穿刺
- [ ] 多仿真器完整 Release 矩阵；性能 benchmark 与回退 Gate
- [ ] `compat/` UVM 双 profile 薄层；`docs/migration/` 迁移指南
- [ ] SBOM 与 license 治理落地

## 已完成（P0 公共底座）

- [x] 仓库框架骨架（根文件 + 8 个 FuseSoC Core 解析通过）
- [x] L0–L4 六层骨架（types/utils/runtime/components/uvm-ral）+ rtl/dpi 骨架 + schemas(6)/metadata(4) + 目录骨架
- [x] 非 UVM 单测 12/12（VCS `-full64`）；minimal UVM example 全链路 PASS；rtl_smoke PASS
- [x] 修复 `dv_config_pkg` 布尔 plusarg、`dv_compare_pkg` wildcard/结构化 diff、Message ID 格式
- [x] tools 工具层（schema_check/dep_check/api_diff/result_check/doc_gen + run_checks.sh ALL CHECKS PASSED）
- [x] `docs/api/` 34 份 API 文档生成

## 阶段路线（0–6）

| 阶段 | 目标 | 状态 |
|---|---|---|
| 0 立项与边界冻结 | 边界/UVM/tool profile/穿刺 DUT | ✅ 完成 |
| 1 仓库与 L0/L1 底座 | types/utils/schema/minimal example | ✅ 完成 |
| 2 运行时服务 | log/status/failure/timeout/reset/config/manifest + clk/rst | ✅ 完成 |
| 3 RAL 与 APB 穿刺 | RAL base + CSR seq + PeakRDL + APB 示例 | 🔶 进行中 |
| 4 Scoreboard 与 Memory | matcher/compare/memory + AXI bridge | ⬜ |
| 5 SoC 与功能安全 | interrupt/fault/coverage + PIC | ⬜ |
| 6 Catalog/Skill/规模化 | Catalog + Skill 消费 + 多项目 | ⬜ |

## 跨仓治理

- [ ] 与 VIP `common/` 划界：协议无关机制收敛到本仓（R6）
- [ ] 修正 ghost repo 引用（eda-flow/eda-rules/hw-models → workflow/tool/techlib，A3）
- [ ] 依赖方向：本仓不得反向依赖 VIP 与具体 IP（C5）
- [ ] Result/Manifest/Failure Schema 与 tool_repo 对齐为单一公共契约（C4）

## 变更记录

| 日期 | 变更内容 | 作者 |
|------|---------|------|
| 2026-08-12 | 建立仓库骨架、8 个 FuseSoC Core、L0–L4 六层骨架、schemas/metadata、VCS 编译/细化验证 | Zoo |
| 2026-08-13 | P0 公共底座实现：12/12 单测 + minimal UVM + rtl_smoke + tools 工具层 + docs/api 34 份 | Zoo |
| 2026-08-13 | 本文件并入 archived 原文阶段 0–6 路线、P0 已完成明细、跨仓一致性修订（合并补充） | Zoo |

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/dv-common.md`（TODO 原文）§21 实施路线图、P0 公共底座实现清单、跨仓一致性修订（2026-08-13）。
