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

## 关联

- Plan：[`plan.md`](plan.md)
- 全局规划：[`../workflow-repo-plan.md`](../workflow-repo-plan.md)
