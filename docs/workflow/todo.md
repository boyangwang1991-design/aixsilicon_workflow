# workflow — Todo

> 状态：`[x]` 已完成 · `[-]` 进行中 · `[ ]` 待办。
> 原文细节见 [`../archived/root/todo.md`](../archived/root/todo.md) 与 [`../archived/root/aixsilicon_build_todolist.md`](../archived/root/aixsilicon_build_todolist.md)。

## P0 优先

- [ ] runner `aix tool` 委托真实 provider（tool_repo 插件）接入，并纳入工具版本锁
- [ ] `aix release prepare/publish` 实现（G7：dirty/override 阻断 + 人工批准）
- [ ] `workspace-lock.schema.json` 增加 `tools:` 段（tool_repo 包版本 + hash）
- [ ] 验证所有 Core 可被 FuseSoC 发现（`aix wf run` 真实执行 `fusesoc.target` 阶段）

## P1 首个季度

- [ ] `aix bundle create` 从模板生成并校验状态机
- [ ] PR refs 联合 checkout（`change-bundle.yml` 占位 → 真实）
- [ ] reusable workflows 固定 Tag v0.1（lint / unit-sim / integration-baseline / change-bundle 真实化）
- [ ] `aix release publish` 端到端（Tag/SBOM/Catalog PR 编排）；baseline 升级 + Workspace Bundle Release
- [ ] 失败 Run 定位接入（仓库/SHA/Stage/工具/Failure Signature）
- [ ] 新成员从零初始化演练（clean 环境）

## P2 两个季度

- [ ] `soc-*` flow 动作接入（`tool.socgen` / `tool.connect`）
- [ ] blue-zone / red-zone 双环境实跑
- [ ] Nightly 兼容矩阵
- [ ] AIXSILICON 项目座舱接入
- [ ] 并发互斥与失败恢复

## 工程化遗留

- [ ] `aix repo pr`（gh CLI 包装，S5 残余）
- [ ] GitHub reusable workflows 真实化（S6，替换 echo 占位）

## 阶段路线执行状态（root/todo.md 阶段 0–5 对照）

> 已合并 `docs/archived/root/todo.md` 的阶段结构与条目；已完成项标注 [x]，未完成项保留待办。

### 阶段总览

| 阶段 | 周期 | 目标出口 | 状态 |
|---|---|---|---:|
| 阶段0 边界与 ADR 冻结 | 2 周 | 仓库责任/依赖方向经 Owner 确认 | 基本达成，CBB/Tool/Catalog/SoCInt 内容待填充 |
| 阶段1 Workspace MVP | 3~4 周 | 一条命令建环境、子仓独立提交 | 基本达成，剩 P0 缺陷 |
| 阶段2 FuseSoC 与跨仓验证 | 4~6 周 | 固定 Lock 重建 APB 验证闭环 | 进行中 |
| 阶段3 Change Bundle 与影响分析 | 4~6 周 | HWIF→VIP→IP 联合变更 | 未开始 |
| 阶段4 发布协调与 Catalog | 4~6 周 | IP 资格验证+人工批准+Catalog 更新 | 未开始 |
| 阶段5 SoC 集成与规模化 | 6~8 周 | SoC 锁定基线可重建 | 未开始 |

### 阶段0：边界与 ADR 冻结

- [x] 冻结 `aixsilicon_workflow` 职责、非目标与 ADR（0001/0002）
- [x] 确认全部 P0 仓库真实 URL、default branch、owner
- [x] 固化全部仓库使用 `aixsilicon_` 前缀
- [x] 定义 Manifest / Lock / Local Override Schema V0.1
- [x] 定义标准目录与 `.gitignore`（运行时目录完整忽略）
- [x] 建立 ownership map（[`ownership-map.yaml`](../../ownership-map.yaml)）
- [x] 建立仓库依赖 DAG（无环校验通过）
- [x] 定义 P0 CLI 错误码与安全策略
- [x] 建立最小 Python 包和测试框架
- [x] 建立 README Quick Start
- [-] 初始化 `aixsilicon_cbb_repo`（已构建，内容续增）
- [ ] 初始化 `aixsilicon_tool_repo` 并迁移确定性脚本
- [ ] 初始化 `aixsilicon_catalog_repo` 并定义首版资产条目 Schema
- [ ] 初始化 `aixsilicon_soc_integration_repo` 并定义 SoC 配置 Schema 边界
- [ ] `aixsilicon_skill_repo`（私有）Skill Metadata 契约

### 阶段1：Workspace MVP

- [x] 实现 `aix wf init/sync/status/doctor/lock`
- [x] 实现 `aix repo status/shell/branch/commit/push` + `diff`
- [x] 实现 remote、dirty、unpublished commit 保护
- [x] 支持 `minimal/ip-dev/cbb-dev/dv-dev/soc-integration/release` Profile
- [x] 生成 `.aix/generated/fusesoc.conf` + core-roots/vlnv-index/dependency-graph
- [x] 完成临时 Git 仓 Fixture 测试
- [x] 验证子仓 commit 不改变 Workflow 父仓状态
- [x] 输出本地 Lock 和状态表
- [ ] 验证所有 Core 可被 FuseSoC 发现（需安装 fusesoc 实跑）
- [ ] 完成新成员从零初始化演练（clean 环境）

阶段1 遗留 P0 缺陷（已修复）：lockfile `tree` 为空（`gitops.rev_parse_any`）、`aix wf lock --no-fetch` 离线模式、`aix wf status` Baseline 列（diverged）、`aix wf sync --lock` 按 Lockfile checkout、真实 `locks/baseline.lock.yaml`。

### 阶段2：FuseSoC 与基础跨仓验证

- [x] 生成 FuseSoC 配置与 VLNV 索引
- [x] Core dependency graph
- [x] Flow DAG 执行器 `aix wf run <flow>`（已接入 CLI；具体 action 待实现）
- [ ] APB 寄存器 IP 穿刺：HWIF SystemRDL/RAL + APB VIP + DV Common 联合闭环
- [x] Run Manifest 与 Evidence Index 接入 run
- [-] GitHub reusable lint/unit workflow：文件已建，内容为占位

### 阶段3：Change Bundle 与影响分析

- [x] Change Bundle Schema 与示例
- [x] Change Bundle CLI：`aix bundle validate/status`（create 为模板指引）
- [ ] PR refs 联合 checkout（`change-bundle.yml` 占位）
- [x] 基础影响分析（`impact.py` + `graph.transitive_closure`）
- [x] `aix wf test --affected` 影响驱动验证入口
- [ ] X2X 三仓联合变更穿刺
- [-] 防递归触发与 correlation ID（`github.py` guard_event_loop 桩）

### 阶段4：发布协调与 Catalog

- [x] Release Policy 与 protected environment 定义
- [x] 幂等发布判定（`release.py` `already_published`）
- [ ] `aix release prepare/publish` 实现（当前桩）
- [ ] IP Release Skill 接入（依赖 skill_repo）
- [ ] Release Manifest / SBOM / RTM 完整性检查
- [ ] Catalog 更新 PR 自动生成（依赖 catalog_repo 内容）
- [ ] Baseline 升级与 Workspace Bundle Release
- [ ] 并发互斥与失败恢复

### 阶段5：SoC 集成与规模化

- [x] SoC 集成 Profile 与 Flow
- [x] blue-zone / red-zone 工具 Profile
- [ ] 地址、中断、CRG、Power 域连接检查接口
- [ ] PIC / 功能安全集成穿刺
- [ ] 私有 Skill 可选依赖边界验证
- [ ] AIXSILICON 项目座舱接入
- [ ] 指标、容量和运营机制 / Nightly 兼容性矩阵

### 一期验收标准对照（root/plan §31）

- [x] 1. 一条命令按 Profile 下载全部仓库
- [x] 2. 子仓位于 `repos/` 并被父仓可靠忽略
- [x] 3. 任一子仓可独立建分支/commit/push，父仓无变化
- [x] 4. dirty tree、错误 remote、不可达 SHA、local override 可识别
- [ ] 5. 生成完整 FuseSoC 配置并发现全部 Core（待实跑 fusesoc）
- [x] 6. Lockfile 记录各仓 SHA 与工具 Profile（可重建）
- [ ] 7. APB 代表性 IP 完成跨仓 Lint/编译/仿真/Evidence
- [x] 8. Change Bundle 描述 HWIF+VIP+IP 联合变更（示例）
- [ ] 9. 联合 CI 拉取各仓 PR HEAD 并产生结构化结论
- [ ] 10. 发布动作前人工确认，dirty/override 环境不可发布
- [ ] 11. 失败 Run 定位到仓库/SHA/Stage/工具/Failure Signature
- [x] 12. README、协作规范、故障文档可用

### 风险对照（root/plan §32，重点盯防）

- [ ] 防止 Workflow 变成超级仓库（ownership map + CI Guard 已建，需持续执行）
- [ ] Manifest 与 Catalog 不重复（Catalog 未建内容，先定边界）
- [ ] 只锁 Git 不锁工具 → Tool Profile 与生成器一并锁定
- [ ] 多仓自动提交失控 → 保持单仓显式命令
- [ ] 影响分析漏测 → 未知依赖按扩大范围
- [ ] EDA 产物撑爆仓库 → ignore + pre-commit Guard 已建，落地 `pre-commit install`

### 新仓接入记录（2026-08-13）

- ✅ `aixsilicon_chipknowledge`（id=`knowledge`，type=`other`）：已在 `manifests/default.yaml` 登记、ownership-map 注册表登记、README/gitlist/schema-ownership 同步；仓库已用 README 骨架初始化并推送 `main`，`aix wf sync` 后 `main / clean / sync`。工作区现共 10 仓。
- [ ] R1 工具收敛：督促 hwif `tools/` 产品级工具分阶段迁入 tool_repo（ADR-0006）
- [ ] R4 发布职责分工：ipkg / `aix release` / hwif package_release 边界落地
- [ ] R5 “影响分析”语义命名区分（接口影响 vs 仓库影响）
- [ ] A1 IP 仓双态模型：dev 分支可编辑、release 版本冻结
- [ ] A2 vendored `reference/` 治理：排除 fusesoc 发现、不发布、不进 Catalog
- [ ] A4 techlib 统一 `aixsilicon_techlib_repo`（P1 待建）

## 关联

- Plan：[`plan.md`](plan.md)
- 全局规划：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
- 阶段路线来源：[`../archived/root/todo.md`](../archived/root/todo.md)
