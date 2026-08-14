# 故障处理

## 症状 → 处理

### 1. `repository 'xxx' is not cloned`

原因：该仓尚未 clone。
处理：

```bash
aix wf sync
```

### 2. `configured remote does not match manifest`

原因：该仓的 `origin` remote 与 Manifest 中 approved URL 不一致（防误操作保护）。
处理：确认 Manifest 的 `remotes.origin.base_url` 正确，然后修正该仓 remote：

```bash
aix repo shell <id>
git remote set-url origin git@github.com:boyangwang1991-design/<repo>.git
```

> 不要随意覆盖：CLI 的 remote 校验是安全机制，防止连到错误远端。

### 3. `revision 'xxx' is not reachable`

原因：分支/tag/commit 不存在，或本地 ref 过期。
处理：

```bash
aix wf sync --repo <id>   # 强制 fetch
aix repo status <id>
```

### 4. `dirty in release mode`

原因：release/lock 模式要求 clean 工作树，存在未提交改动或 untracked 文件。
处理：先 `aix repo commit` 或清理，再进入 release 流程。

### 5. `OPTIONAL_UNAVAILABLE`

原因：私有 Skill 仓无访问权限（`visibility: private` + `required: false`）。
处理：公共确定性流程继续运行；需要 Skill 的增强流程给出权限前置条件，不会静默降级为另一套结果。

### 6. `dependency DAG contains cycle`

原因：Manifest 中 `depends_on` 形成环。
处理：修正 [`manifests/default.yaml`](../../manifests/default.yaml) 的依赖方向，运行 `aix wf graph` 验证。

### 7. `NON-BASELINE / OVERRIDDEN`

原因：`overrides/local.yaml` 生效。
处理：确认后删除或修改 override，再 `aix wf sync`；发布前必须移除。

### 8. 测试失败定位

`aix wf run <flow>` 失败时会输出：
- 仓库、SHA、Stage、工具；
- Failure Signature；
- Evidence（`reports/<run-id>/`）。

先读 `reports/<run-id>/run_manifest.yaml` 与 `evidence_index.yaml`。

## 高危操作保护

- 禁止在工作区根目录执行 `git clean -ffdx` / `rm -rf repos/*` / 无确认 `reset --hard` / 自动 force-push；
- 需要清理生成目录时使用 `aix wf clean`（只清理生成的 build/cache/.aix/generated）。

## 日志脱敏与凭据

- Lockfile、日志、报告中不保存凭据；
- 日志自动脱敏；若发现明文 Token/路径，立即轮换。
