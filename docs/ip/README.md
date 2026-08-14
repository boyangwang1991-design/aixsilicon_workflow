# IP 仓设计契约

IP 仓是可独立集成、验证和发布的完整 IP 事实源。Owner 为 `ip-platform`；SoC 项目和 Catalog 是主要下游。

## 范围与边界

- 负责：IP 规格、SystemRDL、RTL、IP 专用验证环境、交付清单和发布记录；
- 不负责：HWIF 契约、公共 CBB、协议 VIP、通用 DV runtime、跨仓发布编排；
- 开发态允许 feature 分支编辑，发布态冻结为不可变版本目录/Tag；
- `.core` 生成与检查复用 tools，`ipkg` 只处理仓内源码级 stage/publish，跨仓 Gate/Catalog 由 Workflow 编排。

## 首个垂直切片

APB 寄存器 IP 是唯一 P0：HWIF Contract → SystemRDL → RTL/RAL/Header → APB VIP/DV Common → lint/build/sim → G0～G6 → approval/G7 → Release/Catalog。Bridge、PIC 和高级 IP 在该链稳定后再进入活动台账。

## 输入输出

| 输入 | 输出 |
|---|---|
| HWIF/CBB、SystemRDL、工具/验证 provider、固定 Lock | 规格、RTL、RAL/Header、Core/VLNV、验证结果、SBOM/RTM、Release Manifest |

## 验收出口

- 发布资产使用 `aixsilicon:ip:*`、SemVer、Tag 和不可变版本；
- SystemRDL 派生物可重建且漂移检查通过；
- qualification 只判 G0～G6，人工批准后的 release-train 才判 G7；
- 负向寄存器访问、reset、错误响应和缺能力场景不得 false green；
- Catalog 仅通过独立 PR 登记已发布版本。

活动交付见 [`delivery.md`](delivery.md)，历史设计和发布边界见 [`design-reference.md`](design-reference.md)。
