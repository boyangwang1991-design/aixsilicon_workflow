# 所有权与工具归属

本文统一回答三个问题：事实/Schema 由谁维护、哪些仓库是正式注册对象、工具应放在哪一类仓。机器可读写入边界以 [`ownership-map.yaml`](../../ownership-map.yaml) 为准。

## 1. Schema 唯一 Owner

每个事实域只有一个 Schema Owner。Owner 负责演进、版本和兼容迁移；消费者按 `$id` 引用发布契约，不复制同义 Schema。

| 事实域 | Owner |
|---|---|
| Workspace Manifest/Lock、Flow、Change Bundle、Tool Profile、Evidence | `aixsilicon_workflow` |
| 接口 Contract/Profile/Binding/Compatibility | `aixsilicon_hwif_repo` |
| CBB 元数据、参数和结果 | `aixsilicon_cbb_repo` |
| 完整 IP 交付内部契约 | `aixsilicon_ip_repo` |
| DV Run Manifest、Test Result、Failure、Metric | `aixsilicon_dv_common` |
| VIP Metadata、Testplan、Coverage、Release Manifest | `aixsilicon_vip_repo` |
| SoC 实例、地址、IRQ、CRG、Power、连接配置 | `aixsilicon_soc_integration` |
| Catalog Asset | `aixsilicon_catalog_repo` |
| Tool Result、Diagnostic、Artifact、Plugin Manifest | `aixsilicon_tool_repo` |
| Skill Metadata、Context Pack、Result、Eval | `aixsilicon_skill_repo`（私有） |

Breaking Schema 变更必须升 major、提供迁移路径并更新消费者兼容测试。

## 2. 仓库注册表

仓库事实以 [`manifests/default.yaml`](../../manifests/default.yaml) 为准；本表只说明注册边界，不维护 branch/SHA 或开发状态。

| ID | 物理仓 | 类型 | 可见性 |
|---|---|---|---|
| workflow | `aixsilicon_workflow` | control-plane | public |
| hwif | `aixsilicon_hwif_repo` | hw-interface | public |
| cbb | `aixsilicon_cbb_repo` | cbb | public |
| ip | `aixsilicon_ip_repo` | ip | public |
| dv-common | `aixsilicon_dv_common` | dv-common | public |
| vip | `aixsilicon_vip_repo` | vip | public |
| tools | `aixsilicon_tool_repo` | tool | private |
| catalog | `aixsilicon_catalog_repo` | catalog | public |
| soc-integration | `aixsilicon_soc_integration` | soc-integration | public |
| skills | `aixsilicon_skill_repo` | skill | private/optional |
| knowledge | `aixsilicon_chipknowledge` | knowledge | public |

候选 `techlib/model/sw/reference-soc` 不属于当前基线；达到 [`../architecture/repos.md`](../architecture/repos.md) 的建仓条件后，通过 ADR、Manifest 和 ownership map 一次性登记。

## 3. 工具四类归属

| 类别 | 归属 | 典型内容 | 约束 |
|---|---|---|---|
| T1 跨仓确定性工具（私有） | `aixsilicon_tool_repo` | HWIF/CSR/Core/Schema 生成与检查 | 稳定 I/O Schema、独立 SemVer、插件暴露、版本锁；源码不直接开源，生成物写入公开资产仓 |
| T2 单仓脚手架 | 对应资产仓 `tools/` | 单仓测试、CI、文档和本地检查 | 不形成跨仓公共契约 |
| T3 私有/受控适配 | 私有 overlay repo | 商业 EDA、PDK/Memory、内部 Runner/Parser | 实现公共 Plugin/Result 契约；公共 Flow 不硬编码路径 |
| T4 项目专用脚本 | 项目仓 | waiver、胶水、迁移和具体项目规则 | 绑定项目事实；成熟复用后再提炼 |

判定顺序：

```text
跨仓复用且契约稳定？         → T1（私有能力仓，交付件开源）
跨仓复用但敏感/受控？       → T3
否则绑定具体项目？           → T4
否则                         → T2
```

禁止把所有仓内脚本塞入 tool repo、把私有适配放入公共仓、把项目特例硬编码为通用工具，或在公共 Flow 中引用本机绝对路径。

## 4. 执行规则

1. Flow 用 `write_scope` 声明计划写入范围；
2. ownership map 验证 Owner 与路径；
3. action/provider 返回结构化结果，版本/hash 进入 Lock/Evidence；
4. 跨仓修改走 Change Bundle 和独立 PR；
5. 新事实域、新仓或工具类别变化需同步 ADR、Manifest、ownership map 和本文。
