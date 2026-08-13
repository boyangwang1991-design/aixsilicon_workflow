# Manifest 设计

Workspace Manifest 描述**期望工作区**，不记录本地瞬时状态。回答：当前工作区需要克隆哪些 Git 仓库、放在哪里、使用何种开发分支或版本策略。

## 结构与字段

完整示例见 [`manifests/default.yaml`](../manifests/default.yaml)，Schema 见 [`schemas/workspace-manifest.schema.json`](../schemas/workspace-manifest.schema.json)。

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
