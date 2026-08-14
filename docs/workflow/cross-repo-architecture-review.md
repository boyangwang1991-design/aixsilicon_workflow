# AIXSILICON 跨仓整体架构评审

> 日期：2026-08-13
> 范围：`aixsilicon_workflow` 与 9 个资产仓的 plan 整体合理性，检查**重复构建**、**架构不合理**、**引用/被引用不清晰**。
> 依据：各仓 plan/README、[`docs/schema-ownership.md`](schema-ownership.md)、[`docs/adr/0003-0006`](../adr/README.md)。

---

## 1. 重复构建（Duplicate Construction）

| # | 重复点 | 涉及仓 | 判定 | 处置 |
|---|---|---|---|---|
| R1 | 确定性工具重复：hwif `tools/` 6 件 vs tool_repo `aix-hwif-gen/aix-reg-tool/aix-core-tool` | hwif / tool / workflow | **重复** | ADR-0006 分阶段迁移；hwif `tools/` 降级为自维护脚本 |
| R2 | CLI 双入口风险：workflow `aix` vs tool `aix tool` | workflow / tool | **重复（已治理）** | ADR-0004：`aix` 单入口 + 插件组 `aixsilicon.commands` |
| R3 | Schema 重复维护：各仓各定义同域 Schema | workflow / hwif / dv-common / tool / catalog | **重复（已治理）** | [`docs/schema-ownership.md`](schema-ownership.md) 单一 Owner |
| R4 | 发布/打包逻辑：`ipkg publish`（IP）vs `aix release`（workflow）vs hwif `package_release` | ip / workflow / hwif | 职责重叠 | 明确：ipkg=IP 仓源码级发布；workflow=跨仓 Gate/协调/Catalog；hwif package_release=接口仓发布；三者通过 manifest/tag 对齐，不重复实现调度 |
| R5 | “影响分析”名称重复：hwif `impact_analysis`（接口→消费者）vs workflow `impact.py`（仓库→下游） | hwif / workflow | 不重复但易混 | 澄清语义：前者接口语义影响，后者仓库/依赖图影响；在 plan 中显式命名区分 |
| R6 | VIP `common/` 与 dv-common 组件重叠（transaction_policy/fault_injection/coverage_utils/report_adapter） | vip / dv-common | **潜在重复** | 划界：协议/事务相关 → VIP；协议无关机制 → DV-Common；VIP `common/` 仅保留协议相关公共 |
| R7 | Core 生成重复：ipkg 生成 IP `.core` vs tool_repo `aix-core-tool` | ip / tool | 潜在重复 | ipkg 复用 `aix-core-tool` 的生成/lint；不另造第二套 Core 逻辑 |

## 2. 架构不合理（Architecture Issues）

| # | 问题 | 涉及仓 | 处置 |
|---|---|---|---|
| A1 | **IP 仓“不可变版本目录”模型与开发态矛盾**：ip_repo 用 `ips/<vendor>/<ip>/<version>/` 不可变版本 + ipkg，而 workflow 开发工作流假设 IP 仓可编辑源码 | ip / workflow | 澄清双态：开发源码在 feature 分支可编辑；发布时 `ipkg stage` 冻结为版本目录；`registry.yaml` 只索引已发布版本。workflow dev 模式指向分支，release 模式指向 tag/SHA |
| A2 | **vendored `reference/` 第三方 core 污染 FuseSoC**：hwif/vip/ip 仓内 `reference/`（OpenTitan/PULP/wb2axip）以 `.core` 形式被 fusesoc 递归发现，产生 CAPI1 错误、解析警告与跨仓 VLNV 静默遮蔽 | hwif / vip / ip / workflow | workflow 索引已排除 `reference/`；各仓需把 reference 视为只读参考、从 `fusesoc_roots` 排除或移出可发现位置；不将 reference core 作为正式资产发布 |
| A3 | **ghost repo 引用**：dv_common/vip 引用 `eda-flow`/`eda-rules`/`hw-models`；cbb 引用 `cbb-catalog`/`cbb-tech-<node>` | dv-common / vip / cbb | ADR-0005 映射：flow→workflow+tool、rules→workflow policies、models→techlib/model、cbb-catalog→catalog_repo、cbb-tech→私有 overlay/techlib；更新对应 plan 引用章节 |
| A4 | techlib 引用不统一：hwif 用 `hw-techlib`，cbb 用 `cbb-tech`，workflow 用 `aixsilicon_techlib_repo` | hwif / cbb / workflow | 统一为 `aixsilicon_techlib_repo`（P1 待建）；公共仓只定义抽象接口/wrapper，Foundry/Macro 适配入私有 overlay |

## 3. 引用 / 被引用不清晰（Reference Clarity）

| # | 不清晰点 | 处置 |
|---|---|---|
| C1 | 各仓 `tools/` 的定位（自维护脚本 vs 产品级工具） | 统一：`tools/` = 自维护（测试/CI/文档/本地检查）；产品级工具 → tool_repo（ADR-0006） |
| C2 | 各仓 `reference/`（vendored 第三方）的定位 | 统一：只读参考/对拍，不发布、不被 fusesoc 正式发现、不进入 Catalog |
| C3 | 统一 VLNV vendor `aixsilicon:*` 在各仓 plan 中的一致性 | ADR-0003；各仓 plan 中的 `aix:*`/`company:*`/`boyangwang1991-design:*` 示例统一改写 |
| C4 | Schema 引用方向：workflow 校验 HWIF/CBB 等跨仓 Schema 的方式 | 通过 `aix tool schema --schema <$id>` 引用 Owner 仓 Schema，不复制文件（schema-ownership） |
| C5 | 依赖方向：IP 实现依赖 HWIF/CBB；IP 验证依赖 VIP/DV-Common；dv-common 不得反向依赖 VIP/IP | 已在 dependency-policy；各仓 plan 中重申 |

---

## 4. 每仓修订动作

| 仓 | 需更新的 plan/todo | 核心修订 |
|---|---|---|
| workflow | [`plan.md`](plan.md)（§36）、[`todo.md`](todo.md) | 记录本评审结论；补充 R4/R5 边界、A1/A2 治理 |
| hwif | [`plan.md`](../../repos/aixsilicon_hwif_repo/plan.md)、[`todo.md`](../../repos/aixsilicon_hwif_repo/todo.md) | 工具边界（R1）、影响分析语义（R5）、package_release 与 workflow release 边界（R4）、reference/ 治理（A2）、techlib 统一（A4）、VLNV 迁移（C3） |
| dv-common | [`plan.md`](../../repos/aixsilicon_dv_common/plan.md)、[`TODO.md`](../../repos/aixsilicon_dv_common/TODO.md) | 修正 ghost repo 引用（A3）、与 VIP common 划界（R6）、Result schema 对齐 tool_repo（C4） |
| vip | [`plan.md`](../../repos/aixsilicon_vip_repo/plan.md) | 修正 ghost repo 引用（A3）、common 边界（R6）、reference/ 治理（A2）、VLNV 统一（C3） |
| cbb | [`cbb_repo_plan.md`](../../repos/aixsilicon_cbb_repo/cbb_repo_plan.md) | cbb-catalog/tech 映射（A3/A4）、VLNV `aixsilicon:cbb`（C3）、验证依赖方向（C5） |
| ip | [`plan.md`](../../repos/aixsilicon_ip_repo/plan.md) | 双态模型澄清（A1）、ipkg 复用 aix-core-tool（R7）、reference/ 治理（A2） |
| tool | [`tool_repo_plan.md`](../../repos/aixsilicon_tool_repo/tool_repo_plan.md) | 插件组名统一 `aixsilicon.commands`、单入口 `aix`（R2）、工具边界总结（R1/R7） |
| catalog | [`README.md`](../../repos/aixsilicon_catalog_repo/README.md) | 明确“只索引发布资产、与 Manifest 不重复”（C 类），并指向 schema-ownership |
| soc-integration | [`README.md`](../../repos/aixsilicon_soc_integration/README.md) | 明确 Schema 归本仓、生成实现归 tool_repo（C4）、techlib 引用统一（A4） |

---

## 5. 结论

- 架构总体合理：分层（Workflow 控制面 / Tool 确定性执行 / 资产仓事实源 / Catalog 发布 / Skill 增强）清晰；
- 主要风险是**工具与发布逻辑的重复**（R1/R4/R7）与**vendored reference 污染**（A2），均已给出处置并进入各仓 plan/todo；
- 引用不清晰集中在 ghost repo 与 techlib 命名，已由 ADR-0003/0005 与本文档统一。
