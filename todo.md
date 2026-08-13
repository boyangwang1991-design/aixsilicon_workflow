# AIXSILICON Workflow 工作空间优化 TODO

> 基于 2026-08-13 工作空间审查（9 仓已同步、35 测试通过、ruff 干净）。
> 优先级：P0（应立即修，含缺陷）→ P1（本季度）→ P2（后续）。

## 当前基线

- 10 仓已接入（workflow + 9 资产仓），`aix wf sync` 已全部克隆，`aix wf status` 9/9 `main/clean/sync`。
- CLI：`aix wf init/sync/status/doctor/lock/diff/graph/fusesoc/clean/foreach` + `aix repo status/shell/branch/commit/push/diff`。
- 测试：35 通过；ruff 通过；20 个 YAML 通过 Schema 校验。

---

## P0 缺陷（已确认，应立即修）

- [ ] **修复 lockfile tree hash 为空**
  - [`src/aixworkflow/resolver.py`](src/aixworkflow/resolver.py) 用 `rev_parse(path, f"{commit}^{{tree}}")`，但 [`src/aixworkflow/gitops.py`](src/aixworkflow/gitops.py) 的 `rev_parse` 会追加 `^{commit}`，拼成 `commit^{tree}^{commit}` 导致解析失败（已复现：返回 `None`，`tree: ''`）。
  - 修法：新增 `gitops.rev_parse_any(path, rev)`（不带 `^{commit}` 后缀），tree 改用该函数；补单元测试。

- [ ] **`aix wf lock` / `resolve_repository` 每次强制 `git fetch`**
  - 网络波动时整个 lock 失败（已复现 `kex_exchange_identification`）。
  - 优化：增加 `--no-fetch` / `offline` 模式，仅在本地 ref 解析不到时再 fetch；或 fetch 失败仅告警不中断（本地可解析时）。

- [ ] **`aix wf status` Baseline 列逻辑错误**
  - [`src/aixworkflow/cli.py`](src/aixworkflow/cli.py) 嵌套三元：`ahead` 优先，`diverged`（ahead+behind）分支不可达，永远显示 `ahead`。
  - 修法：独立判断 `ahead/behind/diverged/clean`；并真正与 `locks/baseline.lock.yaml` 比较（而非只显示 git ahead/behind）。

- [ ] **`aix wf sync --lock <file>` 未真正按 Lockfile 解析**
  - 当前 `--lock` 仅切换 release 模式，未读取 Lockfile 里的 commit 去 checkout。
  - 修法：读取 lock，按 `commit` 强制 checkout（release 语义：clean 且无 override）。

- [ ] **生成真实 `locks/baseline.lock.yaml`**
  - 当前为全零占位模板；9 仓已可解析，应生成真实 SHA 并走 PR/CI 保护流程。

## P1 功能缺口（阶段2～3 主线）

- [ ] **接入 Flow DAG 执行器 `aix wf run <flow>`**
  - [`src/aixworkflow/runner.py`](src/aixworkflow/runner.py) 已实现，但未接入 CLI；需注册 action、前置条件（clean/lock/no-override）、失败收集 Evidence、结构化 Gate 结果。
  - 首个穿刺：`ip-verification`（APB 寄存器 IP，`workflows/ip-verification.yaml`）。

- [ ] **`aix wf test --affected` 影响驱动验证**
  - 接入 [`src/aixworkflow/impact.py`](src/aixworkflow/impact.py)：按 changed files → 依赖图 → 必测集合。

- [ ] **Change Bundle CLI 完整化**
  - `aix bundle create/validate/status` 目前是桩；补：校验 merge_order、PR refs 联合 checkout、状态机（draft→…→closed）。

- [ ] **`aix wf foreach --allow-write`**
  - 当前 foreach 无写保护开关；补显式 `--allow-write` 并逐仓记录执行结果。

- [ ] **`aix repo pr` 与 `aix repo release`**
  - PR 创建/查看（P1）、受控发布入口（P2）。

## P2 健壮性与体验

- [ ] **并行 fetch**：多仓 `git fetch` 并行执行，输出按仓聚合（plan §13）。
- [ ] **`aix wf doctor` 增加 override/dirty/lock 一致性提示**。
- [ ] **`aix wf clean` 状态数据库登记**：只清理生成目录并登记/回滚（plan §8.3）。
- [ ] **路径逃逸校验**：init 时校验 manifest `path` 位于 `repos_root` 下、无 `..`/绝对路径（schema 已限制，代码层再兜底）。
- [ ] **Schema 单一事实源**：`schemas/` 与 `src/aixworkflow/schemas/` 双份靠 `test_schema_parity` 防漂移；加同步脚本 `scripts/sync_schemas.py`。
- [ ] **日志脱敏**：`evidence/runner` 输出统一脱敏（Token/路径/变量）。
- [ ] **离线/弱网友好**：clone 失败可安全重试，lock 支持 `--no-fetch`。

## CI / GitHub 优化

- [ ] **GitHub Reusable Workflow 从占位到真实实现**
  - `reusable-fusesoc-lint.yml` / `reusable-unit-sim.yml` 目前是 echo 占位；接 FuseSoC 真实命令并打 Tag（V1）。
- [ ] **`integration-baseline.yml` 接入 `aix wf lock` 生成真实 baseline**。
- [ ] **`change-bundle.yml` 实现 PR refs 联合 checkout**。
- [ ] **pre-commit 安装落地**：`pre-commit install` 并纳入 CI。

## 资产仓内容建设（P0 新仓骨架已就绪，待填充）

- [ ] `aixsilicon_catalog_repo`：资产索引/兼容矩阵/成熟度 Schema 与首批条目。
- [ ] `aixsilicon_tool_repo`：`packages/aix-schema`、`aix-core-gen` 等确定性工具首包。
- [ ] `aixsilicon_soc_integration`：SoC/地址/中断/CRG/Power Schema 与集成模板。
- [ ] `aixsilicon_skill_repo`（私有）：Skill 声明式 Metadata 契约与首批 Skill。

## 测试与质量

- [ ] 补测试：tree hash、status baseline、`sync --lock`、`--no-fetch`、路径逃逸、foreach 写保护。
- [ ] `tests/golden/` 填充：fusesoc.conf / vlnv-index / dependency-graph 的确定性 golden。
- [ ] 覆盖率基线：`pytest --cov` 目标 ≥ 70%。

## 里程碑对照（plan.md 阶段）

| 阶段 | 出口 | 对应 TODO |
|---|---|---|
| 阶段1 Workspace MVP | 一键按 Profile 建环境、子仓独立提交 | 已基本达成 ✅ |
| 阶段2 FuseSoC+跨仓验证 | 固定 Lock 重建 APB 闭环 | P1 的 `aix wf run` + baseline lock |
| 阶段3 Change Bundle | HWIF→VIP→IP 联合变更 | P1 的 bundle CLI + affected tests |
| 阶段4 发布协调 | IP 资格验证+人工批准+Catalog | P2 的 release + catalog |
| 阶段5 SoC 集成 | SoC 锁定基线重建 | 资产仓建设 + soc flow 接入 |
