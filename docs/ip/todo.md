# ip — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/ip.md`](../archived/architecture/repo-plans/ip.md)。

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

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
