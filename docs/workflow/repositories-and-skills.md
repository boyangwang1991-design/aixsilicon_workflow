# 仓库与 Skill 使用地图

以下链接指向本地独立 clone。仅克隆 workflow 时，`../../repos/` 链接不会存在；同步相应 Profile 后可用。
skills/tools 为私有仓，其链接需要本地副本或仓库访问权限。仓库远端清单见 [根 README](../../README.md)。

## 任务路由

| 逻辑 repo ID | 仓库入口与主要资产 | 开发方法入口 |
|---|---|---|
| `hwif` | [HWIF](../../repos/aixsilicon_hwif_repo/README.md)：Contract/Profile/Binding、SV 多视图、兼容性 | [hwif-development-suite](../../repos/aixsilicon_skill_repo/skills/hwif-development-suite/SKILL.md)；`hwif_tool.py` |
| `dv-common` | [DV Common](../../repos/aixsilicon_dv_common/README.md)：`src/`、`rtl/`、`schemas/`、通用组件与示例 | 当前没有独立 dv-common suite；以仓内架构、依赖规则和测试为准，由消费领域套件联调 |
| `vip` | [VIP](../../repos/aixsilicon_vip_repo/README.md)：registry、`vip/` 工程包、仓库准入检查 | [vip-development-suite](../../repos/aixsilicon_skill_repo/skills/vip-development-suite/SKILL.md)；`vip_tool.py` |
| `cbb` | [CBB](../../repos/aixsilicon_cbb_repo/README.md)：registry、`components/`、`adapters/`、构件证据 | [cbb-development-suite](../../repos/aixsilicon_skill_repo/skills/cbb-development-suite/SKILL.md)；`cbb_tool.py` |
| `ip` | [IP](../../repos/aixsilicon_ip_repo/README.md)：`ips/`、索引生成源、工程包与集成文档 | [ip-development-suite](../../repos/aixsilicon_skill_repo/skills/ip-development-suite/SKILL.md)；按子 skill 调用 extractor、验证与打包脚本 |
| `soc-integration` | [SoC Integration](../../repos/aixsilicon_soc_integration/README.md)：公共 Schema、模板、规则和示例 | [soc-integration-suite](../../repos/aixsilicon_skill_repo/skills/soc-integration-suite/SKILL.md)；具体项目另选授权工作区 |
| `tools` | [Tool Repo](../../repos/aixsilicon_tool_repo/README.md)：跨仓确定性能力与插件 | 先确认 `aix tool` 插件实际可用；不把命令名当成已安装能力 |
| `catalog` | [Catalog](../../repos/aixsilicon_catalog_repo/README.md)：发布资产索引、兼容与成熟度 | 发布流程维护，不用来登记未经认证的研发结论 |
| `skills` | [Skill Repo](../../repos/aixsilicon_skill_repo/README.md)：canonical `skills/` | [workspace-management](../../repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/SKILL.md) 管物化与 CLI |
| `knowledge` | [知识库](../../repos/aixsilicon_chipknowledge/README.md)：术语、方法与参考 | 作为上下文，不代替契约或测试证据 |

`workflow` 是父仓的特殊逻辑 ID；`skills`、`dv-common`、`soc-integration` 等 ID 不等于物理目录名。
不要使用不存在的 `soc` 或 `dvcommon` ID 代替命令参数。

## 每类事实改在哪里

| 事实 | 编辑入口 | 派生/消费侧 |
|---|---|---|
| 工作区仓库集合 | `manifests/default.yaml` | `.aix/` 状态、Lock、FuseSoC 聚合配置 |
| HWIF 接口语义 | 契约 YAML、Profile、Binding | 工具生成或一致性检查的 SV、flat、文档、交换视图 |
| CBB 索引与资产合同 | registry 管索引状态；`cbb.yaml` 等管资产身份、参数和契约 | 配置空间、RTL 实现、验证与表征证据；生成配置不得手改 |
| IP 索引 | `scripts/data/*.py`；`ip_ids.json` 保留稳定编号 | `registry.yaml` 与 README 状态块 |
| IP 设计意图 | Markdown 正文及 META，LRS/HLD/LLD/VPLAN 各司其职 | extractor 生成 `model/*.yaml`；trace/质量模型按 owner 工具生成 |
| IP 寄存器结构 | `regs/*.rdl`；字段行为在 LLD 定义 | CSR RTL、软件头文件、RAL 等派生物 |
| VIP 需求与认证 | 套件定义的需求、架构、验证计划、RTM 与运行证据 | Qualification/Release 包；仓库 registry 是准入索引，不等同完整生命周期模型 |
| DV 通用机制 | 仓内公共类型、服务、Schema 与组件实现 | VIP/IP/SoC 环境复用，不反向依赖具体 DUT |
| SoC 资源与连接 | 按子 skill 维护带 META 的源文档并抽取 | `ssot/*.yaml` 为机器消费权威、`model/` 与指纹为生成结果；不可双向手改 |

“SSOT”不是“所有 YAML 都能手改”。先区分设计编辑源、机器模型、索引和运行证据，再执行 owner 的生成步骤。

## 套件怎样加载

先读 suite 根 `SKILL.md`，再按任务选子 skill 与必需 reference；不要求每次加载整套模板。
`partial-task` 只做本任务必需链路，`review-only` 不生成正式下游交付，`full-flow` 才要求端到端门禁。
不同套件的模式、参数与默认行为以各自文件为准。

canonical 源在 `repos/aixsilicon_skill_repo/skills/`；`bootstrap.py --ensure` 将其物化到选定 agent 目录，默认 `.roo/skills/`。
只编辑 canonical 源，物化副本会被覆盖。物化不等于 Flow action 注册，也不安装商业 EDA 或许可证。

辅助套件还包括 `ip-fusa-suite`、`chipdraw-skill-suite` 和文档转换技能；仅在任务确实需要时加载。
这些辅助能力不代替主域的设计 owner、质量门禁或发布审批。
