# 跨仓协作与 Change Bundle

一个功能可能同时涉及 HWIF、VIP、IP、Skill 与 Workflow 多个仓库。Git 无法原生提供跨仓原子提交，因此用 **Change Bundle** 建立这些独立变更之间的逻辑关系与验证/合并顺序。

## Change Bundle 文件

Schema：[`schemas/change-bundle.schema.json`](../../schemas/change-bundle.schema.json)
示例：[`changesets/examples/CHG-2026-0042.yaml`](../../changesets/examples/CHG-2026-0042.yaml)

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

validation:
  profile: ip-dev
  flow: cross-repo-qualification
  required_targets:
    - aixsilicon:vip:axi:unit
    - aixsilicon:ip:x2x:regression

release_plan:
  hwif: 2.0.0
  vip: 1.4.0
  ip: 1.1.0
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

输入：Git diff 与 changed files、Manifest 仓库依赖图、FuseSoC Core dependency graph、HWIF contract 消费者索引、VIP binding 关系、Test-to-Requirement 和 Test-to-Core 映射、历史失败与 Flaky 标签。

输出示例：

```yaml
change:
  repository: hwif
  paths: [interfaces/axi/contract.yaml]
affected:
  direct:
    - aixsilicon:vip:axi
    - aixsilicon:cbb:axi_width_converter
  transitive:
    - aixsilicon:ip:x2x
required_gates:
  - hwif-schema
  - hwif-generated-diff
  - axi-vip-unit
  - x2x-smoke
recommended_gates:
  - x2x-regression
```

保守原则：

- 影响图不完整时**扩大**测试范围，不静默缩小；
- 无法解析动态脚本依赖时标记 `UNKNOWN`；
- Release Gate 不能仅依赖文件路径规则；
- AI 可辅助解释影响原因，但确定性规则决定最低必测集合。

## GitHub 协作架构

### 两层 CI

| 层级 | 所在仓库 | 职责 |
|---|---|---|
| Repo CI | 每个资产仓 | 本仓 Lint、Unit、Schema、文档、包检查 |
| Integration CI | Workflow Repo | 多仓 checkout、兼容性、代表性回归、Bundle 和 Release Train |

### Reusable Workflow 策略

Workflow Repo 提供版本化公共工作流：`reusable-fusesoc-lint.yml`、`reusable-unit-sim.yml`、`reusable-schema-check.yml`、`reusable-release-gate.yml`、`integration-baseline.yml`、`change-bundle.yml`。资产仓只保留薄调用：

```yaml
jobs:
  qualification:
    uses: aixsilicon/aixsilicon_workflow/.github/workflows/reusable-unit-sim.yml@v1
    with:
      repo_type: vip
      target: unit_sim
    secrets: inherit
```

公共 Workflow 引用必须固定 Release Tag 或 Commit SHA，不能长期引用 `main`。私有仓共享 Actions 时需评估日志和访问边界。

### 跨仓 CI 触发

1. 资产仓 PR 完成后，通过 API 触发 Workflow Repo 的 `workflow_dispatch`；
2. Change Bundle PR 变更时由 Workflow Repo checkout 指定 PR refs；
3. 正式 Release 后发送受控 `repository_dispatch` 更新 Catalog；
4. Nightly 由 Workflow Repo 定时解析最新合格版本，发现漂移但不自动改 baseline。

所有事件携带 `correlation_id`、source repo、source SHA 和 depth；禁止形成“仓 A 触发仓 B、仓 B 又触发仓 A”的事件环，编排层拒绝超过允许深度的递归事件。

### 权限

- 默认 `contents: read`；只在发布 Job 中临时授予 `contents: write`；
- PR 检查不持有发布 Token；跨仓 Token 使用 GitHub App 或组织批准的短期凭据；
- 环境 Secret 按 blue-zone/red-zone 和项目隔离；发布需要 protected environment 人工批准；
- Fork PR 不得获得组织 Secret。

## Skill 协同调用契约

每个 Skill 通过声明式 Metadata 告诉 Workflow：输入资产类型、输出资产 owner 仓与允许路径、前置 Gate、依赖的工具和 Core、是否允许修改文件、人工确认点、结果 Schema、后续消费者：

```yaml
skill:
  id: aix.ip.release
  version: 1.0.0
  inputs:
    repo: ip
    ip_vlnv: required
    candidate_version: required
  writes:
    - repo: ip
      paths: [metadata, docs, release]
    - repo: workflow
      paths: [changesets]
  gates:
    - ip-qualification
    - release-policy
  approval:
    required_before: [commit, tag, publish, catalog-update]
```

AI 与确定性工具边界：AI 负责需求理解、内容生成、变更解释、失败归因建议和流程推荐；YAML SSOT 固化接口、配置、版本、依赖和发布事实；脚本负责 Schema 校验、生成、Git 操作、影响计算和证据整理；事实未知时写 `TBD` 并阻断相应 Gate，不允许 AI 猜测通过。
