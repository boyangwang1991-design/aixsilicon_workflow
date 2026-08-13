# catalog — AIXSILICON Catalog Repository 规划与待办（占位）

> 来源：`repos/aixsilicon_catalog_repo/`（原无独立 plan/todo 文件，仅有 `README.md`、`catalog/index.yaml`、`catalog/assets/*`、`schemas/catalog-asset.schema.json`）
> 状态：**📄 占位待建** —— 请在本文件补充 catalog 仓的规划与待办。
> 仓库实现现状见 [`../repos.md`](../repos.md) §1.7。

## 现状

- `catalog/index.yaml`：发布资产索引入口；
- `catalog/assets/`：首批资产条目（cbb-hac-adapters / dv-common-types / hwif-apb / hwif-hac-if / ip-hac-aes / ip-uart / vip-hac-if）；
- `schemas/catalog-asset.schema.json`：资产条目 Schema。

## 规划（待补充）

- [ ] 定义 Catalog 仓的定位、边界与生命周期（索引哪些资产、成熟度分级、兼容矩阵）；
- [ ] 明确发布/更新流程（生成草案 + PR，不自动 merge，配合 `release-train`）；
- [ ] 建立与 `aixsilicon_workflow` 发布流（`aix release publish`）的对接。

## 待办

- [ ] 补充本文件（规划正文）。
