# AIXSILICON 统一建设路线图

本文件是跨仓优先级、依赖顺序和里程碑的唯一活动规划。目标架构见 [`architecture/target-design.md`](architecture/target-design.md)，仓级任务见对应 `docs/<repo>/delivery.md`。

## 1. 规划原则

1. 先修正工作区语义，再扩充 Flow；
2. 先闭环后扩面：先完成一个 APB IP 的 C0→C4，再复制到 CBB 和 SoC；
3. 契约、provider 和 Evidence 必须同时存在，才算能力可用；
4. 公共流程不能依赖私有 Skill、商业 EDA 路径或 Knowledge；
5. 只有出现真实复用和独立生命周期才新增仓库；
6. 不用模糊百分比，用里程碑出口和可重建证据报告进度。

## 2. 优化后的里程碑

| 里程碑 | 目标出口 | 关键交付 | 状态 |
|---|---|---|---|
| M0 文档与决策基线 | 新材料自包含，目标方案可审核 | 统一 docs、45/45 迁移、ADR-0007/0008 建议稿 | `in-progress` |
| M1 工作区语义 v2 | Profile 精确、依赖有类型、旧配置兼容 | `include_repositories`、typed dependencies、迁移测试 | `planned` |
| M2 可执行契约 | P0 action 可预检、可调用、可锁定 | provider metadata、`wf preflight`、tool/provider lock | `planned` |
| M3 APB 资格闭环 | 固定 Lock 可重建 APB lint/编译/仿真/Evidence | HWIF + reg tool + IP + DV Common + APB VIP | `planned` |
| M4 协作与发布闭环 | PR HEAD 联测，人工批准后发布到 Catalog | Change Bundle CI、G7、SBOM/RTM、Catalog PR | `planned` |
| M5 CBB 产品化 | 三个示范构件验证参数/PPA 平台后按需扩种子池 | CBB Flow、arbiter/pipeline/FIFO 三闭环、发布证据 | `planned` |
| M6 最小 SoC | Catalog 资产可生成并验证最小 SoC 基线 | 地址/IRQ/CRG/Top/软件派生、boot smoke | `planned` |
| M7 规模化运营 | 多环境、Nightly、兼容矩阵与项目座舱 | blue/red zone、容量/失败指标、baseline train | `deferred` |

## 3. 关键路径

```text
M0 文档与 ADR 审核
  → M1 Profile / typed dependency
  → M2 capability preflight / provider lock
  → M3 APB C0→C3
  → M4 APB C4 / Catalog
  → M5 CBB
  → M6 SoC
  → M7 规模化
```

M1 与 M2 可以并行设计，但 APB 实跑前必须共同完成。CBB Flow 可在 M3 后半段开始设计，但发布复用 M4；SoC 只提前冻结 Schema，不提前铺开生成器。

## 4. 近期执行包

### WP0：完成方案审核

- 审核 [`architecture/target-design.md`](architecture/target-design.md)；
- 决定是否接受 ADR-0007/0008；
- 审核 10 个 Repo/Workflow 的设计契约与交付台账，以及候选仓激活门禁；
- 审核 [`findings.md`](findings.md) 的处置与关闭证据；
- 归档材料已完成 45/45 迁移并删除旧目录，保留 Git 可恢复性；
- 保持 `progress.md` 为唯一组合看板。

### WP1：Profile 与依赖模型

- Manifest Schema 兼容增加 `include_repositories` 和 `dependencies.*`；
- `depends_on` 过渡映射为 `product`；
- Profile exact-set、各类型 DAG/闭包和旧配置兼容测试；
- 迁移默认 Manifest，使 `minimal/ip-dev/cbb-dev/dv-dev/soc-integration` 得到不同仓集；
- Lock/Evidence 记录依赖类型和解析策略版本。

### WP2：Action Capability

- 生成全部 Flow action inventory；
- 定义 provider metadata、版本约束和 availability 状态；
- 新增 `aix wf preflight <flow>`；
- P0 action 接入真实 tools provider；
- 工具/provider/容器/EDA 摘要进入 Lock 和 Evidence；
- FuseSoC 实跑全部启用 Core。

### WP3：APB 垂直闭环

- 冻结 APB Contract 与兼容规则；
- 从 SystemRDL 确定性生成 RTL/Header/RAL；
- APB VIP 完成 driver/monitor/checker/coverage；
- DV Common 提供 RAL base、CSR sequence 和 result model；
- IP 仓落地代表性寄存器 IP；
- 固定 Lock 下产生 G0～G6 Evidence。

### WP4：协作和发布

- `aix bundle create` 真实生成并联合 checkout PR refs；
- reusable workflows 固定 release tag；
- `release prepare/publish` 实现 clean/lock/override/审批/幂等保护；
- 生成 SBOM、RTM、Release Manifest 和 Catalog PR；
- APB IP 达到 C4 Released。

## 5. 各仓近期目标

| 仓 | 当前阶段目标 | 能力出口 |
|---|---|---|
| workflow | typed dependency、exact Profile、preflight、工具锁、CI/Release | M1/M2/M4 |
| tools | P0 provider metadata 和真实 action 接入 | C2 Integrated |
| hwif | APB 契约 + CBB/VIP/IP 两个以上真实消费者 | G3 报告 |
| dv-common | RAL base + CSR sequence + 标准 Result | G4 单测/Smoke |
| vip | 最小 APB VIP 与 negative/self-check | G4/G5 |
| ip | APB 代表性 IP | Qualification G0～G6；Release G7/C4 |
| catalog | 首个 qualified/released IP 与兼容关系 | Catalog PR |
| cbb | 先定义 CBB Flow，再做种子构件 | M5 |
| soc-integration | 先冻结最小 Schema/Golden，暂缓大规模生成 | M6 |
| skills | 对齐 action/artifact 契约并完成 eval，不成为 required | 可选增强 |
| knowledge | 建立可引用索引，不进入 Lock/Gate | 内容质量报告 |

## 6. 候选仓评审点

详细建仓边界和首个切片见 [`proposals/repositories/`](proposals/repositories/README.md)。下列条目是复审门，不是活动开发任务。

| 候选 | 建仓触发条件 | 复审点 |
|---|---|---|
| techlib | 两类以上 Generic/FPGA/ASIC 真实适配和两个消费者 | M5 |
| model | 两个以上 IP 共享同一参考模型 | 按需 |
| sw | M6 需要独立 BSP/Boot/HAL 生命周期 | M6 前 |
| reference-soc | 最小 SoC Golden 稳定并需要独立发布 | M6 后 |
