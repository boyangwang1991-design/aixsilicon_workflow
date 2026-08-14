# catalog — 完整设计参考

> 本文保留建仓时的实现现状，不维护活动设计或状态。当前契约见 [`README.md`](README.md)，交付见 [`delivery.md`](delivery.md)。

> 来源：`repos/aixsilicon_catalog_repo/`（原无独立 plan/todo 文件，仅有 `README.md`、`catalog/index.yaml`、`catalog/assets/*`、`schemas/catalog-asset.schema.json`）
> 仓库边界同时见 [`../architecture/repos.md`](../architecture/repos.md)。

## 现状

- `catalog/index.yaml`：发布资产索引入口；
- `catalog/assets/`：首批资产条目（cbb-hac-adapters / dv-common-types / hwif-apb / hwif-hac-if / ip-hac-aes / ip-uart / vip-hac-if）；
- `schemas/catalog-asset.schema.json`：资产条目 Schema。

## 历史规划诉求

- [ ] 定义 Catalog 仓的定位、边界与生命周期（索引哪些资产、成熟度分级、兼容矩阵）；
- [ ] 明确发布/更新流程（生成草案 + PR，不自动 merge，配合 `release-train`）；
- [ ] 建立与 `aixsilicon_workflow` 发布流（`aix release publish`）的对接。

以上诉求已在当前 [`README.md`](README.md) 和 [`delivery.md`](delivery.md) 中结构化；此处不再维护完成状态。
