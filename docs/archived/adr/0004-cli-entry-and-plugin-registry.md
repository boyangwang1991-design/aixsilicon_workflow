# ADR-0004：统一 CLI 入口与插件注册组

- 状态：接受
- 日期：2026-08-13

## 背景

[`pyproject.toml`](../../pyproject.toml:38) 已将 `aix = aixworkflow.cli:main` 注册为唯一入口；
[`tool_repo_plan.md`](../../repos/aixsilicon_tool_repo/tool_repo_plan.md:955) 规划 `aix tool <domain> <command>`。
若 tool_repo 也注册 `aix`，会产生控制台入口冲突；若拆成两个命令，则工程师/Agent 记忆与脚本契约分叉。

## 决策

- `aix` 是唯一总入口（`aix` 为 `aixsilicon` 命令工具的唯一短入口），由 `aixsilicon_workflow` 提供（保持现有 `aix wf` / `aix repo` / `aix bundle` / `aix release`）；
- `aixsilicon_tool_repo` 通过 **Python Entry Point 组 `aixsilicon.commands`** 注册 `aix tool` 域，实现插件式扩展；
- `cli/registry.py` 在 `register_all()` 时扫描 `aixsilicon.commands` 组，把注册的 handler 并入分发表；
- 未安装 tool_repo 时，`aix tool ...` 返回明确错误：`tool domain unavailable: install aixsilicon_tool_repo or use --offline repo scripts`，语义与 manifest 中私有 Skill 的 `OPTIONAL_UNAVAILABLE` 一致；
- 不允许第三方包再注册顶层 `aix` 入口；公共契约（CLI 参数、退出码、Result）由 workflow 侧 `docs/` 冻结。

参考：Python Entry Points 规范 <https://packaging.python.org/specifications/entry-points/>。

## 备选方案

- tool_repo 注册独立 `aix-tool` 二进制：命令记忆分叉、脚本契约不稳定，不采用；
- workflow 硬编码所有 tool 子命令：导致 workflow 反向依赖 tool_repo 内部实现，破坏分层。

## 结果

- 正向：单一入口 + 插件发现，tool_repo 独立演进不冲突；`aix tool` 在未安装时显式降级而非静默；
- 负向：`aixsilicon.commands` 插件协议需要稳定版本化（`api_version`）；
- 权衡：插件协议作为公共契约由 workflow 与 tool_repo 共同维护，见 `docs/schema-ownership.md`。
