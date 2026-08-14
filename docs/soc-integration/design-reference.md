# soc-integration — 完整设计参考

> 本文保留建仓时的实现现状，不维护活动设计或状态。当前契约见 [`README.md`](README.md)，交付见 [`delivery.md`](delivery.md)。

> 来源：`repos/aixsilicon_soc_integration/`（原无独立 plan/todo 文件，仅有 `README.md`、`examples/*`、`schema/soc-config.schema.json`）
> 仓库边界同时见 [`../architecture/repos.md`](../architecture/repos.md)。

## 现状

- `schema/soc-config.schema.json`：SoC 配置 Schema（instance/address/irq/crg/power/connect 等事实域 Owner）；
- `examples/`：`minimal-soc.yaml`、`hac-accel-soc.yaml` 参考配置。

## 历史规划诉求

- [ ] 定义 SoC 集成 Schema、模板、规则的边界（通用能力 vs 具体产品 Top，后者归私有 `chip_<project>_soc_repo`）；
- [ ] 明确与 tools（TopGen/地址/中断/CRG 生成器）的输入输出契约；
- [ ] 明确与 `soc-integration` workflow 的校验/生成衔接。

以上诉求已在当前 [`README.md`](README.md) 和 [`delivery.md`](delivery.md) 中结构化；此处不再维护完成状态。
