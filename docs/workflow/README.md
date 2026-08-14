# Workflow 控制面设计契约

Workflow 是 Manifest 驱动的多仓工作区控制面，负责 Workspace、Flow、Gate、Evidence、Change Bundle 和发布协调；不保存资产源码，不实现领域算法，不绕过各仓 Review/Release 或人工批准。

## 能力边界

| 能力域 | 负责 | 完成出口 |
|---|---|---|
| Workspace | Manifest/Profile/Lock/Override、依赖闭包、init/sync/status/doctor | exact Profile、typed dependency、固定 SHA、跨平台可重建 |
| Flow | DAG、precondition、Action/Provider 调度、失败传播、write scope | preflight 全覆盖；required 能力 fail-closed |
| Evidence/Gate | Run Manifest、Evidence Index、G0～G7 判定链 | repo/provider/tool/env/hash/seed 可追溯；资格与发布分离 |
| Collaboration | Change Bundle、影响分析、PR HEAD 联验、合入顺序 | 多仓各自 Review/merge，联合结果绑定精确 SHA |
| Release | candidate、人工批准、Tag/Release、Catalog diff/PR | clean/locked/no-override、幂等、失败恢复 |

## 文档地图

| 材料 | 唯一职责 |
|---|---|
| [`delivery.md`](delivery.md) | Workflow 稳定任务定义、依赖和验收条件；状态见 [`../todo.md`](../todo.md) |
| [`manifest.md`](manifest.md) | Manifest、Profile、Lock 与 Override |
| [`ownership.md`](ownership.md) | Schema/仓库/工具的唯一归属和写入边界 |
| [`collaboration.md`](collaboration.md) | Change Bundle、影响分析和跨仓 CI |
| [`release.md`](release.md) | Gate、Evidence、成熟度、Baseline 与 Release |
| [`troubleshooting.md`](troubleshooting.md) | 故障、安全、凭据和恢复 |

系统结构/Flow 关系见 [`../architecture/`](../architecture/README.md)，跨仓顺序见 [`../roadmap.md`](../roadmap.md)，当前状态见 [`../progress.md`](../progress.md)，未关闭缺陷见 [`../findings.md`](../findings.md)，完整旧需求与评审见 [`../reference/`](../reference/README.md)。

## 稳定不变量

1. Manifest 表达期望，Lock 固定事实，Catalog 只发现已发布资产；
2. Flow 只调用注册 Action，Provider 声明能力/版本/权限，YAML 不执行任意 shell；
3. required stage 被跳过、blocked 或缺证据时总体不得通过；
4. `write_scope`、ownership map 和 Change Bundle 共同约束写入；
5. qualification 只判 G0～G6，G7 只在人工批准后的 release-train 判定；
6. Skill/Knowledge/商业 EDA/PDK Overlay 可选、可预检、可审计；
7. 失败必须定位到 repo/SHA/stage/provider/failure signature。

实现事实仍以 `manifests/`、`schemas/`、`workflows/`、`ownership-map.yaml` 和 `src/aixworkflow/` 为准；目标与实现差距登记在 Findings，不能把目标描述成现状。
