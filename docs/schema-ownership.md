# Schema 所有权注册表

> 每个事实域的 Schema 有且只有一个 Owner 仓，避免多仓各自维护同义 Schema 造成漂移。
> Owner 仓负责演进与版本化；消费者通过 `aix tool schema`（见 ADR-0004）按 `$id` 解析校验。

## 所有权表

| 事实域 | Schema 文件示例 | Owner 仓 |
|---|---|---|
| 工作区 Manifest / Lockfile | `workspace-manifest.schema.json` / `workspace-lock.schema.json` | `aixsilicon_workflow`（`schemas/`） |
| Flow / Change Bundle | `flow.schema.json` / `change-bundle.schema.json` | `aixsilicon_workflow` |
| Tool Profile / Evidence | `tool-profile.schema.json` / `evidence-index.schema.json` | `aixsilicon_workflow` |
| 硬件接口 Contract / Profile / Binding / Compatibility | `interface_contract.schema.yaml` 等 | `aixsilicon_hwif_repo`（`schema/`） |
| CBB 元数据 / 参数 / 结果 | `cbb.yaml`、`result` 相关 | `aixsilicon_cbb_repo` |
| VIP 元数据 / Testplan / Coverage / Release Manifest | `vip_metadata.schema.yaml` 等 | `aixsilicon_vip_repo` |
| DV 组件 / Run Manifest / Test Result / Failure | `run_manifest.schema.yaml` 等 | `aixsilicon_dv_common` |
| SoC 集成配置（实例/地址/中断/CRG/Power/连接） | SoC 配置 Schema | `aixsilicon_soc_integration` |
| Catalog 资产条目 | `catalog-asset.schema.json` | `aixsilicon_catalog_repo` |
| Tool 自身 Result / Diagnostic / Artifact / 插件 Manifest | `aix.tool-result/v1` 等 | `aixsilicon_tool_repo` |
| Skill Metadata / Context Pack / Skill Result / Eval | `context-pack.schema.yaml` 等 | `aixsilicon_skill_repo`（私有） |

## 仓库注册表（附注）

> 任何新仓库名必须先在此登记，杜绝“口头建仓”（见 ADR-0005）。

| 仓库 | 类型 | 状态 |
|---|---|---|
| `aixsilicon_workflow` | workflow | 已建 |
| `aixsilicon_hwif_repo` | hw-interface | 已建 |
| `aixsilicon_cbb_repo` | cbb | 已建 |
| `aixsilicon_ip_repo` | ip | 已建 |
| `aixsilicon_dv_common` | dv-common | 已建 |
| `aixsilicon_vip_repo` | vip | 已建 |
| `aixsilicon_tool_repo` | tool | 已建（内容待填充） |
| `aixsilicon_catalog_repo` | catalog | 已建（内容待填充） |
| `aixsilicon_soc_integration` | soc-integration | 已建（内容待填充） |
| `aixsilicon_skill_repo` | skill（私有） | 已建（内容待填充） |
| `aixsilicon_chipknowledge` | other（知识库） | 已建（README 初始提交） |
| `aixsilicon_techlib_repo` | techlib | 待建（P1） |
| `aixsilicon_model_repo` | model | 按需（P1/P2） |
| `aixsilicon_sw_repo` | software | 待建（P1） |
| `aixsilicon_reference_soc_repo` | reference-soc | 待建（P2） |

## 原则

- 同一事实域禁止在两个仓各维护一份 Schema；发现重复即向 Owner 仓收敛；
- 跨域依赖（如 workflow 校验 HWIF Contract）通过 `aix tool schema --schema <$id>` 引用 Owner 仓发布的 Schema，不复制文件；
- Schema 版本按 ADR-0002 演进，Breaking 变更升 major 并给出迁移路径。
