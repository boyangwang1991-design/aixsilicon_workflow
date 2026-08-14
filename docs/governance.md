# 文档与规划治理

本文定义 `docs/` 的单一事实源、更新规则和历史材料退出条件。目标是让架构决策、执行规划和开发状态各有唯一落点，同时完整保留已有设计细节。

## 1. 文档分层

| 层级 | 权威材料 | 用途 | 是否维护状态 |
|---|---|---|---|
| 导航 | [`index.md`](index.md) | 唯一入口与阅读路径 | 否 |
| 架构 | [`architecture/`](architecture/README.md)、[`adr/`](adr/README.md) | 边界、依赖、责任和已批准决策 | 否 |
| 组合规划 | [`roadmap.md`](roadmap.md) | 跨仓目标、里程碑、依赖顺序和验收出口 | 是 |
| 组合进度 | [`progress.md`](progress.md) | 当前状态、风险、阻塞项和近期动作 | 是 |
| 仓级设计 | `docs/<repo>/README.md` | 单仓定位、边界、契约和验收 | 否 |
| 仓级交付 | `docs/<repo>/delivery.md` | 唯一活动里程碑、任务和证据 | 是 |
| Workflow 契约 | [`workflow/`](workflow/README.md) | Manifest、所有权、协作、发布和运行支持 | 仅 `plan/todo` 维护仓级任务 |
| 设计参考 | `docs/<repo>/design-reference.md`、[`reference/`](reference/README.md) | 完整历史细节、旧需求和评审依据 | 否 |
| 候选提案 | [`proposals/repositories/`](proposals/repositories/README.md) | 未建仓方案与激活门禁 | 否 |
| 决策历史 | `docs/adr/` | 已接受的关键架构决策 | 仅新增/废止，不改写历史 |
| 迁移审计 | [`MIGRATION.md`](MIGRATION.md) | 历史文件到新材料的逐项映射 | 迁移期间维护 |
| 审核发现 | [`findings.md`](findings.md) | 方案/实现差距、处置决策和关闭证据 | 是 |

旧 `docs/archived/` 已在完成 45/45 迁移、断链检查和人工批准后于 2026-08-13 删除。Git 历史承担原文追溯；活动材料不得重新建立对旧路径的依赖。

## 2. 单一事实源

- 仓库清单与依赖：`manifests/default.yaml`，文档只解释，不复制为可编辑事实。
- 写入边界与 Schema Owner：`ownership-map.yaml`。
- Flow 定义：`workflows/*.yaml`。
- 当前跨仓优先级与里程碑：`docs/roadmap.md`。
- 当前组合状态：`docs/progress.md`。
- 仓内任务状态：对应 `docs/<repo>/delivery.md`；Workflow 使用 `docs/workflow/delivery.md`。
- 审核发现及关闭判据：`docs/findings.md`；任务执行仍落在对应 `delivery.md`，不以 Finding 代替任务。
- 当前仓级设计：对应 `README.md`；完整历史细节在 `design-reference.md`，其中旧状态、日期和优先级不具有执行效力。
- Workflow 契约：`docs/workflow/`；完整旧需求与评审仅在 `docs/reference/` 追溯。

如果实现与文档不一致，现状判断以可执行配置和代码事实为依据；目标方案以已批准 ADR/活动方案为依据。差距先登记 Finding，再由对应任务关闭，禁止把目标描述成已实现事实。

## 3. 仓级材料规范

活动材料采用“设计与交付分离”，历史参考不参与状态：

| 文件 | 必须回答 | 禁止内容 |
|---|---|---|
| `README.md` | 定位、Owner/消费者、范围/非范围、输入输出、能力路径、验收 | 当前百分比、完成勾选、逐项开发日志 |
| `delivery.md` | 唯一任务 ID、优先级、里程碑、依赖、验收/证据、Owner 角色、状态 | 重复任务、整段历史计划、设计百科 |
| `design-reference.md` | 完整历史设计、清单、取舍依据和来源 | 当前状态权威声明、与 `delivery.md` 竞争的活动清单 |

任务状态统一使用 `planned / in-progress / blocked / done / deferred`。每个活动任务只能出现一次；大范围设想保留在设计参考，只有具备 Owner、依赖和出口时才进入 delivery。`done` 任务在证据稳定后移出活动台账，由 Git/PR/Evidence 追溯。

Workflow 的稳定设计已按主题拆为 Manifest/Ownership/Collaboration/Release 等契约，因此不复制一个总 `design-reference`；其 `README.md` 只做边界和导航，活动任务统一在 `delivery.md`。

## 4. 状态与更新规则

统一使用以下状态：

| 状态 | 含义 | 证据要求 |
|---|---|---|
| `planned` | 已进入路线图但尚未开始 | Owner、依赖和验收出口明确 |
| `in-progress` | 已有正在进行的实现 | 有分支/PR/运行记录之一 |
| `blocked` | 无法继续 | 记录阻塞原因、解除条件和 Owner |
| `done` | 已完成 | Gate 通过且有代码/测试/证据引用 |
| `deferred` | 明确延后 | 记录决策理由和重新评审点 |

每次涉及功能、接口、依赖或发布能力的变更，应同步：

1. 更新仓级 `delivery.md`；
2. 若影响跨仓里程碑，更新 `roadmap.md`；
3. 更新 `progress.md` 的状态、风险和证据；
4. 若改变长期边界或不可逆技术选择，新增 ADR；
5. 若改变 Manifest、Flow、Schema 或 Owner，同步其规范源并运行校验。

每个 Delivery 行至少包含：稳定 ID、优先级/工作包、任务、依赖、验收证据、Accountable 角色和状态。任务进入 `in-progress` 前，还必须在组合看板或外部任务系统补齐具体负责人、目标日期/复审点和首个证据动作。

## 5. 规划评审门禁

新规划进入 `roadmap.md` 前必须回答：

- Owner 仓是否唯一，是否违反 `ownership-map.yaml`；
- 输入/输出 Schema 的 Owner 是否明确；
- 上下游依赖是否形成 DAG，是否需要 Manifest 变更；
- Tool、Workflow、Skill 和 Asset 的职责是否混淆；
- 最小可验证闭环是什么，Gate 和 Evidence 是什么；
- 是否要求私有 Skill/EDA/PDK；公共流程能否在缺少私域能力时明确降级；
- 是否存在重复生成、重复存储或双 SSOT；
- 发布、兼容性和迁移策略是否明确。
- 是否具备正向、负向、失败恢复和可重建验证；
- 任务是否映射到唯一 Finding/里程碑，是否存在候选仓被提前当作既定依赖。

## 6. 历史材料删除门禁（已完成）

本次删除已按以下条件执行；未来进行类似清理时继续沿用：

- [`MIGRATION.md`](MIGRATION.md) 覆盖 45/45 个历史文件；
- 每个历史长篇设计文件已有当前 `design-reference.md` 或等价正文；
- 活动文档和根级说明中不存在指向 `docs/archived/` 的链接；
- Markdown 本地链接检查通过；
- 项目等价 lint/test/schema/guard 与 Markdown 链接检查通过；统一入口或 pre-commit 若受平台/网络阻塞，必须在 `progress.md` 明确记录；
- 评审人确认旧状态与旧计划没有被误当作当前承诺；
- 删除必须使用受 Git 跟踪的明确路径，保证可恢复。

## 7. 图示与生成图片治理

- 可维护关系图优先使用 Mermaid；需要快速建立整体心智模型时可增加生成式信息图；
- 图片统一放入 [`assets/`](assets/README.md)，记录用途、生成方式、提示主题和尺寸；
- 每张图片必须有 alt 文本及相邻解释，不能把精确字段或唯一规则只写在图片里；
- 图片只是辅助材料，发生冲突时以正文、ADR、Manifest、Flow、Schema 和 ownership map 为准；
- 生成图片必须人工检查标签、箭头、边界和是否暗示了错误的完成状态。
