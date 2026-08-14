# ADR-0006：确定性工具归属与迁移路径

- 状态：接受
- 日期：2026-08-13

## 背景

[`aixsilicon_hwif_repo`](../../repos/aixsilicon_hwif_repo/todo.md:40) 已在仓内 `tools/` 建设 6 件确定性工具
（`contract_validate` / `sv_consistency_check` / `view_generate` / `compatibility_check` / `impact_analysis` / `package_release`），
与 [`aixsilicon_tool_repo`](../../repos/aixsilicon_tool_repo/tool_repo_plan.md:417) 规划的 `aix-hwif-gen` 等产品级工具重叠。

## 决策

1. **资产仓 `tools/` 只保留“仓库自维护脚本”**（测试、CI、文档生成、本地检查入口），不承载跨仓复用的产品级确定性工具；
2. **产品级确定性工具统一归 `aixsilicon_tool_repo`**，作为 `aix tool` 插件发布（见 ADR-0004）；
3. **分阶段迁移**：
   - 阶段 A：workflow 的 action 注册表同时支持“本仓脚本”与“`aix tool` 委托”，工具结果统一为结构化 Result；
   - 阶段 B：tool_repo P0 五包（`aix-tool-core`/`aix-schema`/`aix-hwif-gen`/`aix-reg-tool`/`aix-core-tool`）落地，asset 仓切换到 `aix tool` 调用；
   - 阶段 C：asset 仓内旧工具标记 deprecated，一个 release 周期后移除或降级为自维护脚本；
4. 迁移期间 hwif 仓内工具仍是可用的 fallback，公共确定性流程不因 tool_repo 未装而中断。
5. **工具归属四类**（详见 [`docs/tool-placement.md`](../workflow/tool-placement.md)）：T1 跨仓公共工具 → tool_repo；T2 单仓自维护脚本 → 留资产仓 `tools/`；T3 私有/受控适配（商业 EDA/PDK/内部 Runner）→ **独立私有 overlay repo**（同一 Plugin API，不开源）；T4 项目专用脚本 → 留项目仓。

## 备选方案

- 保留工具散落各资产仓：重复实现、版本难锁、Skill/Workflow 调用路径分裂，不采用；
- 立即删除资产仓工具：在 tool_repo 未就绪前破坏可用性，不采用。

## 结果

- 正向：确定性能力收敛到单一 tool 平台，Workflow 通过 Tool Registry 版本锁定调用；
- 负向：迁移需要过渡期（阶段 A→C），期间存在两套执行入口；
- 权衡：以 `aix tool` 委托 + 版本锁消除重复，同时保留 fallback 保证公共流程可运行。
