# 跨仓成熟度与质量 Gate 统一映射

> 各资产仓使用各自的内部成熟度/质量词汇。Catalog 对外只暴露**统一外部尺度**，
> 各仓内部子状态通过下表映射，避免在 Catalog、兼容矩阵与 Release 判定中出现多重标准。

## 统一外部尺度

| 外部成熟度 | 含义 | Catalog/项目可用性 |
|---|---|---|
| `draft` | 需求/语义讨论中，或代码为实验 | 禁止正式项目依赖 |
| `qualified` | 完成规定质量 Gate，契约冻结 | 允许正式项目使用 |
| `proven` | 至少两个真实项目/场景验证 | Catalog 默认推荐 |
| `deprecated` | 已有替代，进入迁移窗口 | 禁止新项目使用 |

## 各仓内部词汇 → 外部尺度

| 仓 | 内部词汇 | 映射 |
|---|---|---|
| workflow [`plan.md`](../../plan.md:1550) §24 | `G0`–`G7` | 跨仓质量 Gate 顺序（不直接等同成熟度；全部通过且人工批准 → `qualified`） |
| hwif [`plan.md`](../../repos/aixsilicon_hwif_repo/plan.md:995) §17.1 | `draft / reviewed / qualified / proven / deprecated` | 一一对应（`reviewed` → `qualified` 前身） |
| dv-common [`plan.md`](../../repos/aixsilicon_dv_common/plan.md:836) §15.1 | `Draft / Experimental / Candidate / Qualified / Deprecated / Retired` | `Candidate`→`qualified`；`Retired`→`deprecated` |
| cbb [`cbb_repo_plan.md`](../../repos/aixsilicon_cbb_repo/cbb_repo_plan.md:359) §7.2 | `E0 Concept…E5 Proven` | `E0/E1`→`draft`；`E2/E3`→`qualified`；`E4/E5`→`proven` |
| vip [`plan.md`](../../repos/aixsilicon_vip_repo/plan.md:508) §10.2 | `V0 Prototype…V4 Proven` | `V0`→`draft`；`V1–V3`→`qualified`；`V4`→`proven` |
| tool [`tool_repo_plan.md`](../../repos/aixsilicon_tool_repo/tool_repo_plan.md:1215) §29 | `experimental / preview / qualified / production / deprecated / retired` | 一一对应 |
| skill [`skill_repo_plan.md`](../../repos/aixsilicon_skill_repo/skill_repo_plan.md:863) §17.3 | `experimental / pilot / stable / deprecated / retired` | 一一对应 |

## 使用规则

- **Catalog 只记录外部尺度**，各仓内部词汇保留在各自 metadata；
- 成熟度升级必须携带 Evidence 引用（Release Manifest / 质量报告 / 项目复用记录）；
- 不允许无证据地从 `draft` 直接声明 `qualified`；`proven` 必须有至少两个独立项目/场景记录；
- workflow 的 `G0–G7` 是跨仓执行顺序，不替换上述成熟度；两者通过 Evidence 关联。
