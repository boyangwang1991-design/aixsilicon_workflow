# ADR-0002：所有工作区/流程/证据事实以 YAML SSOT + JSON Schema 固化

- 状态：接受
- 日期：2026-08-13

## 背景

多仓协同的可靠性与可复现性依赖“事实唯一”。Manifest、Lockfile、Flow、Change Bundle、Tool Profile、Evidence 都需要机器可校验、可迁移、可审计。

## 决策

- 事实文档一律使用 YAML 作为 SSOT；
- 每个文档类型对应一份 JSON Schema（`schemas/`）；
- CLI 在任何使用前先做 Schema 校验；
- 生成物（RTL、Header、FuseSoC Core）必须由工具从 SSOT 确定性派生，不能手改漂移。

## 备选方案

- 仅 JSON：可读性差，不适合人工维护；
- 无 Schema 的自由 YAML：无法拒绝非法组合，破坏可复现性；
- TOML：生态支持弱于 YAML，且 YAML 已用于 HWIF/SoC 体系。

## 结果

- 正向：非法配置在入口即被拒绝，跨工具契约稳定；
- 负向：Schema 演进需要版本化与迁移路径；
- 权衡：Schema 跟随 `aixworkflow` 包内嵌与仓库 `schemas/` 双份，由测试 `test_schema_parity` 防止漂移。
