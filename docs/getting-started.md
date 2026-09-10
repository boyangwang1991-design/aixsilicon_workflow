# Getting Started

本文档面向新成员，说明如何获得 AIXSILICON 开发环境。Workflow 只负责三件事：**维护 GitHub 仓库、提供工作空间、提供工作原则与指导**。

## 前置条件

- Python 3.11+（推荐 3.12）
- Git 2.30+
- SSH Key 已配置并加入 GitHub 账号（`boyangwang1991-design` 组织下仓库）
- uv（统一依赖入口）；FuseSoC 按根项目依赖安装，不另用系统 pip

## 1. 克隆 Workflow 仓库

```bash
git clone git@github.com:boyangwang1991-design/aixsilicon_workflow.git
cd aixsilicon_workflow
```

## 2. 安装 CLI（Skill 集中管理）

`aix` CLI 的源码由私有 skill `aixsilicon-workspace-management` 统一管理；
本仓库通过 [`bootstrap.py`](../bootstrap.py)（纯标准库引导器）下载 skill repo 并把 skills
物化到 `/<agent-dir>/skills/`（默认 `/.roo/skills/`，git 忽略）后运行。

```bash
# 1) 安装依赖（Python 一律经 uv，唯一环境为根 .venv）
uv venv .venv --python 3.12
uv sync --locked

# 2) 物化 skills（下载/更新 repos/aixsilicon_skill_repo + 物化到 .roo/skills）
uv run python bootstrap.py --ensure

# 3) 使用 aix（引导器从选定 <agent-dir>/skills 中的 runtime 委托）
uv run python bootstrap.py aix wf init --profile ip-dev
# 等价：安装后可 `uv run aix ...`（pyproject 将 aix 指向 aix_launcher）
```

> 私有 skill 仓无权限且本地没有已物化副本时，bootstrap 与依赖该 runtime 的 `aix` 命令
> 不可用；已有副本可用 `bootstrap.py --skip-materialize ...` 离线复用。

## 3. 选择 Profile 并初始化

Profile 使用 `include_repositories` 精确集合语义（`optional_repositories` 为可选附加，`aix wf sync` 也会同步它们）。

| Profile | 用途 |
|---|---|
| `minimal` | 精确包含 HWIF、Tools；不是 base 组的全部仓 |
| `ip-dev` | IP 设计验证开发（流程由 ip-development-suite 约束） |
| `cbb-dev` | CBB 设计验证开发（流程由 cbb-development-suite 约束） |
| `soc-integration` | SoC 集成（流程由 soc-integration-suite 约束） |
| `all` | 管理/审计，不作为普通开发环境 |

```bash
aix wf init --profile ip-dev      # IP 设计验证开发
aix wf sync                       # clone / fetch / checkout 全部所需仓库
aix wf status                     # 查看各仓状态
```

> `ip-dev` 会启用：HWIF、CBB、IP、DV Common、VIP、Tools、Catalog、Skills。
> `skills` 是 optional repo；同步阶段无权限时会显示 `OPTIONAL_UNAVAILABLE`。首次启动 CLI
> 仍需要 canonical skill repo 或可信的既有物化副本。

## 4. 单仓独立开发

```bash
# 子仓（repos/<id>）
aix repo branch vip feature/my-change
aix repo commit vip -m "feat: ..."     # commit 前先在子仓内 git add
aix repo push vip

# 父仓（workflow 控制面根目录，repo_id=workflow）
aix repo status workflow
aix repo commit workflow -m "feat: ..."
aix repo push workflow
```

- 子仓提交不会污染 Workflow 仓库（`repos/` 整体忽略）。
- `aix repo commit` 只执行 `git commit -m`，不自动 `git add`，提交前需先在目标仓内 `git add <files>`（父仓同理）。
- 父仓建议顺序：`make check` 全绿 → `pre-commit run --all-files` 全绿 → `git add` → `aix repo commit workflow` → `aix repo push workflow`。

## 5. 生成 FuseSoC 配置

```bash
aix wf fusesoc --generate
# 生成：
#   .aix/generated/fusesoc.conf
#   .aix/generated/core-roots.txt
#   .aix/generated/vlnv-index.json
#   .aix/generated/dependency-graph.json
```

## 6. 环境诊断

```bash
aix wf doctor
```

标准 Flow 在执行前先检查 capability。领域 Skill stage 是 required，provider 未注册时会
明确 blocked，而不会把 skipped 误报为通过：

```bash
aix wf preflight ip-development
```

## 典型报错速查

完整命令、副作用与 Flow 输入示例见 [操作手册](workflow/operations.md)。
当前三条领域 Flow 的 provider 尚未注册，preflight 阻断是预期结果，不能据此宣称设计流程已执行；详见 [当前限制](workflow/current-state.md)。

| 现象 | 处理 |
|---|---|
| `not cloned` | 先执行 `aix wf sync` |
| `remote does not match manifest` | 检查该仓 remote 是否指向 approved URL |
| `revision not reachable` | 确认分支/tag/commit 存在且已 fetch |
| `OPTIONAL_UNAVAILABLE` | optional repo/provider 不可用；检查当前命令是否依赖它 |
| override 显示 `NON-BASELINE` | 检查 `overrides/local.yaml` 与 `aix wf status` |
