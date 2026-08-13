# hwif — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/hwif.md`](../archived/architecture/repo-plans/hwif.md)。

## P0 优先

- [ ] Techlib binding（`aixsilicon_techlib_repo` 待建前以抽象接口承接，A4）
- [ ] 完成 2 个真实消费者（CBB + VIP）依赖其 core 并通过编译
- [ ] VLNV 迁移 `aix:interface:*` → `aixsilicon:interface:*`（deprecated 窗口）
- [ ] `tools/` 产品级确定性工具分阶段迁入 `aixsilicon_tool_repo`（R1 / ADR-0006）

## P1 首个季度

- [ ] G1 Semantic 架构评审（当前待评审）
- [ ] 正式 IP / VIP / SoCGen 真实消费证据（当前仅示例）
- [ ] Skill / SoCGen 消费闭环
- [ ] `reference/` 治理：排除 fusesoc 正式发现、不发布、不进 Catalog（A2）

## P2 两个季度

- [ ] 2 个 IP + 1 个 Subsystem 达到 `proven`
- [ ] 版本迁移与 Deprecated 自动检查
- [ ] 新协议/Profile 准入流程

## 质量 Gate（客观状态）

- G0 Contract ✅ / G1 Semantic ⬜ / G2 HDL ✅ / G3 Roundtrip ✅ / G4 Consumer ✅（示例）/ G5 Compatibility ✅ / G6 Release ✅

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
