# ADR-0001：采用 Manifest + 独立 Clone，默认不用 Git Submodule

- 状态：接受
- 日期：2026-08-13

## 背景

AIXSILICON 需要同时管理 HWIF、CBB、IP、DV Common、VIP、Tool、Catalog、SoC Integration、Skill 等多个仓库，并需要“按清单下载、保持独立 Git 历史、跨仓验证与发布协调”。选择工作区组织方案是本平台的关键决策。

## 决策

采用 **Manifest 驱动的多仓工作区 + 独立 Git Clone**：

- 子仓就是普通 Git 仓库，直接使用原有分支、commit、push 和 PR；
- 父仓只版本化 Manifest、Lockfile、Schema、流程、公共 CI、脚本和文档；
- 子仓统一克隆到 `repos/`，`repos/` 被父仓 `.gitignore` 完整忽略；
- Manifest 描述开发分支；Lockfile 记录不可变 SHA。

## 备选方案

| 方案 | 结论 | 原因 |
|---|---|---|
| Git Submodule | 不采用 | 指针变化变成父仓变化，detached HEAD、递归操作与 PR 噪声 |
| 复制到 Workflow 并提交 | 禁止 | 双事实源、历史重复、发布边界消失 |
| Git Subtree | 不推荐 | 上游同步和历史处理复杂 |
| 仅 Shell 脚本 clone main | 不足 | 无 Schema、无版本锁、无依赖图、不可复现 |
| Monorepo | 当前不采用 | 破坏资产责任、授权与发布边界 |

## 结果

- 正向：子仓独立性完整保留，FuseSoC 多 Core Library 模型自然匹配，适合影响分析与 Release Train；
- 负向：需要自研轻量 CLI 与 Schema（对比 `repo` 的 XML Manifest），但更贴合 YAML SSOT 体系；
- 权衡：对 `repos/` 的写入保护（pre-commit Guard、CI Guard、CLI Safety）成为必要。
