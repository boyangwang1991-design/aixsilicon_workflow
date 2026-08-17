# Repo 方案与交付索引

本文是现有仓和候选仓的统一入口。现有仓的 `README.md` 是仓级设计契约，`delivery.md` 是任务定义与验收清单，`design-reference.md` 只保存历史细节；全部任务状态统一在 [`todo.md`](todo.md) 维护。

## 1. 现有仓覆盖矩阵

| 仓 | Owner | 设计契约 | 活动交付 | 历史细节 | 近期出口 |
|---|---|---|---|---|---|
| hwif | hw-platform | [`hwif/README.md`](hwif/README.md) | [`hwif/repo-architecture.md`](hwif/repo-architecture.md) | [`hwif/skill.md`](hwif/skill.md) | APB 契约与消费者联验（task 定义见 `../todo.md`） |
| cbb | hw-platform | [`cbb/README.md`](cbb/README.md) | [`cbb/delivery.md`](cbb/delivery.md) | [`cbb/design-reference.md`](cbb/design-reference.md) | 3 个参数/PPA 示范闭环 |
| ip | ip-platform | [`ip/README.md`](ip/README.md) | [`ip/delivery.md`](ip/delivery.md) | [`ip/design-reference.md`](ip/design-reference.md) | APB G0～G6 + Release G7/Catalog |
| dv-common | dv-platform | [`dv-common/README.md`](dv-common/README.md) | [`dv-common/delivery.md`](dv-common/delivery.md) | [`dv-common/design-reference.md`](dv-common/design-reference.md) | RAL/CSR/Result 公共底座 |
| vip | dv-platform | [`vip/README.md`](vip/README.md) | [`vip/delivery.md`](vip/delivery.md) | [`vip/design-reference.md`](vip/design-reference.md) | APB VIP V3 Qualified |
| tools（私有） | engineering-platform | [`tools/README.md`](tools/README.md) | [`tools/delivery.md`](tools/delivery.md) | [`tools/design-reference.md`](tools/design-reference.md) | provider/preflight/APB 实跑 |
| catalog | release-platform | [`catalog/README.md`](catalog/README.md) | [`catalog/delivery.md`](catalog/delivery.md) | [`catalog/design-reference.md`](catalog/design-reference.md) | 发布索引与 Catalog PR |
| soc-integration | soc-platform | [`soc-integration/README.md`](soc-integration/README.md) | [`soc-integration/delivery.md`](soc-integration/delivery.md) | [`soc-integration/design-reference.md`](soc-integration/design-reference.md) | 最小 Golden/boot smoke |
| skills（私有） | ai-engineering | [`skills/README.md`](skills/README.md) | [`skills/delivery.md`](skills/delivery.md) | [`skills/design-reference.md`](skills/design-reference.md) | APB Author/Verifier Eval |
| knowledge | engineering-platform | [`knowledge/README.md`](knowledge/README.md) | [`knowledge/delivery.md`](knowledge/delivery.md) | [`knowledge/design-reference.md`](knowledge/design-reference.md) | APB 知识路径与检索 |

Workflow 控制面入口为 [`workflow/README.md`](workflow/README.md)，任务定义与验收清单为 [`workflow/delivery.md`](workflow/delivery.md)，状态统一见 [`todo.md`](todo.md)。

## 2. 跨仓方案完整性

| 能力链 | 事实 Owner | 确定性能力 | 验证供给 | 控制/发布 | 当前缺口 |
|---|---|---|---|---|---|
| 接口契约 | hwif | tools/hwif provider | vip + 消费者编译 | workflow + catalog | provider/消费者联验 |
| 寄存器 IP | ip/SystemRDL | tools/reg/core | dv-common + APB vip | workflow + catalog | 固定 Lock 的 G0～G6 与 Release G7 |
| CBB/PPA | cbb | tools/param/PPA | dv-common + 属性/随机 | workflow + catalog | 专用 Flow 与 3 个示范切片 |
| SoC 集成 | 项目仓；通用规则 soc-integration | tools/socgen/connect | dv-common + vip | workflow + catalog | Schema/Golden/boot smoke |
| AI/知识辅助 | skills/knowledge | 只调用已授权 tools | 独立 Verifier/Eval | 不判 Gate | 契约/Eval 与确定性流程对齐 |

## 3. 候选仓

候选仓只做方案评审，不代表已建仓、已排期或已加入依赖：[`proposals/repositories/README.md`](proposals/repositories/README.md)。达到真实消费者、独立生命周期、唯一 Owner/Schema、首个垂直切片与 CI 条件后，必须经 ADR 才能激活。
