# soc-integration — AIXSILICON SoC Integration Repository 规划与待办（占位）

> 来源：`repos/aixsilicon_soc_integration/`（原无独立 plan/todo 文件，仅有 `README.md`、`examples/*`、`schema/soc-config.schema.json`）
> 状态：**📄 占位待建** —— 请在本文件补充 soc-integration 仓的规划与待办。
> 仓库实现现状见 [`../repos.md`](../repos.md) §1.8。

## 现状

- `schema/soc-config.schema.json`：SoC 配置 Schema（instance/address/irq/crg/power/connect 等事实域 Owner）；
- `examples/`：`minimal-soc.yaml`、`hac-accel-soc.yaml` 参考配置。

## 规划（待补充）

- [ ] 定义 SoC 集成 Schema、模板、规则的边界（通用能力 vs 具体产品 Top，后者归私有 `chip_<project>_soc_repo`）；
- [ ] 明确与 tools（TopGen/地址/中断/CRG 生成器）的输入输出契约；
- [ ] 明确与 `soc-integration` workflow 的校验/生成衔接。

## 待办

- [ ] 补充本文件（规划正文）。
