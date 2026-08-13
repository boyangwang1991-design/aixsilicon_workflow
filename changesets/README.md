# Changesets / Change Bundle

Change Bundle 用于建立跨多个仓库独立变更之间的逻辑关系与验证、合并顺序，但不伪造“跨仓原子提交”。

## 状态机

```text
draft → ready → validating → review → merge-ready → merged → released → closed
                         ↘ blocked
```

## 合并规则

- 各仓必须独立 Review 并通过本仓 CI；
- Bundle CI 拉取所有 PR HEAD 做联合测试；
- 按依赖顺序合并（`merge_order`）；
- 上游合并后，下游必须 rebase/merge 并用上游真实 SHA 重测；
- 合并不具备分布式事务语义，失败时停止后续合并并修复 PR；
- Bundle 文件不保存访问 Token。

## 使用

```bash
cp templates/change-bundle.yaml changesets/CHG-2026-0042.yaml
# 编辑后
aix bundle validate CHG-2026-0042
aix bundle status CHG-2026-0042
```
