# HWIF Domain

HWIF（Hardware Interface）域是硬件接口的**类型系统、契约系统与兼容性判断系统**的唯一事实源所在。

## 域定位

- **HWIF 仓**（`aixsilicon_hwif_repo`）：接口语义 SSOT（Contract/Profile/Binding/Schema）+ 多视图 + 兼容规则；
- **HWIF Skill**（`hwif-development-suite`）：HWIF 全生命周期方法 + 确定性唯一入口（校验/生成/兼容/影响/打包）；
- **不消耗**：协议行为（VIP）、适配实现（CBB）、实例连接（SoC）、CSR（SystemRDL）。

## 文档导航

| 文档 | 内容 |
|---|---|
| [`repo-architecture.md`](repo-architecture.md) | hwif 仓现行架构：L0–L6、Schema、三视图、兼容模型、唯一入口收敛、版本治理 |
| [`skill.md`](skill.md) | `hwif-development-suite` 设计：9 子 skill、唯一入口 CLI、G0–G6 门禁、Eval/触发测试 |
| [`../repositories.md`](../repositories.md) | 仓级设计契约注册表 |
| [`../todo.md`](../todo.md) | 任务状态唯一台账 |
| [`../roadmap.md`](../roadmap.md) | 组合里程碑 |

历史参考（完整设计原文、P1–P4 收敛过程）已归档至 hwif-repo `archived/`，不作为执行依据。

## 当前架构速览（2026-08-17 起）

- 接口族：L0–L6 + 加速接口，**64 `.core` / 62 Contract / 18 Profile**；
- 确定性能力：**唯一入口 `hwif_tool.py`**（validate/generate/consistency/compat/impact/core/package）；
- 收敛状态：hwif 仓 `tools/`、`tests/` 已移除；`aix-hwif-gen`（tool-repo）已 deprecated；
- 当前能力：契约/生成/兼容/门禁链路可用，正式消费者联验与发布进入 M2/M3 阶段。
