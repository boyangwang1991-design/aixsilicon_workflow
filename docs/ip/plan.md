# ip — AIXSILICON IP Repository 建设规划

> 客观事实基线：2026-08-13（建仓，uart 0.1.0）。原文细节见 [`../archived/architecture/repo-plans/ip.md`](../archived/architecture/repo-plans/ip.md)。

## 1. 定位与边界

**定位**：IP **事实源与交付的统一仓**（monorepo）——保存 IP 规格、SystemRDL、RTL、IP 专用验证环境与发布记录；FuseSoC 只 add 本仓即可发现全部 IP。

| 归属本仓 | 归属其他仓 |
|---|---|
| IP 规格 / SystemRDL / RTL / IP 验证 / 交付 | 接口契约 → hwif |
| `ips/<vendor>/<ip>/<version>/` 不可变版本目录 + `registry.yaml` | 通用验证底座 → dv-common |
| `ipkg`（本仓源码级发布工具） | 协议 VIP → vip |
| | 确定性工具（CSR/HWIF/Core 生成）→ tools |
| | 已发布资产索引 → catalog |

## 2. 现状（客观）

- 已建仓：`ipkg`、`registry.yaml`、`ips/`、`fusesoc.conf`；
- 已发布 `uart` 0.1.0（`aixsilicon:ip:uart`）；
- **缺口**：首个 APB 寄存器 IP 内容与发布；registry/ipkg 与统一契约全面对齐。

## 3. 依赖与角色

- **依赖**：`[hwif, cbb]`（IP 实现依赖 HWIF/CBB；IP 验证依赖 VIP/DV-Common）；
- **被依赖**：soc-integration；
- **IP 主线角色**：**核心写入方**——spec/contract/csr/rtl/dv 各阶段写入 `ips/`，发布前在此联合验证与打包；
- **SoC 主线角色**：作为实例化资产进入 SoC（经 catalog 选型）。

## 4. 契约

- **VLNV**：`aixsilicon:ip:<ip>:<version>`（历史 `boyangwang1991-design:ip` 走 deprecated 别名窗口）；
- **双态模型（A1）**：开发源码在 feature 分支可编辑；发布时 `ipkg stage` 冻结为版本目录；`registry.yaml` 只索引已发布版本；workflow dev 模式指向分支、release 模式指向 tag/SHA；
- **生成边界（R7）**：`.core` 生成/lint 复用 `aixsilicon_tool_repo` 的 `aix-core-tool`，ipkg 调用而非另造第二套。

## 5. 建设路线（客观）

| 目标 IP | 说明 | 状态 |
|---|---|---|
| P0：APB 寄存器型 IP 端到端穿刺 | HWIF→SystemRDL/RAL→RTL→VIP→DV Common→Evidence→Catalog | ⬜（当前编排级） |
| P1：X2X/AXI Bridge | 宽度/Outstanding/异步时钟 | ⬜ |
| P2：PIC 中断控制器 | 功能安全语义 | ⬜ |

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/ip.md`](../archived/architecture/repo-plans/ip.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
