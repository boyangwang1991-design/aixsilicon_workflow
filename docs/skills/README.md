# Skills 仓设计契约（私有、可选）

Skills 仓提供 AI 辅助研发方法、Context Pack、受控生成和评审能力。Owner 为 `ai-engineering`；它不是确定性工具、资产事实源或 Gate 判定器，缺失时公共最低流程必须仍可运行。

## 边界与安全

- Skill 可理解上下文、生成候选变更/计划/解释和调用已授权 Tool；
- 事实、最低确定性结果和最终批准分别归资产仓、Tools/Workflow 和人类 Reviewer；
- 使用最小写权限，所有输出带 provenance、输入范围、模型/版本、风险和待验证项；
- 私有材料、prompt injection、secret、许可证和红区数据按分类隔离；
- Author 与 Verifier 角色分离，AI 生成不等于 AI 批准。

## 契约

每个 Skill 声明触发语义、所需/可选上下文、读写 scope、Tool bindings、输出 Schema、失败/降级方式和 Eval。Context Pack/Change Plan/Skill Result 只能引用精确 repo SHA/文件范围，确定性输出由 Tool 产生并进入 Evidence。

## 建设顺序

先验证现有 IP Development Suite 的结构、8 个 Eval、契约和真实 APB Golden Path；CBB/SoC Suite 只在相应确定性 Flow 已稳定后启动。多模型评估以正确性、安全、返工率和成本为指标，而不是追求调用数量。

## 验收出口

- suite validator、单测、触发碰撞、注入/越权和端到端 Eval 通过；
- 同一 APB 任务由 Author/Verifier 双角色完成，所有产物仍经过确定性 Gate；
- 禁用 Skills 后 APB 公共流程仍可运行并给出清晰降级；
- metadata、版本、兼容矩阵和分发权限可审计。

活动交付见 [`delivery.md`](delivery.md)，完整 Suite 地图、安全/Eval 设计见 [`design-reference.md`](design-reference.md)。
