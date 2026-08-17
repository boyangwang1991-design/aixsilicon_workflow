# ADR-0008：Action Capability Preflight 与 Provider 锁定

- 状态：已接受
- 日期：2026-08-13
- 接受日期：2026-08-17
- 决策记录：见本文件末尾「决策记录」节

## 背景

当前 Flow YAML 已引用大量 `tool.*`、`release.*`、`catalog.*`、`soc.*`、`eda.*` 和 `skill.*` action，但标准 runner 只注册少量基础实现。Flow 能通过 Schema 校验并不表示能够执行，且 Lock/Evidence 尚不能完整记录 action provider 版本。

## 决策

1. 分离 Flow、Action Contract 和 Provider；
2. Action registry 返回稳定名称、provider、版本、输入输出 Schema、确定性、环境要求、写入范围和证据要求；
3. 新增 Flow preflight，在执行前产生 capability matrix；
4. 统一状态为 `available/optional-unavailable/unimplemented/version-mismatch/environment-unavailable`；
5. 未实现或版本不匹配的必需 action 必须在 Stage 执行前阻断；
6. 实际 provider 包版本、hash、容器/EDA 摘要写入 Lock 和 Evidence；
7. Flow 只有在 preflight、代表性端到端测试和 Evidence 均通过后才能标记 active。

## 备选方案

- 遇到未注册 action 时运行期再失败：反馈太晚，无法形成可靠计划；
- 在 Flow 中写脚本路径：破坏安全边界、插件替换和版本锁；
- 所有缺失能力都 skipped：会产生假通过；
- 仅记录 Python 包版本：不能覆盖容器、EDA、私有 Overlay 和生成器实现。

## 结果

正向影响：Flow 的可运行性可在执行前判断；公共/私有 provider 使用统一契约；Evidence 可重建；规划完成度不再依赖 YAML 数量。

负向影响：需要 provider metadata、版本约束、preflight 命令、Lock/Evidence Schema 和测试；私有 EDA/PDK adapter 也必须提供最小公开元数据。

## 决策记录

- 日期：2026-08-17
- 决策：**接受**（WF-003），附以下修订点
- 审批人：boyang wang
- 决策证据：
  - [`evidence/action-inventory.md`](../evidence/action-inventory.md)：8 条 Flow 引用 46 个唯一 action，注册 6、缺口 40（F-004 量化）
  - 实现审计：[`src/aixworkflow/runner.py`](../src/aixworkflow/runner.py) 未注册 action 走 `blocked` 且不阻断（F-001）；G0/G1 硬编码 pass（F-002）；`timeout_seconds`/`retries` 有 Schema 无执行（F-007）

### 修订点

1. **REV-1（fail-closed 阻断）**：未注册或状态为 `unimplemented`/`version-mismatch`/`environment-unavailable` 的 **required** action，必须在 stage 执行前阻断 Flow；`blocked`/`skipped` 一律不得汇总为 pass（关闭 F-001）。
2. **REV-2（Gate 真实判定）**：`G0`（clean）、`G1`（lock）等 precondition 与全部 Gate 必须由真实校验器依据 Evidence 判定，禁止硬编码 `pass`；precondition 先于 stage 执行（关闭 F-002）。
3. **REV-3（capability matrix 标准输出）**：preflight 输出结构化的 capability matrix：`action × provider × version × availability × write_scope × evidence_requirement`，状态用 ADR 规定的 6 态枚举；`timeout_seconds`/`retries`/`on_failure` 必须由 runner 真实执行并纳入契约测试（关闭 F-007）。

### 验收与迁移

- 首件交付物：**action inventory**（[`evidence/action-inventory.md`](../evidence/action-inventory.md)）作为 M1 WF-004/TOOL-001 基线，逐一为 40 个缺口 action 确定 provider 落点、版本约束与 availability；
- 未实现/版本不匹配的 required action 阻断；optional action 可降级但必须显式标注状态；
- provider 包版本、hash、容器/EDA 摘要写入 Lock 和 Evidence；
- 关闭证据：M1 preflight 负向测试 + M3 真实 APB Evidence（F-004 最终关闭）。
