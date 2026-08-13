# Lockfiles

Lockfile 是可复现性的核心，记录 Manifest 解析后的不可变状态（每个仓库的 canonical URL、resolved commit SHA、工具 Profile、Catalog commit 等）。

## 三类锁文件

| 类型 | 是否入库 | 用途 |
|---|---:|---|
| `baseline.lock.yaml` | 是 | 团队默认集成基线，受 PR 和 CI 保护 |
| `releases/*.lock.yaml` | 是 | 正式 Bundle/项目里程碑，不允许原地修改 |
| `.aix/local.lock.yaml` | 否 | 开发者当前解析结果，可包含本地分支 |

## 说明

- `baseline.lock.yaml` 与 `releases/` 下的示例文件展示了预期的结构；真实 SHA 需通过 `aix wf lock` 在已解析的真实仓库上生成，示例中的占位符**不得**提交为真实基线。
- 更新正式 Lockfile 必须经过完整跨仓资格验证，不能因为执行了一次 `sync` 就自动覆盖。
- 凭据不进入 Lockfile；所有 URL 来自 Manifest 批准 remote。

## 生成方式

```bash
# 本地解析（可包含本地分支/override）
aix wf lock --output .aix/local.lock.yaml

# 更新团队基线（需 PR + CI 保护）
aix wf lock --output locks/baseline.lock.yaml
```
