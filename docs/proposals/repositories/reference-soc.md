# Reference SoC 候选仓提案

建议状态：M6 后复审，当前示例继续留在 `soc-integration`。

## 拟解决的问题

当最小 SoC Golden 成为独立可发布产品，用于演示、回归、软件启动和生态集成时，为其提供独立配置、Top、软件和 Release 生命周期。

## 边界

- 拟负责：特定参考产品的配置/Top/集成验证/发布材料；
- 通用 Schema/规则归 soc-integration，生成器归 tools，资产来源归各资产仓/Catalog；
- 不成为所有项目的万能模板，不包含私有 PDK/产品数据。

## 建仓触发与首个切片

soc-integration 中的 Golden 已在固定 Catalog/Lock 下稳定通过 compile/sim/boot smoke，且需要独立版本、下载或外部消费者。首个 PR 必须从原示例可追溯迁移，包含 Qualification G0～G6、Release G7 与恢复/兼容策略。

## 需要的决策

Owner、与 sw 候选仓的组合方式、发布物、支持平台和长期维护预算需 ADR 批准。
