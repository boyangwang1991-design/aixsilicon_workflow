# skills — AIXSILICON Skill Repository 建设规划（私有）

> 客观事实基线：2026-08-13（canonical `ip-development-suite` 已落地）。原文细节见 [`../archived/architecture/repo-plans/skills.md`](../archived/architecture/repo-plans/skills.md)。

## 1. 定位与边界

**定位**：AI 辅助研发 Skill Suite（IP 开发/验证方法论、Agent 编排、Prompt）与核心方法论；**私有仓**。

| 本仓负责 | 不负责 |
|---|---|
| Skill 方法论、Agent 编排、Context Pack、Skill Result | 资产事实/源码（各资产仓） |
| Skill Metadata / Eval / 权限分层 | 确定性生成/检查（tools） |
| 与 Workflow 的 Gate/evidence 契约 | Gate 编排与发布（workflow） |

**不可违反的边界**：私有能力、公开契约；轻量路由、按需加载；判断与执行分离；最小写权限；证据优先；**AI 生成不等于 AI 批准**（P0/P1 需独立 Verifier 或人工批准）。

## 2. 现状（客观）

- **canonical `ip-development-suite`（V1.0）已落地**：
  - 顶层路由 SKILL.md + README（21 个子 skill：00 工作区/01 LRS/02 寄存器/03 HLD/…/18 发布）；
  - 辅助 skill（drawio-ip-diagram / wavedrom-timing-diagram）；
  - 公共 scripts（log_step / validate_suite / instantiate_template / vcs_lint_* 等）；
  - references（artifact-contract 唯一权威 + 10 份指南/模板/FAQ）；templates/verification_template；lib/uvm-1.2（离线参考）；
  - `evals/evals.json`（8 个端到端 eval）；
- **缺口**：套件自校验/Eval 全链路未跑通；与 workflow/tool 契约对齐待做；CBB/SoC suite 未建。

## 3. 依赖与角色

- **依赖**：无（DAG 之外，能力增强层）；
- **角色**：指导 Workflow 选择与执行流程；公共流程**不依赖**本仓（无 Skill 时确定性流程仍可运行）。

## 4. 契约

- **Schema 所有权**：`skill-metadata / context-pack / skill-result / eval`；
- **成熟度**：experimental / pilot / stable / deprecated / retired；
- **权限分层**：P3 只读 / P2 测试临时报告 / P1 RTL-UVM-Schema 修改需 Change Plan+人工审批 / P0 接口-复位-FUSA-发布双重审查；
- **VLNV**：发布产物对齐 `aixsilicon:*` 与 Unified Catalog。

## 5. 建设路线（客观）

| 阶段 | 目标 | 状态 |
|---|---|---|
| 0 契约与仓库骨架 | Metadata/Context Pack/Skill Result | ✅ 骨架完成 |
| 1 Foundation + IP MVP | `ip-development-suite` canonical | ✅ 已落地 |
| 2 CBB + UVM 完整化 | CBB suite、UVM 1800.2 双 profile | ⬜ |
| 3 SoC Integration | SoC suite（衔接 soc-integration + socgen） | ⬜ |
| 4 规模化与高级能力 | 多模型 eval、成本/返工治理 | ⬜ |

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/skills.md`](../archived/architecture/repo-plans/skills.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
