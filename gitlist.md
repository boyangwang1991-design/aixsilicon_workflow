# AIXSILICON 已配置 Git 仓库清单

以下仓库已配置并接入 AIXSILICON 平台（组织：`boyangwang1991-design`）。

## 资产/平台仓库（开源基线）

| 逻辑 ID | 仓库 | URL | 状态 |
|---|---|---|---|
| workflow | `aixsilicon_workflow` | https://github.com/boyangwang1991-design/aixsilicon_workflow | 已构建 |
| hwif | `aixsilicon_hwif_repo` | https://github.com/boyangwang1991-design/aixsilicon_hwif_repo | 已构建 |
| cbb | `aixsilicon_cbb_repo` | https://github.com/boyangwang1991-design/aixsilicon_cbb_repo | 已构建 |
| ip | `aixsilicon_ip_repo` | https://github.com/boyangwang1991-design/aixsilicon_ip_repo | 已构建 |
| dv-common | `aixsilicon_dv_common` | https://github.com/boyangwang1991-design/aixsilicon_dv_common | 已构建 |
| vip | `aixsilicon_vip_repo` | https://github.com/boyangwang1991-design/aixsilicon_vip_repo | 已构建 |
| catalog | `aixsilicon_catalog_repo` | https://github.com/boyangwang1991-design/aixsilicon_catalog_repo | 已创建（空，待初始提交） |
| tools | `aixsilicon_tool_repo` | https://github.com/boyangwang1991-design/aixsilicon_tool_repo | 已创建（空，待初始提交） |
| skills | `aixsilicon_skill_repo` | https://github.com/boyangwang1991-design/aixsilicon_skill_repo | 已创建（空，待初始提交） |

## 计划新增（P0，尚未创建）

| 逻辑 ID | 仓库 | 状态 |
|---|---|---|
| soc-integration | `aixsilicon_soc_integration_repo` | 待创建 |

> 与 [`manifests/default.yaml`](manifests/default.yaml) 保持一致。空仓库在 `main` 上有初始提交后，`aix wf sync` 即可纳入工作区；`aix wf sync` 对空仓库会给出明确提示。
