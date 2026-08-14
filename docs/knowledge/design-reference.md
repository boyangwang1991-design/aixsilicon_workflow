# knowledge — 完整设计参考

> 完整保留历史长篇设计要求；旧状态、日期和优先级不再作为执行依据。当前设计见 [`README.md`](README.md)，活动交付见 [`delivery.md`](delivery.md)。

> 来源：repos/aixsilicon_chipknowledge/TODO.md + ROADMAP.md + plans/reference-material-spec.md（完整剪切至 docs/architecture/repo-plans 统一管理）
> 迁移日期：2026-08-13
> 仓库实现现状见 docs/architecture/repos.md §1.10

---

## 一、TODO.md 完整原文

# 芯片设计验证知识手册 TODO

本清单是章节建设的唯一执行看板。任务按“调研 → Draft → Technical Review → Engineering Verified → Released”推进；未获得 Owner、Reviewer 或工程证据时，不把状态虚标为完成。

## 完成定义

单个章节只有同时满足以下条件，才能将“内容完成”标记为完成：

- 使用统一元数据，明确范围、前置知识、Assumption、Owner、版本和安全域。
- 回答原理、设计方法、验证方法、PPA/安全影响、常见 Bug 和工程资产。
- 关键外部结论引用官方标准、规范、论文或工具官方资料，并记录适用版本。
- Checklist 可判定；示例明确标注教学简化、工程参考或组织基线。
- 本地链接、JSON/JSONL 和元数据检查通过。
- 章节内部不存在未解释的关键 `TBD`；组织专有阈值可以保留 TBD，但必须说明由谁、在什么 Gate 决定。

“内容完成”不等于 Released。Technical Review、Engineering Verified 和 Released 仍需相应责任人及证据。

## 优先级和顺序

1. 基础导航：卷 01、02。
2. 首条 MAC 案例知识链：卷 03、06、07、08、09、10、11、12、18。
3. 系统与领域扩展：卷 04、05、13、14、15、16、17。
4. 其余贯穿案例：ECC SRAM、AXI-Lite Crossbar、图像 Pipeline、DMA + 中断。

## 卷 01：芯片研发全景

- [x] V01-00 建立卷目录、阅读路径和章节关系。
- [x] V01-01 芯片类型、抽象层级与研发边界。
- [x] V01-02 芯片研发全生命周期。
- [x] V01-03 组织角色、责任边界与协作接口。
- [x] V01-04 设计验证全景与六个研发闭环。
- [x] V01-05 EDA 工具链、计算环境与结果证据。
- [x] V01-06 配置、版本、数据与许可证基础。
- [x] V01-07 新人学习路径与工程任务地图。
- [x] V01-08 来源、术语、交叉链接和结构检查。
- [ ] V01-09 领域 Owner 技术评审。
- [ ] V01-10 试点项目工程验证与发布。

## 卷 02：研发流程与项目交付

- [x] V02-01 公司级 IPD 与技术评审分层（内容 Draft；待 Owner 技术评审）。
- [x] V02-02 芯片产品主流程（内容 Draft；待 Owner 技术评审）。
- [x] V02-03 SoC/Subsystem/IP 研发流程（内容 Draft；待 Owner 技术评审）。
- [x] V02-04 模块开发与 PPA 收敛流程（内容 Draft；待 Owner 技术评审）。
- [x] V02-05 Verification 与 Closure 流程（内容 Draft；待 Owner 技术评审）。
- [x] V02-06 Tape-out、Bring-up 与量产反馈接口（内容 Draft；待 Owner 技术评审）。
- [x] V02-07 Stage Gate、RACI 与准出机制（内容 Draft；待 Owner 技术评审）。
- [x] V02-08 配置、基线、变更和 ECO（内容 Draft；待 Owner 技术评审）。
- [x] V02-09 流程裁剪、异常与升级路径（内容 Draft；待 Owner 技术评审）。
- [x] V02-10 交付物矩阵和项目证据包（内容 Draft；待 Owner 技术评审）。

## 卷 03：数字设计基础

- [x] V03-01 组合逻辑、时序逻辑与同步设计（内容 Draft；待 Owner 技术评审）。
- [x] V03-02 Clock、Reset 与复位释放（内容 Draft；待 Owner 技术评审）。
- [x] V03-03 FSM 设计、编码与验证（内容 Draft；待 Owner 技术评审）。
- [x] V03-04 ready/valid、握手与背压（内容 Draft；待 Owner 技术评审）。
- [x] V03-05 Pipeline、延迟、吞吐与停顿（内容 Draft；待 Owner 技术评审）。
- [x] V03-06 数制、定点数、舍入、截断和饱和（内容 Draft；待 Owner 技术评审）。
- [x] V03-07 参数化与非法配置防护（内容 Draft；待 Owner 技术评审）。
- [x] V03-08 FIFO、仲裁器、计数器和常用结构（内容 Draft；待 Owner 技术评审）。

## 卷 04：SoC 架构与系统基础

- [x] V04-01 处理器、加速器与软硬件划分（内容 Draft；待 System/Software Owner 技术评审）。
- [x] V04-02 存储层次与一致性基础（内容 Draft；待架构一致性与平台验证）。
- [x] V04-03 互联、地址、QoS 与系统流控（内容 Draft；待 AMBA Checker/性能模型与 Owner 评审）。
- [x] V04-04 中断、寄存器和软件可见资源（内容 Draft；待 GIC/寄存器生成链与 Firmware 验证）。
- [x] V04-05 CRG、电源域与系统状态（内容 Draft；待 LPI/Power-aware/CDC-RDC 与 Owner 评审）。
- [x] V04-06 Boot、Debug 与可观测性（内容 Draft；待目标平台 Boot/CoreSight 与安全评审）。
- [x] V04-07 性能模型、Workload 与预算分解（内容 Draft；待真实 Workload、PMU 和平台校准）。
- [x] V04-08 FPGA、Emulation 与 Firmware-driven Verification（内容 Draft；待原型平台工程验证）。
- [x] V04-09 SoC 知识证据图谱与资料使用方法（内容 Draft；待 Owner 技术评审与图谱 Schema 落地）。
- [x] V04-10 跨 ISA 特权架构与平台契约（内容 Draft；待冻结项目 ISA/Profile 并运行合规测试）。
- [x] V04-11 一致性互联与 NoC 工程方法（内容 Draft；待目标协议 Checker、死锁与流量模型验证）。
- [x] V04-12 内存控制器、DRAM 与 RAS 系统方法（内容 Draft；待 Controller/PHY/器件配置及硅后相关性验证）。
- [x] V04-13 高速 I/O 与 Chiplet 系统契约（内容 Draft；待授权规范、合规和互操作验证）。
- [x] V04-14 Timer、DMA 与 IOMMU 端到端设计（内容 Draft；待真实 OS/设备和安全 Fault Campaign 验证）。
- [x] V04-15 Firmware、OS 与硬件平台契约（内容 Draft；待平台固件/OS 兼容矩阵验证）。
- [x] V04-16 开源 SoC、模型与原型案例研读法（内容 Draft；待固定案例版本并形成复现报告）。

## 卷 05：核心领域与典型 IP

- [ ] V05-01 计算类 IP。
- [ ] V05-02 存储类 IP。
- [ ] V05-03 互联类 IP。
- [ ] V05-04 媒体类 IP。
- [ ] V05-05 控制类 IP。
- [ ] V05-06 外设、CRG、电源、安全和 DFX 扩展。
- [ ] V05-07 领域差异对照与案例导航。

## 卷 06：需求与架构设计

- [x] V06-01 场景、Use Case 与需求获取（内容 Draft；待 Owner 技术评审）。
- [x] V06-02 需求质量、唯一 ID 和分解（内容 Draft；待 Owner 技术评审）。
- [x] V06-03 Assumption、约束、风险和变更（内容 Draft；待 Owner 技术评审）。
- [x] V06-04 RTM 与端到端追踪（内容 Draft；待 Owner 技术评审）。
- [x] V06-05 HLD、LLD 和架构决策记录（内容 Draft；待 Owner 技术评审）。
- [x] V06-06 接口、寄存器和时序契约（内容 Draft；待 Owner 技术评审）。
- [x] V06-07 性能/PPA 预算和可达成性（内容 Draft；待 Owner 技术评审）。
- [x] V06-08 可验证性、可测性、安全和异常设计（内容 Draft；待 Owner 技术评审）。

## 卷 07：RTL 设计方法

- [x] V07-01 可综合 RTL 与编码语义（内容 Draft；待 Owner 技术评审）。
- [x] V07-02 组合/时序代码模板和赋值规则（内容 Draft；待 Owner 技术评审）。
- [x] V07-03 数据通路与控制通路（内容 Draft；待 Owner 技术评审）。
- [x] V07-04 Pipeline、Buffer、仲裁和资源共享（内容 Draft；待 Owner 技术评审）。
- [x] V07-05 参数化、生成结构和配置保护（内容 Draft；待 Owner 技术评审）。
- [x] V07-06 Clock/Reset、CDC 友好结构（内容 Draft；待 Owner 技术评审）。
- [x] V07-07 低功耗、DFT、安全与可验证性（内容 Draft；待 Owner 技术评审）。
- [x] V07-08 Code Review、重构和 ECO（内容 Draft；待 Owner 技术评审）。

## 卷 08：SystemVerilog 基础

- [x] V08-01 类型、作用域和四态语义（内容 Draft；待工具验证与 Owner 评审）。
- [x] V08-02 数组、结构、联合和 Package（内容 Draft；待工具验证与 Owner 评审）。
- [x] V08-03 Interface、Modport 和 Clocking Block（内容 Draft；待工具验证与 Owner 评审）。
- [x] V08-04 类、继承、多态和 Factory 基础（内容 Draft；待工具验证与 Owner 评审）。
- [x] V08-05 随机化与约束（内容 Draft；待工具验证与 Owner 评审）。
- [x] V08-06 进程、事件、Mailbox 和 Semaphore（内容 Draft；待工具验证与 Owner 评审）。
- [x] V08-07 SVA 序列、属性和采样语义（内容 Draft；待工具验证与 Owner 评审）。

## 卷 09：功能验证方法

- [x] V09-01 风险驱动验证策略（内容 Draft；待 Owner 技术评审）。
- [x] V09-02 Verification Plan、Feature、TP 和 TC（内容 Draft；待 Owner 技术评审）。
- [x] V09-03 参考模型、Scoreboard 和端到端检查（内容 Draft；待 Owner 技术评审）。
- [x] V09-04 激励、约束和 Corner Case（内容 Draft；待 Owner 技术评审）。
- [x] V09-05 Assertion 与协议检查（内容 Draft；待 Owner 技术评审）。
- [x] V09-06 功能覆盖、代码覆盖和 Closure（内容 Draft；待 Owner 技术评审）。
- [x] V09-07 回归、缺陷、Debug 和复现（内容 Draft；待 Owner 技术评审）。
- [x] V09-08 验证签核证据（内容 Draft；待 Owner 技术评审）。

## 卷 10：UVM 工程化

- [x] V10-01 Transaction、Sequence 和 Sequencer（内容 Draft；待工具验证与 Owner 评审）。
- [x] V10-02 Driver、Monitor 和 Agent（内容 Draft；待工具验证与 Owner 评审）。
- [x] V10-03 Env、TLM、Scoreboard 和 Predictor（内容 Draft；待工具验证与 Owner 评审）。
- [x] V10-04 Factory、Config DB、Phase 和 Objection（内容 Draft；待工具验证与 Owner 评审）。
- [x] V10-05 RAL 与寄存器验证（内容 Draft；待工具验证与 Owner 评审）。
- [x] V10-06 Virtual Sequence 与跨接口场景（内容 Draft；待工具验证与 Owner 评审）。
- [x] V10-07 IP 到 Subsystem 复用（内容 Draft；待工具验证与 Owner 评审）。
- [x] V10-08 性能、日志、Debug 和组件单测（内容 Draft；待工具验证与 Owner 评审）。

## 卷 11：形式与静态验证

- [x] V11-01 Lint 方法与 Closure（内容 Draft；待工具验证与 Owner 评审）。
- [x] V11-02 CDC 与约束质量（内容 Draft；待工具验证与 Owner 评审）。
- [x] V11-03 RDC 与复位域风险（内容 Draft；待工具验证与 Owner 评审）。
- [x] V11-04 Formal Property Verification（内容 Draft；待工具验证与 Owner 评审）。
- [x] V11-05 Connectivity 与结构检查（内容 Draft；待工具验证与 Owner 评审）。
- [x] V11-06 X-Propagation（内容 Draft；待工具验证与 Owner 评审）。
- [x] V11-07 LEC 与 ECO 等价性（内容 Draft；待工具验证与 Owner 评审）。
- [x] V11-08 告警分类、Waiver 和证据治理（内容 Draft；待工具验证与 Owner 评审）。

## 卷 12：综合、STA 与 PPA

- [x] V12-01 PPA 可达成分析（内容 Draft；待工具验证与 Owner 评审）。
- [x] V12-02 综合输入、约束和结果解释（内容 Draft；待工具验证与 Owner 评审）。
- [x] V12-03 STA 基础、多模式多角和异常路径（内容 Draft；待工具验证与 Owner 评审）。
- [x] V12-04 面积分析和资源根因（内容 Draft；待工具验证与 Owner 评审）。
- [x] V12-05 活动率、功耗场景和功耗分析（内容 Draft；待工具验证与 Owner 评审）。
- [x] V12-06 关键路径和物理感知优化（内容 Draft；待工具验证与 Owner 评审）。
- [x] V12-07 时序/面积/功耗联合收敛（内容 Draft；待工具验证与 Owner 评审）。
- [x] V12-08 基线比较、偏差审批和报告 Schema（内容 Draft；待工具验证与 Owner 评审）。

## 卷 13：低功耗设计

- [x] V13-01 功耗组成与早期估算（内容 Draft；待工具验证与 Owner 评审）。
- [x] V13-02 电源域与电源状态表（内容 Draft；待 Owner 技术评审）。
- [x] V13-03 UPF 基础与版本边界（内容 Draft；待冻结 IEEE 1801/工具版本）。
- [x] V13-04 Isolation、Retention 和 Level Shifter（内容 Draft；待工具验证与 Owner 评审）。
- [x] V13-05 Clock Gating、Power Gating 和 DVFS（内容 Draft；待工具验证与 Owner 评审）。
- [x] V13-06 功耗感知验证与低功耗 CDC/RDC（内容 Draft；待工具验证与 Owner 评审）。
- [x] V13-07 活动率、功耗场景和签核（内容 Draft；待工具验证与 Owner 评审）。

## 卷 14：DFT、后端与签核

- [x] V14-01 Scan、ATPG 与前端接口（内容 Draft；待 DFT 工具验证与 Owner 评审）。
- [x] V14-02 MBIST、LBIST 和存储测试（内容 Draft；待 DFT 工具验证与 Owner 评审）。
- [x] V14-03 Floorplan、布局布线和时钟树接口知识（内容 Draft；待物理实现验证与 Owner 评审）。
- [x] V14-04 前后端协同与物理反馈（内容 Draft；待项目流程验证与 Owner 评审）。
- [x] V14-05 门级仿真和时序回标（内容 Draft；待仿真工具验证与 Owner 评审）。
- [x] V14-06 Sign-off、ECO 与 Tape-out Readiness（内容 Draft；待企业流程与 Owner 评审）。

## 卷 15：安全、功能安全与可靠性

- [x] V15-01 Threat Model 与安全需求（内容 Draft；待安全 Owner 在红区评审）。
- [x] V15-02 Secure Boot、密钥和访问控制（内容 Draft；待安全 Owner 在红区评审）。
- [x] V15-03 ECC、Parity、Lockstep 和错误处理（内容 Draft；待 Safety Owner 与工具验证）。
- [x] V15-04 Safety Lifecycle、Safety Goal 和追踪（内容 Draft；待冻结适用标准与 Owner 评审）。
- [x] V15-05 FMEDA、DFMEA 和诊断覆盖（内容 Draft；待项目数据与工具验证）。
- [x] V15-06 Fault Injection（内容 Draft；待 campaign 工具验证与 Safety Owner 评审）。
- [x] V15-07 可靠性、恢复和证据（内容 Draft；待工艺/可靠性数据与 Owner 评审）。
- [x] V15-08 红区知识与 AI 安全边界（内容 Draft；待企业安全策略与数据 Owner 评审）。

## 卷 16：工程工具与自动化

- [x] V16-01 寄存器/中断/CRG/SOCGEN（内容 Draft；待生成器样例验证与 Owner 评审）。
- [x] V16-02 可复现环境、依赖和制品（内容 Draft；待 CI 环境验证与 Owner 评审）。
- [x] V16-03 CI 与分层回归（内容 Draft；待流水线验证与 Owner 评审）。
- [x] V16-04 日志、波形和失败聚类（内容 Draft；待真实回归数据验证）。
- [x] V16-05 结果 Schema、报告解析和 Dashboard（内容 Draft；待解析器与 Dashboard 验证）。
- [x] V16-06 工具适配器和开源替代路径（内容 Draft；待适配器合约测试）。
- [x] V16-07 自动化质量、权限和审计（内容 Draft；待企业 CI/安全流程评审）。

## 卷 17：AI 辅助芯片研发

- [ ] V17-01 可信知识 RAG。
- [ ] V17-02 知识生产与文档 Agent。
- [ ] V17-03 RTL、SVA、UVM 和 Formal Skill。
- [ ] V17-04 静态检查与 PPA 分析助手。
- [ ] V17-05 RTM、评审与 Sign-off 核对。
- [ ] V17-06 工具调用和闭环执行。
- [ ] V17-07 输入输出契约、人审和权限。
- [ ] V17-08 评测、Prompt 注入、安全和审计。

## 卷 18：工程实践与典型案例

- [ ] V18-01 参数化流水线 MAC 完整案例。
  - [x] 建立贯穿知识页，覆盖需求、数值、接口、Pipeline、验证、PPA、RTM、Gate、Bug 与 AI 边界。
  - [ ] 指定 Owner/Reviewer，批准 `ADR-MAC-001` 至 `ADR-MAC-005` 并冻结 P0 需求。
  - [ ] 补齐 LLD、RTL/SVA、独立参考模型、验证、约束、报告和 Release 资产，以统一命令形成可复现证据。
- [ ] V18-02 多 Bank ECC SRAM 控制器完整案例。
- [ ] V18-03 AXI-Lite Crossbar 完整案例。
- [ ] V18-04 流式图像 Pipeline 完整案例。
- [ ] V18-05 DMA + 中断控制器快速案例。
- [ ] V18-06 常见 Bug 模式库。
- [ ] V18-07 项目复盘、ECO 和回片问题模板。
- [ ] V18-08 Sign-off 包与可复现证据样例。

## 横向资产

- [ ] X-01 统一术语表。
- [ ] X-02 来源登记与许可证清单。
- [ ] X-03 流程—章节—模板—案例交叉索引。
- [ ] X-04 首批 100–200 道知识评测题。
- [ ] X-05 首批 20–30 个确定性代码/验证任务。
- [ ] X-06 过期、断链、重复、冲突和敏感信息检查。
- [ ] X-07 Owner、Reviewer、季度巡检和版本发布机制。

---

## 二、ROADMAP.md 完整原文

# 建设路线图与执行看板

## 阶段 0：基线设计（已形成 Draft 基线）

| ID | 任务 | 输出 | 状态 | 验收口径 |
|---|---|---|---|---|
| B0-01 | 冻结一级信息架构 | 18 卷、流程、评审门、模板、案例、评测目录 | 已完成（草案） | 目录与规划说明书一致 |
| B0-02 | 建立统一元数据 | 页面 Front Matter 规范与示例 | 已完成（草案） | Owner、状态、版本、适用范围、来源可表达 |
| B0-03 | 建立对象关系模型 | ID 规则、对象类型、核心关系、JSON Schema | 已完成（草案） | 可表达需求到签核证据链 |
| B0-04 | 建立页面与流程模板 | 知识页、流程页、Gate、LLD、VP、Release | 已完成（草案） | 模板含填写说明、示例、审核要点 |
| B0-05 | 选定首条案例链 | 参数化流水线 MAC 案例章程与结构 | 已完成（草案） | 交付链覆盖需求到 Sign-off |
| B0-06 | 指定 Owner/Reviewer | RACI 与领域人员名单 | 待组织决策 | 每个 P0 资产有 Owner 和 Reviewer |
| B0-07 | 冻结工具基线 | 仿真、Lint、综合及开源替代路径 | 待环境盘点 | 版本、许可证、运行入口和结果格式明确 |
| B0-08 | 技术评审基线 | 评审记录与问题闭环 | 待评审 | P0 模板和模型无阻塞问题 |
| B0-09 | 五层架构迁移 | knowledge、app、template/script/schema、skill、project-data 边界 | 已完成（结构迁移） | 单一知识源、旧路径清理、全仓校验通过 |

## 阶段 1：MVP（建议第 2–3 月）

| 工作流 | 主要交付 | 完成定义 |
|---|---|---|
| 流程主线 | 模块研发闭环、需求/LLD/RTL/DV/静态/PPA Gate | 输入、输出、RACI、准出和裁剪规则齐全 |
| 核心知识 | 数字基础、需求架构、RTL、功能验证、静态、PPA 的 P0 页面 | Technical Review 覆盖 100%，关键页完成工程验证 |
| MAC 案例 | 需求、LLD、RTL、SVA、参考模型、验证、约束、报告、Release | 统一命令可复现，证据绑定版本与配置 |
| 检索与评测 | 结构化索引样本、首批知识问答和代码任务 | 引用可定位；错误版本与无证据问题能拒答 |

当前已进入阶段 1 内容与能力建设；所有资产仍保持 Draft，Technical Review 和 Engineering Verified 门槛未降低。

## 决策与风险日志

| 日期 | 类型 | 内容 | Owner | 状态 |
|---|---|---|---|---|
| 2026-07-24 | 决策 | 首条贯穿案例采用参数化流水线 MAC | TBD | 待批准 |
| 2026-07-24 | 假设 | 首版同时保留商业 EDA 适配接口与开源可运行路径 | TBD | 待工具盘点 |
| 2026-07-24 | 风险 | 尚未指定领域 Owner，所有内容仅可视为 Draft | 指导委员会 | 开放 |
| 2026-07-24 | 风险 | 企业规范、工艺/PVT、签核阈值未知，不得填入推测值 | 各领域 Owner | 开放 |

## 下一批可执行任务

1. 由总编/架构组确认元数据字段、对象 ID 规则和状态机。
2. 指定卷 03、06、07、09、11、12 与 MAC 案例的 Owner/Reviewer。
3. 盘点现有 LRS/HLD/LLD、RTL、UVM、静态检查、PPA 报告及许可边界。
4. 冻结 MAC 的功能参数、定点规则、接口、时钟复位、吞吐/延迟与 PPA 目标。
5. 依据已批准需求生成 RTM；之后才进入 RTL 与验证实现。
6. 接入 VitePress 门户适配器，直接读取 `knowledge/`，不复制正文。
7. 为 `templates/`、`scripts/` 和 `examples/` 建立自动测试与发布契约。

---

## 三、plans/reference-material-spec.md 完整原文

# 参考资料保存规范设计方案

## 1. 目录结构规范

### 1.1 整体结构

```
reference/
├── README.md                          # 参考资料总索引
├── knowledge-handbook/                # 知识手册参考资料（已有）
│   ├── README.md                      # 主索引文档
│   ├── 01-standards/                  # 按领域分类
│   │   ├── README.md                  # 领域索引
│   │   └── REF-STD-001/              # 单个资料目录
│   │       ├── README.md              # 资料说明（VitePress 可渲染）
│   │       ├── metadata.yaml          # 元数据
│   │       ├── images/                # 图片资源
│   │       │   ├── figure-01.png
│   │       │   └── figure-02.svg
│   │       └── origin/                # 原始格式文件
│   │           ├── ieee-1800-2023.pdf
│   │           └── notes.docx
│   ├── 02-architecture/
│   └── ...
└── offline/                           # 离线资料存放位置
```

### 1.2 单个资料目录结构

每个参考资料独立存放在一个以内部 ID 命名的目录中：

```
REF-{TYPE}-{NNN}/
├── README.md              # 主文档（VitePress 渲染）
├── metadata.yaml          # 结构化元数据
├── images/                # 图片资源目录
│   ├── *.png
│   ├── *.jpg
│   ├── *.svg
│   └── *.gif
└── origin/                # 原始格式文件
    ├── *.pdf              # PDF 原文
    ├── *.docx             # Word 原文
    ├── *.html             # HTML 原文
    └── *.md               # Markdown 原文
```

## 2. 元数据规范

### 2.1 metadata.yaml 格式

```yaml
# 基本信息
id: REF-STD-001                    # 内部知识实体 ID
title: IEEE Std 1800-2023 SystemVerilog LRM
type: standard                     # standard | textbook | tool | paper | spec | guide
status: offline                    # online | offline | pending

# 来源信息
source:
  author: IEEE
  publisher: IEEE
  version: "1800-2023"
  publish_date: 2023
  isbn: "978-1-5044-9221-7"        # 可选
  url: https://standards.ieee.org/ieee/1800/7743/

# 分类信息
category:
  domain: 标准与方法学
  topic: HDL
  tags: [systemverilog, hdl, lrm, assertion, coverage]

# 关联信息
relations:
  knowledge_pages: [KNOW-RTL-0001, KNOW-DV-0002]
  volumes: ["07", "08", "09"]
  prerequisites: []
  related_refs: [REF-STD-002, REF-STD-006]

# 文件信息
files:
  markdown: README.md
  images:
    - images/figure-01.png
    - images/figure-02.svg
  origin:
    - path: origin/ieee-1800-2023.pdf
      format: pdf
      size: 15.2MB
      hash: sha256:abc123...
    - path: origin/notes.docx
      format: docx
      size: 2.1MB

# 治理信息
governance:
  source_role: 权威事实源
  coverage_boundary: 定义适用范围内的接口或行为
  version_baseline: "1800-2023"
  maintenance_status: 有效；季度检查
  verified_date: 2026-07-27
  verified_by: TBD

# 推荐信息
recommendation:
  level: S                           # S | A | B | C
  target_audience: [RTL, DV, 工具开发]
  applicable_stages: [规格, RTL, DV, 签核]
  suggested_form: Standard/Glossary/Rule Set
```

### 2.2 README.md 格式

```markdown
---
id: REF-STD-001
title: IEEE Std 1800-2023 SystemVerilog LRM
category: 标准与方法学
tags: [systemverilog, hdl, lrm]
status: offline
---

# IEEE Std 1800-2023 SystemVerilog LRM

> **推荐级别**: S | **语言**: 英文 | **类型**: 标准

## 基本信息

| 属性 | 值 |
|------|-----|
| 发布机构 | IEEE |
| 版本 | 1800-2023 |
| 内部 ID | REF-STD-001 |

## 核心概述

SystemVerilog 语言、RTL、断言、覆盖率、OOP 与 DPI 的权威语义定义。

## 为什么值得收录

所有 SystemVerilog 语法与语义争议的最终事实源。

## 适用信息

- **适用阶段**: 规格/RTL/DV/签核
- **推荐对象**: RTL、DV、工具开发
- **建议沉淀形态**: Standard/Glossary/Rule Set

## 获取方式

- **获取方式**: IEEE GET 可免费获取
- **官方入口**: [IEEE Standards](https://standards.ieee.org/ieee/1800/7743/)

## 本地文件

| 文件 | 格式 | 大小 | 说明 |
|------|------|------|------|
| `origin/ieee-1800-2023.pdf` | PDF | 15.2MB | 历史规划记录的本地路径；当前仓库未包含该文件 |

## 相关图片

历史图片路径：`images/figure-01.png`（当前仓库未包含该文件）。

## 关联知识

- `KNOW-RTL-0001: 同步 FIFO 设计`（历史规划路径，当前内容树未落地）
- [第 07 卷: RTL 设计方法](../../repos/aixsilicon_chipknowledge/knowledge/volumes/07-rtl-design/)

---

*最后更新: 2026-07-27*
```

## 3. VitePress 配置

### 3.1 修改 config.mts

需要修改 `apps/handbook/.vitepress/config.mts` 以支持参考资料展示：

```typescript
// 新增参考资料相关配置
const referenceRoot = resolve(repoRoot, 'reference')

// 添加参考资料侧边栏
function referenceSidebar(): DefaultTheme.SidebarItem[] {
  const root = resolve(referenceRoot, 'knowledge-handbook')
  const categories = readdirSync(root, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && entry.name.match(/^\d{2}-/))
    .sort((left, right) => left.name.localeCompare(right.name, 'zh-CN', { numeric: true }))

  return [
    { text: '参考资料总览', link: '/reference/' },
    ...categories.map((category) => {
      const categoryDir = resolve(root, category.name)
      const refs = readdirSync(categoryDir, { withFileTypes: true })
        .filter((entry) => entry.isDirectory() && entry.name.startsWith('REF-'))
        .sort()

      return {
        text: pageTitle(resolve(categoryDir, 'README.md')),
        link: `/reference/knowledge-handbook/${category.name}/`,
        collapsed: true,
        items: refs.map((ref) => ({
          text: pageTitle(resolve(categoryDir, ref.name, 'README.md')),
          link: `/reference/knowledge-handbook/${category.name}/${ref.name}/`
        }))
      }
    })
  ]
}

// 在 themeConfig.sidebar 中添加
sidebar: {
  '/volumes/': volumeSidebar(),
  '/reference/': referenceSidebar(),
  // ... 其他侧边栏
}

// 添加 rewrites 支持参考资料路径
const referenceRewrites = Object.fromEntries(
  markdownFiles(referenceRoot)
    .filter((path) => path.endsWith('README.md'))
    .map((path) => {
      const source = relative(referenceRoot, path).replaceAll('\\', '/')
      const destination = source === 'README.md' ? 'index.md' : source.replace(/README\.md$/, 'index.md')
      return [`reference/${source}`, destination]
    })
)
```

### 3.2 添加参考资料导航

在导航栏添加参考资料入口：

```typescript
nav: [
  { text: '知识', link: '/knowledge/' },
  { text: '参考资料', link: '/reference/' },
  { text: '模板', link: '/templates/' },
  // ...
]
```

## 4. 参考资料解析 Skill 设计

### 4.1 Skill 目录结构

```
skills/reference-parser/
├── SKILL.md                    # Skill 定义文件
├── scripts/
│   ├── parse_pdf.py            # PDF 解析脚本
│   ├── parse_docx.py           # Word 解析脚本
│   ├── parse_html.py           # HTML 解析脚本
│   ├── parse_markdown.py       # Markdown 处理脚本
│   └── utils.py                # 工具函数
├── templates/
│   ├── README_template.md      # README 模板
│   └── metadata_template.yaml  # 元数据模板
└── examples/
    └── example_usage.md        # 使用示例
```

### 4.2 SKILL.md 内容

```markdown
# Reference Parser Skill

## 功能

解析多种格式的参考资料文件，生成标准化的参考资料目录结构。

## 支持格式

- PDF (.pdf)
- Word (.docx)
- Markdown (.md)
- HTML (.html, .htm)

## 使用方法

### 基本用法

```
请解析参考资料文件 path/to/document.pdf
- 内部 ID: REF-STD-001
- 标题: IEEE Std 1800-2023 SystemVerilog LRM
- 领域: 标准与方法学
- 主题: HDL
```

### 批量解析

```
请批量解析以下参考资料：
- path/to/doc1.pdf -> REF-STD-001
- path/to/doc2.docx -> REF-STD-002
```

## 输出结构

解析后生成的目录结构：

```
reference/knowledge-handbook/{category}/{REF-ID}/
├── README.md              # 生成的主文档
├── metadata.yaml          # 生成的元数据
├── images/                # 提取的图片
└── origin/                # 原始文件
    └── {original_file}
```

## 处理流程

1. **文件分析**: 检测文件格式，提取基本信息
2. **内容提取**:
   - PDF: 使用 PyMuPDF/pdfplumber 提取文本和图片
   - DOCX: 使用 python-docx 提取内容
   - HTML: 使用 BeautifulSoup 解析
   - Markdown: 直接复制并处理相对路径
3. **图片提取**: 提取并保存到 images/ 目录
4. **元数据生成**: 根据输入参数生成 metadata.yaml
5. **README 生成**: 使用模板生成标准化的 README.md
6. **索引更新**: 更新上级目录的 README.md 索引

## 依赖

- Python 3.10+
- PyMuPDF (fitz)
- python-docx
- beautifulsoup4
- PyYAML
- Pillow

## 注意事项

- 大文件可能需要较长处理时间
- PDF 中的扫描件需要 OCR 支持（可选）
- 图片格式自动转换为 PNG/SVG
- 保留原始文件的完整性
```

### 4.3 核心脚本设计

#### parse_pdf.py

```python
#!/usr/bin/env python3
"""PDF 参考资料解析器"""

import fitz  # PyMuPDF
import os
import yaml
from pathlib import Path
from datetime import datetime

def parse_pdf(pdf_path: str, output_dir: str, metadata: dict):
    """
    解析 PDF 文件并生成标准化目录结构

    Args:
        pdf_path: PDF 文件路径
        output_dir: 输出目录路径
        metadata: 元数据字典
    """
    # 创建目录结构
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'origin'), exist_ok=True)

    # 复制原始文件
    origin_path = os.path.join(output_dir, 'origin', os.path.basename(pdf_path))
    shutil.copy2(pdf_path, origin_path)

    # 打开 PDF
    doc = fitz.open(pdf_path)

    # 提取文本
    full_text = []
    for page in doc:
        full_text.append(page.get_text())

    # 提取图片
    image_count = 0
    for page_num, page in enumerate(doc):
        for img_index, img in enumerate(page.get_images()):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_filename = f"figure-{image_count:03d}.{image_ext}"
            image_path = os.path.join(output_dir, 'images', image_filename)

            with open(image_path, 'wb') as f:
                f.write(image_bytes)
            image_count += 1

    # 生成 metadata.yaml
    metadata['files'] = {
        'markdown': 'README.md',
        'images': [f"images/figure-{i:03d}.{ext}" for i, ext in enumerate(...)],
        'origin': [{
            'path': f"origin/{os.path.basename(pdf_path)}",
            'format': 'pdf',
            'size': f"{os.path.getsize(pdf_path) / 1024 / 1024:.1f}MB"
        }]
    }

    with open(os.path.join(output_dir, 'metadata.yaml'), 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, allow_unicode=True, default_flow_style=False)

    # 生成 README.md
    readme_content = generate_readme(metadata, full_text)
    with open(os.path.join(output_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme_content)

    doc.close()
    return output_dir
```

#### parse_docx.py

```python
#!/usr/bin/env python3
"""Word 参考资料解析器"""

from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import os
import yaml
import shutil

def parse_docx(docx_path: str, output_dir: str, metadata: dict):
    """解析 DOCX 文件"""
    # 创建目录结构
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'origin'), exist_ok=True)

    # 复制原始文件
    origin_path = os.path.join(output_dir, 'origin', os.path.basename(docx_path))
    shutil.copy2(docx_path, origin_path)

    # 打开文档
    doc = Document(docx_path)

    # 提取文本
    paragraphs = [p.text for p in doc.paragraphs]

    # 提取图片
    image_count = 0
    for rel in doc.part.rels.values():
        if "image" in rel.reltype:
            image_data = rel.target_part.blob
            image_ext = rel.target_part.content_type.split('/')[-1]

            image_filename = f"figure-{image_count:03d}.{image_ext}"
            image_path = os.path.join(output_dir, 'images', image_filename)

            with open(image_path, 'wb') as f:
                f.write(image_data)
            image_count += 1

    # 生成元数据和 README
    # ... 类似 PDF 处理

    return output_dir
```

## 5. 实施计划

### 阶段 1: 规范制定
- [ ] 确定目录结构规范
- [ ] 确定元数据格式
- [ ] 确定 README 模板

### 阶段 2: VitePress 配置
- [ ] 修改 config.mts 支持参考资料
- [ ] 添加侧边栏配置
- [ ] 添加导航入口
- [ ] 测试构建和预览

### 阶段 3: Skill 开发
- [ ] 创建 Skill 目录结构
- [ ] 编写 SKILL.md
- [ ] 实现 PDF 解析脚本
- [ ] 实现 DOCX 解析脚本
- [ ] 实现 HTML 解析脚本
- [ ] 实现 Markdown 处理脚本
- [ ] 编写使用文档和示例

### 阶段 4: 测试验证
- [ ] 测试单个资料解析
- [ ] 测试批量解析
- [ ] 测试 VitePress 展示
- [ ] 验证链接和导航

## 6. 待确认问题

1. **图片处理**: 是否需要自动压缩图片？支持哪些格式？
2. **OCR 支持**: 是否需要支持扫描版 PDF 的 OCR 识别？
3. **索引更新**: 是否需要自动更新上级目录的索引？
4. **版本管理**: 同一资料多个版本如何管理？
5. **权限控制**: 是否需要支持资料的访问权限控制？
