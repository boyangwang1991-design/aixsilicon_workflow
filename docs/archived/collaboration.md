# 跨仓协作与 Change Bundle

一个功能可能同时涉及 HWIF、VIP、IP、Skill 与 Workflow 多个仓库。Git 无法原生提供跨仓原子提交，因此用 **Change Bundle** 建立这些独立变更之间的逻辑关系与验证/合并顺序。

## Change Bundle 文件

Schema：[`schemas/change-bundle.schema.json`](../schemas/change-bundle.schema.json)
示例：[`changesets/examples/CHG-2026-0042.yaml`](../changesets/examples/CHG-2026-0042.yaml)

```yaml
schema_version: aix.change-bundle/v1
id: CHG-2026-0042
title: AXI USER sideband端到端支持
owner: wang-boyang
status: validating
repositories:
  hwif:
    branch: feature/axi-user-contract
    base: main
    pr: 128
    merge_order: 1
  vip:
    branch: feature/axi-user-vip
    base: main
    pr: 207
    depends_on: [hwif]
    merge_order: 2
  ip:
    branch: feature/x2x-axi-user
    base: main
    pr: 381
    depends_on: [hwif, vip]
    merge_order: 3
```

## 状态机

```text
draft → ready → validating → review → merge-ready → merged → released → closed
                         ↘ blocked
```

## 合并规则

- 各仓必须独立 Review 并通过本仓 CI；
- Bundle CI 拉取所有 PR HEAD 做联合测试；
- 按依赖顺序合并（`merge_order`）；
- 上游合并后，下游必须 rebase/merge 并用上游真实 SHA 重测；
- 合并不具备分布式事务语义，失败时停止后续合并并修复 PR；
- Release Bundle 记录所有最终 SHA 与对应 Release；
- Bundle 文件不保存访问 Token。

## 影响分析

输入：Git diff、Manifest 依赖图、FuseSoC Core 依赖图、HWIF 消费者索引、VIP binding、Test-to-Requirement 映射。

保守原则：

- 影响图不完整时**扩大**测试范围，不静默缩小；
- 无法解析动态脚本依赖时标记 `UNKNOWN`；
- Release Gate 不能仅依赖文件路径规则；
- AI 可辅助解释影响原因，但确定性规则决定最低必测集合。

## 跨仓 CI 触发

1. 资产仓 PR 完成后，通过 API 触发 Workflow Repo 的 `workflow_dispatch`；
2. Change Bundle PR 变更时由 Workflow Repo checkout 指定 PR refs；
3. 正式 Release 后发送受控 `repository_dispatch` 更新 Catalog；
4. Nightly 由 Workflow Repo 定时解析最新合格版本，发现漂移但不自动改 baseline。

所有事件携带 `correlation_id`、source repo、source SHA 和 depth；禁止跨仓事件环。
