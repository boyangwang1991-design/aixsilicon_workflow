# Action Inventory — 8 条 Flow 与注册表对照

> 证据类型：决策证据（WF-003 / ADR-0008）
> 生成方式：从 `workflows/*.yaml` 提取 `uses:` 名称，与 runner 注册表 [`src/aixworkflow/runner.py`](../src/aixworkflow/runner.py) `default_registry()` 对照。
> 生成日期：2026-08-17
> 对应 Finding：F-004（46 个唯一使用名中 40 个未注册）；本表为 F-004 关闭证据的基线起点。
> 状态说明：`registered` = runner 内置注册；`gap` = 未注册（计划由 ADR-0008 preflight 统一能力矩阵覆盖）。

## 1. 汇总

| 指标 | 数值 |
|---|---|
| 唯一 `uses:` 名称总数 | **46** |
| 已注册能力 | **6** |
| 缺口（未注册） | **40** |
| 涉及的 Flow 文件 | 8 |
| 覆盖的域 | workspace / hwif / tool / fusesoc / eda / release / catalog / soc / bundle / git / graph / impact / flow / skill / evidence |

> 与 F-004 完全吻合：46 个唯一使用名中 40 个未注册。
> 别名说明：`hwif.compatibility` 是 `hwif.compatibility-check` 的别名（[`runner.py`](../src/aixworkflow/runner.py) L63），Flow 中未单独使用，不计入唯一名。

## 2. 完整对照表

| # | Action（uses） | 出现在 Flow | 注册状态 | 建议 Provider / 落点 | 备注 |
|---|---|---|---|---|---|
| 1 | `workspace.resolve` | apb-register-ip, ip-development, ip-verification, soc-integration | ✅ registered | workflow builtin | 基础 DAG + FuseSoC 配置 |
| 2 | `workspace.clean-check` | release-train | ❌ gap | workflow builtin | F-002 dirty/unlocked 判定 |
| 3 | `hwif.compatibility-check` | apb-register-ip, ip-development, ip-verification | ✅ registered | hwif repo 脚本（ADR-0006 迁移 tool_repo） | 别名 `hwif.compatibility` |
| 4 | `tool.schema` | apb-register-ip | ❌ gap | aixsilicon_tool_repo | `aix tool schema` |
| 5 | `tool.reg` | apb-register-ip | ❌ gap | aixsilicon_tool_repo | `aix tool reg` |
| 6 | `tool.schema-check` | hwif-change | ❌ gap | aixsilicon_tool_repo | Schema 校验 |
| 7 | `tool.contract-semantics` | hwif-change | ❌ gap | aixsilicon_tool_repo | 契约语义 |
| 8 | `tool.hwif-gen` | hwif-change | ❌ gap | aixsilicon_tool_repo | HWIF 视图生成 |
| 9 | `tool.semver-impact` | hwif-change | ❌ gap | aixsilicon_tool_repo | SemVer 影响 |
| 10 | `tool.reg-gen` | ip-development | ❌ gap | aixsilicon_tool_repo | CSR 生成 |
| 11 | `tool.address-gen` | soc-integration | ❌ gap | aixsilicon_tool_repo | 地址生成 |
| 12 | `tool.irq-gen` | soc-integration | ❌ gap | aixsilicon_tool_repo | 中断生成 |
| 13 | `tool.crg-gen` | soc-integration | ❌ gap | aixsilicon_tool_repo | clock/reset 生成 |
| 14 | `tool.power-check` | soc-integration | ❌ gap | aixsilicon_tool_repo | 电源检查 |
| 15 | `tool.top-gen` | soc-integration | ❌ gap | aixsilicon_tool_repo | Top 生成 |
| 16 | `tool.sw-gen` | soc-integration | ❌ gap | aixsilicon_tool_repo | SW 视图 |
| 17 | `tool.connect-check` | soc-integration | ❌ gap | aixsilicon_tool_repo | 连接检查 |
| 18 | `fusesoc.target` | apb-register-ip, cross-repo-qualification, hwif-change, ip-development, ip-verification, soc-integration, vip-development | ✅ registered | fusesoc CLI | 依赖外部工具 |
| 19 | `eda.regression` | apb-register-ip, cross-repo-qualification, ip-development, ip-verification, soc-integration, vip-development | ✅ registered | EDA provider | 显式 argv |
| 20 | `eda.synthesis` | ip-development | ❌ gap | EDA provider | PPA/synthesis |
| 21 | `eda.simulator-matrix` | vip-development | ❌ gap | EDA provider | 多 simulator |
| 22 | `eda.self-check` | vip-development | ❌ gap | EDA provider | VIP 自检 |
| 23 | `eda.reference-dut` | vip-development | ❌ gap | EDA provider | 参考 DUT |
| 24 | `eda.coverage-baseline` | vip-development | ❌ gap | EDA provider | coverage 基线 |
| 25 | `evidence.index` | apb-register-ip, cross-repo-qualification, hwif-change, ip-development, ip-verification, release-train, soc-integration, vip-development | ✅ registered | runner builtin | 证据收集（Schema 标记） |
| 26 | `release.package` | ip-verification | ✅ registered | workflow builtin | G7 guard 在内部 |
| 27 | `release.select-candidate` | release-train | ❌ gap | release/catalog | 候选选择 |
| 28 | `release.check-material` | release-train | ❌ gap | release/catalog | 物料检查 |
| 29 | `release.check-version` | release-train | ❌ gap | release/catalog | 版本检查 |
| 30 | `release.human-approval` | release-train | ❌ gap | release/catalog | 人工批准 |
| 31 | `release.tag` | release-train | ❌ gap | release/catalog | Tag 创建 |
| 32 | `release.bundle-evidence` | release-train | ❌ gap | release/catalog | Bundle 证据 |
| 33 | `catalog.update` | apb-register-ip | ❌ gap | catalog repo | Catalog 更新 |
| 34 | `catalog.compatibility-update` | hwif-change | ❌ gap | catalog repo | 兼容性更新 |
| 35 | `catalog.update-pr` | release-train | ❌ gap | catalog repo | Catalog PR |
| 36 | `catalog.resolve` | soc-integration | ❌ gap | catalog repo | 资产解析 |
| 37 | `soc.schema-check` | soc-integration | ❌ gap | soc-integration / tool | SoC Schema 校验 |
| 38 | `soc.baseline` | soc-integration | ❌ gap | soc-integration / tool | 基线生成 |
| 39 | `bundle.resolve` | cross-repo-qualification | ❌ gap | workflow bundle | Change Bundle 解析 |
| 40 | `git.checkout-pr-refs` | cross-repo-qualification | ❌ gap | workflow gitops | PR HEAD checkout |
| 41 | `graph.build` | cross-repo-qualification | ❌ gap | workflow graph | 依赖图构建 |
| 42 | `impact.analyze` | cross-repo-qualification, hwif-change | ❌ gap | workflow impact | 影响分析 |
| 43 | `flow.qualification` | release-train | ❌ gap | workflow flow | 资格 Flow 执行 |
| 44 | `skill.ip.spec` | ip-development | ❌ gap | skill provider | IP 规格（可选） |
| 45 | `skill.ip.rtl` | ip-development | ❌ gap | skill provider | RTL（可选） |
| 46 | `skill.vip.design` | vip-development | ❌ gap | skill provider | VIP 设计（可选） |

## 3. 缺口分布（按域）

| 域 | 缺口数 | 关键 action |
|---|---|---|
| tool | 14 | schema / reg / 各 gen / check |
| eda | 5 | synthesis / simulator-matrix / self-check / reference-dut / coverage-baseline |
| release | 6 | select-candidate / check-material / check-version / human-approval / tag / bundle-evidence |
| catalog | 4 | update / compatibility-update / update-pr / resolve |
| soc | 2 | schema-check / baseline |
| skill | 3 | ip.spec / ip.rtl / vip.design |
| workspace | 1 | clean-check |
| bundle | 1 | resolve |
| git | 1 | checkout-pr-refs |
| graph | 1 | build |
| impact | 1 | analyze |
| flow | 1 | qualification |
| **合计** | **40** | 注册 6 + 缺口 40 = 46 |

## 4. 结论与下一步

1. **当前 8 条 Flow 均无法在 clean workspace 完整执行**：6/46 注册率远不足以支撑端到端；未注册 action 走 `blocked` 路径（F-001）。
2. **ADR-0008 preflight 是必要基础设施**：capability matrix 应在 stage 执行前判定 `available / optional-unavailable / unimplemented / version-mismatch / environment-unavailable`。
3. **M1 首件工作**：为 40 个缺口 action 逐一确定 provider 落点（上表"建议 Provider"列）、版本约束与 availability，形成可执行 inventory。
4. 本表作为 F-004 关闭证据的**基线**；每实现一个 provider 更新本表状态，直至 M3 真实 APB Evidence 关闭 F-004。
