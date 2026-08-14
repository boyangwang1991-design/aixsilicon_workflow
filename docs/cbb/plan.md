# cbb — AIXSILICON CBB Repository 建设规划

> 客观事实基线：2026-08-13（骨架 + 构件清单）。原文细节见 [`../archived/architecture/repo-plans/cbb.md`](../archived/architecture/repo-plans/cbb.md)。
> 本文件已并入 archived 原文的完整规划细节：六维资产坐标（§3.3）、PPA 表征体系（§6）、E0–E5 成熟度（§7.2）、首期建设范围（§12）与工具链规划（§10）。

## 1. 定位与边界

**定位**：**PPA-aware CBB Platform**——经功能验证、实现验证和多维 PPA 表征，可按设计约束自动检索、比较、选型和集成的芯片公共基础构件平台。

**四类资产**：构件资产（A0–A4）/ 实现变体 / 参考架构与 Recipe / PPA 数据与证据。
**四个支撑平面**：质量验证 / PPA 表征与模型 / 生成集成与发布 / 检索推荐与选型。

| 分层 | 定位 | 示例 |
|---|---|---|
| A0 技术适配 | 隔离工艺/宏/平台 | SRAM/ICG/Isolation Wrapper |
| A1 原子机制 | 功能单一 | Mux/Encoder/Counter/LZC/Synchronizer |
| A2 通用复合 | 协议无关 | FIFO/Arbiter/Adder Tree/Register File/ECC |
| A3 协议构件 | 带握手/总线语义 | Ready-Valid Slice/AXI Buffer/APB Adapter |
| A4 子系统模板 | 可配置系统能力 | AXI Fabric/Memory Subsystem（复杂时升级为 IP） |

边界：RTL 工具函数（无独立接口/验证生命周期）→ 公共包，不进入可实例化 CBB；原语适配 → A0；参考架构/Recipe → 配方资产，非可实例化 CBB；完整业务 IP（DMA/GIC/CLIC/FFT/NPU 等）→ 独立 IP 仓。一个资产进入正式 CBB Catalog 需同时满足：功能语义通用、接口契约清晰、独立验证入口与质量结果、明确综合语义及约束、版本/维护人/依赖/兼容声明、PPA 型构件至少完成一个基准工艺/库表征。

## 2. 现状（客观）

- 仓库骨架 + 完整构件清单（registry ~330 项登记）；
- 目录齐备：components/adapters/recipes/schemas/verification/flows/docs；
- **缺口**：P0 15 种子构件多为 planned（未 verified）；`cbb.yaml` SSOT 未落地；无 PPA 表征数据。

## 3. 依赖与角色

- **依赖**：`[hwif]`（CBB 实现依赖 HWIF；验证可依赖 DV-Common/VIP，实现不依赖）；
- **被依赖**：ip、soc-integration；
- **IP 主线角色**：IP 复用 CBB 构件，`tool.ppa-bench` 可做参数化 PPA 评估；
- **SoC 主线角色**：作为实例化单元进入 SoC。

## 4. 契约

- **VLNV**：`aixsilicon:cbb:*`；
- **Schema 所有权**：`cbb-metadata / params / result`；
- **成熟度**：E0–E5（E0/E1→draft；E2/E3→qualified；E4/E5→proven）；
- **SSOT**：每构件 `cbb.yaml`（机器可读），文档由元数据/结果生成。

### 4.1 六维资产坐标

每个 CBB 至少用六个正交维度描述：

1. **抽象粒度**：A0～A4；
2. **技术域**：主 Domain + 次 Domain（Arithmetic/Selection & Decode/Arbitration/Storage & Queue/Streaming & Pipeline/Interconnect/CDC-RDC/Clock-Reset-Power/Control/Safety & Integrity/Monitor & Debug）；
3. **功能契约**：接口、顺序、吞吐、背压、异常行为；
4. **实现变体**：真正不同的微架构（`AREA/PERFORMANCE/LOW_POWER` 是优化意图，不能直接作为实现名；同一个实现是否“高性能”取决于参数、工艺和约束）；
5. **适用区域**：参数范围、工艺、频率、延迟和使用限制；
6. **成熟度**：实验、验证、表征、发布、量产复用。

实现变体管理：同一构件族先定义不可歧义的功能契约，再挂多个实现（`impl_linear/tree/segmented/pipelined`）；功能参数与微架构参数分离；不用大量 `ifdef` 隔离微架构（差异大时用独立实现文件共享接口/断言/参考模型）；每个实现声明参数合法域、最大推荐规模、延迟/吞吐/顺序语义、对 RAM/ICG/DFT/UPF/CDC 约束的依赖与已表征/外推区域；“能编译”不等于“被支持”，未验证参数组合默认属于实验域。

### 4.2 PPA 表征体系

- **统一基准环境**：固定并版本化工艺/库、综合/STA/功耗工具及版本、PVT/RC Corner、时钟周期/uncertainty/IO delay/transition/load、层次化/retiming 等选项、活动率来源与功耗窗口；用 `benchmark_profile_id` 标识，任何数据必须绑定该 ID。
- **表征维度**：实现 / 功能参数 / 性能参数（pipeline、latency、throughput）/ 工艺环境 / 约束 / 活动场景 / 工具环境 / 结果（area、WNS/TNS、Fmax、leakage/internal/switching）。功耗至少分 Leakage/Internal/Switching，动态功耗必须保存活动场景与采样窗口。
- **控制组合爆炸（三阶段）**：锚点扫描（典型参数）→ 边界扫描（最小/最大值、架构切换附近）→ 自适应补点（模型误差大、Pareto 边界、选型临界区）。原始测量与拟合模型分开保存，模型输出必须含误差/置信信息。
- **PPA 比较原则**：先硬约束过滤 → 再 Pareto 分析 → 只有给出偏好后才加权排序 → 返回 `recommended`/`alternatives`/`rejected_with_reason` 三组结果。
- **PPA 回归门限**：每次提交至少与最近发布基线比较；功能/参数合法域/综合成功率不得退化；面积/Fmax/功耗按关键表征点设门限；测量噪声范围标记为无显著差异；工具或库版本变化时重建新基线。

### 4.3 成熟度 E0–E5

| 等级 | 含义 | 使用策略 |
|---|---|---|
| E0 Concept | 方案或实验代码 | 不进入正式 Catalog |
| E1 Functional | 基础功能通过 | 仅限探索 |
| E2 Verified | 完成规定验证 | 可在非关键场景试用 |
| E3 Characterized | 完成基准 PPA 表征 | 可供选型器推荐 |
| E4 Released | 版本化发布并持续回归 | 项目可正式依赖 |
| E5 Proven | 多项目或量产验证 | 默认优选资产 |

成熟度与抽象层级无关，也不能用代码覆盖率单指标代替。生命周期：`Proposal → Incubating → Verified → Characterized → Released → Proven`，弃用需提供替代构件、迁移说明与最后支持版本，已发布版本不可静默覆盖。

## 5. 建设路线（客观）

| 阶段 | 目标 | 状态 |
|---|---|---|
| Phase 0 定义 | 边界/Schema/基准环境/Gate/种子清单 | 🔶 定义完成、实现待做 |
| Phase 1 MVP | 15 种子构件 + Catalog + 表征/比较闭环 | ⬜ |
| Phase 2 PPA 产品化 | 多实现/Pareto/Selector/回归/试点 | ⬜ |
| Phase 3 规模化 | 协议构件/Recipe/技术适配/多项目 | ⬜ |
| Phase 4 智能化 | Pattern Scanner/AI Advisor | ⬜ |

首期不要用“构件数量”作为唯一目标，优先证明端到端链路：资产定义 → 验证 → 表征 → 发布 → 检索 → 选型 → 集成 → PPA 回归。

### 5.1 首期建设范围

- **P0 平台底座**：元数据 Schema、Catalog 与 FuseSoC 发布、统一 Test Harness、综合/STA/功耗表征流程、PPA Comparator 与基础 Selector、CI 质量门禁与版本回归。
- **P0 15 种子构件**：Priority Encoder / One-hot-Binary Mux / Round-Robin Arbiter / Address Decoder / Counter-Timer / Popcount-LZC / Adder Tree / Sync FIFO / Async FIFO / Skid Buffer / Ready-Valid Register Slice / SRAM Wrapper / Synchronizer 族 / ICG-Reset Sync Wrapper / AXI Register Slice。覆盖选择、仲裁、算术、存储、流水、CDC、时钟复位与协议，足以验证平台真实可用。
- **P1 形成可量化 PPA 收益**：Compressor/CSA Tree、常系数乘法器、流水 MAC、分层 Mux/仲裁、Register/SRAM FIFO 自动切换、Banked Memory 多端口映射 Recipe、Stream Width Converter 与 Pipeline FIFO、Operand Isolation 与高扇出本地复制 Recipe、AXI Buffer/Outstanding Limiter/Width Converter、选型器/PPA 回归/项目试点。
- **P2 扩展到架构优化与 AI 闭环**：AXI/APB 桥、AXI CDC、分层互联模板、多 Bank 存储子系统、资源共享与低功耗缓冲、RTL Pattern Scanner、AI PPA Advisor、与 AIXSILICON/PPASight、RTL Coding 和 SoC 集成 Skill 打通。

### 5.2 示范闭环

三个代表性场景验证控制路径、协议流水与存储映射，避免先建设大量孤立模块：

1. **32 路仲裁器**：对比 Linear Priority / Mask RR / Rotate+Priority / Hierarchical RR，在 250/500/800 MHz 与不同请求活动率下形成 Pareto 曲线，验证“选型而非固定最佳实现”。
2. **Ready/Valid 长链**：对比 Bypass / Forward Slice / Skid / Full Slice / Pipeline FIFO，展示组合 Ready 路径、吞吐、首拍延迟与面积关系，形成自动插入 Recipe。
3. **FIFO 存储映射**：扫描数据宽度与深度，对比 Register / Shift / SRAM / Banked SRAM，实现参数到存储结构的自动选择，并覆盖功耗活动场景。

### 5.3 工具链规划（节选）

| 工具 | 职责 | 优先级 |
|---|---|---|
| Schema Validator / CBB Test Runner / Characterization Runner / PPA Comparator / Catalog Builder | 元数据校验、统一 Lint-仿真-Formal-CDC-综合、参数采样与归档、Pareto 前沿、可查询索引 | P0 |
| CBB Selector / Wrapper-Instance Generator / PPA Regression Bot | 硬约束过滤与候选排序、实例与 FuseSoC 依赖生成、退化与 Pareto 变化检测 | P1 |
| RTL Pattern Scanner / AI PPA Advisor | 识别可替换热点并匹配 CBB、解释热点并驱动闭环 | P2 |

AI 职责边界：AI 适合需求转约束、热点解释、候选搜索、Recipe 匹配、参数建议、报告生成；确定性工具负责代码生成、Schema 校验、综合、STA、功耗、形式验证与 Gate 判定；最终选择必须由工具证据闭环。CDC/RDC、ICG、Isolation、Retention、Clock Mux 等采用白名单实现，AI 只能选型和参数化，不能任意重写。

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/cbb.md`](../archived/architecture/repo-plans/cbb.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- **来源**：本文件并入 archived `repo-plans/cbb.md` §3.3 六维资产坐标、§5 实现变体管理、§6 PPA 表征体系、§7.2 E0–E5 成熟度、§12 首期建设范围、§10 工具链规划、§17 示范闭环与 §25 跨仓一致性修订（2026-08-13）。
