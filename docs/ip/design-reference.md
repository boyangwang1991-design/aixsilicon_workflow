# ip — 完整设计参考

> 完整保留历史设计要求；当前设计见 [`README.md`](README.md)，活动交付见 [`delivery.md`](delivery.md)，组合状态见 [`../progress.md`](../progress.md)。

> 来源：repos/aixsilicon_ip_repo/plan.md（完整剪切至 docs/architecture/repo-plans 统一管理）
> 迁移日期：2026-08-13
> 仓库实现现状见 docs/architecture/repos.md §1.3

---

## 一、plan.md 完整原文

# AIXSILICON IP Repository 规划

> 版本：V0.1
> 日期：2026-08-13
> 定位：可独立集成与发布的完整 IP 的统一仓库（monorepo）。

## 1. 建设结论

`aixsilicon_ip_repo` 是 **IP 事实源与交付的统一仓**：保存 IP 规格、SystemRDL、RTL、
IP 专用验证环境与发布记录；FuseSoC 只 add 本仓即可发现全部 IP。

- **VLNV 命名空间**：`aixsilicon:ip:<ip>:<version>`（ADR-0003；历史 `boyangwang1991-design:ip` 走 deprecated 别名窗口）；
- **目录组织**：`ips/<vendor>/<ip>/<version>/` 不可变版本目录，`registry.yaml` 内嵌索引；
- **入库/发布**：`ipkg`（本仓工具）负责 stage/publish；Workflow 的 `aix release` 编排与
  Catalog 更新不替代 ipkg 的源码级发布，二者通过 manifest/tag 对齐。

## 2. 边界

| 内容 | 归属 |
|---|---|
| IP 规格 / SystemRDL / RTL / IP 验证 / 交付 | 本仓 |
| 接口契约（HWIF） | `aixsilicon_hwif_repo` |
| 通用验证基础设施（DV Common） | `aixsilicon_dv_common` |
| 协议 VIP | `aixsilicon_vip_repo` |
| 确定性工具（CSR/HWIF/Core 生成） | `aixsilicon_tool_repo` |
| 已发布资产索引 | `aixsilicon_catalog_repo` |
| 私有 Skill / 方法论 | `aixsilicon_skill_repo`（私有） |

## 3. 首批 IP 与路线图

- P0：APB 寄存器型 IP 端到端穿刺（HWIF→SystemRDL/RAL→RTL→VIP→DV Common→Evidence→Catalog）；
- P1：X2X/AXI Bridge（宽度/Outstanding/异步时钟）；
- P2：PIC 中断控制器（功能安全语义）。

## 4. 验收

- 每个发布 IP 具有 `aixsilicon:ip:*` VLNV、SemVer、Tag 与 registry 条目；
- 生成物（RTL/RAL/Header）由 SystemRDL 确定性派生，禁止手改漂移；
- 发布前经过 G0–G7 Gate（`aix release prepare`）且工作区 clean/locked。

---

## 5. 跨仓一致性修订（2026-08-13）

> 依据历史 [`cross-repo-architecture-review.md`](../reference/cross-repo-architecture-review.md)（ADR-0003/0006）。

- **双态模型（A1）**：开发源码在 feature 分支可编辑；发布时 `ipkg stage` 冻结为 `ips/<vendor>/<ip>/<version>/` 不可变版本；`registry.yaml` 只索引已发布版本；workflow dev 模式指向分支、release 模式指向 tag/SHA；
- **Core 生成边界（R7）**：`.core` 生成/lint 复用 `aixsilicon_tool_repo` 的 `aix-core-tool`，ipkg 调用而非另造第二套；
- **vendored `reference/` 治理（A2）**：只读参考、不发布、不进入 fusesoc 正式发现与 Catalog；
- **发布职责（R4）**：ipkg = 本仓源码级发布；跨仓 Gate/协调/Catalog 更新由 workflow `aix release` 编排。
