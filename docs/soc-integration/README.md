# SoC Integration 仓设计契约

SoC Integration 保存通用 SoC 配置 Schema、模板、集成规则和 Golden 示例。Owner 为 `soc-platform`；具体芯片事实写入私有 `chip-<project>-soc`，确定性生成器归 Tools。

## 范围与边界

- 负责：instance/address/IRQ/CRG/power/connect 等输入事实域、通用 tie-off/default-slave/timeout/CDC-RDC 规则和最小示例；
- 不负责：具体产品配置/Top、资产源码、生成器实现、商业 PDK/Memory/EDA adapter；
- Catalog 负责发布资产发现，Lock 固定精确版本；SoC Schema 不复制 Catalog 或 HWIF 事实；
- 先冻结最小 Schema/Golden，M3/M4 稳定前不铺开大规模 socgen。

## 最小 SoC 切片

从 Catalog 选择已发布 APB IP，实例化并分配地址/IRQ/clock/reset，生成软件 Header 和 Top 草案，执行 Schema、地址冲突、IRQ、连接、接口兼容、编译/仿真和 boot smoke，最后形成 baseline Lock 与 G0～G6 Evidence。

## 验收出口

- 输入/输出 Schema 正负样例覆盖重叠地址、缺端点、宽度/时钟/reset 不兼容和非法连接；
- 生成物标明来源/hash，可重建且不覆盖手写区；
- Golden 在固定 Catalog/Lock/provider 下通过 compile/sim/boot smoke；
- 通用仓与具体产品仓写入边界由 ownership 校验；
- 是否建立 `sw`/`reference-soc` 独立仓由触发门决定，不预先形成硬依赖。

活动交付见 [`delivery.md`](delivery.md)，历史仓现状见 [`design-reference.md`](design-reference.md)。
