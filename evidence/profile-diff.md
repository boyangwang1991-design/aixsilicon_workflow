# Profile 精确仓集与 typed 依赖建议

> 证据类型：决策证据（WF-001 / ADR-0007）
> 生成方式：对比 [`manifests/default.yaml`](../manifests/default.yaml) 现状展开结果与 [`docs/architecture/target-design.md`](../docs/architecture/target-design.md) §4–5 目标集合。
> 生成日期：2026-08-17
> 对应 Finding：F-010（Profile 失真、依赖无类型）；本表为 F-010 / WF-002 的输入证据。
> 仓库全集（10）：hwif、cbb、ip、dv-common、vip、tools、catalog、soc-integration、skills、knowledge

## 1. 现状 vs 目标（实测展开）

现状基于 [`Profile.includes()`](../src/aixworkflow/models.py:109) set 交集逻辑；目标基于 [`target-design.md`](../docs/architecture/target-design.md:41) 的 `include_repositories`。

| Profile | 现状仓集（实测） | 现状仓数 | 目标必需仓 | 目标可选仓 | 目标仓数(必需) | 变化 |
|---|---|---|---|---|---|---|
| `minimal` | hwif,cbb,ip,dv-common,vip,tools,catalog,soc-integration,knowledge | 9 | hwif,tools | — | 2 | **−7** |
| `ip-dev` | 全 10 仓 | 10 | hwif,cbb,ip,dv-common,vip,tools | catalog,skills | 6 | −4 |
| `cbb-dev` | 全 10 仓 | 10 | hwif,cbb,dv-common,tools | vip,catalog,skills | 4 | −6 |
| `dv-dev` | 全 10 仓 | 10 | hwif,dv-common,vip,tools | skills | 4 | −6 |
| `soc-integration` | 全 10 仓 | 10 | hwif,cbb,ip,dv-common,vip,tools,catalog,soc-integration | skills | 8 | −2 |
| `release` | hwif,cbb,ip,dv-common,vip,tools,catalog,soc-integration,knowledge | 9 | hwif,cbb,ip,dv-common,vip,tools,catalog,soc-integration | — | 8 | −1 |
| `knowledge-dev` | 不存在 | — | knowledge | skills | 1 | **新增** |
| `all` | 全 10 仓 | 10 | 全部公共仓 | skills | 9 | −1 |

**关键观察**：现状 5 个开发 Profile（ip-dev/cbb-dev/dv-dev/soc-integration）展开为**完全相同**的 10 仓；`minimal` 与 `release` 仅差 1 仓。目标通过 `include_repositories` 将 `minimal` 收敛到 2 仓、`cbb-dev` 4 仓、`dv-dev` 4 仓，场景差异可表达。

## 2. 建议的精确仓集（迁移目标）

```yaml
profiles:
  minimal:
    include_repositories: [hwif, tools]
  ip-dev:
    include_repositories: [hwif, cbb, ip, dv-common, vip, tools]
    optional_repositories: [catalog, skills]
  cbb-dev:
    include_repositories: [hwif, cbb, dv-common, tools]
    optional_repositories: [vip, catalog, skills]
  dv-dev:
    include_repositories: [hwif, dv-common, vip, tools]
    optional_repositories: [skills]
  soc-integration:
    include_repositories: [hwif, cbb, ip, dv-common, vip, tools, catalog, soc-integration]
    optional_repositories: [skills]
  release:
    include_repositories: [hwif, cbb, ip, dv-common, vip, tools, catalog, soc-integration]
  knowledge-dev:
    include_repositories: [knowledge]
    optional_repositories: [skills]
  all:
    include_repositories: [hwif, cbb, ip, dv-common, vip, tools, catalog, soc-integration, knowledge]
    optional_repositories: [skills]
```

> 说明：
> - Skills 始终 `required: false`，作为 `optional_repositories`（target-design §4 注）；
> - Knowledge 不进入确定性开发/验证/发布 Profile，仅存在于 `knowledge-dev` 与 `all`；
> - `release` 不含 skills（发布资格验证不依赖可选技能）。

## 3. typed 依赖建议（target-design §5.2 固化）

| 仓 | product | verification | tooling | discovery | context |
|---|---|---|---|---|---|
| hwif | — | — | tools | — | skills, knowledge |
| cbb | hwif | dv-common | tools | catalog（发布） | skills, knowledge |
| ip | hwif, cbb | dv-common, vip | tools | catalog（发布） | skills, knowledge |
| dv-common | — | — | tools | — | skills, knowledge |
| vip | hwif | dv-common | tools | catalog（发布） | skills, knowledge |
| tools | — | — | — | — | knowledge |
| catalog | — | — | tools（校验） | — | knowledge |
| soc-integration | hwif, cbb, ip | dv-common, vip | tools | catalog | skills, knowledge |
| skills | — | — | tools | — | knowledge |
| knowledge | — | — | — | — | — |

**现有 `depends_on` 对照**（[`manifests/default.yaml`](../manifests/default.yaml)）：
- `cbb.depends_on: [hwif]` → 迁移为 `dependencies.product: [hwif]`
- `ip.depends_on: [hwif, cbb]` → `dependencies.product: [hwif, cbb]`
- `vip.depends_on: [hwif, dv-common]` → `dependencies.product: [hwif]` + `dependencies.verification: [dv-common]`
- `soc-integration.depends_on: [hwif, cbb, ip, catalog, tools]` → 按矩阵拆分为 `product: [hwif, cbb, ip]` + `verification: [dv-common, vip]` + `tooling: [tools]` + `discovery: [catalog]`

## 4. 闭包计算规则（按操作）

| 操作 | 使用的依赖闭包 |
|---|---|
| clone / sync | Profile 显式集合 + `product` |
| build / lint | 上者 + `tooling` |
| unit / regression / qualification | 上者 + `verification` |
| release / resolve | 上者 + `discovery` |
| impact analysis | 按变更类型计算反向闭包；类型未知时**扩大**范围 |

Product DAG 必须无环；其余类型分别校验，不混成一张无类型图。context（skills/knowledge）永不成为公共确定性流程的 required 依赖。

## 5. 迁移路径（≥2 发布周期）

1. **兼容读取**：Schema 支持 `include_groups`（旧）与 `include_repositories`（新）双字段；`depends_on` ↔ `dependencies.product` 双解析；
2. **迁移 Manifest**：按 §2/§3 写入 7+1 个 Profile 的精确仓集与 typed dependencies；
3. **deprecated 警告**：检测到 `include_groups` 仍被使用且无 `include_repositories` 时告警；
4. **删除**：两个发布周期后移除旧字段（不破坏既有 Lock/测试，需预先清理）。

## 6. 结论与下一步

1. 现状 Profile 失真已量化：**5 个开发 Profile 完全相同**，必须迁移为精确集合；
2. §2 建议集与 target-design §4 一致，可直接作为 WF-002 的输入；
3. typed 依赖（§3）解决影响/验证闭包失真（F-010、R-00）；
4. **M1 WF-002 首件工作**：实现 Schema 双字段解析 + typed DAG/closure 测试（含负向：非 DAG、未知类型、缺失闭包）。
