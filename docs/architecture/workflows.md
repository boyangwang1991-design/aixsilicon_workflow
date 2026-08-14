# Workflow 统筹方案（workflows）

> 本页回答：**Workflow 如何统筹各 repo，完成 IP 设计验证与 SoC 集成验证两条主线**，以及支撑流程在框架中的位置、统筹矩阵与 Gate 卡点。
> 数据源：[`workflows/*.yaml`](../../workflows)、[`src/aixworkflow/actions.py`](../../src/aixworkflow/actions.py)、[`manifests/default.yaml`](../../manifests/default.yaml)。

---

## 1. 统筹模型总述（五要素）

Workflow 对仓库的统筹不是“脚本串一串”，而是五要素共同作用：

| 要素 | 载体 | 作用 |
|---|---|---|
| **Flow DAG** | `workflows/*.yaml`（`aix.flow/v1`） | 声明 Stage 顺序、`needs` 依赖、`preconditions`、`gates` |
| **注册 action** | [`src/aixworkflow/actions.py`](../../src/aixworkflow/actions.py) + `aix tool` 插件 | 确定性执行单元；调用工具/仓内脚本，**绝不执行 Flow YAML 任意 Shell**；环境缺失时 `OPTIONAL_UNAVAILABLE`/`skipped` |
| **write_scope** | Stage 上的 `write_scope` | 声明本 Stage 写哪个仓、哪些路径，实施写入边界 |
| **Gate** | G0–G7 | 卡在关键节点，由证据（Run Manifest/Log/Report/Hash）驱动，不凭摘要自证 |
| **Evidence** | Run Manifest + Evidence Index | 把“谁跑过、用什么版本、结果如何”结构化留存 |

### 8 个 Workflow 全景

| Workflow | 定位 | 主线/支撑 | 覆盖 Gate |
|---|---|---|---|
| [`ip-development.yaml`](../../workflows/ip-development.yaml) | IP 设计开发主线 | **主线一** | G0–G4, G6 |
| [`ip-verification.yaml`](../../workflows/ip-verification.yaml) | IP 发布前联合资格验证 | **主线一** | G0–G7 |
| [`apb-register-ip.yaml`](../../workflows/apb-register-ip.yaml) | APB 寄存器 IP 端到端穿刺 | 主线一（示例/穿刺） | — |
| [`soc-integration.yaml`](../../workflows/soc-integration.yaml) | SoC 集成与验证主线 | **主线二** | G0–G6 |
| [`hwif-change.yaml`](../../workflows/hwif-change.yaml) | 接口契约变更子流程 | 支撑 | G0–G6 |
| [`vip-development.yaml`](../../workflows/vip-development.yaml) | VIP/DV Common 开发 | 支撑 | G0–G2, G4–G6 |
| [`cross-repo-qualification.yaml`](../../workflows/cross-repo-qualification.yaml) | 跨仓 Change Bundle 联合验证 | 支撑 | G0–G6 |
| [`release-train.yaml`](../../workflows/release-train.yaml) | 发布协调（候选→批准→发布） | 支撑 | G0–G7 |

> 核心纪律：**Skill 决定“如何理解与辅助”→ Workflow 决定“顺序与 Gate”→ Tool 负责“确定性执行”→ 资产仓保存 SSOT → Catalog 发布 → EDA 提供证据**（详见 [`overview.md`](overview.md) §3）。

---

## 2. 主线一：IP 设计验证端到端

**入口**：`ip-development`（设计）→ `ip-verification`（发布前验证）→ `release-train`（发布进 Catalog）。
**输入**：`ip_vlnv`、`tool_profile`、`lock_required`。
**输出**：可发布的 IP（RTL/CSR/验证/文档）+ Evidence + Catalog 条目。

### 2.1 阶段编排与统筹（设计主线）

| 阶段 | 关键 action | 统筹的 repo（读写） | 目的 |
|---|---|---|---|
| resolve | `workspace.resolve` | workflow（Manifest/Lock）+ 全体 repos | 解析工作区、生成 FuseSoC 聚合配置 |
| spec | `skill.ip.spec` | **写 ip**（metadata/docs/testplan） | 规格与测试计划 |
| contract | `hwif.compatibility-check` | **读 hwif**（契约/Profile） | 接口兼容性判定 |
| csr | `tool.reg-gen` | **写 ip**（csr/rtl/dv）；读 hwif | SystemRDL→CSR/RAL/Header 确定性生成 |
| rtl | `skill.ip.rtl` | **写 ip**（rtl） | RTL 实现（AI 辅助生成/编码） |
| lint | `fusesoc.target`(lint) | hwif/cbb/ip（FuseSoC 聚合） | 静态检查 |
| unit | `fusesoc.target`(unit_sim) | ip + dv-common + vip | 单元仿真 |
| regression | `eda.regression` | ip 验证环境（dv-common/vip） | 功能回归 |
| ppa | `eda.synthesis` | ip/cbb（tool_profile） | 实现评估（综合/PPA） |
| evidence | `evidence.index` | workflow（Evidence Index） | 汇总证据 |

### 2.2 阶段编排与统筹（发布前验证）

| 阶段 | 关键 action | 统筹的 repo | 目的 |
|---|---|---|---|
| resolve | `workspace.resolve` | workflow + 全体 repos | clean/locked 环境 |
| contract | `hwif.compatibility-check` | 读 hwif | 契约校验 |
| lint / unit | `fusesoc.target` | hwif/cbb/ip + dv-common/vip | 门禁检查 |
| regression | `eda.regression` | ip 验证环境 | 联合回归（level 可配置） |
| package | `release.package` | ip（release 材料） | 打包发布物 |
| evidence | `evidence.index` | workflow | 证据汇总 |

### 2.3 Gate 卡点与证据链

- `ip-development` 覆盖 **G0–G4 + G6**（设计侧：卫生→解析→依赖→契约→构建单测→证据）；
- `ip-verification` 覆盖 **G0–G7**（含 **G5** 跨仓资格与 **G7** 发布就绪，是进入 release-train 的前置）；
- 端到端证据链：Run Manifest → 报告 → Hash → Evidence Index →（经 `release-train`）Catalog 条目。

---

## 3. 主线二：SoC 集成验证端到端

**入口**：`soc-integration`（消费 Catalog 已发布资产）。
**输入**：`soc_project`、`tool_profile`、`lock_required`。
**输出**：SoC Top、软件派生（BSP/Header/DTS）、集成验证结果、集成基线。

### 3.1 阶段编排与统筹

| 阶段 | 关键 action | 统筹的 repo（读写） | 目的 |
|---|---|---|---|
| resolve | `workspace.resolve` | workflow + 全体 repos | 解析工作区 |
| asset-selection | `catalog.resolve` | **读 catalog**（资产条目） | 按项目选型已发布资产 |
| instance-config | `soc.schema-check` | **读 soc-integration**（schema/规则）；**写 chip-\<project\>-soc**（config/instances） | SoC 配置与实例化 |
| address-space / interrupt / clock-reset / power-safety | `tool.address-gen` / `tool.irq-gen` / `tool.crg-gen` / `tool.power-check` | **读 soc-integration**；写 chip-\<project\>-soc | 地址/中断/CRG/Power 派生 |
| topgen | `tool.top-gen` | **写 chip-\<project\>-soc**（generated） | Top 生成 |
| sw-derive | `tool.sw-gen` | **写 sw**（bsp/headers/dts） | 软件侧确定性派生 |
| connectivity-check | `tool.connect-check` | 读 hwif/soc-integration | 连通性检查 |
| build-sim | `fusesoc.target`(soc_top_sim) | hwif/cbb/ip + dv-common/vip + chip-\<project\>-soc | 构建 SoC 仿真 |
| boot-smoke | `eda.regression`(boot-smoke) | SoC 验证环境 | 启动冒烟 |
| baseline | `soc.baseline` | workflow（lock） | 锁定集成基线 |
| evidence | `evidence.index` | workflow | 证据汇总 |

### 3.2 Gate 卡点与证据链

- `soc-integration` 覆盖 **G0–G6**（集成侧不强制 G7，发布由 release-train 管理）；
- 证据链：SoC 配置 → 派生生成物 → 构建/仿真报告 → baseline lock → Evidence Index。

---

## 4. 支撑流程定位（在框架中的位置）

| 支撑流程 | 服务对象 | 一句话定位 |
|---|---|---|
| **hwif-change** | 主线一/二的上游能力 | 接口契约变更→语义检查→多视图生成→SemVer 判定→下游影响验证（VIP 编译/CBB-IP 受影响编译/SoC 消费者） |
| **vip-development** | 主线一/二的验证组件 | 公共 API 变更→单元→模拟器矩阵→自检→参考 DUT→代表性回归→系统抽查→覆盖率基线 |
| **cross-repo-qualification** | 跨仓 Change Bundle | 拉取 Bundle 所有 PR HEAD→依赖图→影响分析→必需 target→代表性回归→结论 |
| **release-train** | 主线一/二产出 → Catalog | 候选版本→clean/locked 确认→资格验证→材料检查（docs/RTM/manifest/SBOM）→版本/CHANGELOG→**人工批准**→tag/release→Catalog 更新→Bundle 证据 |

> 这 4 个支撑流程**不逐 stage 罗列**——它们是主线上游的“能力/契约”供给与下游的“发布/联验”出口，具体 stage 见对应 [`workflows/*.yaml`](../../workflows)。

---

## 5. workflow × repo 统筹矩阵

| 仓库 | ip-development | ip-verification | soc-integration | hwif-change | vip-development | cross-repo-qual | release-train |
|---|---|---|---|---|---|---|---|
| **hwif** | 读契约 | 读契约 | 读契约/连通 | **写/生成** | 读 | 影响分析 | 发布（随资产） |
| **cbb** | 依赖复用 | 依赖复用 | 实例化 | 受影响编译 | 代表性回归 | 影响分析 | 发布 |
| **ip** | **写本体** | **写/打包** | 实例化 | 受影响编译 | 参考 DUT | 影响分析 | **发布主体** |
| **dv-common** | 验证底座 | 验证底座 | 验证底座 | — | **写公共组件** | 影响分析 | — |
| **vip** | 验证组件 | 验证组件 | 系统验证 | 编译测试 | **写协议组件** | 影响分析 | 发布 |
| **tools** | 生成/检查 | 生成/检查 | **生成派生** | 生成 | 生成/自检 | — | — |
| **catalog** | 读/更新 | 读 | **选型** | 兼容矩阵更新 | — | 依赖一致性 | **写条目** |
| **soc-integration** | — | — | **写规则/校验** | 消费规则 | — | — | — |
| **skills** | 指导 | — | — | — | 指导 | — | — |
| **knowledge** | 参考 | 参考 | 参考 | 参考 | 参考 | — | — |

> 加粗 = 该流程在该仓的主要写动作或关键消费点；`—` = 无直接动作。

---

## 6. 主线之间的衔接

1. **发布衔接**：主线一（IP 设计验证）产出经 `ip-verification` + `release-train` 写入 Catalog → 主线二（SoC 集成验证）从 `catalog.resolve` 选型实例化。
2. **契约衔接**：`hwif-change` 维护的契约是两条主线共同的输入；契约变更触发下游影响验证（VIP 编译、CBB-IP 受影响编译、SoC 消费者）。
3. **跨仓改动**：跨多仓功能走 **Change Bundle**（`aix bundle create/validate`）→ `cross-repo-qualification` 联合验证 → 按 `merge_order` 合入。
4. **证据可重建**：所有主线/支撑流程的结论均由 Run Manifest + Evidence Index + 固定 SHA（Lockfile）支持重建。

---

## 7. 方案讨论要点（开放问题 / 待决策）

1. **命名统一**：`dv-common`、`soc-integration` 无 `_repo` 后缀，与其余 7 仓不一致，是否统一改名。
2. **工具迁移阶段**：T1 工具按 ADR-0006 阶段 A 双入口 → 阶段 B `aix tool` → 阶段 C deprecated 的迁移节奏如何排期。
3. **私有 Overlay 接入点**：商业 EDA/PDK/Memory 适配（T3）以何种 capability 声明接入公共 Flow，且公共 Flow 不硬编码私有路径。
4. **流程粒度**：`apb-register-ip` 作为端到端穿刺示例，是否作为标准“Hello World”基准持续维护。
5. **证据门禁强度**：Gate 是否全部由 Evidence + Hash 驱动（避免“目录存在即通过”），各 Gate 的最小证据集如何定义。

---

## 8. 相关文档

- 被统筹对象：**[repos.md](repos.md)**
- 关系框图：**[relationship-diagram.md](relationship-diagram.md)**
- 各仓计划/待办：**[docs/index.md](../index.md)** §各仓 Plan / Todo
- 门禁定义：**[README.md](../../README.md)** §质量 Gate；成熟度：**[docs/workflow/maturity-model.md](../workflow/maturity-model.md)**
