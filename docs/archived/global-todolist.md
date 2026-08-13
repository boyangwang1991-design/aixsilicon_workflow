# AIXSILICON 统一 Todo 计划

> 统筹旧版 `todo.md`（阶段0–5）、`aixsilicon_build_todolist.md`（B0–B4）与各仓收口的 plan/todo 形成统一待办。
> 状态标记：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。
> 各仓详细 plan/todo（完整原文）见归档区 [`archived/architecture/repo-plans/`](archived/architecture/repo-plans/README.md)；建设规划见 [`workflow-repo-plan.md`](workflow-repo-plan.md)。

---

## 1. workflow 本体（`aixsilicon_workflow`）

### 1.1 P0 优先

- [ ] runner `aix tool` 委托真实 provider（tool_repo 插件）接入，并纳入工具版本锁
- [ ] `aix release prepare/publish` 实现（当前桩；G7 需 dirty/override 阻断 + 人工批准）
- [ ] `workspace-lock.schema.json` 增加 `tools:` 段（tool_repo 包版本 + hash）
- [ ] 验证所有 Core 可被 FuseSoC 发现（`aix wf run` 真实执行 `fusesoc.target` 阶段）

### 1.2 P1 首个季度

- [ ] `aix bundle create` 从模板生成并校验状态机（当前为模板指引）
- [ ] PR refs 联合 checkout（`change-bundle.yml` 占位 → 真实）
- [ ] reusable workflows 固定 Tag v0.1 上线（lint/unit-sim/integration-baseline/change-bundle 真实化）
- [ ] `aix release publish` 端到端（Tag/SBOM/Catalog PR 编排）；baseline 升级 + Workspace Bundle Release
- [ ] 失败 Run 定位接入（仓库/SHA/Stage/工具/Failure Signature）
- [ ] 新成员从零初始化演练（clean 环境）

### 1.3 P2 两个季度

- [ ] `soc-*` flow 动作接入（`tool.socgen`/`tool.connect`）
- [ ] blue-zone / red-zone 双环境实跑
- [ ] Nightly 兼容矩阵
- [ ] AIXSILICON 项目座舱接入
- [ ] 并发互斥与失败恢复

### 1.4 工程化遗留

- [ ] `aix repo pr`（gh CLI 包装，S5 残余）
- [ ] GitHub reusable workflows 真实化（S6，替换 echo 占位）

---

## 2. 各仓待办

> 细节与原文见 [`archived/architecture/repo-plans/`](archived/architecture/repo-plans/README.md)。

### 2.1 hwif（现状：57 接口族建成）

- [ ] Techlib binding（`aixsilicon_techlib_repo` 待建前以抽象接口承接）
- [ ] 完成 2 个真实消费者（CBB + VIP）依赖其 core 并通过编译
- [ ] VLNV 迁移 `aix:interface:*` → `aixsilicon:interface:*`（deprecated 窗口）
- [ ] G1 Semantic 架构评审（当前 `[ ]`）；正式 IP/VIP/SoCGen 消费证据

### 2.2 cbb（现状：骨架 + 清单）

- [ ] P0 15 种子构件从 planned → verified（FIFO/Arbiter/Slice/Sync 等）
- [ ] `cbb.yaml` SSOT + 统一验证 harness 落地
- [ ] 3 个示范闭环（32 路仲裁器 / Ready-Valid 长链 / FIFO 存储映射）
- [ ] 至少 10 个构件达 E2/E3，Catalog 可检索

### 2.3 ip（现状：建仓，uart 0.1.0）

- [ ] 首个 APB 寄存器 IP（SystemRDL/RAL/RTL）发布为 `aixsilicon:ip:*`
- [ ] registry/ipkg 对齐统一契约；`.core` 复用 `aix-core-tool`（R7）
- [ ] 双态模型落地（dev 分支可编辑 / release 版本目录冻结，A1）
- [ ] G0–G5 门禁产物

### 2.4 dv-common（现状：P0 底座完成）

- [ ] RAL base 与 CSR sequence 正式行为（smoke/reset/rw/bit-bash）
- [ ] PeakRDL UVM RAL 输出链接入
- [ ] APB 寄存器 IP 示例（`examples/apb_csr_ip`）+ 首个 Candidate + Catalog 接入
- [ ] out-of-order matcher、reset epoch（P1/P2）
- [ ] CI 三段接入（PR/Nightly/Release）

### 2.5 vip（现状：规划为主）

- [ ] APB VIP 达 V3 Qualified
- [ ] Clock/Reset、Generic Memory、Interrupt 达 V2
- [ ] AXI4-Lite / AXI-Stream beta
- [ ] 双仿真器矩阵 + cocotb 交叉验证；接入 UVM Verification Skill

### 2.6 tools（现状：P0 五包骨架）

- [ ] `aix-reg-tool` 真实实现（SystemRDL→RTL/RAL/Header）
- [ ] `aix-hwif-gen` 真实实现（契约→多视图）
- [ ] `aix-core-tool` 真实实现 + `aixsilicon.commands` 插件可被 workflow `aix tool` 调用
- [ ] Golden Test + 工具版本锁

### 2.7 catalog（现状：骨架）

- [ ] 首批 `qualified` 资产条目（IP/HWIF/DV-Common 各至少 1）
- [ ] 兼容矩阵与成熟度映射落地
- [ ] 随各仓 release 自动/受控更新

### 2.8 soc-integration（现状：骨架）

- [ ] 完整 Schema 集（address/irq/crg/power/connect）
- [ ] 配合 tool 的 Address/IRQ/CRG Checker 接入
- [ ] 最小 SoC Golden 示例
- [ ] SoC YAML 可通过地址/中断/连接检查

### 2.9 skills（现状：canonical 已落地，私有）

- [ ] 套件自校验 / Eval 全链路
- [ ] 与 workflow / tool 契约对齐（Context Pack / Change Plan / Skill Result）
- [ ] IP Golden Path 端到端；Author/Verifier 双 Agent
- [ ] CBB / SoC Integration suite

### 2.10 knowledge（现状：已接入，内容待填充）

- [ ] 方法论 / 术语 / 参考索引填充
- [ ] 与 Skill 与工程实践联动

---

## 3. 跨仓治理遗留（来自跨仓评审/优化）

- [ ] **R1 工具收敛**：hwif `tools/` 产品级工具分阶段迁入 tool_repo（ADR-0006 阶段 A/B/C）
- [ ] **R4 发布职责分工**：ipkg（IP 源码发布）/ `aix release`（跨仓 Gate 编排）/ hwif package_release 边界落地
- [ ] **R5 影响分析语义**：接口影响 vs 仓库影响命名区分
- [ ] **A1 IP 双态模型**：dev 分支可编辑、release 版本冻结
- [ ] **A2 vendored `reference/` 治理**：排除 fusesoc 发现、不发布、不进 Catalog
- [ ] **A4 techlib 统一**：`aixsilicon_techlib_repo`（P1 待建）
- [ ] **D2 仓库命名统一**：dv-common / soc-integration 是否加 `_repo` 后缀（方案 A 重命名 / B 固化现状）
- [ ] **C3 VLNV 迁移窗口**：存量 `aix:*`/`company:*`/`boyangwang1991-design:*` 统一至 `aixsilicon:*`

## 4. 待建仓

- [ ] `aixsilicon_techlib_repo`（P1）：工艺/FPGA 抽象与适配
- [ ] `aixsilicon_sw_repo`（P1）：BSP/Boot/HAL/驱动/SoC Smoke
- [ ] `aixsilicon_reference_soc_repo`（P2）：可运行最小 SoC/FPGA 参考
- [ ] `aixsilicon_model_repo`（按需）：跨 IP 共享参考模型

> 建仓前先在 `archived/schema-ownership.md` 仓库注册表登记，禁止“口头建仓”。

## 5. 依赖顺序与近期第一步

**依赖**：hwif 先于 cbb/vip/ip；dv-common 先于 vip/ip 验证；`aix-reg-tool` 先于 APB 完整穿刺；Catalog 随各仓 release 持续填充；workflow 的 `aix tool` 接入依赖 tool_repo 插件；公共流程不依赖私有 Skill。

**近期第一步（下一轮执行）**：

1. **tool_repo**：实现 `aix-reg-tool` 与 `aix-hwif-gen`，让 `aix tool` 在 workflow 真实可用；
2. **ip_repo + dv_common + vip_repo**：协作完成 APB 寄存器 IP 完整仿真穿刺（替换当前编排级）；
3. **cbb_repo**：P0 15 种子构件首批 verified；
4. **catalog_repo**：将上述发布资产登记为 `qualified`；
5. **workflow**：把 `aix wf run ip-verification` / `apb-register-ip` 的 `tool.*` / `eda.*` 阶段全部转真实执行。

## 6. 关联

- 建设规划：**[`workflow-repo-plan.md`](workflow-repo-plan.md)**
- 规划索引：**[`index.md`](index.md)**
- 各仓 plan/todo 原文：**[`archived/architecture/repo-plans/`](archived/architecture/repo-plans/README.md)**
- 旧版 todo / build_todolist（历史）：[`archived/root/`](archived/root/README.md)
