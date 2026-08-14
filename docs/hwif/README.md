# HWIF 仓设计契约

HWIF 是接口语义、兼容规则和可生成多视图的唯一事实源。Owner 为 `hw-platform`；主要消费者是 CBB、IP、VIP、SoC Integration 和生成工具。

## 范围与边界

- 负责：Interface Contract、Role/Signal/Profile/Capability、Binding、兼容性规则、SemVer 和可发布视图；
- 不负责：具体 IP/CBB 实现、协议验证环境、SoC 产品 Top、生成器实现；
- Contract YAML 是 SSOT；SV package/interface/flattened ports、文档和 binding 均为确定性派生物；
- 第三方参考只用于对照，不进入正式 FuseSoC 发现和 Catalog 发布。

## 输入、输出与依赖

| 项 | 内容 |
|---|---|
| 输入 | 协议规范、消费者需求、兼容性反馈、Schema |
| 输出 | Contract/Profile/Binding、兼容报告、多视图 HDL、VLNV/Core、发布材料 |
| 工具依赖 | tools 的 schema/hwif/core provider；Workflow 的 Lock/Evidence/Release |
| 验证依赖 | 至少两个真实消费者；VIP/产品编译与负向兼容样例 |

## 目标能力与阶段

1. 先冻结 APB 最小 Contract、角色、reset、profile 和兼容规则；
2. 以工具生成三视图并做漂移检查；
3. 在 APB VIP 和代表性 IP/CBB 中联合消费，形成 G3 Evidence；
4. 扩展 L0/L1 公共接口，再按真实项目需求扩展 AMBA/外设/安全接口；
5. 只有出现两个真实工艺适配消费者后，才评审 techlib 候选仓。

## 验收出口

- Contract 通过 Schema、语义和兼容性检查；生成物可重建且禁止手改；
- breaking change 有 SemVer/迁移窗口；消费者矩阵记录精确 SHA；
- 固定 Lock 下至少两类消费者编译/验证通过，负向不兼容样例被拒绝；
- 发布物包含 VLNV、版本、契约 hash、兼容报告和 Evidence 索引。

活动交付见 [`delivery.md`](delivery.md)，完整历史设计与 L0～L6 清单见 [`design-reference.md`](design-reference.md)。
