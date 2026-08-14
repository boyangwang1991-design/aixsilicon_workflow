# ADR-0007：有类型依赖与显式 Profile

- 状态：建议
- 日期：2026-08-13

## 背景

现有 Profile 通过 `include_groups` 的任一命中选择仓库，而多数仓都属于 `base`，导致 `minimal` 启用 9 个仓，主要开发 Profile 几乎得到相同的 10 仓工作区。单一 `depends_on` 同时被用来表达产品、验证、工具和发现关系，无法为 build、impact、qualification 和 release 分别计算正确闭包。

## 决策

1. Profile 增加显式 `include_repositories`，作为精确工作区集合；group 退回展示、检索和策略标签；
2. 仓库依赖增加 `product/verification/tooling/discovery/context` 五类；
3. 过渡期 `depends_on` 等价于 `dependencies.product`；
4. Product 依赖必须形成 DAG，其他类型分别验证；
5. 不同操作按类型计算闭包，context 永不成为公共确定性流程的 required 依赖；
6. 默认 Profile 按 [`target-design.md`](../architecture/target-design.md) §4 的目标集合迁移。

## 备选方案

- 继续调整现有 group：无法消除“任一 group 命中”导致的隐式选择和漂移；
- 每种场景维护独立 Manifest：容易复制仓库 URL、revision 和 Owner 事实；
- 继续使用无类型 `depends_on`：实现简单，但影响分析和验证闭包会持续失真；
- 立即删除旧字段：会破坏现有 Manifest、Lock 和测试，不接受。

## 结果

正向影响：Profile 成本和权限边界清晰；影响分析更准确；Knowledge/Skill 不再污染基础闭包；SoC/IP 的验证和工具依赖可显式表达。

负向影响：需要升级 Schema、模型、Graph、FuseSoC 索引、Lock、测试和文档；过渡期存在双字段解析。

迁移要求：先兼容读取、再迁移 Manifest、最后发出 deprecated 警告；至少保留两个发布周期。
