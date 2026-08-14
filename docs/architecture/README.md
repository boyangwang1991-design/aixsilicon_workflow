# AIXSILICON 架构文档

本目录只描述系统结构和长期边界。开发顺序与状态分别由 [`../roadmap.md`](../roadmap.md) 和 [`../progress.md`](../progress.md) 管理，不在架构文档中重复维护。

## 文档关系

```text
overview ──定义系统模型与不变量
   ├── repos ──定义仓库职责、当前依赖与写入边界
   ├── workflows ──定义 Flow、Action、Gate 和端到端链路
   └── target-design ──基于现状差距给出目标模型与迁移路径
```

| 文档 | 唯一职责 | 不包含 |
|---|---|---|
| [`overview.md`](overview.md) | 定位、责任链、L0～L5、核心对象和公共/私有边界 | 单仓任务、Flow 阶段明细 |
| [`repos.md`](repos.md) | 仓库 Owner、拥有/不拥有的事实、当前依赖和写入边界 | 路线图、重复的仓级 Plan |
| [`workflows.md`](workflows.md) | 执行模型、现有 Flow、IP/SoC 链路、Gate/Evidence | 仓库背景介绍、目标迁移细节 |
| [`target-design.md`](target-design.md) | 现状差距、显式 Profile、有类型依赖、Capability Preflight 和迁移顺序 | 当前进度和任务状态 |

## 阅读方式

- 初次了解：`overview → repos → workflows`；
- 审核优化方案：`overview → target-design → roadmap`；
- 判断改动归属：`repos → ownership-map.yaml → workflow/ownership.md`；
- 排查流程能力：`workflows → target-design §6 → progress`。

## 规范源

- 仓库清单和当前无类型依赖：[`manifests/default.yaml`](../../manifests/default.yaml)；
- 写入边界和 Schema Owner：[`ownership-map.yaml`](../../ownership-map.yaml)；
- 可执行流程定义：[`workflows/`](../../workflows)；
- 已接受/建议决策：[`../adr/README.md`](../adr/README.md)。
