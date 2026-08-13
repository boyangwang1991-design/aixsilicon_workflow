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
- 工具链 Profile（open-source / blue-zone / red-zone）与容器定义。
- 七类跨仓 Flow YAML 定义。
- `aix` Python CLI 骨架与 P0 命令：
  - `aix wf init / sync / status / doctor / lock / diff`
  - `aix repo status / shell / branch / commit / push`
- FuseSoC 聚合配置生成（`fusesoc.conf` / `core-roots.txt` / `vlnv-index.json` / `dependency-graph.json`）。
- GitHub Reusable Workflows V0.1 与薄入口示例。
- Change Bundle Schema 与示例。
- 单元测试与临时 Git 仓集成测试 Fixture。

### 计划（后续阶段）

- [ ] Flow DAG 执行器与 Run Manifest / Evidence Index 运行时实现。
- [ ] Change Bundle CLI 与 PR refs 联合 checkout。
- [ ] 影响分析引擎与 affected tests。
- [ ] 发布协调、SBOM、签名与 Catalog 更新 PR。
