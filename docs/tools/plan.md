# tools — AIXSILICON Tool Repository 建设规划

> 客观事实基线：2026-08-13（P0 五包已实现并接入 `aix tool`）。原文细节见 [`../archived/architecture/repo-plans/tools.md`](../archived/architecture/repo-plans/tools.md)。
> 本文件以**附录**形式并入 archived 原文的完整规划细节：五层架构（§4）、统一 Result 契约（§7）、CLI 设计（§23）、插件机制（§24/§48）、Tool 全地图（§44.1–44.15）。

## 1. 定位与边界

**定位**：跨仓公共**确定性执行能力**（生成/检查/转换/打包），经 `aixsilicon.commands` 插件暴露为 `aix tool`；是 T1 工具的核心载体。

| 归属（T1 公共工具） | 不归本仓 |
|---|---|
| 确定性生成/检查/转换/打包工具 | workflow 的 Gate 编排 |
| `aixsilicon.commands` 插件 | Skill 的方法判断 |
| 工具版本锁（workspace-lock `tools:`） | 资产仓事实源 |
| | T2 单仓脚本（留资产仓）/ T3 私有适配（私有 overlay）/ T4 项目脚本（项目仓） |

边界判断规则：相同输入应产生语义相同输出 → Tool；能定义严格输入输出 Schema → Tool；负责步骤顺序/重试/Gate → Workflow；需要大模型理解和专业判断 → Skill/Agent；保存设计事实或源码 → 资产仓。能力进入正式 Tool 前必须满足：输入/输出契约明确、错误码稳定、幂等策略明确、单元测试充分、Golden Case 存在、Owner 明确。

## 2. 现状（客观）

- **P0 五包已实现并接入 `aix tool` 实跑**：
  - `aix-tool-core`：Result/Diagnostic/Artifact 契约、分段退出码、插件入口；
  - `aix-schema`：validate/lint/diff（`migrate` 骨架待补）；
  - `aix-hwif-gen`：Contract→SV package/interface/flat 视图 + `--check-only` + `hac-generate`；
  - `aix-reg-tool`：PeakRDL 封装 validate/generate（RTL/RAL/Header/Doc）+ 一致性 check；
  - `aix-core-tool`：core list/lint/init/graph；
- `make check` 全绿（30 用例）；五包全部注册进 `aixsilicon.commands`；
- **缺口**：`aix wf run` 的 `tool.*` 阶段转真实 provider；workspace-lock `tools:` 段；`reference/` 适配测试。

## 3. 依赖与角色

- **依赖**：无；
- **被依赖**：soc-integration（`depends_on` 含 tools），及 IP/CBB/SoC 主线的 `tool.*` action；
- **IP 主线角色**：`tool.reg-gen` / `tool.schema` / `tool.core-tool` 执行确定性生成；
- **SoC 主线角色**：`tool.address-gen/irq-gen/crg-gen/top-gen/sw-gen/connect-check` 派生 SoC 视图。

## 4. 契约

- **CLI**：`aix` 唯一入口，本仓注册 `tool` 插件（Entry Point 组 `aixsilicon.commands`）；
- **退出码分段**：0 成功 / 10 使用错误 / 20 输入或契约失败 / 30 环境依赖缺失（`OPTIONAL_UNAVAILABLE`）/ 40 工具内部错误 / 50 输出校验失败 / 60 安全拒绝；
- **成熟度**：experimental/preview/qualified/production/deprecated/retired；
- **可复现**：同输入 + 同版本 → 语义一致输出（确定性）；写操作支持 `--dry-run/--check` 且路径白名单。

## 5. 建设路线（客观）

| 阶段 | 状态 |
|---|---|
| S0 aix-tool-core（底座） | ✅ 完成 |
| S1 aix-schema | ✅ 完成（migrate 骨架待补） |
| S2 aix-hwif-gen | ✅ 完成 |
| S3 aix-reg-tool | ✅ 完成 |
| S4 aix-core-tool | ✅ 完成 |
| S5 集成（插件/真实 provider/版本锁/CI） | 🔶 五包已注册，`aix wf run` 转真实 provider 待做 |
| 扩展（P1） | aix-project-init / aix-param-matrix / aix-dv-gen / aix-ppa-bench / aix-socgen / aix-connect-check 等 |

## 附录 A：五层架构（§4）

| 层级 | 责任 | 典型内容 |
|---|---|---|
| T0 Foundation | 所有工具共享的稳定底座 | Config、Schema、Result、Logging、Hash |
| T1 Domain Model | 领域中间表示 | HWIF IR、CSR IR、SoC IR、Asset IR |
| T2 Tool Engine | 确定性生成和分析 | Generator、Checker、Normalizer |
| T3 Adapter | 外部系统适配 | FuseSoC、PeakRDL、EDA、Git、Catalog |
| T4 Interface | 对 Agent/Workflow 开放 | CLI、Python API、Plugin、JSON Result |

依赖必须单向：`Interface → Tool Engine → Domain Model → Foundation`（另分支 `→ Adapter`）；单个工具不能反向依赖 Workflow 或私有 Skill。技术选型：一期以 Python 3.11+ 为主，性能敏感模块可用 Rust/C++ 但必须保留相同结构化 CLI/API 契约；人工维护事实优先 YAML，Schema 统一 JSON Schema Draft 2020-12，机器输出默认 JSON；用 `pyproject.toml` + Entry Points 管理包与插件，CLI 薄封装调用同一 Python API，禁止两套业务逻辑。

## 附录 B：统一 Result / Diagnostic / Artifact 契约（§7）

- **状态语义**：`pass`（继续）/ `pass_with_warnings`（按 Policy 处理）/ `fail`（Gate 失败）/ `error`（工具/环境/依赖故障，可重试）/ `skip`（记录原因）；工具不得仅用日志文本表达结果。
- **退出码分段**：0 成功 / 10–19 输入-Schema 错误 / 20–29 设计或规则检查失败 / 30–39 外部工具-环境错误 / 40–49 文件-权限-安全错误 / 50–59 兼容性-版本错误 / 60–69 内部错误。
- **Result 结构**：`schema_version(aix.tool-result/v1) + tool(id/version) + run(id/mode) + status + exit_code + summary(errors/warnings) + diagnostics(code/severity/message/source{file/path}) + artifacts(type/path/sha256)`。
- **状态与 Gate 关系**：Tool 输出事实和指标，Workflow/Policy 决定是否通过（如 `aix-report` 解析 `unconstrained_paths=2` → 解析成功 ≠ 设计通过，Timing Policy 判定 Gate FAIL）。

## 附录 C：统一 CLI 设计（§23）

- 顶层形式：`aix tool <domain> <command> [options]`；命令域：`schema / hwif / reg / core / project / params / dv / soc / connect / ppa / report / rtm / package / catalog`。
- 通用参数：`--input/--output/--profile/--config/--workspace/--format json|yaml|text/--result-file/--artifact-dir/--dry-run/--check/--strict/--offline/--no-color/--log-level`。
- CLI 契约：交互式友好输出走 stdout，日志/诊断走 stderr；`--format json` 必须只有机器 JSON；所有写操作支持 `--dry-run/--check`；输出目录显式或由 Tool Context 提供；默认不覆盖 SSOT；支持无 TTY CI 运行；相同主版本 CLI 参数向后兼容，deprecated 参数至少保留一个 minor 窗口。
- Agent-Native 接口：`capabilities / explain / plan / dry-run / execute / result / artifacts / version`；AI 安全约束——只通过允许的 Tool ID 调用、执行前报告读写集合、写路径受 Ownership Map 限制、不执行输入 YAML 中任意 Shell、不把 Prompt 拼进命令、不得据 warning 自改 pass、建议与判定分字段、所有生成记录 Tool 版本/输入 Hash/模板版本。

## 附录 D：插件机制（§24/§48）

- **Entry Point 组**：统一以 `aixsilicon.` 为前缀演进（规划中的 `aix.tools` / `aix.report_adapters` / `aix.soc_generators` 等组名统一收敛），如 `[project.entry-points."aixsilicon.commands"] tool = "..."`、`"aixsilicon.report_adapters" yosys = "..."`、`"aixsilicon.soc_generators" irq = "..."`。
- **插件 Manifest**：`plugin(id/version/api_version/supports{tool,versions}/input_schema/output_schema)`；私有插件可安装到运行环境由标准 Entry Point 发现，公共 Repo 不引用其源码路径。
- **CLI 入口（ADR-0004）**：`aix` 为唯一总入口，本仓通过 `aixsilicon.commands` 注册 `tool` 插件；Workflow 通过 Tool Registry 解析工具，不在 Flow 中硬编码仓库脚本路径；工具版本锁入 workspace-lock `tools:` 段（`version/source/sha256` 或 `git_commit`）。

## 附录 E：Tool 全地图（§44.1–44.15 摘要）

工具处置四类：`SELF`（自研完整实现）/ `WRAP`（封装成熟开源工具：Adapter+Profile+Result Parser）/ `EXTERNAL`（商业 EDA：抽象接口+Schema+Mock）/ `DEFER`（只记录需求不进入 P0/P1）。

- **44.1 需求/规格/项目初始化**：`aix.spec.validate`、`aix.trace.validate`、`aix.asset.init`、`aix.asset.metadata`（P0）；`aix.doc.build/linkcheck`、`aix.diagram.data`、`aix.change.impact`（P1）。自然语言规格生成器归私有 Skill。
- **44.2 资产发现与依赖管理**：`aix.catalog.query/validate`、`aix.core.lint/graph/generate`、`aix.license.scan`、`aix.vendor.lock`、`aix.asset.compatibility`。FuseSoC 为主包管理入口，Bender 只作 Lockfile/源集导出参考，不并行建第二套依赖事实源。
- **44.3 架构/接口/数据模型**：`aix.hwif.validate/generate/compatibility`（P0）、`aix.hwif.diff`、`aix.arch.graph`、`aix.config.space`、`aix.ir.inspect`（P1）、`aix.ipxact.export/import-check`（P2）。IP-XACT 不取代 YAML SSOT。
- **44.4 CSR 与软硬件接口**：`aix.reg.validate/rtl/ral/cheader/doc`（P0，WRAP/扩展 PeakRDL）、`aix.reg.diff/test`（P1）、`aix.reg.ipxact`（P2）。优先扩展 PeakRDL 而非重写 Compiler。
- **44.5 RTL 编码/语法/静态质量**：`aix.rtl.format/style/compile-lint`（WRAP Verible/Verilator，P0）、`aix.rtl.parse`（Surelog/UHDM，P1）、`aix.rtl.metrics/rule`（P1）、`aix.rtl.diff-semantic`（P2）、`aix.rtl.waiver`、`aix.generated.drift`（P0）。至少区分 Style Lint / Compile Lint / Structural / CDC-RDC / Low-Power / Signoff Lint，不叫模糊 `lint`。
- **44.6 CBB 专用**：`aix.params.validate/matrix`（P0）、`aix.cbb.harness/property-bind/impl-profile/equivalence/ppa-sweep/pareto`（P1）、`aix.cbb.mutation`（P2）。
- **44.7 功能验证与回归**：`aix.dv.init/testlist/vip-bind/ral-bind/run-manifest/result`（P0）、`aix.dv.coverage/plan-check/seed/failure-signature/cross-model`（P1）、`aix.dv.flaky`（P2）。总调度归 Workflow，不把 DVSim 嵌套为第二总编排器。
- **44.8 Assertion/Formal/等价**：`aix.formal.harness/bind/plan/run/result`（P1）、`aix.formal.vacuity`（P2）、`aix.equiv.run`（P1）；SymbiYosys 作开源 Formal Adapter 基础。
- **44.9 CDC/RDC/Clock-Reset/低功耗**：`aix.clock.intent`、`aix.reset.intent`（P0）、`aix.cdc.intent-compile`、`aix.rdc.intent-compile`、`aix.cdc.result`、`aix.rdc.result`、`aix.sync.recognize`、`aix.power.intent`（P1）、`aix.upf.crosscheck`、`aix.lowpower.result`（P2）。不自研 Signoff 引擎，价值在 Intent SSOT/约束派生/Waiver 治理/结果归一化。
- **44.10 综合/STA/PPA**：`aix.constraint.validate`、`aix.synth.run/result`、`aix.sta.run/result`、`aix.power.result`、`aix.ppa.sweep/compare/pareto`、`aix.qor.health`（P0/P1）；Yosys/OpenSTA/OpenROAD 作开源基线，商业 Signoff 走 Adapter。
- **44.11 SoC 集成与系统生成**：`aix.soc.validate/resolve`、`aix.address.resolve`、`aix.irq.resolve`、`aix.connect.check`（P0）、`aix.crg.resolve`、`aix.power.resolve`、`aix.interconnect.resolve`、`aix.top.generate`、`aix.integration.assert`、`aix.soc.doc`（P1）、`aix.soc.diff`（P2）。参考 OpenTitan topgen 的“配置→生成→autogen 禁止手改”机制，不继承 TL-UL/HJSON。
- **44.12 软件协同/Boot/FPGA**：`aix.sw.header`（P0）、`aix.sw.dts/linker/bsp-metadata/hw-crosscheck`（P1）、`aix.boot.image`、`aix.fpga.target/result`、`aix.emulation.adapter`（P2）。软件视图必须与 CSR/SoC SSOT 同源。
- **44.13 DFT/功能安全/网络安全**：`aix.fusa.mechanism-map`、`aix.sec.connect-check`（P1）、`aix.dft.intent/result`、`aix.fusa.fault-campaign/metric-result`、`aix.sec.asset-map/formal-result`（P1/P2）。专业判断（FMEA/威胁分析/Safety Concept）归私有 Skill 与人工评审。
- **44.14 Release/开源治理/供应链**：`aix.release.validate/package`、`aix.catalog.patch`、`aix.provenance.collect`、`aix.secret.scan`（P0）、`aix.release.sbom`、`aix.license.reuse`、`aix.release.sign`（P1）。
- **44.15 暂不值得自研的引擎**：SV 完整编译器/仿真器、UVM 内核、SAT/SMT/Formal 求解器、CDC/RDC Signoff、综合/STA/Power Signoff、P&R/CTS/DRC/LVS、ATPG/Fault Simulator/Memory Compiler、Emulator/FPGA 厂商引擎、波形数据库/Debug GUI、Git 托管/CI 调度器/制品库——只维护统一 Adapter/Capability/Tool Profile/Result Schema/Mock/兼容测试。

**收敛后建设组合**：P0（12 项）以 `aix-tool-core + aix-schema + aix-hwif-gen + aix-reg-tool + aix-core-tool` 为真正 P0，先用 APB 寄存器 IP 打通统一契约/生成/FuseSoC/验证/发布，再扩展 CBB 参数/PPA（P1-A），最后进入 SoC Address/IRQ/CRG/TopGen（P1-B），P2 做 Signoff/原型/生态。

## 附录 F：成熟度 / 测试体系 / 版本治理（§29–31）

- **成熟度**：experimental（不进 Gate）/ preview（试点、可设非阻断 Gate）/ qualified（正式 Workflow）/ production（Release/Signoff 支撑）/ deprecated / retired。Preview→Qualified 至少需：API/CLI/Schema 冻结、Unit/Contract/Golden/Integration Test 通过、两种以上真实资产验证、错误/异常路径覆盖、文档示例完整、Reproducibility 通过、Owner 与 SLA 明确、许可证与 SBOM 通过。
- **测试体系**：Unit / Schema / Contract / Golden / Metamorphic / Property-based / Integration / Reproducibility / Migration / Security / Performance。Golden 必须小而可读、生成器升级后不得盲目批量接受、CI 展示语义 Diff、非确定字段不入关键内容、Golden 更新由领域 Owner Review。真实穿刺：APB 寄存器 IP（Schema/HWIF/CSR/Core/DV/RTM/Package）、Async FIFO（参数矩阵/Formal-CDC 报告/PPA/Catalog）、PIC 最小 SoC（SoCGen/Address/IRQ/CRG/Connect/SW View）。
- **版本治理**：每 Package 独立 SemVer；Breaking Change（删/改 CLI 参数、改 API 签名、改 Result/Artifact Schema、改关键生成语义、改错误码含义、改插件 API、移除已支持输入构造）需 major；Tool 版本与输出 Schema 版本分离（`tool_version` + `result_schema` + `artifact_schema`）。FuseSoC Generator 集成只做参数化 wrapper/CSR fileset/局部 Core/测试实例/构建目录派生 Core，不得在 Generator 参数中重述完整 SoC、下载未锁外部依赖、修改源码仓 SSOT、执行发布或调用 LLM。

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/tools.md`](../archived/architecture/repo-plans/tools.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件以附录并入 archived `repo-plans/tools.md` §4 五层架构、§7 Result 契约、§23 CLI、§24/§48 插件机制与 CLI 入口、§44.1–44.15 Tool 全地图、§29–31 成熟度/测试/版本治理、§46 收敛建设组合。
