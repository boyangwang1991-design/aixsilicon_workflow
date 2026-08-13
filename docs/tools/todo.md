# tools — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/tools.md`](../archived/architecture/repo-plans/tools.md)。

## 已完成（P0 五包）

- [x] `aix-tool-core`：Result/Diagnostic/Artifact 契约、分段退出码、`aixsilicon.commands` 插件入口
- [x] `aix-schema`：validate / lint / diff（含负向测试）
- [x] `aix-hwif-gen`：Contract→SV 多视图、`--check-only`、`hac-generate`
- [x] `aix-reg-tool`：PeakRDL validate / generate（RTL/RAL/Header/Doc）、一致性 check
- [x] `aix-core-tool`：core list / lint / init / graph
- [x] 五包注册进 `aixsilicon.commands` `tool` 插件并实跑；`make check` 全绿（30 用例）

## S5 集成收尾（当前）

- [ ] `aix wf run ip-verification` / `apb-register-ip` 的 `tool.*` 阶段转真实 provider
- [ ] workspace-lock `tools:` 段记录本仓包版本（工具版本锁）
- [ ] `reference/`（fusesoc/edalize/peakrdl/verible/surelog/yosys 等）适配测试
- [ ] `aix-schema migrate` 骨架补全（显式版本迁移）

## P1 扩展（首个季度）

- [ ] `aix-project-init`：工程骨架初始化
- [ ] `aix-param-matrix`：参数空间 / 组合矩阵
- [ ] `aix-dv-gen`：UV M 验证派生（testlist/vip-bind/ral-bind/run-manifest/result）
- [ ] `aix-ppa-bench`：PPA 表征 / pareto
- [ ] `aix-socgen` / `aix-connect-check`：SoC 生成与集成检查
- [ ] `aix-catalog-tool`：Catalog 检查与更新草案

## P2 规模化

- [ ] `aix-report`（EDA 报告归一化）、`aix-rtm`（需求追踪/证据）、`aix-package`（交付打包）、`aix-catalog-patch`
- [ ] Golden Test 策略 + 真实穿刺（APB / CBB / SoC）
- [ ] 商业 EDA 私有 Adapter 接入规范

## 跨仓治理

- [ ] hwif 六件工具与本仓 `aix-hwif-gen` 等分阶段合并（R1）
- [ ] ipkg 复用 `aix-core-tool`（R7）
- [ ] 统一退出码与 `aixworkflow.errors` 保持一致（分段映射）

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
