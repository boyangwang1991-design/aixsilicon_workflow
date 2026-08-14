# ip — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/ip.md`](../archived/architecture/repo-plans/ip.md)。
> 本文件已并入 archived 原文的首批 IP 与路线图（§3）、验收标准（§4）与跨仓一致性修订（§5），并追加仓级待办。

## P0 优先

- [ ] 首个 APB 寄存器 IP（SystemRDL/RAL/RTL）发布为 `aixsilicon:ip:*`
- [ ] registry / ipkg 对齐统一契约（VLNV、SemVer、Tag）
- [ ] `.core` 生成/lint 复用 `aix-core-tool`（R7）
- [ ] 双态模型落地：dev 分支可编辑 / `ipkg stage` 冻结版本目录（A1）
- [ ] G0–G5 门禁产物（配合 `aix release prepare`）

## P1 首个季度

- [ ] X2X / AXI Bridge（宽度、Outstanding、异步时钟）
- [ ] IP 验证环境接入 dv-common + vip（APB VIP）

## P2 两个季度

- [ ] PIC 功能安全中断控制器
- [ ] `reference/` 治理：只读参考、不发布、不进 fusesoc 正式发现（A2）
- [ ] 完整 IP 交付：文档/RTM/发布记录

## 仓级待办（本批追加）

- [ ] 首个 APB 寄存器 IP 发布：出口 `aixsilicon:ip:apb_csr` 可被 Catalog 查询并经 `aix release` 资格验证
- [ ] registry / ipkg 对齐统一契约（VLNV、SemVer、Tag）、`.core` 复用 `aix-core-tool`（R7）
- [ ] 双态模型落地（A1）：dev 分支可编辑 / `ipkg stage` 冻结版本目录
- [ ] G0–G5 门禁产物（Gate 报告 + canonical 模型/SHA 哈希，配合 `aix release prepare`）

## 变更记录

| 日期 | 变更内容 | 作者 |
|------|---------|------|
| 2026-08-13 | 创建 todo.md：P0 首个 APB 寄存器 IP、registry/ipkg 契约、R7、A1、G0–G5 门禁 | Zoo |
| 2026-08-13 | 本文件并入 archived 原文首批 IP 与路线图、验收标准、跨仓一致性修订（合并补充）并追加仓级待办（出口 `aixsilicon:ip:apb_csr`） | Zoo |

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/ip.md` §3 首批 IP 与路线图、§4 验收、§5 跨仓一致性修订（A1/A2/R4/R7）；仓级待办为本批追加。
