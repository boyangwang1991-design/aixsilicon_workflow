# AIXSILICON 已配置 Git 仓库清单

以下仓库已配置并接入 AIXSILICON 平台（组织：`boyangwang1991-design`），并已通过 `aix wf sync` 纳入工作区。

## 资产/平台仓库（开源基线）

| 逻辑 ID | 仓库 | URL | 状态 |
|---|---|---|---|
| workflow | `aixsilicon_workflow` | https://github.com/boyangwang1991-design/aixsilicon_workflow | 已构建 |
| hwif | `aixsilicon_hwif_repo` | https://github.com/boyangwang1991-design/aixsilicon_hwif_repo | 已构建 |
| cbb | `aixsilicon_cbb_repo` | https://github.com/boyangwang1991-design/aixsilicon_cbb_repo | 已构建 |
| ip | `aixsilicon_ip_repo` | https://github.com/boyangwang1991-design/aixsilicon_ip_repo | 已构建 |
| dv-common | `aixsilicon_dv_common` | https://github.com/boyangwang1991-design/aixsilicon_dv_common | 已构建 |
| vip | `aixsilicon_vip_repo` | https://github.com/boyangwang1991-design/aixsilicon_vip_repo | 已构建 |
| catalog | `aixsilicon_catalog_repo` | https://github.com/boyangwang1991-design/aixsilicon_catalog_repo | 已构建（README 初始提交） |
| tools | `aixsilicon_tool_repo` | https://github.com/boyangwang1991-design/aixsilicon_tool_repo | 已构建（README 初始提交） |
| soc-integration | `aixsilicon_soc_integration` | https://github.com/boyangwang1991-design/aixsilicon_soc_integration | 已构建（README 初始提交） |
| skills | `aixsilicon_skill_repo` | https://github.com/boyangwang1991-design/aixsilicon_skill_repo | 已构建（README 初始提交，私有） |
| knowledge | `aixsilicon_chipknowledge` | https://github.com/boyangwang1991-design/aixsilicon_chipknowledge | 已接入（仓库已建，内容待填充） |

> 与 [`manifests/default.yaml`](manifests/default.yaml) 保持一致。`aix wf sync` 已克隆全部 10 仓，`aix wf status` 显示均为 `main / clean / sync`；`.aix/local.lock.yaml` 已记录各仓真实 SHA。
