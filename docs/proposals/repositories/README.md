# 候选 Repo 提案

本目录用于在建仓前审查职责、触发条件和最小切片。提案状态不进入 Manifest、Lock、Flow required closure、路线图承诺或开发进度。

| 候选 | 提案 | 当前建议复审点 |
|---|---|---|
| techlib | [`techlib.md`](techlib.md) | M5，出现两类适配与两个消费者 |
| model | [`model.md`](model.md) | 任意阶段，两个 IP 共享同一模型且需独立发布 |
| sw | [`sw.md`](sw.md) | M6 前，BSP/Boot/HAL 出现独立生命周期 |
| reference-soc | [`reference-soc.md`](reference-soc.md) | M6 后，Golden 稳定且需要独立发布 |

## 激活门禁

1. 至少两个真实消费者，或由 ADR 批准的强制例外；
2. 与现有仓不同的独立版本/发布/权限生命周期；
3. 唯一 Owner、Schema/路径边界和依赖类型；
4. 首个 PR 包含最小资产、README、测试和 CI，而非空骨架；
5. Manifest/Profile/ownership/Catalog/Workflow 影响已评审；
6. 退出、合并回现有仓和迁移策略明确。
