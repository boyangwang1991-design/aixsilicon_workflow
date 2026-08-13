# catalog — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/catalog.md`](../archived/architecture/repo-plans/catalog.md)。

## 已完成

- [x] `catalog/index.yaml` 索引入口
- [x] 首批 7 条资产条目（cbb-hac-adapters / dv-common-types / hwif-apb / hwif-hac-if / ip-hac-aes / ip-uart / vip-hac-if）
- [x] `catalog-asset.schema.json`（Schema 所有权）

## P0 优先

- [ ] 首批 `qualified` 资产条目（IP / HWIF / DV-Common 各至少 1）
- [ ] 定义 Catalog 仓定位、边界与生命周期（索引范围、成熟度分级、兼容矩阵）

## P1 首个季度

- [ ] 兼容矩阵与成熟度映射落地（各仓内部词汇 → `draft/qualified/proven/deprecated`）
- [ ] 随各仓 release 自动/受控更新（`aix release publish` → Catalog PR，不自动 merge）

## 治理

- [ ] 只索引发布资产、与 Workspace Manifest 不重复（C 类）
- [ ] 与 `release-train` / `cross-repo-qualification` 的依赖一致性检查

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
