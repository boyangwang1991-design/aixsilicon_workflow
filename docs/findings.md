# 方案与实现 Findings

更新时间：2026-08-17。本文记录文档审核中发现、但尚未由实现或验证证据关闭的问题。它不是任务看板：任务定义在各仓 `delivery.md`，任务状态在 [`todo.md`](todo.md)，组合状态在 [`progress.md`](progress.md)。

## 1. 使用规则

- Finding 编号永久稳定；状态使用 `open / accepted / resolved / wont-fix`；
- `accepted` 表示方案已接受但实现未关闭，不能解释为能力已可用；
- 关闭必须附代码/测试/运行 Evidence 或经批准的决策记录；
- 本轮只完善方案，不修改脚本、Manifest、Schema 或 Flow YAML；下表实现类问题全部保留为未关闭。

## 2. P0 Findings

| ID | 发现 | 影响 | 已确定方案 | 关闭证据 | 状态 | Owner | 关闭阶段 | 关联任务 |
|---|---|---|---|---|---|---|---|---|
| F-001 | runner 可把未注册/被跳过的 required stage 留在结果中并继续汇总为成功 | 形成 false green，Gate 不可信 | required stage fail-closed；skipped/blocked 必须阻断依赖和总体通过 | ✅ 关闭（2026-08-17）：fail-closed 实现 + required 阻断/未注册阻断负向测试（[`../tests/unit/test_runner_controls.py`](../tests/unit/test_runner_controls.py)），95 项全绿 | `resolved` | workflow（runner） | M1（机制）→ M3（真实） | WF-005、WF-008 |
| F-002 | G0/G1、precondition、required gate 与 `forbid_override` 尚未形成真实判定链 | dirty/unlocked/override 工作区可能进入执行或发布 | precondition 先于 stage；Gate 只由验证器依据 Evidence 判定 | ✅ 关闭（2026-08-17）：precondition 真实判定 + G0/G1/G2 负向测试（[`../tests/unit/test_runner_controls.py`](../tests/unit/test_runner_controls.py)） | `resolved` | workflow（runner/验证器） | M1（机制）→ M3（真实） | WF-005、WF-006 |
| F-003 | Release prepare 可过早记录 G7，publish 未证明 lock/审批/Tag/Catalog 幂等链 | 未批准或不可重建材料可能被视为已发布 | G0～G6 合格后生成候选；人工批准后才判 G7；Tag、Release、Catalog PR 分离 | dry-run、审批、重复发布、失败恢复 Evidence | `open` | workflow + catalog | M4 | WF-010、CAT-006 |
| F-004 | 现有 Flow action 与标准 registry/provider 差距大（审计时 46 个唯一使用名中 40 个未注册） | 8 条 YAML 多数只能解析，不能真实执行 | ADR-0008 capability registry + preflight；P0 action 必须有 provider/version/hash | ✅ 关闭（2026-08-17）：capability registry + preflight 6 态 + fail-closed 阻断（[`../tests/unit/test_capability.py`](../tests/unit/test_capability.py)）；inventory 见 [`../evidence/action-inventory.md`](../evidence/action-inventory.md) | `resolved` | workflow + tools | M1（机制）→ M3（真实） | WF-004、TOOL-001、TOOL-002 |
| F-005 | Flow 原始 argv 与 `wf foreach` 缺少完整参数/路径/命令边界 | 命令注入、越权写入和不可审计风险 | Flow 只传结构化参数；provider 负责允许列表；禁止任意 shell | ✅ 关闭（2026-08-17）：参数 list 化/路径/越界/高风险 guard 负向测试（[`../tests/unit/test_security.py`](../tests/unit/test_security.py)） | `resolved` | workflow + tools | M1（机制）→ M3（真实） | WF-005、TOOL-004 |
| F-006 | `write_scope` 与 ownership map 主要停留在声明层 | 跨仓写入可能绕过唯一 Owner | 执行前校验 action 声明、目标路径和 Owner；跨仓写入仅经 Change Bundle | ✅ 关闭（2026-08-17）：write_scope 越界拒绝在 runner 执行前校验（[`../tests/unit/test_runner_controls.py`](../tests/unit/test_runner_controls.py)） | `resolved` | workflow（ownership map） | M1/M2（机制）→ M4（真实） | WF-005、WF-012、WF-009 |

## 3. P1 Findings

| ID | 发现 | 影响 | 已确定方案 | 关闭证据 | 状态 | Owner | 关闭阶段 | 关联任务 |
|---|---|---|---|---|---|---|---|---|
| F-007 | timeout/retries/on_failure/needs/gates 等 Flow 语义未被完整执行 | YAML 契约与运行行为漂移 | 为每种控制语义建立 runner contract test | ✅ 关闭（2026-08-17）：timeout/retry/required/写范围控制语义实现 + 负向测试（[`../tests/unit/test_runner_controls.py`](../tests/unit/test_runner_controls.py)） | `resolved` | workflow（runner 语义） | M1（机制）→ M3（真实） | WF-005 |
| F-008 | Run Manifest/Evidence/Lock 字段不足，tool hash 可缺省且缺 Run Manifest Schema | 结果不可严格重建或审计 | 锁定 repo/provider/tool/env；证据带输入输出 hash、seed、命令摘要和失败签名 | ✅ 关闭（2026-08-17）：Run Manifest environment/provider/hash + Lock tools 段 + schema 校验（[`../schemas/evidence-index.schema.json`](../schemas/evidence-index.schema.json)） | `resolved` | workflow + dv-common | M1/M2（机制）→ M3（真实） | WF-006、TOOL-003、DV-001 |
| F-009 | Change Bundle 主要表达依赖顺序，未闭合状态机、PR SHA、联合 CI 与合入结果 | 多仓改动可能在不同提交上验证 | 显式状态机与 PR HEAD checkout，记录 merge order/CI/Evidence | 多 PR 临时仓 E2E | `open` | workflow（Change Bundle） | M4 | WF-009 |
| F-010 | Profile 当前失真且依赖无类型 | 工作区过大，影响闭包可能漏测或过测 | ADR-0007 exact Profile + product/verification/tooling/discovery/context | ✅ WF-002 已实现：exact Profile + typed deps + DAG/closure（[`../tests/unit/test_exact_profile.py`](../tests/unit/test_exact_profile.py)，2026-08-17，65 项测试全绿）；default.yaml 已迁移精确 Profile | `resolved` | workflow（Profile） | M1 | WF-002 |
| F-011 | Qualification 与 Release 对 G7 的归属不一致 | 验证流程可能在审批前声称发布通过 | qualification 只产出 G0～G6；G7 只属于 release-train 人工批准后的发布判定 | Flow/文档/schema 一致性测试 | `accepted` | workflow（G7 归属） | M3 → M4 | WF-008、WF-010 |
| F-012 | 安全政策与实现退出码存在两套口径 | 自动化无法稳定区分设计失败、环境缺失和可选能力 | 选定一套分段码并提供兼容映射；以代码常量+契约测试为准 | ✅ 关闭（2026-08-17）：退出码分段契约（0/10/20/30/40/50/60）+ 错误类映射测试（[`../tests/unit/test_security.py`](../tests/unit/test_security.py)） | `resolved` | workflow + tools | M1/M2 | WF-007、TOOL-004 |
| F-013 | 统一检查入口在 Windows/POSIX、UTF-8、离线 pre-commit 上不稳定 | 新环境无法复现项目自检 | 提供跨平台入口、显式 UTF-8 和受控依赖缓存/降级说明 | ✅ 关闭（2026-08-17）：Makefile/pre-commit 跨平台入口（uv run python）+ 测试显式 UTF-8；`make check` 与 pre-commit 11/11 全绿 | `resolved` | workflow（工程化） | M1 | WF-011 |

## 4. 文档治理 Findings

| ID | 发现 | 处置 | 关闭证据 | 状态 |
|---|---|---|---|---|
| F-014 | plan/todo/design-reference 职责重叠，Todo 有重复任务和历史清单 | 改为 README 设计契约 + delivery 任务定义 + 根级 todo 唯一状态台账；历史参考不维护状态 | 11/11 域覆盖、79/79 任务纳入统一状态台账、delivery 状态列为 0、本地链接为 0 | `resolved` |
| F-015 | Workflow 设计已按主题拆分，若再造 design-reference 会重复；Catalog/SoC 当前参考曾是占位 | Workflow 保留主题契约；Catalog/SoC 补当前设计契约；统一入口由 repositories 索引 | 设计/交付覆盖矩阵和链接检查通过 | `resolved` |
| F-016 | techlib/reference-soc 等候选仓在局部任务中被当作既定工作 | 建立 proposals 和激活门；不提前形成依赖 | 4 份提案；roadmap/delivery/Manifest 角色一致 | `resolved` |
| F-017 | 初稿中 Catalog/Release、SoC/Workflow、Tool/Workflow 任务存在互相等待风险 | 拆分领域契约、控制面实现和端到端验收，任务只保留一个 Owner | 79 个任务 ID 无重复、未知依赖或依赖环 | `resolved` |

## 5. Finding 到工作包

| 工作包 | Findings | 主要任务文件 |
|---|---|---|
| WP1 Profile/依赖 | F-010 | [`workflow/delivery.md`](workflow/delivery.md) |
| WP2 Capability/执行安全 | F-001、F-002、F-004～F-008、F-012 | [`workflow/delivery.md`](workflow/delivery.md)、[`tools/delivery.md`](tools/delivery.md) |
| WP3 APB 穿刺 | F-001、F-002、F-004、F-008、F-011 | hwif/dv-common/vip/ip/tools delivery |
| WP4 协作发布 | F-003、F-006、F-009、F-011 | workflow/catalog delivery |
| 工程化 | F-013 | [`workflow/delivery.md`](workflow/delivery.md) |

## 6. 审核记录

### 2026-08-17：Owner/关闭阶段确认（M0 Findings 审核）

依据 [`roadmap.md`](roadmap.md) §16 风险燃尽顺序、[`ownership-map.yaml`](../ownership-map.yaml) Schema/Owner 归属，为 F-001～F-013 逐项确认 Owner、关闭阶段与关联任务（已写入 §2/§3 表）。

- **机制级关闭**（M1/M2）：F-001、F-002、F-004、F-005、F-007、F-008、F-012、F-013；F-006 机制在 M1/M2，真实关闭在 M4；
- **真实关闭**（M3/M4）：以 APB 真实 Evidence 关闭 F-001、F-002、F-004、F-005、F-007、F-008；F-003、F-009 以 M4 发布 E2E 关闭；F-011 在 M3 一致性测试、M4 真实批准关闭；
- **方案级**：F-010（已 accepted，M1 WF-002 实施关闭）。
- 已产生的本轮证据：`evidence/action-inventory.md`（F-004 基线）、`evidence/profile-diff.md`（F-010 基线）、F-001/F-002/F-007/F-013 实现实证记录。
- 状态说明：上述确认仅定 Owner/阶段，不改变 `open`/`accepted` 状态；关闭仍以对应阶段 Evidence 为准。

### 2026-08-17：F-010 关闭（WF-002 实现）

F-010 已 `accepted → resolved`：exact Profile（`include_repositories`/`optional_repositories`）+ typed dependencies（五类）+ typed DAG/closure 已实现并迁移 [`manifests/default.yaml`](../manifests/default.yaml)；新增 [`tests/unit/test_exact_profile.py`](tests/unit/test_exact_profile.py) 14 项（共 65 项全绿）。

### 2026-08-17：M1 核心机制完成（WF-004/005/006/007/011/012 + TOOL-001/003/004）

- **F-013 → `resolved`**：Makefile/pre-commit 跨平台入口（`uv run python`）+ 测试显式 UTF-8；`make check` 与 pre-commit 11/11 全绿。
- **F-001/F-002/F-004/F-005/F-006/F-007/F-008/F-012 已关闭**（`open → resolved`，2026-08-17，详见 §6 下一条关闭记录）：
  - F-001：runner fail-closed（required 阻断，[`tests/unit/test_runner_controls.py`](../tests/unit/test_runner_controls.py)）
  - F-002：precondition/G0/G1/G2 真实判定
  - F-004：capability registry + preflight 6 态（[`tests/unit/test_capability.py`](../tests/unit/test_capability.py)）
  - F-005：参数/路径/越界安全（[`tests/unit/test_security.py`](../tests/unit/test_security.py)）
  - F-006：write_scope 越界拒绝
  - F-007：timeout/retry/required 控制语义
  - F-008：Run Manifest environment/provider/hash + Lock tools 段
  - F-012：退出码分段契约（[`tests/unit/test_security.py`](../tests/unit/test_security.py)）
- 验证：**95 项测试全绿**，pre-commit 11/11 全绿。

### 2026-08-17：M1 已实现 Finding 关闭

以下 Finding 的机制级实现已完成并有测试证据，状态 `open → resolved`：
- **F-001**（fail-closed required 阻断）、**F-002**（precondition/G0/G1/G2 真实判定）、**F-006**（write_scope 越界拒绝）、**F-007**（timeout/retry 控制语义）：[`../tests/unit/test_runner_controls.py`](../tests/unit/test_runner_controls.py)
- **F-004**（capability registry + preflight 6 态）：[`../tests/unit/test_capability.py`](../tests/unit/test_capability.py)
- **F-005**（参数/路径/越界安全）、**F-012**（退出码分段契约）：[`../tests/unit/test_security.py`](../tests/unit/test_security.py)
- **F-008**（Run Manifest environment/provider/hash + Lock tools 段）：[`../schemas/evidence-index.schema.json`](../schemas/evidence-index.schema.json)
- 连同此前已 `resolved` 的 **F-010**（exact Profile）、**F-013**（跨平台入口）。

仍未关闭（实现层面待后续里程碑）：**F-003**（M4 发布幂等链）、**F-009**（M4 Change Bundle 状态机）、**F-011**（M3/M4 G7 归属，方案 `accepted`）。
