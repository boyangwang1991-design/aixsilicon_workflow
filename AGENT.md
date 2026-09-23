# AGENT.md — AIXSILICON Workflow 工作方法

本文件定义 AI / Agent 在本仓库（`aixsilicon_workflow`，多仓工作区控制面）中的**工作方法、纪律与完成定义**。
遵循本文件，可保证跨仓协作的一致性、可复现性与可审计性。

---

## 1. 定位

- 本仓是 **Manifest 驱动的多仓工作区控制面**，不是源码汇总仓；子仓统一克隆到 `repos/`（父仓 `.gitignore` 完整忽略）。
- **Skill 集中管理**：`aix` CLI 的源码/测试/脚本由私有 skill `aixsilicon-workspace-management`（`repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/`）统一管理；本仓通过 [`bootstrap.py`](bootstrap.py) 下载 skill repo 并把 skills 物化到 `/<agent-dir>/skills/`（默认 `/.roo/skills/`，git 忽略）后运行。首次使用先 `uv run python bootstrap.py --ensure`。
  - **skill repo 的 manifest id 是 `skills`**（目录名为 `repos/aixsilicon_skill_repo`）；子仓 git 操作用 `aix repo <cmd> skills`（id 不是目录名）。
  - **物化带内容指纹缓存**：canonical `skills/` 的文件内容未变化时自动跳过全量复制；强制更新 repo 并重物化用 `--force`，离线复用已有副本用 `--skip-materialize`。
  - **uv.lock 防漂移**：镜像源已**项目级固定为清华源**（根 [`uv.toml`](uv.toml) `index-url`），
    并要求本机全局 `%APPDATA%\uv\uv.toml` 仅保留清华源、不配置 aliyun 等备用镜像
    （uv 会从全局 named index 命中非默认源改写 lock）；若仍发现 `uv.lock` 被改写为
    其他源 URL，`git checkout -- uv.lock` 还原并检查全局 uv.toml；环境一致性校验用
    `uv run --locked ...`。
- **Skill 修改原则（canonical 源优先 + 重新物化）**：必须先修改 `repos/aixsilicon_skill_repo/skills/<skill-name>/`，再执行 `uv run python bootstrap.py --ensure`；**禁止直接编辑 `<agent-dir>/skills/` 下的物化副本**。
- 责任链：**Skill 决定“领域研发方法与流程”→ Workflow 决定“仓库生命周期/临时场地”→ Tool 负责“确定性执行”→ 资产仓保存 SSOT/交付 → Catalog 发布合格资产 → EDA 提供工程证据**。
- 统一命名：VLNV 一律 `aixsilicon:*`（canonical guard [`check_vlnv_namespace.py`](repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/scripts/hooks/check_vlnv_namespace.py) 强制）；CLI 单入口 `aix`（canonical [`cli/registry.py`](repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/src/aixworkflow/cli/registry.py) 插件发现）。

## 2. 开工前必读（按需渐进加载）

| 场景 | 必读 |
|---|---|
| 任何任务前（快速） | [`README.md`](README.md)、[`docs/index.md`](docs/index.md)（统一入口） |
| 规划/排期 | 各 repo `delivery.md`（任务定义由各仓自行维护） |
| 跨仓契约/命名 | [`docs/workflow/ownership.md`](docs/workflow/ownership.md)、[`policies/dependency-policy.yaml`](policies/dependency-policy.yaml) |
| 工具归属 | [`docs/workflow/ownership.md`](docs/workflow/ownership.md)（T1 公共工具 / T2 单仓脚本 / T3 私有适配 / T4 项目脚本） |
| 写入边界 | [`ownership-map.yaml`](ownership-map.yaml) |
| 工作原则 | [`docs/governance.md`](docs/governance.md)、[`policies/`](policies/) |

## 3. 任务分类与路由

先判定任务属于哪个域与哪个仓，再决定改动范围：

| 任务意图 | 主域 | 主落点 |
|---|---|---|
| 工作区/多仓同步/仓库管理 | workflow | 本仓（`manifests/ workflows/ policies/`） |
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
aix wf init --profile <profile>          # 初始化（minimal/ip-dev/cbb-dev/soc-integration/all）
aix wf sync                              # clone/fetch/checkout（按当前 profile 同步仓库）
aix wf status / aix wf doctor            # 状态 / 诊断
aix wf lock -o .aix/local.lock.yaml      # 本地解析锁（可选）
aix wf graph                             # 依赖 DAG
aix wf fusesoc --generate                # 生成 FuseSoC 聚合配置 + VLNV 索引
aix wf preflight <flow>                  # 执行前检查 required provider
aix wf run <flow>                        # 执行标准 flow（标准 action 集）
aix wf test --affected --repo <id>       # 影响分析

# 单仓
aix repo status <id> / diff / shell / branch / commit / push

# 发布协调（workflow 职责；跨仓联合验证由 Skill 在临时场地完成）
aix release prepare --asset <vlnv> --version <v>
aix release publish  --asset <vlnv> --version <v>   # 需人工批准

# 确定性工具（由 aixsilicon_tool_repo 插件提供；未装时显式 OPTIONAL_UNAVAILABLE）
aix tool schema|hwif|reg|core ...
```

- **确定性执行门禁（强制）**：所有已有 `aix` 确定性能力覆盖的动作**必须走 `aix` CLI / 注册 action**，
  禁止手写一次性 git/python 命令替代：
  - **子仓 git 操作唯一入口**：`aix repo status|diff|shell|branch|commit|push <repo_id>`；
    禁止在 `repos/*` 内直接 `git commit/push`。注意：`aix repo commit` 只执行
    `git commit -m`（不会自动 `git add`），提交前需先在子仓内 `git add <files>`；
    git 层的 pre-commit hook 会在 commit 时自动运行。
  - 父仓（workflow 控制面）git 操作统一入口：`aix repo status|diff|branch|commit|push workflow`（`repo_id=workflow` 映射到工作区根）。父仓提交顺序：`make check` 全绿 → `pre-commit run --all-files` 全绿 → `git add <files>` → `aix repo commit workflow -m "..."` → `aix repo push workflow`。
    注：父仓的 `git add` 仍需普通 git 执行（`aix repo commit` 不自动 add）；临时诊断可走普通 git，需在 run_log 注明。
  - **违规示例（Do NOT）**：`git -C repos/xxx commit -m ...`、`git -C repos/xxx push origin main`、
    用 `git status`/`git diff` 代替 `aix repo status`/`aix repo diff` 作为子仓状态证据来源。
  - 唯一豁免：`aix` CLI 未提供且无法注册 action 的临时性诊断（需在 run_log 注明原因）。
- **Profile 连贯性**：`aix wf init --profile <profile>` 将选择写入 `.aix/state.json`，后续
  `sync/status/doctor` 默认继承该 profile；命令行 `--profile` 可显式覆盖。
- **Python 环境一律使用 `uv` 管理**（`uv run python` / `uv sync` / `uv add`），
  禁止再创建新的虚拟环境（不要 `python -m venv`、不要在 `repos/*` 下放置 `.venv`）：
  - 唯一环境：**workflow 仓库根目录** `.venv/`（由根 `pyproject.toml` + `uv.lock` 管理，
    根 `.gitignore` 已忽略）；
  - 各子仓（`repos/*`）的确定性脚本依赖**并入根 `pyproject.toml`**，不单独建环境；
  - 子仓内如需在 CI/独立仓库运行，允许声明其自身 `pyproject.toml`（作为事实源），
    但本地开发/回归统一起 workflow 根环境：`cd <workflow-root> && uv sync && uv run python <script>`；
  - 禁止使用系统 `python`/`pip` 直接安装依赖。

## 4.1 受限执行环境中的 uv 退出挂起

若 `uv run` 已输出完成结果却不退出，先用 `uv run --offline --no-sync /bin/true`
做短超时探针，区分进程退出问题与依赖下载/测试耗时。已确认当前 Linux 沙箱中
uv 0.11.27 可出现子进程已退出但父进程不回收；同一命令在非沙箱环境正常返回。
复现此问题时，通过宿主正常权限机制使用获授权的非沙箱环境执行原始 uv/门禁命令，
不要反复用短超时中断完整门禁，也不要将已打印的 PASS 当作进程退出成功。
保留根 uv 环境、锁文件和全部检查，不修改沙箱策略、不跳过 hook。
详细诊断和运行约定见 canonical workspace Skill 的
[uv 环境说明](repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/references/uv-environment.md)。

## 4.2 环境初始化（首次使用）

```bash
# 1. 下载 skill repo + 物化 skills（首次必须；指纹缓存命中时自动跳过复制）
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

日常反复调用 `aix`（如脚本/回归内嵌多条命令）时可加 `--skip-materialize`
复用已物化 skills、跳过物化子进程：

```bash
uv run python bootstrap.py --skip-materialize aix repo status skills
```

**注意**：若 `sync` 后仍有仓库 MISSING，需手动 `git clone` 缺失仓库：
```bash
git clone git@github.com:boyangwang1991-design/aixsilicon_<repo>.git repos/aixsilicon_<repo>
```

## 5. 工作方法（Step-by-step）

1. **理解与分类**：明确目标、涉及仓、交付物与 Gate（§3）。
2. **上下文最小化**：只读本任务所需文档与文件，不无差别扫描全部仓库。
3. **规划与影响**：跨仓/接口/发布类任务先明确各仓独立 PR 与联合验证场地，不静默扩大/缩小范围。
4. **契约先行**：改动前确认 Schema 所有权（[`docs/workflow/ownership.md`](docs/workflow/ownership.md)）与 VLNV/命名（`aixsilicon:*`）。
5. **确定性执行**：能用工具/脚本确定性生成的（CSR/HWIF/Core/Header/文档）就调用，不手工维护派生视图。
6. **写入边界**：按 [`ownership-map.yaml`](ownership-map.yaml) 只写允许的 owner 仓与路径；私域（Skill/Foundry/PDK/商业 EDA）不写入公共仓。
7. **证据与日志**：关键动作记录结构化结果/证据（run manifest、evidence index、run_log.md），可追溯。
8. **门禁**：改动完成后对照对应 Skill 的领域门禁（如 ip-development-suite G0–G5）与 workflow 仓库卫生（G0/G1）验证，不凭摘要自证通过。
9. **回归验证**：收尾前跑 `make check` + `pre-commit run --all-files`，确保全绿。

## 6. 跨仓协作（各仓独立 PR + 联合验证）

- 跨多仓功能 → 各仓独立 PR，联合验证由对应 Skill 在临时场地完成；
- 影响分析 → `aix wf test --affected`；依赖图不完整时**扩大测试范围**，不静默缩小；
- 事件/CI 防递归：携带 `correlation_id` + `depth`（canonical [`github.py`](repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/src/aixworkflow/github.py)）。

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
| 下一步该建什么 | 各 repo `delivery.md`（任务定义由各仓自行维护） |
| 跨仓边界/命名/工具 | [`docs/workflow/ownership.md`](docs/workflow/ownership.md)、[`policies/dependency-policy.yaml`](policies/dependency-policy.yaml) |
| 领域门禁/方法 | 对应 Skill（ip/cbb/soc/hwif suite，`repos/aixsilicon_skill_repo/skills/`） |
| 具体 IP 研发方法 | skill_repo `skills/ip-development-suite/`（SKILL.md + artifact-contract） |

## 10. 完成定义（Definition of Done）

- [ ] 变更落在正确的 owner 仓与路径，未越权写入；
- [ ] VLNV/命名/Schema 符合统一契约（`aixsilicon:*`、单一 Owner）；
- [ ] 需要确定性生成的产物由工具/脚本生成，未手工维护派生视图；
- [ ] 跨仓变更按各仓独立 Review/merge，联合验证由对应 Skill 在临时场地完成；
- [ ] 关键动作有结构化证据（run manifest / evidence / run_log）；
- [ ] `make check` 与 `pre-commit run --all-files` 全绿；
- [ ] 文档与实现保持一致（发现不一致时同步修订）。
