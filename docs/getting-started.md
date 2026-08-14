# Getting Started

本文档面向新成员，说明如何一次获得完整、正确的 AIXSILICON 开发环境。

## 前置条件

- Python 3.11+（推荐 3.12）
- Git 2.30+
- SSH Key 已配置并加入 GitHub 账号（`boyangwang1991-design` 组织下仓库）
- 可选：FuseSoC（`pip install fusesoc`）

## 1. 克隆 Workflow 仓库

```bash
git clone git@github.com:boyangwang1991-design/aixsilicon_workflow.git
cd aixsilicon_workflow
```

## 2. 安装 CLI

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -e ".[dev]"
alias aix=".venv/bin/aix"
```

> 若使用系统 `python`/`pip`，也可执行 `python -m pip install -e ".[dev]"`，但推荐统一用 `uv` 管理的 `.venv`。

## 3. 选择 Profile 并初始化

> 当前命令仍使用 Manifest v1 的 `include_groups` 语义。现有 `minimal` 和各开发 Profile 启用范围偏大；优化目标与兼容迁移见 [`architecture/target-design.md`](architecture/target-design.md) §4 和 [ADR-0007](adr/0007-typed-dependencies-and-explicit-profiles.md)。在 ADR 落地前，下表描述的是当前运行行为，不代表目标闭包。

各 Profile 覆盖不同的开发场景：

| Profile | 用途 |
|---|---|
| `minimal` | 最小编译所需（base 组） |
| `ip-dev` | IP 设计验证开发 |
| `cbb-dev` | CBB 设计验证开发 |
| `dv-dev` | 验证环境开发 |
| `soc-integration` | SoC 集成 |
| `release` | 正式发布基线 |

```bash
aix wf init --profile ip-dev      # IP 设计验证开发
aix wf sync                       # clone / fetch / checkout 全部所需仓库
aix wf status                     # 查看各仓状态
```

> `ip-dev` 会启用：HWIF、CBB、IP、DV Common、VIP、Tools、Catalog、Skills。
> 若没有私有 Skill 仓库权限，会显示 `OPTIONAL_UNAVAILABLE`，公共确定性流程继续运行。

## 4. 单仓独立开发

```bash
aix repo branch vip feature/my-change
aix repo commit vip -m "feat: ..."
aix repo push vip
```

父仓 `git status` 保持 clean——子仓提交不会污染 Workflow 仓库。

## 5. 生成 FuseSoC 配置与锁

```bash
aix wf fusesoc --generate
aix wf lock -o .aix/local.lock.yaml
# 生成：
#   .aix/generated/fusesoc.conf
#   .aix/generated/core-roots.txt
#   .aix/generated/vlnv-index.json
#   .aix/generated/dependency-graph.json
```

## 6. 建立跨仓 Change Bundle

一个功能跨多个仓库（如 HWIF/VIP/IP）时，用 Change Bundle 建立变更关系与合并顺序：

```bash
aix bundle create --from templates/change-bundle.yaml
aix bundle validate CHG-2026-XXXX
aix bundle status CHG-2026-XXXX
```

详见 [collaboration](workflow/collaboration.md)。

## 7. 环境诊断

```bash
aix wf doctor
```

## 典型报错速查

| 现象 | 处理 |
|---|---|
| `not cloned` | 先执行 `aix wf sync` |
| `remote does not match manifest` | 检查该仓 remote 是否指向 approved URL |
| `revision not reachable` | 确认分支/tag/commit 存在且已 fetch |
| `dirty in release mode` | 先提交或清理再进入 release |
| `OPTIONAL_UNAVAILABLE` | 私有 Skill 仓无权限，公共流程继续 |
| override 显示 `NON-BASELINE` | 检查 `overrides/local.yaml` 与 `aix wf status` |
| 发布被拒 | 确认 clean、无 local override、已固定 Lock |

详见 [troubleshooting](workflow/troubleshooting.md)。
