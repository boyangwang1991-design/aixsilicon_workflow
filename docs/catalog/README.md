# Catalog 仓设计契约

Catalog 是已发布资产、版本、成熟度、兼容关系和获取信息的索引，不是源码仓、开发工作区选择器或发布审批系统。Owner 为 `release-platform`；SoC resolve、资产发现和发布流程是主要消费者。

## 事实边界

- Catalog 条目只引用已存在的不可变 Tag/Release、VLNV 和证据，不复制资产源码；
- Manifest 选择期望仓，Lock 固定实际 SHA，Catalog 发现已发布资产，三者互不替代；
- 资产仓拥有版本与发布材料；Catalog 拥有索引 Schema、兼容边和生命周期视图；
- Workflow 只生成 Catalog diff/PR，不直接写 main，也不在 Catalog 中伪造成熟度。

## 条目最小字段

identity/VLNV、asset type、version、source/release URI、commit/tag、owner、license/visibility、maturity、compatibility、dependencies、tool/profile requirements、evidence/SBOM/RTM links、deprecation/replacement 和 schema version。

## 生命周期

`candidate` 仅存在于 release bundle，不进入公共索引；人工批准和资产 Release 成功后生成 Catalog PR；Review 后进入 `qualified/released`；deprecated/yanked 保留历史和替代路径。重复 publish 必须幂等，来源失效或证据不一致必须阻断。

## 验收出口

- Schema 正负样例和兼容迁移测试通过；
- 首个 APB HWIF/VIP/IP 条目能从 Release/Evidence 反向验证；
- resolve 对不存在、yanked、冲突版本和不兼容 profile 给出确定性结果；
- Catalog PR 可审查、可重放、不可绕过资产发布和人工批准。

活动交付见 [`delivery.md`](delivery.md)，历史仓现状见 [`design-reference.md`](design-reference.md)。
