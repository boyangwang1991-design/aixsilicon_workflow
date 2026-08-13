# Quick Start

## 1. 一次性环境准备

```bash
git clone git@github.com:boyangwang1991-design/aixsilicon_workflow.git
cd aixsilicon_workflow
python -m pip install -e ".[dev]"
```

## 2. 选择 Profile

| Profile | 用途 |
|---|---|
| `minimal` | 最小编译所需（base 组） |
| `ip-dev` | IP 设计验证开发 |
| `cbb-dev` | CBB 设计验证开发 |
| `dv-dev` | 验证环境开发 |
| `soc-integration` | SoC 集成 |
| `release` | 正式发布基线 |

## 3. 初始化并按 Profile 同步

```bash
aix wf init --profile ip-dev
aix wf sync
aix wf status
```

## 4. 生成 FuseSoC 聚合配置

```bash
aix wf lock --output .aix/local.lock.yaml
aix wf fusesoc --generate
# 生成：
#   .aix/generated/fusesoc.conf
#   .aix/generated/core-roots.txt
#   .aix/generated/vlnv-index.json
#   .aix/generated/dependency-graph.json
```

## 5. 独立提交一个子仓

```bash
aix repo branch vip feature/my-change
aix repo commit vip -m "feat: my change"
aix repo push vip
# 父仓 git status 应保持 clean
```

## 6. 建立跨仓 Change Bundle（阶段3）

```bash
aix bundle create --from templates/change-bundle.yaml
aix bundle validate CHG-2026-XXXX
aix bundle status CHG-2026-XXXX
```

## 故障快速定位

- remote 错误 / 不可达 SHA → [`docs/troubleshooting.md`](../docs/troubleshooting.md)
- override 显示 NON-BASELINE → 检查 `overrides/local.yaml` 与 `aix wf status`
- 发布被拒 → 确认 clean、无 local override、已固定 Lock
