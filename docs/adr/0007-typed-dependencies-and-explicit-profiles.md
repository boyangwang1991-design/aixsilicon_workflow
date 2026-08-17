# ADR-0007：有类型依赖与显式 Profile

- 状态：已接受
- 日期：2026-08-13
- 接受日期：2026-08-17
- 决策记录：见本文件末尾「决策记录」节

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

## 决策记录

- 日期：2026-08-17
- 决策：**接受**（WF-001），附以下修订点
- 审批人：boyang wang
- 决策证据：
  - [`evidence/profile-diff.md`](../evidence/profile-diff.md)：现状 5 个开发 Profile 展开为完全相同 10 仓（F-010 量化）
  - [`docs/architecture/target-design.md`](../architecture/target-design.md) §4–5：目标精确集合与 typed 依赖矩阵

### 修订点

1. **REV-1（精确集合语义）**：`include_repositories` 为 Profile 精确工作区集合；`include_groups` 退回展示/检索/策略标签，不再参与工作区选择。Skills 始终 `required: false` 并置于 `optional_repositories`；Knowledge 仅存在于 `knowledge-dev` 与 `all`。
2. **REV-2（过渡期双字段解析）**：过渡期内：
   - 仅 `include_groups` → 按旧逻辑（向后兼容）；
   - 仅 `include_repositories` → 按精确集合；
   - 两者都存在 → 以 `include_repositories` 为准并发出 deprecated 警告。
   - `depends_on` ↔ `dependencies.product` 双解析，其余类型按 target-design §5.2 矩阵补全（`verification`/`tooling`/`discovery`/`context`）。

### 验收与迁移

- 迁移路径：兼容读取 → 迁移 Manifest（§4 建议集写入 7+1 个 Profile）→ deprecated 警告 → 两个发布周期后删除旧字段；
- Product DAG 必须无环；其余类型分别校验；context 永不成为 required；
- 关闭证据：M1 WF-002 的 exact-set、typed DAG/closure 测试（含负向：非 DAG、未知类型、缺失闭包）。
