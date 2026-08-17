# Catalog 交付台账

> 状态、负责人、日期和 Evidence 只在 [`../todo.md`](../todo.md) 维护。

| ID | P | 里程碑 | 任务 | 依赖 | 验收 / Evidence | Owner |
|---|---|---|---|---|---|---|
| CAT-001 | P0 | M4 | 冻结 Catalog asset/lifecycle/compatibility Schema | Release 契约 | 正负样例、版本迁移、Owner 审核 | boyang wang |
| CAT-002 | P0 | M4 | 清查现有条目的来源、状态和证据 | CAT-001 | 每项可追溯或标记 legacy/unverified | boyang wang |
| CAT-003 | P0 | M4 | 建立 APB HWIF/VIP/IP 首批条目模板 | HWIF/VIP/IP release fields | Schema 校验、兼容边、Evidence 链 | boyang wang |
| CAT-004 | P0 | M4 | 冻结 release-train 的 Catalog diff/PR 接口 | CAT-003 | 输入输出、权限、幂等键和失败语义获批 | boyang wang |
| CAT-005 | P1 | M4/M6 | 实现确定性 resolve/compatibility 检查 | CAT-001 | 冲突/yanked/不兼容负向用例 | boyang wang |
| CAT-006 | P0 | M4 | 验收 release-train 的 Catalog PR 闭环 | WF-010、CAT-004 | 不直写 main；审批/幂等/失败恢复测试 | boyang wang |
| CAT-007 | P2 | 运营 | 建立 deprecated/yanked/替代和审计周期 | CAT-005 | 生命周期演练与审计报告 | boyang wang |

现有条目不因文件存在而自动视为 qualified；须由 CAT-002 给出可追溯判定。
