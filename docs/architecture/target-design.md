# Workflow / Repos 评审与目标方案

状态：建议方案，待 ADR-0007/0008 接受后分阶段实施。评审基线更新至 2026-08-14，依据 Manifest、所有权映射、8 条现有 Flow、runner/action 代码和 10 个仓库的实际目录。本文只维护“现状差距 → 目标机制 → 迁移顺序”，现行总体模型见 [`overview.md`](overview.md)。

## 1. 总体判断

“Workflow 控制面 + 独立资产仓”的方向合理，当前十仓边界也基本成立，不需要为解决执行缺口继续拆仓。主要矛盾是规划领先于实现：Profile 和依赖语义过粗，Flow 声明的 action 超过 runner/provider 的实际能力，CBB、发布和跨仓证据闭环尚未贯通。

近期目标不是增加材料或仓库，而是完成一条可重复运行、可留证、可发布的 APB 垂直闭环，再复用同一机制建设 CBB 和最小 SoC。

## 2. 现状问题与决策

| ID | 优先级 | 问题 | 影响 | 目标决策 |
|---|---|---|---|---|
| A0 | P0 | `include_groups` 让多个 Profile 得到几乎相同的仓集合；`depends_on` 无类型 | 成本/权限不清，影响分析过宽或漏测 | 显式 Profile + typed dependencies |
| A1 | P0 | Flow 使用的许多 action 未在标准 runner/provider 注册 | YAML 可解析但不可执行 | capability registry + preflight |
| A2 | P0 | 没有 CBB 专用开发/验证 Flow | CBB 只能依附 IP 流程，PPA/参数验证无闭环 | APB 闭环后补齐两条 CBB Flow |
| A3 | P1 | SoC Flow 消费 dv-common/vip，Manifest 依赖图未表达 | 影响传播依赖 group 偶然并集 | 声明 verification 依赖或 Flow capability |
| A4 | P0 | 工具包骨架与端到端可用被混为“完成” | 进度和风险判断失真 | C0–C4 分级，provider 版本/hash 入 Lock/Evidence |
| A5 | P0 | release-train 仍是契约桩 | G7、Catalog 和幂等发布不可证明 | 人工批准 + 资产 Release + Catalog PR 闭环 |
| A6 | P1 | 文档候选仓名与 Manifest 真实名称漂移 | URL、CI、Lock 和引用可能失效 | Manifest ID/路径为 canonical；重命名单独 ADR |
| A7 | P0 | 多份计划同时维护“当前状态” | 已完成/待接入口径冲突 | `todo.md` 管唯一任务状态，`progress.md` 只汇总组合状态，仓 `delivery.md` 管任务定义，设计文档不报状态 |

A7 已通过“README 设计契约 + delivery 任务定义 + 统一 todo 状态 + historical reference”重组落实；A0–A6 仍需按路线图实施。`techlib`、`model`、`sw`、`reference-soc` 保持候选，方案见 [`../proposals/repositories/`](../proposals/repositories/README.md)，达到激活门禁并通过 ADR 后再建仓。

## 3. 保持不变的架构约束

- Workflow 不保存资产源码；各资产仓保持独立 Git、PR、Tag 和 Release。
- Manifest 描述期望工作区，Lock 固定实际版本，Catalog 只管理已发布资产。
- Tool 提供确定性生成/检查；Skill/Knowledge 是可选辅助，不能判定 Gate。
- 资产事实只能写入唯一 Owner；Flow `write_scope` 与 ownership map 双重约束。
- Flow 只能调用注册 action，禁止从 YAML 执行任意 Shell。
- 发布必须 clean、locked、无 override、有人工批准和完整 Evidence。

仓库职责本身不在本文重复，统一以 [`repos.md`](repos.md) 为准。

## 4. 显式 Profile

当前多数仓包含 `base` group，导致 `minimal` 启用 9 个公共仓，`ip-dev/cbb-dev/dv-dev/soc-integration` 也几乎收敛为同一集合。目标改用 `include_repositories` 精确表达场景，group 仅用于展示、检索和策略。

| Profile | 必需仓 | 可选仓 | 场景 |
|---|---|---|---|
| `minimal` | hwif、tools | — | 契约/工具最小环境 |
| `ip-dev` | hwif、cbb、ip、dv-common、vip、tools | catalog、skills | IP 设计验证 |
| `cbb-dev` | hwif、cbb、dv-common、tools | vip、catalog、skills | CBB 参数验证/PPA |
| `dv-dev` | hwif、dv-common、vip、tools | skills | DV/VIP 开发 |
| `soc-integration` | hwif、cbb、ip、dv-common、vip、tools、catalog、soc-integration | skills | SoC 集成验证 |
| `release` | hwif、cbb、ip、dv-common、vip、tools、catalog、soc-integration | — | 公共资产发布资格验证 |
| `knowledge-dev` | knowledge | skills | 知识与 Skill 内容建设 |
| `all` | 全部公共仓 | skills | 管理/审计，不作为普通开发环境 |

Skills 始终 `required: false`；Knowledge 不进入确定性开发、验证和发布 Profile。

## 5. 有类型依赖

### 5.1 类型与闭包

| 类型 | 含义 | 参与的操作 |
|---|---|---|
| `product` | 产品组成或编译资产 | clone 必需闭包、build、release |
| `verification` | testbench、VIP、模型和资格验证 | unit/regression、impact、qualification |
| `tooling` | 确定性生成/检查 provider | preflight、build/test、Lock/Evidence |
| `discovery` | 已发布资产发现和版本解析 | SoC resolve、release |
| `context` | 可选 Skill/Knowledge | 辅助；缺失时明确降级，不改变最低 Gate |

`depends_on` 在兼容期解释为 `product`。Product DAG 必须无环；其余类型分别校验，不能混成一张无类型图。

### 5.2 目标矩阵

| 仓 | product | verification | tooling | discovery | context |
|---|---|---|---|---|---|
| hwif | — | — | tools | — | skills、knowledge |
| cbb | hwif | dv-common | tools | catalog（发布） | skills、knowledge |
| ip | hwif、cbb | dv-common、vip | tools | catalog（发布） | skills、knowledge |
| dv-common | — | — | tools | — | skills、knowledge |
| vip | hwif | dv-common | tools | catalog（发布） | skills、knowledge |
| tools | — | — | — | — | knowledge |
| catalog | — | — | tools（校验） | — | knowledge |
| soc-integration | hwif、cbb、ip | dv-common、vip | tools | catalog | skills、knowledge |
| skills | — | — | tools | — | knowledge |
| knowledge | — | — | — | — | — |

按操作计算闭包：clone 使用 Profile 显式集合 + product；build 加 tooling；测试再加 verification；发布资格再加 discovery；impact analysis 根据变更类型计算反向闭包，未知类型时扩大而不是缩小范围。

## 6. Flow / Action / Provider 契约

```text
Flow：顺序、依赖、Gate、重试和写入范围
Action Contract：名称、输入输出 Schema、权限、确定性和证据要求
Provider：真实 Python/Tool/EDA/私有 Overlay 实现及版本
```

Flow 不绑定脚本路径。Action registry 返回 provider 元数据，resolved Lock 和 Evidence 记录 provider 名称、版本、hash 与运行环境。

执行前必须生成 capability matrix：

| 状态 | 含义 | 行为 |
|---|---|---|
| `available` | provider、版本和环境满足 | 执行 |
| `optional-unavailable` | 可选 Skill/私域能力缺失 | 明确跳过，不降低最低 Gate |
| `unimplemented` | 有 action 契约但无实现 | 阻断 |
| `version-mismatch` | provider 不满足约束 | 阻断 |
| `environment-unavailable` | EDA/license/PDK 不可用 | 按 Flow 明示策略阻断或跳过 |

在 preflight 和端到端测试通过前，现有 Flow 均保持 `draft / integration-needed`，不能因 YAML 存在标记为完成。

## 7. Flow 建设顺序

| 顺序 | Flow | 验收目的 |
|---|---|---|
| P0-1 | `apb-register-ip` | 第一条真实 Flow→Provider→Evidence 垂直闭环 |
| P0-2 | `cross-repo-qualification`、`release-train` | APB 跨仓资格、人工批准、资产发布和 Catalog PR |
| P1-1 | `ip-development`、`ip-verification`、`hwif-change`、`vip-development` | 将 APB 验证过的契约扩展为领域流程 |
| P1-2 | 新增 `cbb-development`、`cbb-verification` | 参数域、边界、形式/随机、PPA、下游影响 |
| P2 | `soc-integration` | 冻结 Schema 后接入最小生成/验证闭环 |

## 8. Gate 与最小 Evidence

| Gate | 最小证据 |
|---|---|
| G0 | Schema/安全/路径检查结果、仓库 SHA |
| G1 | resolved Lock、remote/dirty/override 状态 |
| G2 | typed dependency graph、VLNV 索引和冲突报告 |
| G3 | Contract/Profile/Binding 兼容报告与模型 hash |
| G4 | lint/build/unit 命令摘要、退出码、报告和 artifact hash |
| G5 | 影响集合、联合测试、覆盖率与已知失败策略 |
| G6 | Run Manifest、Evidence Index、provider/EDA/seed/hash |
| G7 | SemVer、CHANGELOG、SBOM、RTM、审批和 Catalog diff |

Gate 只能由独立证据转为 pass；Skill 输出、目录存在或摘要文字不能作为充分条件。

发布闭环为：

```text
candidate → clean/locked/preflight → G0-G6 qualification
→ material check → human approval → asset tag/release
→ Catalog PR → baseline candidate → bundle evidence
```

发布动作必须幂等；Workflow 只协调和生成 PR，不绕过资产仓 Review，不直接更新 Catalog main。

## 9. 完成度模型

| 等级 | 判定 |
|---|---|
| C0 Defined | Schema、Owner、边界和 action contract 已定义 |
| C1 Implemented | Provider/资产已实现并有单元测试 |
| C2 Integrated | 已由 Flow 调用，实际版本进入 Lock |
| C3 Qualified | 固定 Lock 下通过跨仓 Gate 并产出 Evidence |
| C4 Released | 已发布并进入 Catalog/兼容矩阵 |

因此“工具包已建立”最多说明部分能力达到 C1；只有真实 Flow 调用并锁定版本后才是 C2。规划和进度统一使用该模型，不再报告模糊百分比。

## 10. 兼容迁移

1. 接受 ADR-0007/0008，冻结 Profile、依赖和 action provider 语义；
2. Manifest v1 增加兼容字段，CLI 同时读取旧 `depends_on` 与 typed dependencies；
3. 增加 Profile exact-set 测试并迁移 default Manifest；
4. 增加 provider metadata、capability registry 和 `aix wf preflight`；
5. Lock/Evidence 增加 provider/tool 版本与 hash；
6. 以 APB Flow 完成 C0→C4；
7. 复用闭环建设 CBB，再进入最小 SoC；
8. 稳定运行两个发布周期后废弃旧 `depends_on/include_groups` 的精确选择语义。

实际里程碑、Owner 和退出条件见 [`../roadmap.md`](../roadmap.md)，当前实施状态只看 [`../progress.md`](../progress.md)。
