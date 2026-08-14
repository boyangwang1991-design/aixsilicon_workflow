# Workflow 工程化设计参考

> 历史参考：保留 CLI 拆包、Schema SSOT、任务入口、命令补齐和 CI 真实化的完整工程化依据；当前设计见 [`../workflow/README.md`](../workflow/README.md)，当前任务见 [`../workflow/delivery.md`](../workflow/delivery.md)。

> 对 `aixsilicon_workflow` 项目结构的整体审视与优化方案。
> 执行入口见 [`../workflow/delivery.md`](../workflow/delivery.md)；本文件聚焦**代码结构/工程化**层面。
>
> **执行状态（2026-08-13）**：P0 五项缺陷、R1（cli 拆包 + context + registry + schema-sync + Makefile）、
> R2（`aix wf run` / `aix wf test --affected` / `aix bundle validate|status`）已完成；
> 本规划新增 R2.5（标准 action 集 + release/bundle create + 统一退出码，见 [`cross-repo-optimization-plan.md`](cross-repo-optimization-plan.md)）。
> 剩余：S5 残余（`repo pr`）、S6（reusable workflows 真实化）。

## 1. 现状审视

### 1.1 规模

| 区域 | 规模 | 评价 |
|---|---|---|
| `src/aixworkflow/` | 22 模块 / 2668 LOC | 合理，但 cli.py 过重 |
| `tests/` | 5 文件 / 594 LOC / 35 用例 | 覆盖数据层好，命令层弱 |
| 配置层 YAML/JSON | 6 manifests / 7 workflows / 6 policies / 6 schemas | 齐全 |

### 1.2 主要结构问题

| # | 问题 | 影响 |
|---|---|---|
| S1 | **cli.py 单文件 463 行**：`wf`/`repo`/`bundle`/`release` 四个命令域 + 参数构建 + 分发表 + 格式化全部混在一起 | 扩展 `run/bundle/release/pr` 会继续膨胀，难测试 |
| S2 | **命令与业务耦合**：handler 直接 import 数据/领域模块，无薄服务层与统一上下文 | 重复加载 manifest/profile/override；不易做 CLI 级测试 |
| S3 | **Schema 双份**：`schemas/`（规范源）与 `src/aixworkflow/schemas/`（包内副本）靠手工 `cp` + `test_schema_parity` 防漂移 | 易漏同步，发布包与实际不符 |
| S4 | **无统一任务入口**：无 Makefile/tox/nox，install/test/lint/schema-sync/coverage 无标准命令 | 新成员学习成本高、CI 命令不统一 |
| S5 | **命令为桩/缺失**：`aix wf run`、`aix wf test --affected`、`bundle create/validate/status`、`release prepare/publish`、`repo pr` 未实现 | plan.md §26 API 未闭环 |
| S6 | **GitHub workflows 为占位**：lint/unit-sim 等仍是 echo | 无法实际复用 |

## 2. 优化方案

### 2.1 重构 CLI 为包（S1/S2）— 优先级最高

目标结构：

```text
src/aixworkflow/cli/
├── __init__.py      # main() 入口 + 分发（保持 `aix` 入口不变）
├── context.py       # 统一加载 manifest/profile/override/workspace_root
├── args.py          # 集中参数构建（每域一个 build_parser）
├── wf.py            # wf 命令 handler（init/sync/status/doctor/lock/diff/graph/fusesoc/clean/foreach/run）
├── repo.py          # repo 命令 handler（status/shell/branch/commit/push/diff/pr）
├── bundle.py        # bundle 命令 handler（create/validate/status）
├── release.py       # release 命令 handler（prepare/publish）
└── registry.py      # 轻量命令注册装饰器 @command(domain, name, handler)
```

原则：

- **handler 只做**：解析参数 → 调用领域模块 → 格式化输出；不含 Git/YAML/逻辑。
- **context.py 收敛**：`ctx = load_context(args)` 一次加载，各 handler 复用，消除重复加载。
- **registry.py 注册式**：新增命令 = 新增函数 + 装饰器，clr 不需改动分发。
- 向后兼容：`aix wf init` 等命令签名保持不变。

### 2.2 Schema 单一事实源（S3）

- 新建 `scripts/sync_schemas.py`：把 `schemas/*.json` 同步到 `src/aixworkflow/schemas/`，可 `--check`（CI 用）。
- `schema.py` 运行时优先读仓库 `schemas/`（开发态），否则读包内副本（安装态）。
- 保留 `test_schema_parity` 作为最后防线；CI 增加 `sync_schemas.py --check`。

### 2.3 统一任务入口（S4）

新增 `Makefile`：

```makefile
install:   uv venv + uv pip install -e ".[dev]"
test:      pytest -q
lint:      ruff check src tests scripts
format:    ruff format --check
check:     lint + test + schema-sync --check
coverage:  pytest --cov=aixworkflow --cov-report=term-missing
schema:    python scripts/sync_schemas.py
```

可选 `tox.ini` 支持多 Python 版本矩阵（3.11/3.12）。

### 2.4 补齐命令（S5）

- `aix wf run <flow>`：接入 [`runner.py`](../../src/aixworkflow/runner.py)，注册 action（workspace.resolve / fusesoc.target / eda.regression / evidence.index …），前置条件（clean/lock/no-override）校验，输出 Run Manifest + Evidence。
- `aix wf test --affected`：接入 [`impact.py`](../../src/aixworkflow/impact.py)。
- `aix bundle validate/status`：接入 [`bundle.py`](../../src/aixworkflow/bundle.py)（merge_order、状态机）。
- `aix repo pr`：gh CLI 包装（P1）。

### 2.5 GitHub workflows 真实化（S6）

- `reusable-fusesoc-lint.yml` / `reusable-unit-sim.yml` 接 FuseSoC 真实命令。
- 引用固定 Tag（V0.1）而非 `main`。
- `integration-baseline.yml` 接入 `aix wf lock` 生成真实 baseline。

### 2.6 P0 缺陷（来自审查，同步 todo.md）

- 修 lockfile `tree` 为空（新增 `gitops.rev_parse_any`）。
- `aix wf lock --no-fetch` 离线模式。
- 修 `aix wf status` Baseline 列（diverged 分支）。
- `aix wf sync --lock` 真正按 Lockfile checkout。
- 生成真实 `locks/baseline.lock.yaml`。

## 3. 优先级与顺序

| 阶段 | 内容 | 依赖 |
|---|---|---|
| P0（立即） | 5 项缺陷修复 + 补测试 | 无 |
| R1（结构重构） | cli 拆包 + context + registry + schema-sync 脚本 + Makefile | P0 后 |
| R2（功能落地） | `aix wf run` + `test --affected` + bundle CLI | R1 后 |
| R3（CI/发布） | workflows 真实化 + Tag、release 协调、catalog 接入 | R2 后 |

## 4. 成功标准

- 新增一个命令 ≤ 2 处改动（注册 + handler），且不用改 cli.py 主体。
- `aix wf run ip-verification` 在真实 9 仓工作区输出 Run Manifest + Evidence。
- `make check` 一条命令通过 lint + 全测试 + schema 一致性。
- schema 改动只在一个地方（`schemas/`），发布包自动一致。
