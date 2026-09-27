# Getting Started

本文档面向新成员，说明如何获得 AIXSILICON 开发环境。Workflow 只负责三件事：**维护 GitHub 仓库、提供工作空间、提供工作原则与指导**。

## 前置条件

- Python 3.11+（推荐 3.12）
- Git 2.30+
- SSH Key 已配置并加入 GitHub 账号（`boyangwang1991-design` 组织下仓库）
- uv（统一依赖入口）；FuseSoC 按 `ip-dev` extra 安装，不另用系统 pip

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
uv sync --locked                         # 仅安装轻量 CLI 依赖
# 按需安装（共享根 .venv）：
# uv sync --locked --extra dev            # workflow 开发/门禁
# uv sync --locked --extra docs           # 文档解析（包含 PyTorch 等大型依赖）
# uv sync --locked --extra doc-enhance    # 基础解析 + 增强格式支持
# uv sync --locked --extra ip-dev         # FuseSoC / RTL / 寄存器工具
# 多组可叠加，例如 --extra dev --extra ip-dev

# 2) 物化 skills（下载/更新 repos/aixsilicon_skill_repo + 物化到 .roo/skills）
uv run python bootstrap.py --ensure

# 3) 使用 aix（引导器从选定 <agent-dir>/skills 中的 runtime 委托）
uv run python bootstrap.py aix wf init --profile ip-dev
# 等价：安装后可 `uv run aix ...`（pyproject 将 aix 指向 aix_launcher）
```

### Codex skills 安装

工作区 runtime 的物化与 Codex 用户技能安装是两个步骤。Codex 用户使用：

```bash
uv run --locked python bootstrap.py --install-codex-skills
```

该入口复用已克隆的 canonical skills，无须再次下载，安装到 `$CODEX_HOME/skills`
（未设置时为 `~/.codex/skills`），下一轮对话可用。它记录来源/内容指纹，内容一致时跳过；
受管且未被本地修改的技能可更新。遇到不同来源或本地改动时停止，显式替换需加
`--replace-codex-skills`，旧目录会备份到 Codex 目录下的 `aix-skill-backups/`。
`.roo/skills` 或 `--agent-dir .codex` 的工作区物化路径仍用于 workflow runtime，
不等同于 Codex 用户技能安装。

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
# 可选：并发同步；临时排除知识库，不改变 manifest/profile
# aix wf sync --jobs 3 --exclude knowledge
# 大仓/慢网络：默认 clone 1800 秒、fetch 300 秒，可按次调整
# aix wf sync --repo knowledge --clone-timeout 3600
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
# 可选只读远端访问诊断（不下载仓库；尚未克隆的必需仓仍会报告缺失）
aix wf doctor --network
```

标准 Flow 在执行前先检查 capability。领域 Skill stage 是 required，provider 未注册时会
明确 blocked，而不会把 skipped 误报为通过：

```bash
aix wf preflight ip-development
```

`sync` 默认显示逐仓操作、Git 进度和耗时，`--quiet` 关闭进度。
失败时可用 `--repo <id>` 重试；下载先落入仓库目录旁的隐藏临时目录，完整校验后才改名为
正式路径。超时/中断保留的临时目录会明确打印，不会误报成完整仓库，也不自动删除用户数据。
`--exclude` 仅本次有效，不能用于 `--lock` 发布同步；`--jobs` 范围为 1–16。
`doctor` 对可选工具/仓库缺失输出 WARN，不影响退出码；必需仓缺失仍为 FAIL。
网络/SSH 错误保留原始诊断，不将连接失败误判为空仓。若普通终端可用而受限环境失败，
先核对执行环境权限，不依据沙盒中的所有者映射修改宿主 SSH 配置。

## 典型报错速查

完整命令、副作用与 Flow 输入示例见 [操作手册](workflow/operations.md)。
当前三条领域 Flow 的 provider 尚未注册，preflight 阻断是预期结果，不能据此宣称设计流程已执行；详见 [当前限制](workflow/current-state.md)。

| 现象 | 处理 |
|---|---|
| `not cloned` | 先执行 `aix wf sync`；有意暂缓的仓仍报告缺失 |
| `incomplete repository` / `no valid HEAD` | 保留并检查半成品，移至其他路径后按 `--repo` 重试 |
| 锁文件需要更新，但未改依赖 | 核对镜像地址（清华源末尾必须为 `/simple/`）与本机 uv 版本，不用 `--frozen` 掩盖差异 |
| `remote does not match manifest` | 检查该仓 remote 是否指向 approved URL |
| `revision not reachable` | 确认分支/tag/commit 存在且已 fetch |
| `OPTIONAL_UNAVAILABLE` | optional repo/provider 不可用；检查当前命令是否依赖它 |
| override 显示 `NON-BASELINE` | 检查 `overrides/local.yaml` 与 `aix wf status` |
