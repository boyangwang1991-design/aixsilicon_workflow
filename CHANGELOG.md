# Changelog

本项目的所有显著变更都记录在此文件中，格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)。

## [Unreleased]

### 新增（阶段0 与阶段1：Workspace MVP 框架）

- 平台定位与仓库边界文档（`docs/`、ADR）。
- 标准目录结构、`.gitignore` 与 `pre-commit` 运行时路径 Guard。
- Manifest / Lock / Override / Flow / Tool-Profile / Evidence-Index 六类 Schema V0.1。
- 全部 Profile Manifest：`minimal / default / ip-dev / cbb-dev / dv-dev / soc-integration / release`。
- 六类组织策略（依赖、兼容性、分支、发布、证据、安全）。
- 七类跨仓 Flow YAML 定义。
- `aix` Python CLI 骨架与 P0 命令：
  - `aix wf init / sync / status / doctor / lock / diff`
  - `aix repo status / shell / branch / commit / push`
- FuseSoC 聚合配置生成（`fusesoc.conf` / `core-roots.txt` / `vlnv-index.json` / `dependency-graph.json`）。
- GitHub Reusable Workflows V0.1 与薄入口示例。
- Change Bundle Schema 与示例。
- 单元测试与临时 Git 仓集成测试 Fixture。

### 优化（2026-08-13 结构重构 + P0 修复）

- 结构重构：`cli.py` 拆分为 `cli/` 包（`app` 分发、`args` 参数、`context` 统一上下文、`registry` 注册式命令、`wf/repo/extras` 命令模块）。
- 修复 lockfile `tree` 为空（新增 `gitops.rev_parse_any`）。
- 修复 `aix wf status` Baseline 列（`diverged` 分支可达）。
- `aix wf sync --lock` 真正按 Lockfile commit 强制 checkout（release 语义）。
- `aix wf lock --no-fetch` 离线解析模式。
- 生成真实 `locks/baseline.lock.yaml`（8 仓 release 基线 + 真实 SHA）。
- 新增 `aix wf run <flow>`（DAG 执行器接入）、`aix wf test --affected`（影响分析）、`aix bundle validate/status`（真实实现）。
- 新增 `scripts/sync_schemas.py`（Schema 单一事实源）与 `Makefile`（统一任务入口）。
- 测试扩充至 41 例（CLI 结构、tree 回归、registry 等）。

### 计划（后续阶段）

- [ ] Flow action 真实实现（fusesoc.target / eda.regression / hwif.compatibility-check 等）。
- [ ] Change Bundle PR refs 联合 checkout。
- [ ] 发布协调、SBOM、签名与 Catalog 更新 PR。
