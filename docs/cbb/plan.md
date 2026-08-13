# cbb — AIXSILICON CBB Repository 建设规划

> 客观事实基线：2026-08-13（骨架 + 构件清单）。原文细节见 [`../archived/architecture/repo-plans/cbb.md`](../archived/architecture/repo-plans/cbb.md)。

## 1. 定位与边界

**定位**：**PPA-aware CBB Platform**——经功能验证、实现验证和多维 PPA 表征，可按设计约束自动检索、比较、选型和集成的芯片公共基础构件平台。

**四类资产**：构件资产（A0–A4）/ 实现变体 / 参考架构与 Recipe / PPA 数据与证据。
**四个支撑平面**：质量验证 / PPA 表征与模型 / 生成集成与发布 / 检索推荐与选型。

| 分层 | 定位 | 示例 |
|---|---|---|
| A0 技术适配 | 隔离工艺/宏/平台 | SRAM/ICG/Isolation Wrapper |
| A1 原子机制 | 功能单一 | Mux/Encoder/Counter/LZC/Synchronizer |
| A2 通用复合 | 协议无关 | FIFO/Arbiter/Adder Tree/Register File/ECC |
| A3 协议构件 | 带握手/总线语义 | Ready-Valid Slice/AXI Buffer/APB Adapter |
| A4 子系统模板 | 可配置系统能力 | AXI Fabric/Memory Subsystem（复杂时升级为 IP） |

## 2. 现状（客观）

- 仓库骨架 + 完整构件清单（registry ~330 项登记）；
- 目录齐备：components/adapters/recipes/schemas/verification/flows/docs；
- **缺口**：P0 15 种子构件多为 planned（未 verified）；`cbb.yaml` SSOT 未落地；无 PPA 表征数据。

## 3. 依赖与角色

- **依赖**：`[hwif]`（CBB 实现依赖 HWIF；验证可依赖 DV-Common/VIP，实现不依赖）；
- **被依赖**：ip、soc-integration；
- **IP 主线角色**：IP 复用 CBB 构件，`tool.ppa-bench` 可做参数化 PPA 评估；
- **SoC 主线角色**：作为实例化单元进入 SoC。

## 4. 契约

- **VLNV**：`aixsilicon:cbb:*`；
- **Schema 所有权**：`cbb-metadata / params / result`；
- **成熟度**：E0–E5（E0/E1→draft；E2/E3→qualified；E4/E5→proven）；
- **SSOT**：每构件 `cbb.yaml`（机器可读），文档由元数据/结果生成。

## 5. 建设路线（客观）

| 阶段 | 目标 | 状态 |
|---|---|---|
| Phase 0 定义 | 边界/Schema/基准环境/Gate/种子清单 | 🔶 定义完成、实现待做 |
| Phase 1 MVP | 15 种子构件 + Catalog + 表征/比较闭环 | ⬜ |
| Phase 2 PPA 产品化 | 多实现/Pareto/Selector/回归/试点 | ⬜ |
| Phase 3 规模化 | 协议构件/Recipe/技术适配/多项目 | ⬜ |
| Phase 4 智能化 | Pattern Scanner/AI Advisor | ⬜ |

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/cbb.md`](../archived/architecture/repo-plans/cbb.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
