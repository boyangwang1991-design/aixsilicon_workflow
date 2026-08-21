# AGENT.md — AIXSILICON Workflow 工作方法

本文件定义 AI / Agent 在本仓库（`aixsilicon_workflow`，多仓工作区控制面）中的**工作方法、纪律与完成定义**。
遵循本文件，可保证跨仓协作的一致性、可复现性与可审计性。

---

## 1. 定位

- 本仓是 **Manifest 驱动的多仓工作区控制面**，不是源码汇总仓；子仓统一克隆到 `repos/`（父仓 `.gitignore` 完整忽略）。
- **Skill 集中管理**：`aix` CLI 的源码/测试/脚本由私有 skill `aixsilicon-workspace-management`（`repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/`）统一管理；本仓通过 [`bootstrap.py`](bootstrap.py)（纯标准库引导器）下载 skill repo 并把 skills 物化到 `/.roo/skills/`（git 忽略）后运行。首次使用先 `uv run python bootstrap.py --ensure`。
  - **skill repo 的 manifest id 是 `skills`**（目录名为 `repos/aixsilicon_skill_repo`）；子仓 git 操作用 `aix repo <cmd> skills`（id 不是目录名）。
  - **物化带指纹缓存**：skill repo 工作树指纹（`git describe --always --dirty`）未变化时自动跳过全量复制；强制重物化用 `--force`，离线/反复调用 aix 用 `--skip-materialize`。
  - **uv.lock 防漂移**：本机 `uv run` 可能把 lock 中的镜像源 URL 重写（如 tsinghua -> aliyun，仅 URL/size 字段、无版本变化）；提交前 `git diff uv.lock` 若属此类改动，`git checkout -- uv.lock` 还原；环境一致性校验用 `uv run --locked ...`。
- **Skill 修改原则（aixsilicon-skill-repo 优先 + 重新物化）**：需要更新任何经物化到工作区的 Skill 内容（如 `.roo/skills/*/SKILL.md` 及其配套脚本/模板）时，必须先修改 aixsilicon-skill-repo 源仓 `repos/aixsilicon_skill_repo/skills/<skill-name>/` 下的对应文件，再执行 `uv run python bootstrap.py --ensure` 重新物化到工作区主目录；**禁止直接编辑 `.roo/skills/` 下的物化副本**（该目录被 git 忽略且每次 `--ensure` 会覆盖，直接改动会丢失且无法追踪）。
- 责任链：**Skill 决定“如何理解与辅助”→ Workflow 决定“顺序与 Gate”→ Tool 负责“确定性执行”→ 资产仓保存 SSOT/交付 → Catalog 发布合格资产 → EDA 提供工程证据**。
- 统一命名：VLNV 一律 `aixsilicon:*`（[`ADR-0003`](docs/adr/0003-unified-vlnv-namespace.md)）；CLI 单入口 `aix`（[`ADR-0004`](docs/adr/0004-cli-entry-and-plugin-registry.md)）。

## 2. 开工前必读（按需渐进加载）

| 场景 | 必读 |
|---|---|
| 任何任务前（快速） | [`README.md`](README.md)、[`docs/index.md`](docs/index.md)（统一入口） |
| 规划/排期 | [`docs/roadmap.md`](docs/roadmap.md)、[`docs/todo.md`](docs/todo.md)、[`docs/progress.md`](docs/progress.md)、对应仓 `delivery.md` |
| 跨仓契约/命名 | [`docs/adr/README.md`](docs/adr/README.md)、[`docs/workflow/ownership.md`](docs/workflow/ownership.md)、[`docs/workflow/release.md`](docs/workflow/release.md) |
| 工具归属 | [`docs/workflow/ownership.md`](docs/workflow/ownership.md)（T1 公共工具 / T2 单仓脚本 / T3 私有适配 / T4 项目脚本） |
| 写入边界 | [`ownership-map.yaml`](ownership-map.yaml) |
| 代码工程化 | [`docs/workflow/delivery.md`](docs/workflow/delivery.md) |

## 3. 任务分类与路由

先判定任务属于哪个域与哪个仓，再决定改动范围：

| 任务意图 | 主域 | 主落点 |
|---|---|---|
| 工作区/多仓同步/流程/发布协调 | workflow | 本仓（`manifests/ workflows/ policies/ changesets/`） |
| 接口契约/多视图 | HWIF | `repos/aixsilicon_hwif_repo` |
| 可复用构件/PPA | CBB | `repos/aixsilicon_cbb_repo` |
| IP 规格/SystemRDL/RTL/验证 | IP | `repos/aixsilicon_ip_repo` |
| 协议无关验证基础设施 | DV-Common | `repos/aixsilicon_dv_common` |
| 协议 VIP/Agent/Checker | VIP | `repos/aixsilicon_vip_repo` |
| 确定性生成/检查工具 | Tool | `repos/aixsilicon_tool_repo` |
| 已发布资产索引 | Catalog | `repos/aixsilicon_catalog_repo` |
| SoC 通用 Schema/规则 | SoC Integration | `repos/aixsilicon_soc_integration` |
| 研发方法论 Skill | Skill（私有） | `repos/aixsilicon_skill_repo`（canonical `ip-development-suite`） |

- **只读先于写入**：先 `aix wf status`/`doctor` 摸清现状，再动工。
- **先规划后实现**：涉及多仓/接口/发布变更时，先输出计划与影响，再实施。

## 4. 统一命令与工具

```bash
# 工作区
aix wf init --profile <profile>          # 初始化（minimal/ip-dev/cbb-dev/dv-dev/soc-integration/release/knowledge-dev/all）
aix wf sync                              # clone/fetch/checkout（按当前 profile 同步仓库）
aix wf status / aix wf doctor            # 状态 / 诊断
aix wf lock                              # 生成 resolved lock（正式基线用 --mode release）
aix wf diff --against locks/baseline.lock.yaml
aix wf graph                             # 依赖 DAG
aix wf fusesoc --generate                # 生成 FuseSoC 聚合配置 + VLNV 索引
aix wf run <flow>                        # 执行标准 flow（标准 action 集）
aix wf test --affected --repo <id>       # 影响分析

# 单仓
aix repo status <id> / diff / shell / branch / commit / push

# 跨仓
aix bundle create|validate|status <bundle>
aix release prepare --asset <vlnv> --version <v>
aix release publish  --asset <vlnv> --version <v> --lock <lock>   # 需 G7 guard + 人工批准

# 确定性工具（由 aixsilicon_tool_repo 插件提供；未装时显式 OPTIONAL_UNAVAILABLE）
aix tool schema|hwif|reg|core ...
```

- **确定性执行门禁（强制）**：所有已有 `aix` 确定性能力覆盖的动作**必须走 `aix` CLI / 注册 action**，
  禁止手写一次性 git/python 命令替代：
  - **子仓 git 操作唯一入口**：`aix repo status|diff|shell|branch|commit|push <repo_id>`；
    禁止在 `repos/*` 内直接 `git add/commit/push`。注意：`aix repo commit` 只执行
    `git commit -m`（不会自动 `git add`），提交前需先在子仓内 `git add <files>`；
    git 层的 pre-commit hook 会在 commit 时自动运行。
  - 父仓（workflow 控制面）提交允许普通 git，但**推荐** `aix repo` 保持统一审计；
    父仓提交顺序：`make check` 全绿 → `pre-commit run --all-files` 全绿 → `git add <files>` → `git commit` → `git push`。
  - **违规示例（Do NOT）**：`git -C repos/xxx commit -m ...`、`git -C repos/xxx push origin main`、
    用 `git status`/`git diff` 代替 `aix repo status`/`aix repo diff` 作为子仓状态证据来源。
  - 唯一豁免：`aix` CLI 未提供且无法注册 action 的临时性诊断（需在 run_log 注明原因）。
- **Profile 切换注意事项**：`aix wf init --profile <profile>` 会更新 `.aix/state.json`，
  但 `aix wf sync` 可能仍使用旧 profile。若需同步所有仓库，建议：
  1. 确认 `.aix/state.json` 中 `profile` 字段已更新；
  2. 若 sync 未同步预期仓库，手动 `git clone` 缺失仓库到 `repos/` 目录。
- **Python 环境一律使用 `uv` 管理**（`uv run python` / `uv sync` / `uv add`），
  禁止再创建新的虚拟环境（不要 `python -m venv`、不要在 `repos/*` 下放置 `.venv`）：
  - 唯一环境：**workflow 仓库根目录** `.venv/`（由根 `pyproject.toml` + `uv.lock` 管理，
    根 `.gitignore` 已忽略）；
  - 各子仓（`repos/*`）的确定性脚本依赖**并入根 `pyproject.toml`**，不单独建环境；
  - 子仓内如需在 CI/独立仓库运行，允许声明其自身 `pyproject.toml`（作为事实源），
    但本地开发/回归统一起 workflow 根环境：`cd <workflow-root> && uv sync && uv run python <script>`；
  - 禁止使用系统 `python`/`pip` 直接安装依赖。

## 4.1 环境初始化（首次使用）

```bash
# 1. 下载 skill repo + 物化 skills（首次必须）
uv run python bootstrap.py --ensure

# 2. 初始化工作区（选择 profile）
uv run python bootstrap.py aix wf init --profile ip-dev    # IP 开发（默认）
# 或
uv run python bootstrap.py aix wf init --profile all       # 完整工作区（所有仓库）

# 3. 同步仓库
uv run python bootstrap.py aix wf sync

# 4. 验证状态
uv run python bootstrap.py aix wf status
```

**注意**：若 `sync` 后仍有仓库 MISSING，需手动 `git clone` 缺失仓库：
```bash
git clone git@github.com:boyangwang1991-design/aixsilicon_<repo>.git repos/aixsilicon_<repo>
```

## 5. 工作方法（Step-by-step）

1. **理解与分类**：明确目标、涉及仓、交付物与 Gate（§3）。
2. **上下文最小化**：只读本任务所需文档与文件，不无差别扫描全部仓库。
3. **规划与影响**：跨仓/接口/发布类任务先写 Change Plan（可落为 `changesets/` Change Bundle）。
4. **契约先行**：改动前确认 Schema 所有权（[`docs/workflow/ownership.md`](docs/workflow/ownership.md)）与 VLNV/命名（`aixsilicon:*`）。
5. **确定性执行**：能用工具/脚本确定性生成的（CSR/HWIF/Core/Header/文档）就调用，不手工维护派生视图。
6. **写入边界**：按 [`ownership-map.yaml`](ownership-map.yaml) 只写允许的 owner 仓与路径；私域（Skill/Foundry/PDK/商业 EDA）不写入公共仓。
7. **证据与日志**：关键动作记录结构化结果/证据（run manifest、evidence index、run_log.md），可追溯。
8. **门禁**：改动完成后对照 Gate（workflow G0–G7；skill suite G0–G5）验证，不凭摘要自证通过。
9. **回归验证**：收尾前跑 `make check` + `pre-commit run --all-files`，确保全绿。

## 6. 跨仓协作（Change Bundle / Release）

- 跨多仓功能 → 建立 Change Bundle（`aix bundle create` → 填 repositories/merge_order → `validate`）。
- 影响分析 → `aix wf test --affected`；依赖图不完整时**扩大测试范围**，不静默缩小。
- 发布 → `aix release prepare`（G7 guard：dirty/override 阻断）→ 人工批准 → `publish`（幂等）。
- 事件/CI 防递归：携带 `correlation_id` + `depth`（[`src/aixworkflow/github.py`](src/aixworkflow/github.py)）。

## 7. 质量与证据纪律

- **质量门禁基于证据**：门禁 = Gate 报告 + canonical 模型/SHA 哈希，不只检查“目录存在”。
- **单一事实源**：Manifest 管仓库布局、Catalog 管发布资产、各仓管自身 SSOT；禁止双维护。
- **可复现**：正式基线必须 clean/locked + 固定 SHA + 工具版本锁（workspace-lock `tools:` 段）。
- **Skill 不得伪造通过**：`needs_verification` 状态只能由独立证据 + Gate 转换，不得自封 `verified`。

## 8. 安全红线（Do NOT）

- 不把 `repos/`、`.aix/`、`build/`、`cache/`、`reports/` 或 vendored `reference/` 内容提交进父仓（pre-commit guard 已强制）。
- 不在工作区根执行 `git clean -ffdx`、`rm -rf repos/*`、批量 `reset --hard`、`force-push`。
- 不把凭据/Token/PDK/客户数据写入 YAML、Lockfile、日志或公共仓。
- 不执行 Manifest/Flow 中任意 Shell 字符串；`uses` 只能引用注册 action。
- 不把私有 Skill/内部路径作为开源构建/发布验证的必需依赖。
- 不手工改由工具生成的派生文件（`generated/`、CSR RTL/Header、`.core` 发布产物）。
- 不使用 `aix:`/`company:`/`boyangwang1991-design:` 作 VLNV vendor（guard 已强制 `aixsilicon:`）。

## 9. 参考索引（什么时候读什么）

| 需求 | 文档 |
|---|---|
| 我是谁/在哪 | [`README.md`](README.md)、[`docs/index.md`](docs/index.md)、[`docs/workflow/ownership.md`](docs/workflow/ownership.md) |
| 下一步该建什么 | [`docs/roadmap.md`](docs/roadmap.md)、[`docs/todo.md`](docs/todo.md)、[`docs/progress.md`](docs/progress.md)、对应仓 `delivery.md` |
| 跨仓边界/命名/工具 | [`docs/adr/README.md`](docs/adr/README.md)、[`docs/workflow/ownership.md`](docs/workflow/ownership.md) |
| 成熟度/门禁 | [`docs/workflow/release.md`](docs/workflow/release.md)、[`docs/architecture/target-design.md`](docs/architecture/target-design.md) §8～9 |
| 具体 IP 研发方法 | skill_repo `skills/ip-development-suite/`（SKILL.md + artifact-contract） |

## 10. 完成定义（Definition of Done）

- [ ] 变更落在正确的 owner 仓与路径，未越权写入；
- [ ] VLNV/命名/Schema 符合统一契约（`aixsilicon:*`、单一 Owner）；
- [ ] 需要确定性生成的产物由工具/脚本生成，未手工维护派生视图；
- [ ] 跨仓变更已建立 Change Bundle 并校验 merge_order；
- [ ] 关键动作有结构化证据（run manifest / evidence / run_log）；
- [ ] `make check` 与 `pre-commit run --all-files` 全绿；
- [ ] 文档/plan/todo 与实现保持一致（发现不一致时同步修订）。
