# 历史与设计参考

本目录完整保存早期总体需求、工程化评审和跨仓方案，供追溯设计理由与未迁移细节。这里的日期、百分比、Todo、仓库状态和优先级均为历史上下文，不构成当前承诺。

| 参考材料 | 内容来源 | 当前权威落点 |
|---|---|---|
| [`workflow-requirements.md`](workflow-requirements.md) | 旧 root 总体需求与契约细节 | 架构、workflow 契约、roadmap |
| [`workflow-repo-plan.md`](workflow-repo-plan.md) | 统一十仓建设全景 | architecture、roadmap、各仓 README/delivery |
| [`workflow-engineering-review.md`](workflow-engineering-review.md) | CLI、Schema、任务入口和 CI 工程评审 | workflow plan/todo |
| [`cross-repo-architecture-review.md`](cross-repo-architecture-review.md) | 早期重复建设与边界审查 | architecture target-design、ADR |
| [`cross-repo-optimization-plan.md`](cross-repo-optimization-plan.md) | 早期跨仓优化决策 | architecture target-design、roadmap |

使用规则：

- 只补充来源说明、迁移链接或勘误，不在此维护状态；
- 当前架构以 [`../architecture/`](../architecture/README.md) 为准；
- 当前跨仓顺序和状态以 [`../roadmap.md`](../roadmap.md) 与 [`../progress.md`](../progress.md) 为准；
- 当前 Workflow 实现契约以 [`../workflow/`](../workflow/README.md) 为准；
- 当前仓级设计与任务分别以 `docs/<repo>/README.md` 和 `delivery.md` 为准。
