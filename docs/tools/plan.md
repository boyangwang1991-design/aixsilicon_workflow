# tools — AIXSILICON Tool Repository 建设规划

> 客观事实基线：2026-08-13（P0 五包已实现并接入 `aix tool`）。原文细节见 [`../archived/architecture/repo-plans/tools.md`](../archived/architecture/repo-plans/tools.md)。

## 1. 定位与边界

**定位**：跨仓公共**确定性执行能力**（生成/检查/转换/打包），经 `aixsilicon.commands` 插件暴露为 `aix tool`；是 T1 工具的核心载体。

| 归属（T1 公共工具） | 不归本仓 |
|---|---|
| 确定性生成/检查/转换/打包工具 | workflow 的 Gate 编排 |
| `aixsilicon.commands` 插件 | Skill 的方法判断 |
| 工具版本锁（workspace-lock `tools:`） | 资产仓事实源 |
| | T2 单仓脚本（留资产仓）/ T3 私有适配（私有 overlay）/ T4 项目脚本（项目仓） |

## 2. 现状（客观）

- **P0 五包已实现并接入 `aix tool` 实跑**：
  - `aix-tool-core`：Result/Diagnostic/Artifact 契约、分段退出码、插件入口；
  - `aix-schema`：validate/lint/diff（`migrate` 骨架待补）；
  - `aix-hwif-gen`：Contract→SV package/interface/flat 视图 + `--check-only` + `hac-generate`；
  - `aix-reg-tool`：PeakRDL 封装 validate/generate（RTL/RAL/Header/Doc）+ 一致性 check；
  - `aix-core-tool`：core list/lint/init/graph；
- `make check` 全绿（30 用例）；五包全部注册进 `aixsilicon.commands`；
- **缺口**：`aix wf run` 的 `tool.*` 阶段转真实 provider；workspace-lock `tools:` 段；`reference/` 适配测试。

## 3. 依赖与角色

- **依赖**：无；
- **被依赖**：soc-integration（`depends_on` 含 tools），及 IP/CBB/SoC 主线的 `tool.*` action；
- **IP 主线角色**：`tool.reg-gen` / `tool.schema` / `tool.core-tool` 执行确定性生成；
- **SoC 主线角色**：`tool.address-gen/irq-gen/crg-gen/top-gen/sw-gen/connect-check` 派生 SoC 视图。

## 4. 契约

- **CLI**：`aix` 唯一入口，本仓注册 `tool` 插件（Entry Point 组 `aixsilicon.commands`）；
- **退出码分段**：0 成功 / 10 使用错误 / 20 输入或契约失败 / 30 环境依赖缺失（`OPTIONAL_UNAVAILABLE`）/ 40 工具内部错误 / 50 输出校验失败 / 60 安全拒绝；
- **成熟度**：experimental/preview/qualified/production/deprecated/retired；
- **可复现**：同输入 + 同版本 → 语义一致输出（确定性）；写操作支持 `--dry-run/--check` 且路径白名单。

## 5. 建设路线（客观）

| 阶段 | 状态 |
|---|---|
| S0 aix-tool-core（底座） | ✅ 完成 |
| S1 aix-schema | ✅ 完成（migrate 骨架待补） |
| S2 aix-hwif-gen | ✅ 完成 |
| S3 aix-reg-tool | ✅ 完成 |
| S4 aix-core-tool | ✅ 完成 |
| S5 集成（插件/真实 provider/版本锁/CI） | 🔶 五包已注册，`aix wf run` 转真实 provider 待做 |
| 扩展（P1） | aix-project-init / aix-param-matrix / aix-dv-gen / aix-ppa-bench / aix-socgen / aix-connect-check 等 |

## 6. 关联

- Todo：[`todo.md`](todo.md)；原文：[`../archived/architecture/repo-plans/tools.md`](../archived/architecture/repo-plans/tools.md)
- 全局：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
