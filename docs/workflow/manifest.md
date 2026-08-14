# Manifest 设计

Workspace Manifest 描述**期望工作区**，不记录本地瞬时状态。回答：当前工作区需要克隆哪些 Git 仓库、放在哪里、使用何种开发分支或版本策略。

> 当前规范为 `aix.workspace/v1`：Profile 使用 `include_groups`，依赖使用无类型 `depends_on`。目标方案建议兼容增加显式仓库集合和有类型依赖；在 ADR-0007 接受并完成实现前，目标字段不得写入正式 Manifest。详见 [`../architecture/target-design.md`](../architecture/target-design.md) §4～5。

## 结构与字段

完整示例见 [`manifests/default.yaml`](../../manifests/default.yaml)，Schema 见 [`schemas/workspace-manifest.schema.json`](../../schemas/workspace-manifest.schema.json)。

Manifest 描述**期望工作区**，回答：

- 仓库逻辑 ID；
- Git URL 和 remote；
- checkout 路径；
- 默认 branch/tag/range；
- 所属 Profile 和 Group；
- owner 与权限级别；
- 仓库类型；
- FuseSoC core roots；
- 仓库级依赖；
- required/optional 属性；
- shallow、LFS、sparse checkout 策略；
- 工具和 Skill 暴露入口。

| 顶层 | 说明 |
|---|---|
| `schema_version` | 必须为 `aix.workspace/v1` |
| `workspace` | 名称、默认 Profile、repos_root、generated_root |
| `remotes` | **批准 remote allowlist**（URL 白名单） |
| `repositories` | 仓库列表（id/type/path/remote/repo/revision/groups/依赖/owner） |
| `profiles` | Profile → 启用的 groups |

每个仓库的关键字段：

- `id`：组织内稳定逻辑 ID；
- `type`：`hw-interface / cbb / ip / dv-common / vip / tool / catalog / soc-integration / skill / ...`；
- `path`：必须位于 `repos_root` 下，禁止绝对路径和 `..` 逃逸；
- `revision`：`branch / tag / commit / range` 之一（开发便利）；正式基线由 Lockfile 固定 SHA；
- `depends_on`：仓库级依赖，必须形成有向无环图（DAG）；
- `groups`：仓库归属的组，Profile 通过组启用仓库；
- `visibility`：`public / private`；`private + required:false` 的 Skill 仓无权限时显示 `OPTIONAL_UNAVAILABLE`；
- `fusesoc_roots`：作为 FuseSoC core root 的目录。

### Manifest 规则

- `id` 在组织内稳定，路径可调整但需迁移说明；
- `path` 必须位于配置的 `repos_root` 下，禁止绝对路径和 `..` 逃逸；
- URL 必须来自批准 remote 或明确 allowlist；
- 每个仓库必须声明 owner、type、default branch 和许可证策略；
- `depends_on` 必须形成有向无环图；
- Manifest 中的 branch 用于开发便利，正式基线必须由 Lockfile 固定 SHA；
- 凭据只由 SSH Agent、Git credential helper 或 CI Secret 提供，不进入 YAML；
- 本地私有覆盖只能进入被忽略的 `overrides/local.yaml`；
- `visibility: private` 且 `required: false` 的 Skill 仓在无权限时应明确显示 `OPTIONAL_UNAVAILABLE`，公共确定性 Flow 继续运行；需要 Skill 的增强 Flow 则给出权限前置条件，不得静默降级为另一套结果。

## extends 复用

Profile 文件通过 `extends: default.yaml` 复用基础清单，只声明差异（如默认 Profile）：

```yaml
schema_version: aix.workspace/v1
extends: default.yaml
workspace:
  name: aixsilicon
  default_profile: ip-dev
```

## Local Override

本地临时替换（例如 VIP 依赖尚未合入的 HWIF 分支）：

```yaml
# overrides/local.yaml（被 .gitignore 忽略）
schema_version: aix.workspace-override/v1
repositories:
  hwif:
    revision:
      branch: feature/axi-user-contract
```

规则：

- override 默认只在本地生效；
- `aix wf status` 会显示 `NON-BASELINE / OVERRIDDEN`；
- Evidence 与 Run Manifest 记录实际 SHA，不记录分支名；
- Release Gate 默认拒绝 local override；
- 需要团队共享的跨仓变更改用 **Change Bundle**。

## 版本与 Lock

- Manifest 中的 branch 用于日常开发；
- 正式基线通过 `aix wf lock` 生成 Lockfile 固定 SHA；
- 更新正式 `locks/baseline.lock.yaml` 必须经过完整跨仓资格验证 PR。

### Lockfile 设计

Lockfile 是可复现性的核心，记录 Manifest 解析后的不可变状态：

- 每个仓库的 canonical URL；
- resolved commit SHA；
- branch/tag 来源；
- tree hash 与 dirty 状态；
- Catalog commit；
- 关键 VLNV 与版本；
- FuseSoC、Python、生成器及工具 Profile 版本；
- Manifest digest；
- 生成时间与生成者类型；
- 解析策略版本。

三类锁文件：

| 类型 | 是否入库 | 用途 |
|---|---|---:|
| `baseline.lock.yaml` | 是 | 团队默认集成基线，受 PR 和 CI 保护 |
| `releases/*.lock.yaml` | 是 | 正式 Bundle/项目里程碑，不允许原地修改 |
| `.aix/local.lock.yaml` | 否 | 开发者当前解析结果，可包含本地分支 |

更新正式 Lockfile 必须经过完整跨仓资格验证，不能因为执行了一次 `sync` 就自动覆盖。完整示例见 [`locks/baseline.lock.yaml`](../../locks/baseline.lock.yaml)。

## 目标 v2 兼容迁移

建议新增而不是立即替换现有字段：

```yaml
repositories:
  - id: ip
    depends_on: [hwif, cbb]  # 过渡期兼容，等价 product
    dependencies:
      product: [hwif, cbb]
      verification: [dv-common, vip]
      tooling: [tools]
      context: [skills, knowledge]

profiles:
  minimal:
    include_repositories: [hwif, tools]
```

迁移顺序：Schema/解析器兼容 → exact-set/typed-closure 测试 → 默认 Manifest 迁移 → Lock 记录解析策略 → 两个发布周期后 deprecated。最终决策以 [ADR-0007](../adr/0007-typed-dependencies-and-explicit-profiles.md) 为准。
