# 报告模板

每次执行的标准目录（运行时生成，位于 `reports/<run-id>/`）：

```text
reports/<run-id>/
├── run_manifest.yaml
├── workspace_lock.yaml
├── evidence_index.yaml
├── status.json
├── summary.md
├── stages/
├── logs/
├── reports/
└── artifacts/
```

模板文件：

- `run-manifest.yaml`：Run Manifest 模板（Run ID、Lock、输入、Stage 摘要、Gate 结论）。
- `summary.md`：人类可读摘要模板。

正式证据需要发布时，由命令将经过筛选的 Evidence 打包到 Release 存储或对应资产仓的发布记录中，不能直接把整个运行目录提交到 Workflow Repo。
