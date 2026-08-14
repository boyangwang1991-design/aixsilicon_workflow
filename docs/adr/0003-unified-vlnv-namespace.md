# ADR-0003：全组织统一 VLNV 命名空间 `aixsilicon:*`

- 状态：接受
- 日期：2026-08-13

## 背景

各资产仓 plan 使用了不一致的 VLNV 命名空间：

| 来源 | 当前写法 | 问题 |
|---|---|---|
| workflow / hwif / dv-common / vip plan | `aix:*` | 过短、有歧义 |
| [`ip_repo/ipkg.yaml`](../../repos/aixsilicon_ip_repo/ipkg.yaml:18) | `boyangwang1991-design:ip:*` | 使用 GitHub 组织名作 vendor |
| [`cbb_repo_plan.md`](../../repos/aixsilicon_cbb_repo/cbb_repo_plan.md:425) | `company:cbb:*`（占位） | 占位未冻结 |

命名空间不一致会破坏：Catalog 检索、FuseSoC 依赖闭包、跨仓影响分析、Lockfile 可复现性。

## 决策

- 全组织**统一采用 `aixsilicon` 作为 FuseSoC VLNV 的 vendor 段**，例如
  `aixsilicon:interface:apb:1.0.0`、`aixsilicon:vip:apb:1.0.0`、`aixsilicon:ip:<ip>:1.0.0`、
  `aixsilicon:cbb:<cbb>:1.0.0`、`aixsilicon:dv:common_*`、`aixsilicon:tool:<tool>:<version>`；
- GitHub 组织名 `boyangwang1991-design` 仅作为 **remote URL 与私有 overlay 的物理归属**，不进入 VLNV 语义；
- CLI 二进制名保持 `aix`（`aix` 是 `aixsilicon` 命令工具的唯一短入口），命名空间/标识一律使用完整 `aixsilicon`；
- `ip_repo` 的 `ipkg.yaml` 中 `fusesoc.vendor` 从 `boyangwang1991-design` 改为 `aixsilicon`，`library` 保持 `ip`；
- `cbb_repo` 冻结 `aixsilicon:cbb` 命名（其 registry 已用 `aixsilicon` vendor，保持不变），替换 `company:cbb` 占位；
- 存量已发布 core 走迁移窗口：新增 `aixsilicon:` 别名 core 指向同一内容，旧 vendor（`aix:`/`boyangwang1991-design:`）core 标记 deprecated，一个 release 周期后移除；
- `ownership-map.yaml`、`docs/schema-ownership.md`、`docs/maturity-model.md` 中的 VLNV 引用统一为 `aixsilicon:*`。

## 备选方案

- 保留各仓自定 vendor：Catalog/闭包/影响分析需维护 vendor 别名表，成本持续累积，不可取；
- 使用组织名作 vendor：暴露 GitHub 账号拓扑，且换组织/迁移需要全量改名。

## 结果

- 正向：单一命名空间，Catalog 与依赖图无需别名映射；跨仓引用可静态校验；
- 负向：ip/cbb 需要一次迁移窗口与文档/工具版本同步；
- 权衡：迁移成本集中在初期，由本 ADR + catalog 迁移脚本一次性吸收。
