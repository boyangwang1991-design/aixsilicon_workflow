# 工具归属四类判定（Tool Placement）

> 日期：2026-08-13
> 回答：是否“所有工具都该进 tool_repo”？**不是**。按复用范围、公开性、成熟度、责任域分四类归属。
> 配套：ADR-0006（工具边界）、[`docs/schema-ownership.md`](schema-ownership.md)、`ownership-map.yaml` tool_boundary。

## 判定维度

| 维度 | 关键问题 |
|---|---|
| 复用范围 | 跨仓复用，还是仅单仓/单项目自维护？ |
| 公开性 | 可开源，还是含商业/Foundry/PDK/内部敏感信息？ |
| 成熟度 | 产品级确定性工具，还是仓库本地脚手架脚本？ |
| 责任域 | 是“通用能力”，还是“某仓/某项目的事实与规则”？ |

## 四类归属

| 类 | 归属 | 例子 | 原则 |
|---|---|---|---|
| **T1 跨仓公共确定性工具** | `aixsilicon_tool_repo`（开源） | `aix-hwif-gen` / `aix-reg-tool` / `aix-core-tool` / `aix-schema` | 输入/输出有稳定 Schema，跨仓复用，通过 `aixsilicon.commands` 插件暴露；独立 SemVer + 版本锁 |
| **T2 单仓自维护脚本** | **留在对应资产仓 `tools/`** | dv-common `run_checks.sh` / schema_check、hwif 测试脚本、CI 辅助 | 仓库本地脚手架（测试/CI/文档/本地检查），非跨仓契约；不搬进 tool_repo |
| **T3 私有/受控工具与适配** | **独立私有 repo（overlay）** | 商业 EDA Adapter、PDK/Memory 映射、内部 Runner/License、内部报告 Parser、客户专用 Packager | 实现同一公开 Plugin API 与 Result Schema，但不开源；敏感数据与实现隔离；公共 flow 通过 capability 声明，不硬编码私有路径 |
| **T4 项目专用脚本** | **留在项目仓** | `chip_<project>_soc_repo` 的 Waiver/胶水/迁移脚本、具体项目规则 | 绑定项目事实；高复用后按 T1/T3 流程提炼 |

## 判定流程

```text
是跨仓复用且可开源且契约稳定？
   ├─ 是 → T1 tool_repo
   └─ 否
       是跨仓复用但受控/敏感（EDA/PDK/内部）？
          ├─ 是 → T3 私有 overlay repo
          └─ 否
              是项目专用？
                 ├─ 是 → T4 项目仓
                 └─ 否 → T2 单仓自维护脚本（留在资产仓 tools/）
```

## 反模式

- 把 T2（单仓自维护脚本）全塞进 tool_repo → 仓库失去本地脚手架，tool_repo 变成垃圾场；
- 把 T3（商业/PDK 适配）放进开源 tool_repo → 泄密；
- 把 T4（项目专用）提炼进公共 tool_repo 而不通用化 → 项目特例硬编码进通用工具；
- 在公共 flow 中硬编码私有 T3 脚本绝对路径 → 破坏可复现与开源边界。

## 落地

- 迁移路径沿用 ADR-0006：T1 由各仓 `tools/` 中“产品级工具”分阶段迁入 tool_repo（阶段 A 双入口 → B `aix tool` → C deprecated）；
- T3 仓库在 `docs/schema-ownership.md` 仓库注册表登记（如 `aixsilicon_tool_repo-private` / `<org>_private_overlay_repo`）；
- `ownership-map.yaml` `tool_boundary` 引用本文档。
