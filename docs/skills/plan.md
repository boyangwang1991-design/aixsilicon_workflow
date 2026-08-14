# skills — AIXSILICON Skill Repository 建设规划（私有）

> 客观事实基线：2026-08-13（canonical `ip-development-suite` 已落地）。原文细节见 [`../archived/architecture/repo-plans/skills.md`](../archived/architecture/repo-plans/skills.md)。
> 本文件已并入 archived 原文的完整规划细节：Skill 目录与单 Skill 结构（§4–§5）、Repo Registry 与 Skill Metadata（§6）、Suite 划分（§7，以 §26 canonical 修订为准）、Context Pack（§9）、输出契约（§10）、Eval 体系（§15）与 CI/CD（§16）。

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

### 5.1 Skill 结构规范

- `skills/<skill-name>/` 保持极简：`SKILL.md`（必需）+ `agents/openai.yaml`（推荐）+ `references/`（按需领域知识）+ `scripts/`（Skill 特有小型辅助）+ `assets/`（输出模板，不放知识正文）；
- `SKILL.md` frontmatter 只保留 `name` 与 `description`；正文命令式、约 500 行以内，固定包含：Goal / Preconditions / Required context / Procedure / Tool calls / Output contract / Verification gates / Stop-ask-human conditions / Failure recovery / Relevant references；
- **描述即触发接口**：明确能做什么、在什么任务语义下触发、何时不触发、与相邻 Skill 的区别；需专项测试易冲突组合（如 `implement-ip-rtl` vs `integrate-soc`、`design-register-map` vs `design-hardware-interface`）；
- **三层 Progressive Disclosure**：`name+description`（发现/触发）→ `SKILL.md`（执行）→ `references/scripts/assets`（仅需要时加载）；references 只从 `SKILL.md` 直链一层，超 100 行应提供目录；
- **Repo Registry**：运行时 frontmatter 保持标准化，治理信息放 `registry/skills.yaml`（版本 / Suite 归属 / Owner / 风险级别 / 读写范围 / Tool 与 Workflow 兼容 / Eval 状态 / 成熟度 / 退役与替代关系）。

### 5.2 Suite 划分（现状对齐后，以 canonical 为准）

- **canonical `ip-development-suite`（V1.0）**：21 个子 skill（00 工作区 → 18 发布 + drawio/wavedrom 辅助）；质量门禁 G0–G5 基于证据（Gate 报告 + canonical 模型哈希）；canonical 模型驱动（`META` → `model/*.yaml` SSOT）；统一 UVM 1.2 离线参考；唯一运行日志 `run_log.md`；确定性发布（manifest + SHA-256 + archive）；执行模式 full-flow / partial-task（默认）/ review-only；
- **规划中（按需建设）**：Foundation、CBB Development Suite（参数契约/PPA/选型，衔接 cbb_repo）、SoC Integration Suite（衔接 soc-integration + socgen）、UVM 1800.2 双 profile、多模型 eval 与成本/返工治理；
- 原通用 Suite 划分（RTL Coding / UVM Verification 等）已并入 `ip-development-suite`；仓库根早期 skeleton skills（route-chip-task 等）在 registry 标记 `superseded_by: ip-development-suite`。

### 5.3 Context Pack 设计

- `build-context-pack` 按任务构造带哈希/来源的最小上下文包：`task_id / task_type / objective / repositories（revision+paths）/ contracts / constraints / evidence_baseline / write_scope / human_approval`；
- 上下文来源优先级：已批准规格与 Change Plan → 仓库内 SSOT → 固定 revision 依赖仓 → Catalog 合格版本 → Skill references → 历史讨论（仅建议，不覆盖 SSOT）。

### 5.4 输出契约

- 所有执行型 Skill 输出统一 `skill_result` 结构：`task_id / skill / skill_version / status / summary / assumptions / changed_files / tools_requested / evidence / risks / approvals_required / next_action`；
- 状态机：`planned / changed / needs_verification / blocked / needs_human_decision / verified / rejected`；Skill 不能自封 `verified`，必须由独立证据与 Workflow Gate 转换。

### 5.5 Eval 体系

- **Eval 类型**：Trigger（触发/拒绝/冲突）/ Contract（Schema 与状态转换）/ Procedure（上下文/规划/验证流程）/ Engineering（通过真实 Tool/EDA 基线）/ Safety（越权/泄密/注入）/ Regression（更新不退化）/ Efficiency（上下文与返工合理）；
- **测试集分层**：smoke（每 Skill 3–5 用例）→ core（典型任务/常见失败/边界）→ adversarial（注入/冲突/伪造日志）→ golden（资深工程师确认片段）→ forward-test（未见过诊断过程的 Agent 独立执行）；
- **评分维度**：工程正确性 30 / 契约与可追踪性 20 / 风险识别 15 / Tool-证据使用 15 / 权限与隐私 10 / 清晰度与效率 10；越权写入、泄露受限数据、伪造证据、绕过 Gate 直接判失败；
- **Skill 发布门槛**：frontmatter/命名校验、Trigger 正负样例、输出 Schema 100%、安全用例 100%、Core Eval 达标、至少一次独立 forward-test、Owner 审查。

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/skills.md`](../archived/architecture/repo-plans/skills.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/skills.md`（plan 原文）§4 目录结构、§5 单个 Skill 结构、§6 Registry 与 Skill Metadata、§7 Suite 划分（以 §26 canonical 修订为准）、§9 Context Pack、§10 输出契约、§15 Eval 体系。
