# cbb — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/cbb.md`](../archived/architecture/repo-plans/cbb.md)。
> 本文件已并入 archived 原文的 Phase 0–4 路线（§13）、P0 15 种子清单（§12.1）、3 个示范闭环（§17）、成熟度映射（§7.2）与变更记录。

## P0 优先

- [ ] P0 15 种子构件从 planned → verified（Priority Encoder/Mux/RR Arbiter/Address Decoder/Counter/LZC/Adder Tree/Sync FIFO/Async FIFO/Skid/Register Slice/SRAM Wrapper/Synchronizer 族/ICG/Reset Sync/AXI Register Slice）
- [ ] `cbb.yaml` SSOT + 统一验证 harness 落地
- [ ] 3 个示范闭环（32 路仲裁器 / Ready-Valid 长链 / FIFO 存储映射）
- [ ] 至少 10 个构件达 E2/E3，Catalog 可检索

## P1 首个季度

- [ ] Compressor/CSA Tree、常系数乘法器、流水 MAC
- [ ] 分层 Mux / 分层仲裁
- [ ] Register/SRAM FIFO 自动切换、Banked Memory Recipe
- [ ] AXI Buffer / Outstanding Limiter / Width Converter
- [ ] 选型器（Selector）、PPA 回归、项目试点

## P2 两个季度

- [ ] AXI/APB 桥、AXI CDC、分层互联模板
- [ ] 多 Bank 存储子系统、资源共享、低功耗缓冲
- [ ] RTL Pattern Scanner、AI PPA Advisor
- [ ] 30–50 个 E4 资产，多项目复用

## 阶段路线（Phase 0–4）

| 阶段 | 周期建议 | 主要目标 | 退出条件 |
|---|---|---|---|
| Phase 0 定义 | 4–6 周 | 边界、Schema、基准环境、Gate、仓库、种子清单 | 规范评审通过，3 个样例跑通 |
| Phase 1 MVP | 2–3 个月 | 15 种子构件、Catalog、表征与比较闭环 | 至少 10 个达 E3，项目可检索使用 |
| Phase 2 PPA 产品化 | 3–4 个月 | 多实现、Pareto、Selector、回归、首个试点 | 形成可复现收益和项目替换案例 |
| Phase 3 规模化 | 4–6 个月 | 协议构件、Recipe、技术适配、多项目推广 | 30–50 个 E4 资产，多项目复用 |
| Phase 4 智能化 | 持续 | Pattern Scanner、AI Advisor、闭环优化 | AI 建议均有工具证据和可追溯结果 |

## P0 15 种子构件清单

1. Priority Encoder
2. One-hot/Binary Mux
3. Round-Robin Arbiter
4. Address Decoder
5. Counter/Timer
6. Popcount/LZC
7. Adder Tree
8. Sync FIFO
9. Async FIFO
10. Skid Buffer
11. Ready/Valid Register Slice
12. SRAM Wrapper
13. Bit/Pulse/Handshake Synchronizer 族
14. ICG/Reset Synchronizer Wrapper
15. AXI Register Slice

这 15 项覆盖选择、仲裁、算术、存储、流水、CDC、时钟复位和协议，足以验证整个平台是否真实可用。

## 3 个示范闭环详情

- **场景一：32 路仲裁器**——对比 Linear Priority / Mask RR / Rotate+Priority / Hierarchical RR，在 250/500/800 MHz 和不同请求活动率下形成 Pareto 曲线，验证“选型而非固定最佳实现”。
- **场景二：Ready/Valid 长链**——对比 Bypass / Forward Slice / Skid / Full Slice / Pipeline FIFO，展示组合 Ready 路径、吞吐、首拍延迟和面积之间的关系，并形成自动插入 Recipe。
- **场景三：FIFO 存储映射**——扫描数据宽度和深度，对比 Register / Shift / SRAM / Banked SRAM，实现从参数到存储结构的自动选择，并覆盖功耗活动场景。

三个场景分别验证控制路径、协议流水和存储映射，较完整检验 CBB 平台价值。

## 成熟度 E0–E5 状态映射

- E0 Concept（不进入 Catalog）↔ draft
- E1 Functional（仅探索）↔ draft
- E2 Verified（非关键场景试用）↔ qualified 路径
- E3 Characterized（可供选型器推荐）↔ qualified
- E4 Released（项目可正式依赖）↔ proven
- E5 Proven（默认优选资产）↔ proven

清单治理状态：`candidate → incubator → qualified → released → preferred → deprecated → retired`；本清单定义“候选全集”，实际建设顺序由跨项目复用频率、PPA 潜在收益、正确性风险、现有资产成熟度和表征成本共同决定。

## 跨仓治理

- [ ] VLNV 统一 `aixsilicon:cbb:*`（C3）
- [ ] `cbb-catalog` → `aixsilicon_catalog_repo`；`cbb-tech-<node>` → 私有 overlay / techlib（A3/A4）
- [ ] 验证依赖方向（CBB 实现依赖 HWIF；验证可依赖 DV-Common/VIP）

## 变更记录

| 日期 | 变更内容 | 作者 |
|------|---------|------|
| 2026-08-13 | 创建 todo.md：P0 15 种子、cbb.yaml SSOT、3 示范闭环、E2/E3 检索、跨仓治理 | Zoo |
| 2026-08-13 | 本文件并入 archived 原文 Phase 0–4 路线、15 种子构件清单、3 个示范闭环详情、E0–E5 映射与清单治理状态（合并补充） | Zoo |

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/cbb.md` §13 分阶段实施路线、§12.1 P0 15 种子构件、§17 示范闭环、§7.2 成熟度等级、§24 清单治理建议。
