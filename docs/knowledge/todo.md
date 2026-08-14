# knowledge — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。原文见 [`../archived/architecture/repo-plans/knowledge.md`](../archived/architecture/repo-plans/knowledge.md)。
> 本文件已并入 archived 原文卷 01–18 逐项 TODO 与横向资产明细（合并补充），并追加仓级待办。

## 已完成

- [x] 五层架构迁移（knowledge/app/template-script-schema/skill/project-data）
- [x] 卷 01 芯片研发全景（V01-00~08）
- [x] 卷 02–04 / 06–16 大量章节内容 Draft
- [x] 首条案例链（参数化流水线 MAC）贯穿知识页草案

## 阶段 0 基线收尾

- [ ] B0-06 指定 Owner/Reviewer（RACI 与领域人员名单）
- [ ] B0-07 冻结工具基线（仿真/Lint/综合及开源替代路径）
- [ ] B0-08 技术评审基线（P0 模板和模型无阻塞问题）

## 内容建设（P0）

- [ ] 卷 05 核心领域与典型 IP（计算/存储/互联/媒体/控制/外设）
- [ ] 卷 17 AI 辅助芯片研发（可信 RAG/知识生产/Skill/评测与安全）
- [ ] 卷 18 工程实践与典型案例（MAC 完整案例 V18-01、ECC SRAM、AXI-Lite Crossbar、图像 Pipeline、DMA+中断）
- [ ] 各 Draft 章节完成 Owner 技术评审（卷 02/03/04/06–16）

## 卷 01–18 逐项 TODO（archived 原文合并）

> 逐项状态与 archived `repo-plans/knowledge.md` TODO 原文一致：`[x]` 内容已完成（多为 Draft、待 Owner/工具验证），`[ ]` 待办。

### 卷 01：芯片研发全景

- [x] V01-00 建立卷目录、阅读路径和章节关系
- [x] V01-01 芯片类型、抽象层级与研发边界
- [x] V01-02 芯片研发全生命周期
- [x] V01-03 组织角色、责任边界与协作接口
- [x] V01-04 设计验证全景与六个研发闭环
- [x] V01-05 EDA 工具链、计算环境与结果证据
- [x] V01-06 配置、版本、数据与许可证基础
- [x] V01-07 新人学习路径与工程任务地图
- [x] V01-08 来源、术语、交叉链接和结构检查
- [ ] V01-09 领域 Owner 技术评审
- [ ] V01-10 试点项目工程验证与发布

### 卷 02：研发流程与项目交付

- [x] V02-01 公司级 IPD 与技术评审分层（内容 Draft；待 Owner 技术评审）
- [x] V02-02 芯片产品主流程（内容 Draft；待 Owner 技术评审）
- [x] V02-03 SoC/Subsystem/IP 研发流程（内容 Draft；待 Owner 技术评审）
- [x] V02-04 模块开发与 PPA 收敛流程（内容 Draft；待 Owner 技术评审）
- [x] V02-05 Verification 与 Closure 流程（内容 Draft；待 Owner 技术评审）
- [x] V02-06 Tape-out、Bring-up 与量产反馈接口（内容 Draft；待 Owner 技术评审）
- [x] V02-07 Stage Gate、RACI 与准出机制（内容 Draft；待 Owner 技术评审）
- [x] V02-08 配置、基线、变更和 ECO（内容 Draft；待 Owner 技术评审）
- [x] V02-09 流程裁剪、异常与升级路径（内容 Draft；待 Owner 技术评审）
- [x] V02-10 交付物矩阵和项目证据包（内容 Draft；待 Owner 技术评审）

### 卷 03：数字设计基础

- [x] V03-01 组合逻辑、时序逻辑与同步设计（内容 Draft；待 Owner 技术评审）
- [x] V03-02 Clock、Reset 与复位释放（内容 Draft；待 Owner 技术评审）
- [x] V03-03 FSM 设计、编码与验证（内容 Draft；待 Owner 技术评审）
- [x] V03-04 ready/valid、握手与背压（内容 Draft；待 Owner 技术评审）
- [x] V03-05 Pipeline、延迟、吞吐与停顿（内容 Draft；待 Owner 技术评审）
- [x] V03-06 数制、定点数、舍入、截断和饱和（内容 Draft；待 Owner 技术评审）
- [x] V03-07 参数化与非法配置防护（内容 Draft；待 Owner 技术评审）
- [x] V03-08 FIFO、仲裁器、计数器和常用结构（内容 Draft；待 Owner 技术评审）

### 卷 04：SoC 架构与系统基础

- [x] V04-01~V04-16 系统级章节（处理器加速器与软硬件划分/存储层次一致性/互联地址 QoS 流控/中断寄存器软件可见资源/CRG 电源域系统状态/Boot-Debug 可观测性/性能模型 Workload 预算/FPGA-Emulation/证据图谱/跨 ISA 特权架构/一致性互联 NoC/内存控制器 DRAM RAS/高速 I-O Chiplet/Timer-DMA-IOMMU/Firmware-OS 契约/开源 SoC 研读；内容 Draft、待相应 Owner/工具验证）

### 卷 05：核心领域与典型 IP

- [ ] V05-01 计算类 IP / V05-02 存储类 IP / V05-03 互联类 IP / V05-04 媒体类 IP / V05-05 控制类 IP / V05-06 外设-CRG-电源-安全-DFX 扩展 / V05-07 领域差异对照与案例导航

### 卷 06：需求与架构设计

- [x] V06-01~V06-08（场景 Use Case 需求获取/需求质量唯一 ID 分解/Assumption-约束-风险-变更/RTM 端到端追踪/HLD-LLD-ADR/接口-寄存器-时序契约/性能-PPA 预算可达成性/可验证性-可测性-安全异常设计；内容 Draft、待 Owner 技术评审）

### 卷 07：RTL 设计方法

- [x] V07-01~V07-08（可综合 RTL 编码语义/组合时序模板赋值规则/数据与控制通路/Pipeline-Buffer-仲裁资源共享/参数化生成结构与配置保护/Clock-Reset-CDC 友好结构/低功耗-DFT-安全-可验证性/Code Review-重构-ECO；内容 Draft、待 Owner 技术评审）

### 卷 08：SystemVerilog 基础

- [x] V08-01~V08-07（类型作用域四态/数组结构联合 Package/Interface-Modport-Clocking/类继承多态 Factory/随机化约束/进程事件 Mailbox-Semaphore/SVA 序列属性采样；内容 Draft、待工具验证与 Owner 评审）

### 卷 09：功能验证方法

- [x] V09-01~V09-08（风险驱动验证策略/VP-Feature-TP-TC/参考模型 Scoreboard 端到端检查/激励约束 Corner/Assertion 协议检查/功能覆盖代码覆盖 Closure/回归缺陷 Debug 复现/验证签核证据；内容 Draft、待 Owner 技术评审）

### 卷 10：UVM 工程化

- [x] V10-01~V10-08（Transaction-Sequence-Sequencer/Driver-Monitor-Agent/Env-TLM-Scoreboard-Predictor/Factory-ConfigDB-Phase-Objection/RAL 寄存器验证/Virtual Sequence 跨接口场景/IP 到 Subsystem 复用/性能日志 Debug 组件单测；内容 Draft、待工具验证与 Owner 评审）

### 卷 11：形式与静态验证

- [x] V11-01~V11-08（Lint 方法 Closure/CDC 约束质量/RDC 复位域风险/Formal Property Verification/Connectivity 结构检查/X-Propagation/LEC-ECO 等价性/告警分类 Waiver 证据治理；内容 Draft、待工具验证与 Owner 评审）

### 卷 12：综合、STA 与 PPA

- [x] V12-01~V12-08（PPA 可达成分析/综合输入约束结果/STA 多模式多角异常路径/面积分析资源根因/活动率功耗场景功耗分析/关键路径物理感知优化/时序面积功耗联合收敛/基线比较偏差审批报告 Schema；内容 Draft、待工具验证与 Owner 评审）

### 卷 13：低功耗设计

- [x] V13-01~V13-07（功耗组成早期估算/电源域电源状态表/UPF 基础版本边界/Isolation-Retention-Level Shifter/Clock-Power Gating-DVFS/功耗感知验证低功耗 CDC-RDC/活动率功耗场景签核；内容 Draft、待工具验证与 Owner 评审）

### 卷 14：DFT、后端与签核

- [x] V14-01~V14-06（Scan-ATPG 前端接口/MBIST-LBIST 存储测试/Floorplan-布局布线时钟树/前后端协同物理反馈/门级仿真时序回标/Sign-off-ECO-Tape-out Readiness；内容 Draft、待 DFT/物理/仿真工具验证与 Owner 评审）

### 卷 15：安全、功能安全与可靠性

- [x] V15-01~V15-08（Threat Model 安全需求/Secure Boot 密钥访问控制/ECC-Parity-Lockstep 错误处理/Safety Lifecycle-Goal 追踪/FMEDA-DFMEA 诊断覆盖/Fault Injection/可靠性恢复证据/红区知识与 AI 安全边界；内容 Draft、待安全/Safety Owner 在红区或工具验证）

### 卷 16：工程工具与自动化

- [x] V16-01~V16-07（寄存器-中断-CRG-SOCGEN/可复现环境依赖制品/CI 分层回归/日志波形失败聚类/结果 Schema 报告 Dashboard/工具适配器开源替代/自动化质量权限审计；内容 Draft、待生成器/CI/解析器验证与 Owner 评审）

### 卷 17：AI 辅助芯片研发

- [ ] V17-01 可信知识 RAG / V17-02 知识生产与文档 Agent / V17-03 RTL-SVA-UVM-Formal Skill / V17-04 静态检查与 PPA 分析助手 / V17-05 RTM-评审-Sign-off 核对 / V17-06 工具调用闭环执行 / V17-07 输入输出契约-人审-权限 / V17-08 评测-Prompt 注入-安全-审计

### 卷 18：工程实践与典型案例

- [ ] V18-01 参数化流水线 MAC 完整案例
  - [x] 建立贯穿知识页，覆盖需求、数值、接口、Pipeline、验证、PPA、RTM、Gate、Bug 与 AI 边界
  - [ ] 指定 Owner/Reviewer，批准 `ADR-MAC-001` 至 `ADR-MAC-005` 并冻结 P0 需求
  - [ ] 补齐 LLD、RTL/SVA、独立参考模型、验证、约束、报告和 Release 资产，以统一命令形成可复现证据
- [ ] V18-02 多 Bank ECC SRAM 控制器完整案例
- [ ] V18-03 AXI-Lite Crossbar 完整案例
- [ ] V18-04 流式图像 Pipeline 完整案例
- [ ] V18-05 DMA + 中断控制器快速案例
- [ ] V18-06 常见 Bug 模式库
- [ ] V18-07 项目复盘、ECO 和回片问题模板
- [ ] V18-08 Sign-off 包与可复现证据样例

## 横向资产

- [ ] X-01 统一术语表；X-02 来源登记与许可证清单
- [ ] X-03 流程—章节—模板—案例交叉索引
- [ ] X-04 首批 100–200 道知识评测题；X-05 首批 20–30 个确定性任务
- [ ] X-06 过期/断链/重复/敏感信息检查；X-07 Owner/Reviewer/季度巡检/版本发布机制

## 参考材料规范

- [ ] `plans/reference-material-spec.md` 落地：目录结构、metadata.yaml、VitePress 配置、Reference Parser Skill、测试验证

## 仓级待办（本批追加）

- [ ] 方法论 / 术语 / 参考索引填充（衔接卷 01–18 与横向资产）
- [ ] 与 Skill 与工程实践联动：知识供给 RTL/UVM/SoC 方法论，承接 Eval/检索与工程实践闭环

## 变更记录

| 日期 | 变更内容 | 作者 |
|------|---------|------|
| 2026-08-13 | 创建 todo.md：已完成、阶段 0 收尾、内容建设、横向资产、参考材料规范 | Zoo |
| 2026-08-13 | 本文件并入 archived 原文卷 01–18 逐项 TODO 与横向资产明细（合并补充）并追加仓级待办（方法论/术语/参考索引填充 + Skill 联动） | Zoo |

## 关联

- Plan：[`plan.md`](plan.md)；全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/knowledge.md` TODO 原文卷 01–18 逐项清单与横向资产 X-01~X-07；仓级待办为本批追加。
