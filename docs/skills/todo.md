# skills — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/skills.md`](../archived/architecture/repo-plans/skills.md)。
> 本文件已并入 archived 原文的 P0 首期实现清单（§19）、分阶段路线图（§20）、量化指标（§21）与 Definition of Done（§24），并追加仓级待办。

## 套件主体（ip-development-suite，已完成）

- [x] 顶层路由 SKILL.md + README（21 个子 skill）
- [x] 辅助 skill（drawio-ip-diagram / wavedrom-timing-diagram）
- [x] 公共 scripts + references（artifact-contract 唯一权威 + 10 份指南）+ templates/verification_template
- [x] lib/uvm-1.2（离线参考）+ evals/evals.json（8 个 eval）

## 校验与自测

- [ ] 在含 pyyaml/pytest 的 IP 工作区运行 `validate_suite.py`（结构/引用/契约）
- [ ] `pytest scripts/tests` 全通过（含 extractor 测试）
- [ ] 8 个 eval 用例全链路验证（full-flow 初始化、融合验证方案、追踪矩阵、覆盖率评审、UVM 模板、AXI-Lite agent、formal release、UVM 排错）
- [ ] 生成物示例复核：ip_mcdma（G0–G5 全 pass）、ip_apb_gpio_lite、ip_conv2d_accel、ip_mect

## 集成对齐

- [ ] 与 `aixsilicon_workflow` 的 `aix` 契约对齐（skill metadata → workflow Gate/evidence）
- [ ] 确定性 extractor 与 `aixsilicon_tool_repo` 边界落地（T1/T2）
- [ ] 发布产物对齐 `aixsilicon:*` VLNV 与 Unified Catalog
- [ ] 仓库根通用 skeleton skills 在 registry 标记 `superseded_by: ip-development-suite`

## 后续规划

- [ ] CBB development suite（参数契约/PPA/选型，衔接 cbb_repo）
- [ ] SoC integration suite（衔接 soc-integration + tool socgen）
- [ ] UVM 1800.2 双 profile 兼容薄层
- [ ] 多模型 eval、触发碰撞测试与成本/返工率治理

## 验收标准

- 任意 IP 变更可经套件受控完成：LRS → G0 → … → release → G5，且 evidence/trace/run_log 完整；
- 无私有 Skill 时公共确定性流程仍可运行（不依赖本仓）。

## 仓级待办（本批追加）

- [ ] 套件自校验 / Eval 全链路（`validate_suite.py` + `pytest scripts/tests` + 8 个端到端 eval）
- [ ] 与 workflow / tool 契约对齐：Context Pack / Change Plan / Skill Result（skill metadata → workflow Gate/evidence；确定性 extractor 与 tool_repo 边界，T1/T2）
- [ ] IP Golden Path 端到端、Author/Verifier 双 Agent：出口——一个真实 IP 变更经 Skill 受控完成（LRS → G0 → … → release → G5）
- [ ] CBB development suite、SoC integration suite（后续建设，衔接 cbb_repo / soc-integration + socgen）

## 变更记录

| 日期 | 变更内容 | 作者 |
|------|---------|------|
| 2026-08-13 | 创建 todo.md：套件主体、校验与自测、集成对齐、后续规划、验收标准 | Zoo |
| 2026-08-13 | 本文件并入 archived 原文 P0 首期实现清单、分阶段路线图、量化指标与 Definition of Done（合并补充）并追加仓级待办（出口：真实 IP 变更经 Skill 受控完成） | Zoo |

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/skills.md`（todo 原文 + plan 原文）§19 P0 首期实现清单、§20 分阶段路线图、§21 量化指标、§24 Definition of Done；仓级待办为本批追加。
