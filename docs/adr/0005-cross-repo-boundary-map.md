# ADR-0005：跨仓边界映射（幽灵仓库收敛）

- 状态：接受
- 日期：2026-08-13

## 背景

部分资产仓 plan 引用了本体系未建设或已否决的仓库，导致边界认知分裂：

- [`aixsilicon_dv_common/plan.md`](../../repos/aixsilicon_dv_common/plan.md:120) 与 [`aixsilicon_vip_repo/plan.md`](../../repos/aixsilicon_vip_repo/plan.md:57) 引用 `eda-flow`、`eda-rules`、`hw-models`；
- [`aixsilicon_cbb_repo/cbb_repo_plan.md`](../../repos/aixsilicon_cbb_repo/cbb_repo_plan.md:449) 引用独立 `cbb-catalog`、`cbb-tech-<node>`。

而 workflow [`plan.md`](../../plan.md:239) §4.7 已明确不单独建设 `eda_flow_repo` / `eda_rule_repo`，并采用单一 `aixsilicon_catalog_repo` 与 `aixsilicon_techlib_repo`。

## 决策

建立权威映射，修订引用方 plan：

| 幽灵仓引用 | 归属/落点 | 说明 |
|---|---|---|
| `eda-flow` | `aixsilicon_workflow`（DAG/Gate/Evidence）＋ `aixsilicon_tool_repo`（Result Adapter/Report 归一化） | 总编排不重复建第二套调度器 |
| `eda-rules` | `aixsilicon_workflow` `policies/` | 组织 Gate/waiver 规则 |
| `hw-models` | `aixsilicon_techlib_repo` / `aixsilicon_model_repo`（P1/P2，按需建）；与 IP 强绑定的参考模型随 IP 仓版本 | 不新建独立空仓 |
| `cbb-catalog` | `aixsilicon_catalog_repo` | 单一 Unified Catalog |
| `cbb-tech-<node>` | 私有 overlay 仓 / 待建 `aixsilicon_techlib_repo` | Foundry/PDK/Macro 适配，不入公共仓 |

落地动作：

1. 本 ADR 作为权威边界；
2. 修订 dv-common / vip / cbb 三个 plan 的对应引用章节；
3. [`policies/dependency-policy.yaml`](../../policies/dependency-policy.yaml) 增加 `dep-no-phantom-repo` 规则：新 plan/文档不得引用未注册仓库；
4. 维护 `docs/` 下的“仓库注册表”（见 `docs/schema-ownership.md` 附注），任何新仓名需先在 workflow 侧登记。

## 备选方案

- 为每个引用建仓：制造多个空仓与重复 CI，违背“资产跟随 Owner、机制集中”的原则；
- 静默忽略引用：边界认知继续分裂，不采用。

## 结果

- 正向：仓库边界单一事实源化，plan 与实现一致；
- 负向：需要同步修订三份外部 plan（由 P4 文档同步项完成）；
- 权衡：登记门槛避免“口头建仓”，同时保留 techlib/model 按需扩容通道。
