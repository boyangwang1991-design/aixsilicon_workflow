# tools — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/tools.md`](../archived/architecture/repo-plans/tools.md)。
> 本文件已并入 archived 原文的 S0–S5 逐项 TODO（todo 原文 §3）、阶段与包依赖顺序（§2）与变更记录。

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
- [ ] `aix-dv-gen`：UVM 验证派生（testlist/vip-bind/ral-bind/run-manifest/result）
- [ ] `aix-ppa-bench`：PPA 表征 / pareto
- [ ] `aix-socgen` / `aix-connect-check`：SoC 生成与集成检查
- [ ] `aix-catalog-tool`：Catalog 检查与更新草案

## P2 规模化

- [ ] `aix-report`（EDA 报告归一化）、`aix-rtm`（需求追踪/证据）、`aix-package`（交付打包）、`aix-catalog-patch`
- [ ] Golden Test 策略 + 真实穿刺（APB / CBB / SoC）
- [ ] 商业 EDA 私有 Adapter 接入规范

## S0–S5 逐项 TODO（archived 原文明细）

### S0 aix-tool-core（底座）
- [x] Result / Diagnostic / Artifact 契约
- [x] 分段退出码契约（0/10/20/30/40/50/60，与 `aixworkflow.errors` 一致）
- [x] `aixsilicon.commands` 插件入口 `tool`（路由 schema/reg/core/hwif）
- [x] pytest 单测（5 用例：Result 状态机、exit_code、to_dict、插件路由）
- [x] `uv pip install -e` 可安装验证

### S1 aix-schema
- [x] `validate --schema <json> <file>`（YAML/JSON 实例校验）
- [x] `lint --schema <json>`（Schema 自校验）
- [x] `diff <old.json> <new.json>`（兼容性变化摘要）
- [ ] `migrate` 骨架（显式版本迁移，不自动猜测）
- [x] golden/负向测试（5 用例；含 `type: bogus` 负向）
- [x] 通过 `aixsilicon.commands` 的 `aix tool schema` 可调用验证

### S2 aix-hwif-gen
- [x] 读取 `aixsilicon_hwif_repo` 的 Contract YAML（schema 校验，`aix tool hwif validate` 实跑 OK）
- [x] 生成 SV package / interface/modport / flat port wrapper（按角色分型，含 clock/reset + 双角色 modport）
- [x] `--check-only` 生成漂移检测与确定性输出（宽度表达式受限解析器无 eval）
- [x] golden 测试（6 用例；APB 实契约生成 4 视图通过）
- [x] `hac-generate`：HAC-IF 配置 SSOT → 参数包 + 能力位图

### S3 aix-reg-tool
- [x] PeakRDL 封装：`validate`（structural + `--semantic` 走 systemrdl）
- [x] `generate --views rtl,ral,cheader,doc`（未装 peakrdl 时 `OPTIONAL_UNAVAILABLE`，exit 30）
- [x] 一致性检查 `check --rdl --generated`（addrmap 漂移检测）
- [x] golden/负向测试（8 用例；含脚本注入拒绝）

### S4 aix-core-tool
- [x] `core list` / `core lint`（`fusesoc core` 实跑，VLNV 解析）
- [x] `core init`（从 VLNV/version 生成 CAPI2 `.core` 草案，依赖图扫描）
- [x] `core graph`（VLNV 依赖闭包，跳过 reference/vendor/.roo）
- [x] golden/负向测试（7 用例；复用 fusesoc）

### S5 集成
- [x] 五包全部注册进 `aixsilicon.commands` `tool` 插件并实跑
- [x] 仓库级 Makefile + pre-commit（`make check` = ruff lint + 30 用例全绿）
- [ ] `aix wf run ip-verification/apb-register-ip` 的 `tool.*` 阶段转真实 provider
- [ ] workspace-lock `tools:` 段记录本仓包版本（工具版本锁）
- [ ] `reference/` 引用接入适配测试

## 跨仓治理

- [ ] hwif 六件工具与本仓 `aix-hwif-gen` 等分阶段合并（R1）
- [ ] ipkg 复用 `aix-core-tool`（R7）
- [ ] 统一退出码与 `aixworkflow.errors` 保持一致（分段映射）
- [ ] `aixsilicon.commands` 插件可被 workflow `aix tool` 调用（ADR-0004，已验证，随 S5 真实 provider 收尾）

## 变更记录

| 日期 | 变更内容 | 作者 |
|------|---------|------|
| 2026-08-13 | P0 五包实现并接入 `aix tool` 实跑；`make check` 全绿（30 用例）；五包注册进 `aixsilicon.commands` | Zoo |
| 2026-08-13 | 本文件并入 archived 原文 S0–S5 逐项 TODO 明细、阶段与包依赖顺序（合并补充） | Zoo |

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/tools.md`（todo 原文）§2 阶段与包依赖顺序、§3 S0–S5 逐项 TODO。
