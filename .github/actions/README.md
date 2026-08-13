# GitHub Actions

## Reusable Workflows（Workflow Repo 提供，版本锁定）

| 文件 | 用途 |
|---|---|
| `reusable-fusesoc-lint.yml` | 资产仓 FuseSoC lint 薄入口 |
| `reusable-unit-sim.yml` | 单元仿真薄入口 |
| `reusable-schema-check.yml` | YAML 事实 Schema 校验 |
| `reusable-release-gate.yml` | G7 发布就绪 Gate |
| `integration-baseline.yml` | 多仓 checkout + 兼容性 + 代表性回归 |
| `change-bundle.yml` | Change Bundle PR heads 联合验证 |

## 使用方式（资产仓薄入口）

```yaml
jobs:
  qualification:
    uses: boyangwang1991-design/aixsilicon_workflow/.github/workflows/reusable-unit-sim.yml@v1
    with:
      repo_type: vip
      target: unit_sim
    secrets: inherit
```

## 规则

- 公共 Workflow 引用必须固定 Release Tag 或 Commit SHA，不能长期引用 `main`；
- 默认 `contents: read`；只在发布 Job 中临时授予 `contents: write`；
- 私有仓共享 Actions 时评估日志与访问边界；
- 所有跨仓事件携带 `correlation_id` + depth，编排层拒绝超过深度的递归事件。
