# GitHub Actions CI/CD 状态

2026-10-08 按用户要求整体取消 GitHub Actions CI/CD。

workflow 根仓与 `repos/` 下各仓库不再保留 `.github/workflows/*.yml` 或
`*.yaml` 定义，包括手动入口和可复用 workflow。提交、推送、PR、发布和定时
事件不再触发这些流程，也避免无效 workflow 定义在推送时产生配置错误。

检查脚本、测试、FuseSoC target 和本地 pre-commit 保留，按需在本地执行。
根仓本地检查入口为 `make check` 与 `uv run --locked --extra dev pre-commit run --all-files`；
子仓使用各自的本地检查入口。

这些变更须分别提交、推送到 workflow 根仓及 CBB、HWIF、IP 仓才能在远端生效。
已产生的 Actions 运行记录不会被删除。历史版本中的可复用 workflow 仍可能被外部
仓库按旧 tag/SHA 调用；本次变更不修改外部仓库或 GitHub 仓库设置。
