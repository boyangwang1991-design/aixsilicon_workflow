# AIXSILICON Workflow 执行 TODO（参照 plan.md）

> 依据 [`plan.md`](plan.md) §28 实施路线图、§30 TODO List、§31 验收标准整理。
> 状态标记：[x] 已完成 · [-] 进行中 · [ ] 待办。
> 更新时间：2026-08-13（9 资产仓已同步，35 测试通过，ruff 干净）。

> 代码结构/工程化专项优化见 [`docs/optimization-plan.md`](docs/optimization-plan.md)
> （cli 拆包、context 收敛、schema 单一事实源、Makefile、补齐 run/bundle/release 命令）。

## 总览

| 阶段 | 周期 | 目标出口 | 状态 |
|---|---|---:|---|
| 阶段0 边界与ADR冻结 | 2周 | 仓库责任/依赖方向经 Owner 确认 | 基本达成，CBB/Tool/Catalog/SoCInt 内容待填充 |
| 阶段1 Workspace MVP | 3~4周 | 一条命令建环境、子仓独立提交 | 基本达成，剩 P0 缺陷 |
| 阶段2 FuseSoC与跨仓验证 | 4~6周 | 固定Lock重建APB验证闭环 | 进行中 |
| 阶段3 Change Bundle与影响分析 | 4~6周 | HWIF→VIP→IP 联合变更 | 未开始 |
| 阶段4 发布协调与Catalog | 4~6周 | IP资格验证+人工批准+Catalog更新 | 未开始 |
| 阶段5 SoC集成与规模化 | 6~8周 | SoC锁定基线可重建 | 未开始 |

---

## 阶段0：边界与 ADR 冻结

- [x] 冻结 `aixsilicon_workflow` 职责、非目标（§3）与 ADR（[`docs/adr/0001`](docs/adr/0001-manifest-over-submodule.md)、[`0002`](docs/adr/0002-schema-driven-yaml.md)）
- [x] 确认全部 P0 仓库真实 URL、default branch、owner（[`gitlist.md`](gitlist.md)：9 仓 `boyangwang1991-design`）
- [x] 固化全部仓库使用 `aixsilicon_` 前缀
- [x] 定义 Manifest / Lock / Local Override Schema V0.1（[`schemas/`](schemas/workspace-manifest.schema.json)）
- [x] 定义标准目录与 `.gitignore`（运行时目录完整忽略）
- [x] 建立 ownership map（[`ownership-map.yaml`](ownership-map.yaml)）
- [x] 建立仓库依赖 DAG（[`src/aixworkflow/graph.py`](src/aixworkflow/graph.py)，无环校验通过）
- [x] 定义 P0 CLI 错误码与安全策略（[`src/aixworkflow/errors.py`](src/aixworkflow/errors.py)、[`policies/security-policy.yaml`](policies/security-policy.yaml)）
- [x] 建立最小 Python 包和测试框架（[`pyproject.toml`](pyproject.toml)）
- [x] 建立 README Quick Start（[`README.md`](README.md)）
- [-] 初始化 `aixsilicon_cbb_repo`（已构建 ✅，内容续增）
- [ ] 初始化 `aixsilicon_tool_repo` 并迁移确定性脚本（当前仅 README 骨架）
- [ ] 初始化 `aixsilicon_catalog_repo` 并定义首版资产条目 Schema（当前仅 README 骨架）
- [ ] 初始化 `aixsilicon_soc_integration_repo` 并定义 SoC 配置 Schema 边界（当前仅 README 骨架）
- [ ] `aixsilicon_skill_repo`（私有）Skill Metadata 契约（当前仅 README 骨架）

## 阶段1：Workspace MVP

- [x] 实现 `aix wf init/sync/status/doctor/lock`（[`src/aixworkflow/cli.py`](src/aixworkflow/cli.py)）
- [x] 实现 `aix repo status/shell/branch/commit/push` + `diff`
- [x] 实现 remote、dirty、unpublished commit 保护（[`src/aixworkflow/gitops.py`](src/aixworkflow/gitops.py)、`workspace.py`）
- [x] 支持 `minimal/ip-dev/cbb-dev/dv-dev/soc-integration/release` Profile
- [x] 生成 `.aix/generated/fusesoc.conf` + core-roots/vlnv-index/dependency-graph（[`src/aixworkflow/fusesoc.py`](src/aixworkflow/fusesoc.py)）
- [x] 完成临时 Git 仓 Fixture 测试（`tests/integration/`）
- [x] 验证子仓 commit 不改变 Workflow 父仓状态
- [x] 输出本地 Lock 和状态表（`.aix/local.lock.yaml`、`aix wf status`）
- [ ] 验证所有 Core 可被 FuseSoC 发现（需安装 fusesoc 实跑）
- [ ] 完成新成员从零初始化演练（clean 环境）

### 阶段1 遗留 P0 缺陷（本次审查确认）

- [ ] 修复 lockfile `tree` 为空：`gitops.rev_parse` 追加 `^{commit}` 导致 `commit^{tree}^{commit}` 非法（[`resolver.py`](src/aixworkflow/resolver.py)；新增 `rev_parse_any`）
- [ ] `aix wf lock` 支持 `--no-fetch`/offline：避免每次强制 fetch 受网络波动影响
- [ ] 修复 `aix wf status` Baseline 列：`diverged` 分支不可达，且未对比 baseline lock
- [ ] `aix wf sync --lock` 真正按 Lockfile 的 commit 强制 checkout（当前仅切 release 模式）
- [ ] 生成真实 `locks/baseline.lock.yaml`（当前为占位模板），走 PR/CI 保护

## 阶段2：FuseSoC 与基础跨仓验证

- [x] 生成 FuseSoC 配置与 VLNV 索引（`fusesoc.py`，[`generate_vlnv_index`](src/aixworkflow/fusesoc.py)）
- [x] Core dependency graph（[`graph.py`](src/aixworkflow/graph.py)）
- [-] Flow DAG 执行器 `aix wf run <flow>`：runner 已实现（[`runner.py`](src/aixworkflow/runner.py)），**未接入 CLI**（注册 action、前置条件、Evidence 汇总）
- [ ] APB 寄存器 IP 穿刺：HWIF SystemRDL/RAL + APB VIP + DV Common 联合闭环
- [-] Run Manifest 与 Evidence Index：`evidence.py` 已实现，**未接入 run**（[`evidence.py`](src/aixworkflow/evidence.py)）
- [-] GitHub reusable lint/unit workflow：文件已建，**内容为占位**（[`.github/workflows/`](.github/workflows/reusable-fusesoc-lint.yml)）

## 阶段3：Change Bundle 与影响分析

- [x] Change Bundle Schema 与示例（[`schemas/change-bundle.schema.json`](schemas/change-bundle.schema.json)、[`changesets/examples/`](changesets/examples/CHG-2026-0042.yaml)）
- [-] Change Bundle CLI（`aix bundle create/validate/status` 为桩）：校验 merge_order、状态机
- [ ] PR refs 联合 checkout（`change-bundle.yml` 占位）
- [x] 基础影响分析（[`impact.py`](src/aixworkflow/impact.py) + [`graph.transitive_closure`](src/aixworkflow/graph.py)）
- [ ] HWIF→VIP→IP 影响规则与 affected tests（`aix wf test --affected`）
- [ ] X2X 三仓联合变更穿刺
- [-] 防递归触发与 correlation ID（[`github.py`](src/aixworkflow/github.py) 已有 guard_event_loop 桩）

## 阶段4：发布协调与 Catalog

- [x] Release Policy 与 protected environment 定义（[`policies/release-policy.yaml`](policies/release-policy.yaml)、`reusable-release-gate.yml` 占位）
- [x] 幂等发布判定（[`release.py`](src/aixworkflow/release.py) `already_published`）
- [ ] `aix release prepare/publish` 实现（当前桩）
- [ ] IP Release Skill 接入（依赖 skill_repo）
- [ ] Release Manifest / SBOM / RTM 完整性检查
- [ ] Catalog 更新 PR 自动生成（依赖 catalog_repo 内容）
- [ ] Baseline 升级与 Workspace Bundle Release
- [ ] 并发互斥与失败恢复

## 阶段5：SoC 集成与规模化

- [x] SoC 集成 Profile 与 Flow（[`manifests/soc-integration.yaml`](manifests/soc-integration.yaml)、[`workflows/soc-integration.yaml`](workflows/soc-integration.yaml)）
- [x] blue-zone / red-zone 工具 Profile（[`toolchains/`](toolchains/blue-zone.yaml)）
- [ ] 地址、中断、CRG、Power 域连接检查接口（依赖 soc_integration_repo + tool_repo）
- [ ] PIC / 功能安全集成穿刺
- [ ] 私有 Skill 可选依赖边界验证
- [ ] AIXSILICON 项目座舱接入
- [ ] 指标、容量和运营机制 / Nightly 兼容性矩阵

---

## 一期验收标准（plan.md §31）对照

- [x] 1. 一条命令按 Profile 下载全部仓库（`aix wf init` + `aix wf sync`）
- [x] 2. 子仓位于 `repos/` 并被父仓可靠忽略
- [x] 3. 任一子仓可独立建分支/commit/push，父仓无变化
- [x] 4. dirty tree、错误 remote、不可达 SHA、local override 可识别
- [ ] 5. 生成完整 FuseSoC 配置并发现全部 Core（待实跑 fusesoc）
- [x] 6. Lockfile 记录各仓 SHA 与工具 Profile（可重建）
- [ ] 7. APB 代表性 IP 完成跨仓 Lint/编译/仿真/Evidence
- [x] 8. Change Bundle 描述 HWIF+VIP+IP 联合变更（示例）
- [ ] 9. 联合 CI 拉取各仓 PR HEAD 并产生结构化结论
- [ ] 10. 发布动作前人工确认，dirty/override 环境不可发布（Gate 已定义，未端到端跑）
- [ ] 11. 失败 Run 定位到仓库/SHA/Stage/工具/Failure Signature（runner 就绪，未接入 run）
- [x] 12. README、协作规范、故障文档可用

## 风险对照（plan.md §32，重点盯防）

- [ ] 防止 Workflow 变成超级仓库（ownership map + CI Guard 已建，需持续执行）
- [ ] Manifest 与 Catalog 不重复（Catalog 未建内容，先定边界）
- [ ] 只锁 Git 不锁工具 → Tool Profile 与生成器一并锁定
- [ ] 多仓自动提交失控 → 保持单仓显式命令
- [ ] 影响分析漏测 → 未知依赖按扩大范围
- [ ] EDA 产物撑爆仓库 → ignore + pre-commit Guard 已建，落地 `pre-commit install`
