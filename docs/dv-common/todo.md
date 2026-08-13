# dv-common — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/dv-common.md`](../archived/architecture/repo-plans/dv-common.md)。

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

## 跨仓治理

- [ ] 与 VIP `common/` 划界：协议无关机制收敛到本仓（R6）
- [ ] 修正 ghost repo 引用（eda-flow/eda-rules/hw-models → workflow/tool/techlib，A3）
- [ ] 依赖方向：本仓不得反向依赖 VIP 与具体 IP（C5）

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
