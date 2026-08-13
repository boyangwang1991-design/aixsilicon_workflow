# dv-common — AIXSILICON DV Common Repository 规划与待办

> 来源：repos/aixsilicon_dv_common/plan.md + TODO.md（完整剪切至 docs/architecture/repo-plans 统一管理）
> 迁移日期：2026-08-13
> 仓库实现现状见 docs/architecture/repos.md §1.4

---

## 一、plan.md 完整原文

# AIXSILICON DV Common Repository 完整规划

> 文档版本：V1.0
> 日期：2026-08-12
> 适用范围：IP设计、CBB验证、VIP开发、Subsystem/SoC集成验证、UVM Verification Skill Suite
> 建议仓库名：`aix-dv-common`

---

## 1. 建设结论

`DV Common Repo` 应定位为组织级、与具体协议和具体DUT无关的验证基础设施库，而不是某个项目的 `base_test` 集合，也不是VIP仓库的公共目录。

它在完整资产体系中的位置是：

```text
HW Interface Repo  ──定义接口契约──┐
                                   │
DV Common Repo ──提供通用验证机制──┼──> IP/CBB/VIP/SubSystem/SoC DV环境
                                   │
VIP Repo ──提供协议激励与检查──────┘

EDA Flow ──负责运行、调度、合并、报告和发布
```

核心目标：

1. 让新IP验证环境不再重复生成日志、超时、Clock/Reset、RAL、Scoreboard和结果收集代码；
2. 让不同VIP、不同IP和SoC级环境使用一致的配置、状态、错误码、事务比较和证据格式；
3. 为UVM Verification Skill Suite提供稳定、可发现、可版本锁定的组件，而不是每次由大模型重新发明基础设施；
4. 支持从IP单元验证平滑组合到Subsystem/SoC验证，而不构造一个臃肿的“万能Base Env”；
5. 通过FuseSoC、SemVer、Catalog和质量Gate实现可复用验证资产的工程化发布。

### 1.1 推荐形态

- 一个独立Monorepo；
- 内部按小粒度package/component拆分；
- 每个稳定组件族发布为独立FuseSoC Core；
- 提供一个方便项目使用的聚合Core，但不要求项目全部依赖；
- 依赖方向严格单向，公共库不得依赖任何协议VIP或具体IP；
- UVM类库与轻量SystemVerilog仿真模块分层发布；
- 配置、结果和证据使用YAML/JSON Schema；
- UVM源码以可移植子集为准，CI覆盖现网UVM 1.2与IEEE 1800.2演进基线。

### 1.2 一期最小闭环

一期不要追求组件数量，应优先打通：

> Test启动 → Clock/Reset → RAL访问 → VIP事务 → Scoreboard比较 → Timeout/错误判定 → 结果与证据输出

一期P0组件：

1. `dv_common_types`；
2. `dv_log_report`；
3. `dv_test_status`；
4. `dv_clk_rst`；
5. `dv_timeout_watchdog`；
6. `dv_sequence_base`；
7. `dv_ral_csr`；
8. `dv_scoreboard`；
9. `dv_compare`；
10. `dv_mem_backdoor`；
11. `dv_config`；
12. `dv_result_schema`。

---

## 2. 为什么必须独立建设DV Common Repo

如果没有公共验证底座，典型问题会快速累积：

- 每个IP都有一套不同的Base Test、日志格式和结束条件；
- VIP、IP Env、SoC Env分别实现Clock/Reset和Timeout；
- Scoreboard队列、乱序匹配、compare policy反复复制；
- RAL reset、bit-bash、HW reset、shadow register等公共sequence各自维护；
- 仿真“PASS”只依赖日志中出现某个字符串，缺少机器可读结果；
- Seed、工具版本、Git revision、FuseSoC lock信息没有统一固化；
- Skill生成的代码与手工环境风格不一致，难以持续维护；
- 单元环境能够运行，但组合到Subsystem/SoC后公共服务冲突；
- 对UVM `config_db`、factory override和全局report catcher滥用，产生隐式耦合；
- 换仿真器、换UVM版本或接入回归系统时需要逐项目修改。

DV Common的价值不只在于减少代码量，更重要的是统一“验证环境怎样表达配置、怎样判断通过、怎样输出证据”。

---

## 3. 仓库边界

### 3.1 本仓库负责什么

| 领域 | DV Common负责内容 |
|---|---|
| 基础类型 | 状态、错误、严重度、端点ID、事务ID、时间与统计类型 |
| 测试骨架 | 精简Base Test、Base Env contract、phase/lifecycle helper |
| 配置 | 公共配置对象、plusarg解析、Schema校验、配置快照 |
| 日志与状态 | 统一Message ID、错误聚合、退出码、PASS/FAIL判定 |
| 时钟复位 | 通用Clock/Reset生成、监测、序列和Reset通知 |
| 运行保护 | Timeout、Watchdog、deadlock/liveness基础机制 |
| Sequence服务 | Reset、CSR、Memory、Interrupt等待等通用序列骨架 |
| RAL/CSR | Base RAL扩展、CSR sequence、predictor辅助、排除策略 |
| Scoreboard | In-order/out-of-order基础队列、matcher、flush与drain机制 |
| Compare | 可插拔比较策略、mask/tolerance/don't-care策略 |
| Memory | 镜像、初始化、backdoor/frontdoor抽象、ECC数据辅助 |
| Coverage基础 | 通用采样器、coverage enable/control、结果导出接口 |
| Fault/Test control | 通用故障请求与生命周期接口，不含具体故障模型 |
| 证据 | Run manifest、test result、failure signature、metric schema |
| 工具适配 | 与仿真器隔离的薄适配层，不包含回归调度器 |

### 3.2 明确不归本仓库的内容

| 内容 | 应归属 |
|---|---|
| AXI/APB/UART等transaction、driver、monitor、协议checker | VIP Repo |
| AXI interface、interrupt contract、ready/valid类型 | HW Interface Repo |
| CDC FIFO、位宽转换器、桥接器 | CBB Repo |
| IP专用reference model和算法golden model | IP Repo或HW Models Repo |
| IP专用scoreboard业务规则 | 所属IP验证目录 |
| IP Testplan、功能覆盖点、用例 | 所属IP Repo |
| SoC地址分配、中断号、Clock/Reset topology | SoC Integration Repo/项目Repo |
| 仿真调度、集群提交、coverage merge、rerun | EDA Flow Repo |
| Lint/CDC/coverage门限与组织规则 | EDA Rules Repo |
| SystemRDL寄存器事实源 | 所属IP Repo |
| UVM本身的源码 | 外部依赖或工具提供，不复制进DV Common |
| 商业VIP适配细节 | VIP Repo的adapter层 |

### 3.3 三个关键判断原则

1. **是否与协议有关**：有关则优先进入VIP；无关且可被三类以上环境使用，才考虑DV Common。
2. **是否与DUT功能有关**：有关则留在IP/Subsystem/SoC项目；公共库只提供机制和扩展点。
3. **是否负责“怎么运行”**：大规模回归和EDA命令属于Flow；DV Common只提供仿真内运行时能力和结构化输出。

### 3.4 禁止演变成万能Base Env

公共库不发布包含所有服务的单一 `aix_base_env`。推荐：

- 小型service/component按需实例化；
- 每个服务有清晰input/output和生命周期；
- 通过显式config object传递依赖；
- 使用聚合Core方便依赖，但不形成运行时强绑定；
- 项目可以组合自己的Base Env，公共库只定义最小contract。

---

## 4. 与完整仓库体系的关系

| 仓库 | 提供给DV Common | 从DV Common获得 |
|---|---|---|
| HW Interface | 基础类型、interface contract、时钟复位语义 | TB helper和验证适配规范 |
| VIP | 协议transaction和analysis port | 日志、config、scoreboard、sequence、result服务 |
| IP/CBB | DUT专用配置、模型、功能规则 | 公共测试与验证机制 |
| SoC Integration | 系统拓扑、实例、地址/中断映射 | SoC级公共服务与证据格式 |
| HW Models | reference model API/实现 | adapter、compare和生命周期服务 |
| EDA Flow | 工具、运行矩阵、回归入口 | 标准result/manifest/signature |
| EDA Rules | Gate与waiver规则 | 可被规则检查的统一元数据 |
| Release Catalog | 版本索引、兼容关系 | 已发布Core、成熟度与证据 |
| Skill Suite | 生成规划和项目上下文 | 稳定模板、API、合法组合规则 |

### 4.1 单向依赖规则

```text
UVM / simulator abstraction
          ↓
dv_common_types
          ↓
utility + service + policy packages
          ↓
optional aggregate core
          ↓
VIP / IP Env / SoC Env
```

禁止：

- `dv-common → axi-vip`；
- `dv-common → concrete IP RAL model`；
- `dv-common → soc_top_pkg`；
- `dv-common → project test`；
- 底层package反向依赖聚合package。

---

## 5. 总体技术架构

### 5.1 六层组件模型

| 层 | 名称 | 主要内容 |
|---|---|---|
| L0 | Types & Contracts | 类型、枚举、接口契约、Schema |
| L1 | Utilities | queue、ID、random、string、CRC、mask、统计工具 |
| L2 | Runtime Services | log、status、timeout、objection、config、manifest |
| L3 | Reusable Components | clk/rst、scoreboard、memory、coverage、fault control |
| L4 | UVM Framework | base test/env contract、sequence、RAL服务、virtual sequencer |
| L5 | Integration Adapters | FuseSoC target、Flow结果适配、Skill模板、示例环境 |

依赖只能从上层指向下层。L0/L1中尽量避免UVM依赖，使部分工具可用于非UVM测试台。

### 5.2 组合优于继承

推荐：

- Base Class只定义最小稳定接口；
- 行为变化使用policy object；
- 功能增加使用service/component组合；
- 端口连接使用TLM和显式adapter；
- 状态传播使用typed event/service，避免散落的global event pool；
- 不以多层继承实现项目特性。

### 5.3 配置显式化

公共配置分为四层：

1. `run_cfg`：seed、timeout、verbosity、wave、tool profile；
2. `env_cfg`：active/passive、scoreboard、coverage、RAL开关；
3. `service_cfg`：某个公共服务的具体参数；
4. `project_cfg`：由项目自定义，不进入公共库。

禁止让任意组件通过通配路径自行从 `uvm_config_db` 搜索大量离散字段。推荐顶层只放少量强类型config handle，再显式下发。

---

## 6. 完整组件清单与优先级

### 6.1 L0：基础类型与契约

| 组件 | 作用 | 优先级 |
|---|---|---|
| `dv_common_types_pkg` | status、severity、result、ID、time等公共类型 | P0 |
| `dv_component_contract_pkg` | service lifecycle、reset-aware、drainable等接口 | P0 |
| `dv_result_types_pkg` | test/run/failure/metric结构 | P0 |
| `dv_schema` | YAML/JSON Schema | P0 |
| `dv_capability_pkg` | 组件能力声明和兼容性 | P1 |
| `dv_version_pkg` | 运行时版本与ABI标识 | P1 |

### 6.2 L1：无协议工具类

| 组件 | 作用 | 优先级 |
|---|---|---|
| `dv_queue_utils` | typed queue、bounded queue、flush、peek | P0 |
| `dv_id_allocator` | ID分配、回收、泄漏检查 | P0 |
| `dv_match_utils` | key/hash/tag匹配辅助 | P0 |
| `dv_compare_utils` | mask、wildcard、tolerance、field policy | P0 |
| `dv_random_utils` | weighted choice、受控shuffle、seed派生 | P1 |
| `dv_data_utils` | endian、pack/unpack、byte enable、alignment | P1 |
| `dv_crc_ecc_utils` | 通用CRC/ECC计算辅助，不绑定某协议 | P1 |
| `dv_stats_utils` | counter、histogram、latency统计 | P1 |
| `dv_string_path_utils` | 命名、路径、格式化、稳定ID | P1 |
| `dv_file_utils` | 受限文本/hex加载，带错误处理 | P1 |

### 6.3 L2：运行时服务

| 服务 | 核心能力 | 优先级 |
|---|---|---|
| `dv_log_service` | Message ID、结构化字段、日志上下文 | P0 |
| `dv_status_service` | PASS/FAIL/SKIP/ABORT统一判定 | P0 |
| `dv_failure_service` | 失败聚合、首错、signature、分类 | P0 |
| `dv_timeout_service` | 全局/局部timeout、诊断回调 | P0 |
| `dv_watchdog_service` | 活跃度、事务进展、deadlock观察 | P0 |
| `dv_reset_service` | Reset事件、epoch、reset-aware通知 | P0 |
| `dv_config_service` | 配置解析、快照、来源追踪 | P0 |
| `dv_manifest_service` | 生成run manifest | P0 |
| `dv_objection_guard` | objection泄漏检测和drain保护 | P1 |
| `dv_seed_service` | seed树和子组件可复现派生 | P1 |
| `dv_heartbeat_service` | 多源heartbeat聚合 | P1 |
| `dv_phase_trace` | phase耗时和生命周期诊断 | P2 |
| `dv_resource_audit` | config/resource/factory审计 | P2 |

### 6.4 L3：可复用仿真组件

| 组件 | 核心能力 | 优先级 |
|---|---|---|
| `dv_clk_gen` | 频率、占空比、相位、动态启停 | P0 |
| `dv_rst_gen` | 同步/异步assert/deassert、复位序列 | P0 |
| `dv_clk_rst_monitor` | 周期、稳定性、reset epoch观测 | P0 |
| `dv_scoreboard_base` | 输入、期望、匹配、flush、drain | P0 |
| `dv_in_order_matcher` | 顺序比较 | P0 |
| `dv_out_of_order_matcher` | key/tag/ID乱序匹配 | P0 |
| `dv_memory_model_base` | 稀疏/密集镜像、byte enable、unknown policy | P0 |
| `dv_mem_backdoor` | HDL/DPI/abstract backdoor adapter | P0 |
| `dv_coverage_control` | enable、sample gating、instance标识 | P1 |
| `dv_latency_tracker` | request/response延迟和outstanding统计 | P1 |
| `dv_interrupt_service` | 与协议无关的中断等待/记录抽象 | P1 |
| `dv_fault_control` | fault request、activation、observation生命周期 | P1 |
| `dv_shutdown_manager` | 多组件drain与安全结束 | P1 |
| `dv_perf_monitor_base` | 通用吞吐/占用/延迟采集 | P2 |

### 6.5 L4：UVM框架

| 组件 | 核心能力 | 优先级 |
|---|---|---|
| `dv_base_test` | 最小测试生命周期和公共服务装配 | P0 |
| `dv_env_contract` | env需要暴露的最小状态/端口约定 | P0 |
| `dv_base_virtual_sequence` | objection、reset、timeout、cfg handle | P0 |
| `dv_virtual_sequencer_base` | 仅提供注册机制，不预定义具体VIP sequencer | P0 |
| `dv_reset_sequence` | 通用reset操作接口 | P0 |
| `dv_csr_sequence_lib` | smoke、reset、rw、bit-bash等 | P0 |
| `dv_ral_base` | reg block/map/field公共扩展 | P0 |
| `dv_ral_predictor_utils` | predictor和adapter连接辅助 | P0 |
| `dv_mem_sequence_lib` | init、walk、random、front/backdoor compare | P1 |
| `dv_irq_sequence_base` | 等待、屏蔽、超时、确认抽象 | P1 |
| `dv_error_injection_seq_base` | 错误注入生命周期模板 | P1 |
| `dv_smoke_sequence_base` | 环境bring-up模板 | P1 |
| `dv_sw_sequence_adapter` | SoC软件与UVM同步抽象 | P2 |

### 6.6 L5：适配与示例

| 内容 | 说明 | 优先级 |
|---|---|---|
| FuseSoC Core/target | 编译、lint、unit、smoke、example | P0 |
| APB寄存器IP示例 | 首个完整穿刺 | P0 |
| AXI bridge示例 | 乱序、reset、backpressure场景 | P1 |
| PIC示例 | interrupt/fault/coverage场景 | P1 |
| Flow result adapter | JSON/JUnit/HTML入口 | P1 |
| Skill templates | 环境生成与组件选择规则 | P1 |
| SoC boot示例 | UVM+software协同 | P2 |

---

## 7. 推荐仓库结构

```text
aix-dv-common/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODEOWNERS
├── fusesoc/
│   ├── aix_dv_common_types.core
│   ├── aix_dv_common_utils.core
│   ├── aix_dv_common_runtime.core
│   ├── aix_dv_common_ral.core
│   ├── aix_dv_common_scoreboard.core
│   ├── aix_dv_common_mem.core
│   ├── aix_dv_common_uvm.core
│   └── aix_dv_common_all.core
├── src/
│   ├── types/
│   │   ├── dv_common_types_pkg.sv
│   │   ├── dv_component_contract_pkg.sv
│   │   └── dv_result_types_pkg.sv
│   ├── utils/
│   │   ├── dv_queue_pkg.sv
│   │   ├── dv_id_pkg.sv
│   │   ├── dv_compare_pkg.sv
│   │   ├── dv_data_pkg.sv
│   │   └── dv_stats_pkg.sv
│   ├── runtime/
│   │   ├── dv_log_pkg.sv
│   │   ├── dv_status_pkg.sv
│   │   ├── dv_timeout_pkg.sv
│   │   ├── dv_watchdog_pkg.sv
│   │   ├── dv_reset_service_pkg.sv
│   │   ├── dv_config_pkg.sv
│   │   └── dv_manifest_pkg.sv
│   ├── components/
│   │   ├── clk_rst/
│   │   ├── scoreboard/
│   │   ├── memory/
│   │   ├── coverage/
│   │   ├── interrupt/
│   │   └── fault/
│   ├── ral/
│   │   ├── dv_ral_pkg.sv
│   │   ├── dv_csr_seq_pkg.sv
│   │   └── dv_ral_adapter_contract_pkg.sv
│   └── uvm/
│       ├── dv_base_test_pkg.sv
│       ├── dv_base_vseq_pkg.sv
│       └── dv_vseqr_pkg.sv
├── rtl/
│   ├── dv_clk_gen.sv
│   ├── dv_rst_gen.sv
│   ├── dv_sim_timeout.sv
│   └── dv_signal_probe_if.sv
├── dpi/
│   ├── include/
│   ├── src/
│   └── README.md
├── schemas/
│   ├── component.schema.yaml
│   ├── run_config.schema.yaml
│   ├── run_manifest.schema.yaml
│   ├── test_result.schema.yaml
│   ├── failure.schema.yaml
│   └── metric.schema.yaml
├── metadata/
│   ├── components.yaml
│   ├── compatibility.yaml
│   ├── message_ids.yaml
│   └── deprecations.yaml
├── unit/
│   ├── types/
│   ├── utils/
│   ├── runtime/
│   ├── scoreboard/
│   ├── ral/
│   └── memory/
├── examples/
│   ├── minimal_uvm/
│   ├── apb_csr_ip/
│   ├── axi_bridge/
│   └── pic_interrupt/
├── tests/
│   ├── compile_matrix/
│   ├── negative/
│   ├── reset_stress/
│   └── portability/
├── docs/
│   ├── architecture.md
│   ├── dependency_rules.md
│   ├── component_catalog.md
│   ├── api/
│   ├── migration/
│   └── examples/
├── tools/
│   ├── schema_check/
│   ├── dep_check/
│   ├── api_diff/
│   ├── result_check/
│   └── doc_gen/
└── release/
    ├── release_manifest.yaml
    ├── sbom.spdx.json
    └── evidence/
```

### 7.1 为什么保留`rtl/`

Clock/Reset generator、仿真timeout等是非综合SystemVerilog module，不适合全部包装成UVM class。将其与UVM层隔开，有利于：

- 非UVM testbench复用；
- Verilator或轻量仿真场景使用；
- 减少class世界对信号时序的间接控制；
- 单独lint和编译。

### 7.2 为什么保留DPI但严格限制

DPI只用于文件、压缩、性能敏感模型、外部模型桥接等必要场景。每个DPI组件必须：

- 有纯SV fallback或明确声明不支持；
- 声明平台、编译器和仿真器矩阵；
- 不让公共核心组件依赖DPI；
- 单独Core发布；
- 具备内存/线程安全检查。

---

## 8. 公共API设计规范

### 8.1 最小Base Test

`dv_base_test`只负责：

- 创建/获取强类型run config；
- 安装status、failure、timeout和manifest服务；
- 统一test start/end；
- 收集最终结果；
- 不实例化任何具体VIP；
- 不假设某个DUT寄存器模型存在；
- 不写项目专用virtual sequence选择逻辑。

### 8.2 Service生命周期

公共service统一支持：

```text
configure → start → reset_notify → quiesce → drain → finalize
```

每个service应声明：

- 是否reset-aware；
- 是否需要drain；
- 是否产生最终metric；
- 是否影响test pass/fail；
- thread ownership；
- 销毁和重复启动语义。

### 8.3 Reset Epoch

所有可能跨reset保存状态的组件必须使用 `reset_epoch`：

- reset assert时epoch递增；
- transaction记录所属epoch；
- scoreboard默认禁止跨epoch匹配；
- outstanding事务按policy选择flush、error或preserve；
- coverage可按epoch分组；
- reset中的错误是否计入FAIL由显式policy决定。

### 8.4 Scoreboard API

Scoreboard公共层只提供：

- `write_actual()`；
- `write_expected()`；
- `match()`；
- `flush(reason)`；
- `drain(timeout)`；
- `get_pending_count()`；
- `get_statistics()`；
- matcher和compare policy插槽。

业务层必须提供：

- transaction key；
- compare policy；
- reference model调用；
- reset/错误响应的业务预期。

### 8.5 Compare Policy

至少支持：

- exact；
- field mask；
- byte enable；
- X/Z policy；
- integer tolerance；
- floating-point absolute/relative/ULP tolerance；
- unordered collection；
- ignored metadata；
- 自定义field callback。

比较失败必须输出结构化diff，而不是只打印整对象。

### 8.6 配置优先级

建议固定为：

```text
Schema Default < Organization Profile < Project Config < Test Config < CLI Override
```

最终值必须记录来源，避免出现“为什么这个开关是1”无法追溯。

### 8.7 Message ID治理

Message ID格式：

```text
AIX_DV_<DOMAIN>_<EVENT>
```

例如：

- `AIX_DV_CFG_INVALID`；
- `AIX_DV_SB_MISMATCH`；
- `AIX_DV_SB_PENDING`；
- `AIX_DV_TIMEOUT_GLOBAL`；
- `AIX_DV_RAL_PREDICT`；
- `AIX_DV_RESET_EPOCH`。

禁止使用难以稳定聚类的自由文本作为回归signature。

---

## 9. RAL与CSR公共能力

### 9.1 SystemRDL与UVM RAL边界

- SystemRDL是寄存器事实源，归所属IP；
- PeakRDL生成UVM RAL模型；
- DV Common提供RAL基类、公共sequence、排除/策略对象和连接辅助；
- VIP提供具体总线RAL adapter；
- IP Env负责选择map、adapter、predictor和backdoor路径。

### 9.2 P0 CSR Sequence

1. CSR smoke；
2. HW reset value；
3. RW access；
4. bit-bash；
5. access policy检查；
6. frontdoor/backdoor一致性；
7. reset中断访问；
8. 非法地址/错误响应，由项目与VIP提供行为；
9. volatile字段采样；
10. shadowed/lockable寄存器扩展钩子。

### 9.3 CSR排除机制

不要在sequence中硬编码寄存器名。统一使用metadata/policy表达：

```yaml
csr_exclusions:
  - pattern: "*.status.live_*"
    tests: [bit_bash, rw]
    reason: "hardware-updated volatile field"
    requirement_id: "LRS-CSR-042"
  - pattern: "*.key*"
    tests: [backdoor_compare]
    reason: "write-only security material"
```

排除项必须有reason，安全/功能安全项目建议绑定requirement ID。

---

## 10. Clock、Reset、Timeout与Watchdog

### 10.1 Clock Generator

需支持：

- 周期或频率配置；
- duty cycle；
- phase offset；
- start/stop/gate；
- 平滑/立即频率切换策略；
- jitter扩展接口；
- 多时钟命名和状态查询；
- 结构化metric输出。

### 10.2 Reset Generator

需支持：

- active-high/low；
- synchronous/asynchronous assertion/deassertion；
- pulse width；
- power-on reset和warm reset类型；
- reset during traffic；
- 多reset域；
- reset cause；
- reset epoch广播。

Clock/Reset波形的协议性assertion属于HW Interface或VIP的checker，DV Common只提供产生、监测和事件服务。

### 10.3 Timeout层级

| 类型 | 作用 |
|---|---|
| Global timeout | 防止整个test无限运行 |
| Phase timeout | 约束某阶段 |
| Operation timeout | CSR、memory、sequence等单操作 |
| Progress timeout | 有线程但无有效进展 |
| Drain timeout | 结束时等待outstanding清空 |

Timeout触发时必须先执行诊断hook：打印outstanding、scoreboard pending、objection holder、最近heartbeat和reset状态，再结束测试。

---

## 11. 结果、证据与可追溯Schema

### 11.1 Test Result

```yaml
schema_version: 1.0
test:
  name: apb_csr_smoke
  requirement_ids: [LRS-CSR-001, LRS-APB-014]
run:
  id: run-20260812-00124
  seed: 19283746
  status: PASS
  exit_code: 0
  start_time: "2026-08-12T10:00:00+08:00"
  duration_s: 12.47
failure:
  count: 0
  primary_signature: null
metrics:
  transactions: 1024
  scoreboard_matched: 1024
  scoreboard_pending: 0
artifacts:
  log: sim.log
  wave: null
  coverage: cov.ucdb
```

### 11.2 Run Manifest

必须记录：

- 仿真器与版本；
- UVM版本/profile；
- FuseSoC/Edalize版本；
- 顶层Core VLNV；
- 所有依赖Core的VLNV与Git revision；
- 编译/运行参数的归一化摘要；
- seed和派生seed；
- 配置快照及来源；
- RTL、VIP、DV Common、RAL model版本；
- 容器/OS/toolchain profile；
- waiver/rule profile；
- artifact checksum。

### 11.3 Failure Signature

推荐由以下字段构成：

```text
message_id + component_path_class + transaction_type + normalized_location + root_cause_tag
```

动态数值、时间戳、seed、地址等不稳定字段不直接进入signature，可作为附加context。这样AIXSILICON项目座舱才能可靠聚类。

### 11.4 Exit Code

| Exit Code | 含义 |
|---:|---|
| 0 | PASS |
| 1 | DUT/Checker功能失败 |
| 2 | Testbench基础设施失败 |
| 3 | Compile/Elaboration失败 |
| 4 | Timeout/Deadlock |
| 5 | 配置或Schema错误 |
| 6 | Tool/License/Environment错误 |
| 7 | ABORT/用户终止 |
| 8 | SKIP/不适用，是否视为流水线成功由Flow决定 |

---

## 12. FuseSoC组织

### 12.1 Core拆分

推荐VLNV：

```text
aix:dv:common_types:1.0.0
aix:dv:common_utils:1.0.0
aix:dv:common_runtime:1.0.0
aix:dv:common_scoreboard:1.0.0
aix:dv:common_ral:1.0.0
aix:dv:common_memory:1.0.0
aix:dv:common_uvm:1.0.0
aix:dv:common_all:1.0.0
```

### 12.2 推荐Target

| Target | 用途 |
|---|---|
| `lint` | SV静态检查 |
| `compile` | 最小编译 |
| `unit` | 组件单测 |
| `smoke` | 聚合基本运行 |
| `negative` | 失败路径、timeout、schema非法输入 |
| `example` | 示例工程 |
| `portability` | 多工具/UVM profile编译运行 |
| `package` | 发布检查 |

FuseSoC适合表达源码、依赖、parameters和最小target；Nightly矩阵、coverage merge和集群调度由EDA Flow完成。

### 12.3 聚合Core约束

`common_all`只聚合依赖，不允许：

- 增加新的运行时全局对象；
- 改变子Core编译宏；
- 隐式启用DPI；
- 隐式启用coverage；
- 引入任何VIP。

---

## 13. UVM版本与多工具策略

### 13.1 基线建议

短期采用双profile：

| Profile | 定位 |
|---|---|
| `uvm12_legacy` | 兼容现网商业仿真环境 |
| `uvm1800_2` | 新项目和长期演进目标 |

源码原则：

- 尽量使用两者公共的标准API；
- 不访问UVM内部未文档化成员；
- 避免依赖单一仿真器扩展；
- 版本差异集中在`compat/`薄层；
- 对Accellera实现特有API必须显式标注和隔离；
- 每个Release声明已验证的仿真器/UVM组合。

Accellera官方`uvm-core`是IEEE 1800.2参考实现并明确区分标准API、Accellera扩展及兼容API，适合作为新基线与可移植性审计依据：[Accellera UVM Core](https://github.com/accellera-official/uvm-core)。

### 13.2 建议工具矩阵

| 层级 | 工具矩阵 |
|---|---|
| PR必选 | 主力商业仿真器1种 + 快速lint |
| Nightly | VCS/Xcelium/Questa中组织可用的至少2种 |
| 周期性 | Verilator可编译子集、第三种商业工具 |
| Release | 所有声明支持组合完整执行 |

这里不应在规划中写死具体版本；Catalog Release记录经过验证的版本范围。

---

## 14. 元数据与组件Catalog

```yaml
component:
  name: dv_scoreboard
  vlnv: aix:dv:common_scoreboard:1.2.0
  category: reusable_component
  owner: dv-platform
  maturity: qualified

dependencies:
  - aix:dv:common_types:^1.0
  - aix:dv:common_utils:^1.1

capabilities:
  reset_aware: true
  drainable: true
  ordered_match: true
  out_of_order_match: true
  structured_diff: true

compatibility:
  uvm_profiles: [uvm12_legacy, uvm1800_2]
  simulators: [vcs, xcelium, questa]

quality:
  lint: pass
  unit_test: pass
  negative_test: pass
  portability: pass

evidence:
  release_manifest: release/release_manifest.yaml
  report: release/evidence/qualification.json
```

Skill Suite只从Catalog中选择达到`qualified`且兼容目标tool profile的组件。

---

## 15. 成熟度与质量Gate

### 15.1 成熟度

| 状态 | 含义 |
|---|---|
| Draft | API和行为仍可重构 |
| Experimental | 可PoC，不允许关键项目默认使用 |
| Candidate | API冻结，进入多项目验证 |
| Qualified | 通过完整Gate，可进入正式项目 |
| Deprecated | 只维护兼容和安全修复 |
| Retired | Catalog不再推荐，新项目禁止使用 |

### 15.2 发布Gate

| Gate | 检查内容 |
|---|---|
| G0 边界 | 不依赖VIP/IP/项目；职责清晰 |
| G1 结构 | dependency DAG、命名、package导入、无循环 |
| G2 静态 | lint、格式、未使用代码、宏污染 |
| G3 单测 | 正常、边界、随机和失败路径 |
| G4 Reset | reset before/during/after transaction、multi-reset |
| G5 Portability | UVM profile和多仿真器矩阵 |
| G6 性能 | 仿真时间和内存无不可接受回退 |
| G7 证据 | Schema、manifest、API文档、example完整 |
| G8 项目验证 | 至少两个不同IP/环境成功复用 |
| G9 Release | SemVer、changelog、license、SBOM、Catalog |

### 15.3 单元测试要求

每个组件至少覆盖：

- 默认配置；
- 最小/最大合法配置；
- 非法配置；
- reset；
- timeout；
- 空输入；
- 并发/乱序，如适用；
- flush/drain；
- 重复启动/结束；
- 结构化结果校验；
- 内存/对象泄漏的可观测替代检查。

### 15.4 性能基线

记录：

- 编译时间；
- elaboration时间；
- 仿真wall time；
- 峰值内存；
- 每百万transaction开销；
- 大型RAL模型查找耗时；
- report数量和日志体积。

公共库的功能正确不等于可发布，显著性能回退必须Gate。

---

## 16. CI/CD与自动发布

### 16.1 PR流水线

1. Schema/metadata校验；
2. 依赖方向和循环检查；
3. 格式、lint、license header；
4. 受影响Core编译；
5. 单元测试和negative测试；
6. 最小示例；
7. API diff；
8. 文档链接检查；
9. 结果Schema自校验。

### 16.2 Nightly

- 全量Core和examples；
- 多仿真器、多UVM profile；
- reset stress；
- randomized seed；
- performance benchmark；
- long-running scoreboard/memory测试；
- failure signature稳定性测试；
- 与VIP主干版本集成测试。

### 16.3 Release

```text
Tag候选
  → 全Gate
  → 生成API/依赖diff
  → 生成release manifest与SBOM
  → 生成资格证据
  → 签署Tag/Release
  → 更新统一Catalog
  → 通知下游依赖更新窗口
```

### 16.4 兼容性CI

对每个Candidate Release，至少验证：

- VIP Repo当前稳定版；
- 一个APB/CSR IP；
- 一个含乱序事务的AXI类IP；
- 一个Subsystem/SoC环境；
- UVM Verification Skill生成的最小工程。

---

## 17. 版本治理

### 17.1 SemVer规则

| 变更 | 版本 |
|---|---|
| 新增可选组件/方法，默认行为不变 | Minor |
| 修复bug，不改变合法用户行为 | Patch |
| 删除/改名公共类、方法、字段 | Major |
| 默认compare/reset/timeout语义变化 | Major |
| 结果Schema新增可选字段 | Minor |
| 结果Schema删除/改变必选字段 | Major |
| 新增仿真器兼容修复 | Patch或Minor，视API而定 |

### 17.2 API稳定性

- `public`、`protected extension`、`internal`三级；
- 只有public进入兼容承诺；
- extension point有明确override契约；
- internal文件不允许下游直接import；
- CI扫描下游是否使用internal symbol；
- field macro、factory override、config key也属于API。

### 17.3 Deprecated流程

1. Minor版本标记deprecated；
2. 提供替代API和迁移文档；
3. 至少保留一个稳定发布周期；
4. Major版本才删除；
5. Catalog记录影响范围；
6. Skill模板先迁移，再允许删除旧接口。

---

## 18. 开源参考项目与采用建议

### 18.1 推荐参考矩阵

| 项目 | 可重点借鉴 | 采用方式 | 注意事项 |
|---|---|---|---|
| Accellera UVM Core | 标准API、版本兼容、deviation管理 | 标准基线，不复制源码 | 区分IEEE API与实现扩展 |
| OpenTitan `hw/dv/sv` | DV utils、RAL扩展、CIP通用环境、scoreboard/log风格 | 架构和局部实现参考 | 去除TL-UL、HJSON、项目层级耦合 |
| OpenTitan DVSim | 配置、回归、结果和Flow组织 | EDA Flow参考 | 不把DVSim本体塞进DV Common |
| PULP `common_verification` | clk/rst、sim timeout、stream watchdog、queue | 轻量组件PoC | 多为非UVM；需多工具审计 |
| OpenHW CORE-V-VERIF | 多核公共库、日志、环境复用、ISS协同 | SoC/CPU环境参考 | 项目和Makefile耦合较强 |
| Surelog/UHDM相关测试生态 | SystemVerilog解析可移植性 | 补充静态兼容检查 | 不能替代商业仿真运行 |

官方入口：

- [Accellera UVM Core](https://github.com/accellera-official/uvm-core)
- [OpenTitan Common SystemVerilog and UVM Components](https://opentitan.org/book/hw/dv/sv/index.html)
- [OpenTitan DVSim](https://opentitan.org/book/util/dvsim/index.html)
- [PULP Common Verification](https://github.com/pulp-platform/common_verification)
- [OpenHW CORE-V-VERIF](https://github.com/openhwgroup/core-v-verif)

PULP的`common_verification`明确提供常用非综合SystemVerilog模块和类，例如clock/reset generator、simulation timeout和stream watchdog，适合用来校验轻量仿真组件边界，但不应直接决定组织级UVM架构：[PULP Common Verification README](https://github.com/pulp-platform/common_verification/blob/master/README.md)。

CORE-V-VERIF的`lib`和多核环境适合参考“公共能力支撑多个具体环境”的组织方式；其文档也明确反对试图用一个万能环境覆盖所有核，这与本规划的组合式设计一致：[CORE-V Verification Environment](https://github.com/openhwgroup/core-v-verif/blob/master/docs/VerifStrat/source/corev_env.rst)。

### 18.2 开源引入流程

1. 来源与license确认；
2. 代码粒度和依赖审计；
3. 协议/行为测试；
4. 多仿真器与UVM profile编译；
5. 隔离PoC；
6. 决定“直接依赖、重构吸收、只参考、不采用”；
7. 保留版权和NOTICE；
8. SBOM和来源commit固化；
9. 内部API重构；
10. 通过本仓库Gate后发布。

不得整仓复制OpenTitan或CORE-V-VERIF，也不得把不同license代码混入而不保留来源。

### 18.3 推荐优先PoC

- PULP `clk_rst_gen` vs 内部需求；
- PULP `sim_timeout`/`stream_watchdog` vs 统一诊断要求；
- OpenTitan DV utils/RAL思路 vs PeakRDL生成链；
- CORE-V-VERIF日志/结果组织 vs AIXSILICON座舱Schema；
- Accellera UVM 1.2/1800.2 API差异审计。

---

## 19. 与UVM Verification Skill Suite结合

### 19.1 Skill不再生成的内容

当DV Common达到Qualified后，Skill默认不重新生成：

- Base Test；
- 通用Clock/Reset；
- Timeout/Watchdog；
- Scoreboard队列和matcher；
- 通用CSR sequence；
- Memory backdoor抽象；
- 日志、manifest、test result schema；
- failure signature机制。

### 19.2 Skill仍需生成的内容

- IP testplan；
- IP Env装配；
- VIP instance/config；
- reference model adapter；
- IP业务scoreboard policy；
- coverage model；
- testcase/virtual sequence；
- RTM绑定；
- FuseSoC顶层Core和项目配置。

### 19.3 组件选择输入

Skill读取：

```yaml
dv_profile:
  uvm: uvm12_legacy
  simulator: vcs
  components:
    ral: aix:dv:common_ral:^1.0
    scoreboard: aix:dv:common_scoreboard:^1.1
    clk_rst: aix:dv:common_runtime:^1.0
  capabilities:
    out_of_order_match: true
    reset_during_traffic: true
    structured_result: true
```

生成前执行Catalog兼容性检查，禁止Skill猜测不存在的class或method。

---

## 20. 首批三个穿刺场景

### 20.1 场景A：APB寄存器IP

验证链：

```text
SystemRDL → PeakRDL RAL → APB VIP → CSR sequence
          → Scoreboard/Status → Result/Manifest
```

覆盖：

- Clock/Reset；
- RAL adapter和predictor；
- CSR smoke/reset/rw/bit-bash；
- timeout和非法配置negative test；
- requirement ID与结果绑定；
- FuseSoC Release。

### 20.2 场景B：X2X/AXI Bridge

覆盖：

- 多outstanding；
- 乱序匹配；
- 32～1024bit数据宽度；
- reset during traffic；
- backpressure；
- 多Clock/异步场景；
- latency和throughput metric；
- scoreboard drain与pending诊断。

### 20.3 场景C：PIC功能安全中断控制器

覆盖：

- pulse/level interrupt；
- interrupt record/clear；
- fault request/activation/observation；
- stuck/lost/duplicate注入；
- reset epoch；
- Safety mechanism响应时延；
- requirement、fault ID和test evidence绑定。

---

## 21. 实施路线图

### 阶段0：立项与边界冻结，2周

任务：

- 冻结与VIP、HW Interface、EDA Flow的边界；
- 盘点现有IP/VIP重复公共代码；
- 确定UVM/tool profile；
- 确定license与开源引入规则；
- 建立组件提案模板；
- 选择APB穿刺DUT。

出口：架构决策记录、组件清单、依赖规则、一期验收标准。

### 阶段1：仓库与L0/L1底座，4周

任务：

- 建仓、FuseSoC Core骨架；
- types/contracts；
- queue、ID、compare基础工具；
- Schema和metadata；
- PR CI和API diff；
- minimal UVM example。

出口：基础Core达到Candidate。

### 阶段2：运行时服务，4～6周

任务：

- log/status/failure；
- timeout/watchdog；
- reset service；
- config/manifest/result；
- clk/rst generator；
- negative tests。

出口：测试能够稳定开始、结束、失败聚类和输出证据。

### 阶段3：RAL与APB穿刺，6周

任务：

- RAL base与CSR sequence；
- PeakRDL生成模型适配；
- APB VIP集成；
- APB寄存器IP示例；
- frontdoor/backdoor；
- RTM和结果链路。

出口：第一个正式可演示闭环，P0运行时和RAL组件Qualified。

### 阶段4：Scoreboard与Memory，6～8周

任务：

- in-order/out-of-order matcher；
- compare policy；
- structured diff；
- memory model/backdoor；
- reset/flush/drain；
- AXI bridge穿刺；
- 性能基线。

出口：支撑复杂数据通路IP。

### 阶段5：SoC与功能安全能力，6～8周

任务：

- interrupt service；
- fault control；
- coverage control；
- shutdown manager；
- PIC场景；
- SoC环境组合验证。

出口：支撑Subsystem/SoC集成及功能安全验证。

### 阶段6：Catalog、Skill与规模化运营，持续

任务：

- Catalog qualification；
- Skill组件选择；
- AIXSILICON座舱展示；
- 多项目迁移；
- 性能优化；
- UVM 1800.2迁移；
- deprecation治理。

---

## 22. 人力与周期建议

### 22.1 推荐团队：4～5人，约7～9个月形成主干

| 角色 | 人数 | 责任 |
|---|---:|---|
| DV架构/Owner | 1 | 边界、API、版本、评审、下游协调 |
| UVM/RAL工程师 | 1 | Base、Sequence、RAL、CSR |
| Scoreboard/Model工程师 | 1 | matcher、compare、memory、性能 |
| Flow/工具工程师 | 1 | FuseSoC、CI、Schema、结果、Catalog |
| 项目验证工程师 | 0.5～1 | 穿刺、迁移、多项目反馈 |

### 22.2 精简团队：3人

6个月合理目标：

- types/utils；
- status/log/timeout/clk-rst；
- RAL/CSR；
- 基础in-order scoreboard；
- APB寄存器IP穿刺；
- FuseSoC、CI和result schema。

不要承诺同期完成完整乱序Scoreboard、SoC软件协同、性能框架和功能安全fault campaign。

---

## 23. 现有环境迁移策略

### 23.1 不做大爆炸迁移

采用四步：

1. **Inventory**：扫描重复base class、timeout、scoreboard、CSR sequence；
2. **Adapter**：为旧环境提供兼容adapter；
3. **Pilot**：选择一个简单IP和一个复杂IP迁移；
4. **Default**：新项目默认使用，旧项目按版本窗口迁移。

### 23.2 迁移优先级

优先迁移：

- 日志和result；
- timeout；
- clk/rst；
- CSR sequence；
- compare工具。

后迁移：

- Base Test继承体系；
- scoreboard；
- reset lifecycle；
- virtual sequence结构。

这些后者对现有环境侵入较大，需要项目级验证。

### 23.3 兼容层约束

- 兼容层单独Core；
- 明确结束日期；
- 不新增功能；
- 仅桥接旧API到新API；
- Catalog标记deprecated；
- 不允许新项目依赖。

---

## 24. 主要风险与控制

| 风险 | 表现 | 控制措施 |
|---|---|---|
| 过度抽象 | API复杂、项目不愿用 | 先三个穿刺，再冻结抽象 |
| 万能Base Env | 隐式依赖、组合困难 | 小组件、显式config、依赖Gate |
| 版本割裂 | UVM 1.2/1800.2分叉 | 公共子集+compat薄层+双CI |
| 仿真性能下降 | 日志/scoreboard开销大 | 性能基线和Release Gate |
| config_db滥用 | 行为无法追踪 | 强类型config、来源快照 |
| 开源代码污染 | license/来源不清 | 准入流程、NOTICE、SBOM |
| Flow边界混乱 | Repo内充满脚本和调度 | DV Common仅仿真内能力和薄adapter |
| 结果不稳定 | 无法聚类和追溯 | Message ID、signature和Schema |
| Skill生成漂移 | 生成不存在API | Catalog+版本锁+模板测试 |
| Owner缺失 | 组件无人维护 | 组件级CODEOWNER与SLA |

---

## 25. 一期验收标准

一期可验收必须同时满足：

1. P0 Core均有独立FuseSoC target；
2. 依赖DAG无环且不依赖VIP/IP/SoC项目；
3. 至少两个UVM profile完成声明范围内验证；
4. 至少两种组织可用仿真器完成Release测试；
5. APB寄存器IP穿刺全链路可重复运行；
6. CSR smoke/reset/rw/bit-bash可用；
7. Scoreboard支持顺序匹配、flush、drain和结构化diff；
8. Clock/Reset/Timeout/Watchdog有正常和negative测试；
9. 每次运行输出合法test result和run manifest；
10. 失败signature在不同seed下能稳定聚类；
11. Release包含SemVer、changelog、license、SBOM和qualification evidence；
12. UVM Verification Skill能够基于Catalog生成并运行示例工程；
13. 至少一个非示例真实IP采用；
14. 文档包含组件Catalog、API、迁移和最小示例；
15. 无P0已知阻断问题。

---

## 26. 首批TODO List

### P0：立即启动，0～2周

- [ ] 任命DV Common Owner和组件Owner；
- [ ] 冻结Repo边界和依赖方向；
- [ ] 盘点现有IP/VIP公共代码；
- [ ] 确定UVM 1.2/1800.2兼容策略；
- [ ] 确定主力仿真器CI矩阵；
- [ ] 确定APB寄存器IP穿刺对象；
- [ ] 建立仓库、CODEOWNERS、贡献规范；
- [ ] 定义组件提案和ADR模板；
- [ ] 定义VLNV命名；
- [ ] 定义result/manifest/failure Schema V0.1；

### P0：公共底座，2～8周

- [ ] 实现`common_types`和contract；
- [ ] 实现log/status/failure service；
- [ ] 实现timeout/watchdog；
- [ ] 实现clk/rst module和reset service；
- [ ] 实现config snapshot；
- [ ] 实现run manifest；
- [ ] 实现queue/ID/compare utils；
- [ ] 建立unit/negative/portability target；
- [ ] 建立API diff和dependency check；
- [ ] 完成minimal UVM example；

### P1：首个季度

- [ ] 实现RAL base与CSR sequence；
- [ ] 接入PeakRDL UVM RAL输出；
- [ ] 与APB VIP完成adapter/predictor连接；
- [ ] 实现in-order scoreboard；
- [ ] 实现structured diff；
- [ ] 实现memory mirror/backdoor contract；
- [ ] 完成APB寄存器IP穿刺；
- [ ] 发布首个Candidate；
- [ ] 接入统一Catalog；
- [ ] UVM Verification Skill改为消费公共组件；

### P1/P2：两个季度

- [ ] 实现out-of-order matcher；
- [ ] 实现reset epoch和跨reset policy；
- [ ] 实现latency/outstanding统计；
- [ ] 完成AXI/X2X穿刺；
- [ ] 实现interrupt/fault control；
- [ ] 完成PIC穿刺；
- [ ] 多仿真器完整Release矩阵；
- [ ] 性能benchmark和回退Gate；
- [ ] AIXSILICON项目座舱接入；
- [ ] 至少三个真实项目复用；

---

## 27. 最终推荐

DV Common应遵循以下最终原则：

1. **公共的是机制，不是项目策略**；
2. **组合优先于继承**；
3. **显式配置优先于全局搜索**；
4. **稳定Schema和证据与代码同等重要**；
5. **FuseSoC管理可复用源码依赖，EDA Flow管理运行与回归**；
6. **开源项目用于参考和审计，不整仓搬运**；
7. **先用APB、X2X、PIC三个场景证明抽象，再扩大组件范围**；
8. **新项目默认复用，旧项目渐进迁移**；
9. **公共库绝不能反向依赖VIP、具体IP和SoC项目**；
10. **最终目标不是代码最多，而是让每个验证环境更小、更一致、更可追溯。**

建议将整个资产体系归纳为：

> HW Interface定义“接口是什么”，VIP定义“协议怎样激励和检查”，DV Common定义“验证环境怎样运行、比较、结束和留证”，IP/SoC项目定义“具体功能要验证什么”，EDA Flow定义“怎样规模化执行”。

这五者边界固定后，IP设计和SoC集成验证才能真正形成可复用、可组合、可发布的工程体系。

---

## 28. 跨仓一致性修订（2026-08-13）

> 依据 [`plans/cross-repo-architecture-review.md`](../../plans/cross-repo-architecture-review.md)（ADR-0003/0005/0006）。

- 修正幽灵仓引用：`eda-flow`/`eda-rules`/`hw-models` 分别映射到 workflow（DAG/Gate）+ tool（Result adapter）、workflow `policies/`、techlib/model；本仓不建这三个仓；
- 与 VIP 划界（R6）：协议/事务相关公共 → VIP `common/`；协议无关机制（log/status/scoreboard/clk_rst/result/manifest）→ 本仓；
- Result/Manifest/Failure Schema 为跨仓公共契约，确定性实现归 `aixsilicon_tool_repo`（C4）；
- 依赖方向重申（C5）：本仓不得反向依赖 VIP 与具体 IP。

---

## 二、TODO.md 完整原文

# AIX DV Common — TODO List

> 依据 `plan.md` 第 26 节「首批 TODO List」并结合当前仓库实际进度整理。
> 状态：`[ ]` 待办 / `[-]` 进行中 / `[x]` 已完成
> 所有里程碑与验收标准见 `plan.md` 第 25 节。
> 最近更新：2026-08-13（P0 公共底座实现 + tools 工具层完成）

## 0. 已完成：仓库框架骨架（2026-08-12）

- [x] 建立仓库根文件（README/LICENSE/CHANGELOG/CONTRIBUTING/CODEOWNERS/.gitignore）
- [x] 建立 FuseSoC Core 骨架（types/utils/runtime/ral/scoreboard/mem/uvm/all，8 个 Core 解析通过）
- [x] L0 types 层（dv_common_types / dv_component_contract / dv_result_types）
- [x] L1 utils 层（queue / id / compare / data / stats）
- [x] L2 runtime 层（log / status / timeout / watchdog / reset / config / manifest）
- [x] L3 components 层（clk_rst / scoreboard / memory / coverage / interrupt / fault）
- [x] L4 uvm / ral 层（base_test / base_vseq / vseqr / env_contract / reset_seq / ral / csr_seq）
- [x] rtl/ 与 dpi/ 骨架（clk_gen / rst_gen / sim_timeout / signal_probe_if）
- [x] schemas/ 与 metadata/（6 个 Schema + 4 个元数据，YAML/JSON 校验通过）
- [x] unit/ examples/ tests/ docs/ tools/ release/ 目录骨架
- [x] VCS 编译/细化验证（非 UVM 层 + UVM 层均通过）

## 0.2 已完成：P0 公共底座实现（2026-08-13）

- [x] 非 UVM 单测 12/12 通过（VCS `-full64`）
- [x] minimal UVM example 全链路运行（`fusesoc run --target=smoke --tool=vcs aix:dv:common_all` PASS）
- [x] RTL 模块验证（新增 `tests/smoke/dv_rtl_smoke_tb.sv`，`rtl_smoke` target PASS）
- [x] 修复 `dv_config_pkg` 布尔 plusarg、`dv_compare_pkg` wildcard/结构化 diff
- [x] 修复 `metadata/message_ids.yaml` Message ID 格式
- [x] 实现 tools 工具层（schema_check / dep_check / api_diff / result_check / doc_gen + run_checks.sh）
- [x] `tools/run_checks.sh` 本地检查入口 ALL CHECKS PASSED
- [x] `docs/api/` 34 份 API 文档已生成

## P0：立即启动，0～2 周

- [ ] 任命 DV Common Owner 和组件 Owner（CODEOWNERS 占位映射待实际负责人）
- [ ] 冻结 Repo 边界和依赖方向（对应 `docs/dependency_rules.md`）
- [ ] 盘点现有 IP/VIP 公共代码，形成 Inventory
- [ ] 确定 UVM 1.2/1800.2 兼容策略并建立 `compat/` 薄层
- [ ] 确定主力仿真器 CI 矩阵（vcs/xcelium/questa，参考 `metadata/compatibility.yaml`）
- [ ] 确定 APB 寄存器 IP 穿刺对象
- [ ] 定义组件提案与 ADR 模板
- [ ] 定义 result/manifest/failure Schema V0.1（当前骨架已建，需评审冻结）
- [ ] 建立 PR 流水线骨架（schema 校验 → 依赖检查 → lint → 编译 → 单测 → API diff）

## P0：公共底座实现，2～8 周

- [x] 实现 `dv_common_types` 与 contract 的正式行为
- [x] 实现 log/status/failure service（Message ID 治理 + signature 聚合）
- [x] 实现 timeout/watchdog（含诊断 hook 接口）
- [x] 实现 clk/rst module 与 reset service（`rtl/dv_clk_gen.sv`、`rtl/dv_rst_gen.sv` 行为经 rtl_smoke 验证）
- [x] 实现 config snapshot 与来源追踪（优先级覆盖规则）
- [x] 实现 run manifest 正式输出（YAML，smoke 中已验证）
- [x] 实现 queue/ID/compare utils 的完整行为与边界（单测修正并通过）
- [x] 建立 unit/smoke target 并通过 FuseSoC+VCS 运行（12/12 单测 + smoke + rtl_smoke）
- [x] 建立 API diff 与 dependency check（`tools/api_diff`、`tools/dep_check` 已实现）
- [x] 完成 minimal UVM example 全链路运行（`fusesoc run --target=smoke --tool=vcs aix:dv:common_all` PASS）
- [x] 补齐 `tools/schema_check`、`tools/result_check` 实现
- [x] 实现 `tools/doc_gen` API 文档生成器（已生成 docs/api/ 34 份）
- [x] 建立本地检查入口 `tools/run_checks.sh`（schema_check + dep_check + api_diff）

## P1：首个季度

- [ ] 实现 RAL base 与 CSR sequence 正式行为（smoke/reset/rw/bit-bash）
- [ ] 接入 PeakRDL UVM RAL 输出链
- [ ] 与 APB VIP 完成 adapter/predictor 连接（RAL adapter 契约）
- [ ] 实现 in-order scoreboard 业务装配（matcher/flush/drain/pending 基础已实现并单测通过）
- [x] 实现结构化 diff 输出（`dv_compare_pkg::dv_diff_fields` 字段级差异）
- [x] 实现 memory mirror/backdoor contract 基础（`dv_memory_model` / `dv_mem_backdoor` 单测通过）
- [ ] 完成 APB 寄存器 IP 穿刺（`examples/apb_csr_ip`）
- [ ] 发布首个 Candidate 版本
- [ ] 接入统一 Catalog（`metadata/components.yaml` 成熟度更新为 qualified 路径）
- [ ] UVM Verification Skill 改为消费公共组件

## P1/P2：两个季度

- [ ] 实现 out-of-order matcher 与乱序匹配
- [ ] 实现 reset epoch 与跨 reset 策略（flush/error/preserve）
- [ ] 实现 latency/outstanding 统计（`dv_latency_tracker`）
- [ ] 完成 AXI/X2X 穿刺（`examples/axi_bridge`）
- [ ] 实现 interrupt/fault control 正式行为
- [ ] 完成 PIC 功能安全穿刺（`examples/pic_interrupt`）
- [ ] 多仿真器完整 Release 矩阵
- [ ] 性能 benchmark 与回退 Gate（编译时间/内存/百万 transaction 开销）
- [ ] AIXSILICON 项目座舱接入（result/manifest/failure schema 消费）
- [ ] 至少三个真实项目复用

## 工程化完善（随阶段穿插）

- [ ] `compat/` UVM 双 profile（uvm12_legacy / uvm1800_2）薄层
- [x] FuseSoC 后端仿真运行验证（smoke / rtl_smoke 经 VCS 后端 PASS，`-full64` + 统一 `-timescale`）
- [x] `docs/api/` 由 `tools/doc_gen` 生成（34 份）
- [ ] `docs/migration/` 补齐旧环境迁移指南
- [ ] CI 接入（PR/Nightly/Release 三段，见 `plan.md` 第 16 节；可将 `tools/run_checks.sh` 挂入 PR）
- [ ] SBOM 与 license 治理流程落地
- [ ] 一期验收标准核对（`plan.md` 第 25 节 15 项）

## 跨仓一致性修订（2026-08-13）

- [ ] 修订 plan.md 幽灵仓引用（eda-flow/eda-rules/hw-models → workflow/tool/techlib，ADR-0005）
- [ ] 与 VIP `common/` 划界：协议无关机制全部收敛到本仓（R6）
- [ ] Result/Manifest/Failure Schema 与 tool_repo 对齐为单一公共契约（C4）
