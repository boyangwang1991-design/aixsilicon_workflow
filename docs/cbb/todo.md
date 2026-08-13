# cbb — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/cbb.md`](../archived/architecture/repo-plans/cbb.md)。

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

## 跨仓治理

- [ ] VLNV 统一 `aixsilicon:cbb:*`（C3）
- [ ] `cbb-catalog` → `aixsilicon_catalog_repo`；`cbb-tech-<node>` → 私有 overlay / techlib（A3/A4）
- [ ] 验证依赖方向（CBB 实现依赖 HWIF；验证可依赖 DV-Common/VIP）

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
