# 发布与基线治理

## 发布子流程

```text
候选版本选择
→ Clean/Locked 环境确认
→ IP Qualification（G0~G7）
→ 文档/RTM/Manifest/SBOM 检查
→ 版本与 CHANGELOG 检查
→ 人工批准
→ 对应 IP 仓 Tag/Release
→ Catalog 更新 PR
→ Release Bundle 留证
```

## 发布 Gate（Release Readiness，G7）

- SemVer 与变更类型一致；
- CHANGELOG、文档、SBOM 和许可证完整；
- 所有仓库 clean 且固定 SHA；
- 无本地 override；
- 受保护环境人工批准完成；
- Catalog 更新内容已生成并 Review。

## 版本策略

- 每个资产仓独立使用 SemVer（HWIF 按 Contract 兼容性、VIP 按协议能力、IP 按交付兼容性等）；
- 可发布 `aix-workspace-bundle` 兼容组合，只包含 Lockfile、兼容矩阵、Tool Profile、Qualification Evidence 索引、Release Notes；
- Bundle 不重新打包所有源码，也不改变各仓 Release。

## Baseline 更新

```text
候选依赖版本
→ 解析候选 Lock
→ 全量兼容检查
→ 代表性回归
→ PR Review
→ 更新 baseline.lock.yaml
→ 发布 Bundle（里程碑时）
```

## 三类锁文件

| 类型 | 是否入库 | 用途 |
|---|---:|---|
| `baseline.lock.yaml` | 是 | 团队默认集成基线，受 PR 和 CI 保护 |
| `releases/*.lock.yaml` | 是 | 正式 Bundle/项目里程碑，不允许原地修改 |
| `.aix/local.lock.yaml` | 否 | 开发者当前解析结果，可包含本地分支 |

## 幂等与并发

- 发布动作必须幂等，可检测“已发布”而不是重复创建；
- 并发 Release 使用互斥组（GitHub Actions `concurrency`），防止同一资产重复发布；
- 发布需要 protected environment 人工批准；
- Fork PR 不得获得组织 Secret。
