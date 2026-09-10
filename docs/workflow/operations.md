# 工作区操作手册

所有命令从 workflow 根执行，Python 使用根 uv 环境。尖括号是需要替换的参数，不要原样复制。
首次安装见 [Getting Started](../getting-started.md)。下表说明命令副作用，避免把检查和修改混在一起。

## 常用入口与副作用

| 命令（统一前缀 `uv run aix`） | 用途 | 副作用/限制 |
|---|---|---|
| `wf status` / `wf doctor` | 仓库状态、环境与依赖诊断 | 不证明 RTL 或领域质量通过 |
| `repo status <id>` / `repo diff <id>` | 单仓状态和差异 | 不自动暂存 |
| `wf init --profile <profile>` | 选择 Profile、初始化状态与目录 | 写 `.aix/` 等本地状态，不 clone |
| `wf sync` | 按 Profile clone/fetch/checkout | 访问网络并改本地仓；先检查 dirty 状态 |
| `wf lock -o .aix/local.lock.yaml --mode workspace --no-fetch` | 从本地 refs 生成解析锁 | 写 Lock；离线结果不保证 refs 最新 |
| `wf diff --against .aix/local.lock.yaml` | 对照当前版本和锁 | 不是 dirty 文件内容的完整快照 |
| `wf fusesoc --generate` | 生成聚合配置与 VLNV/依赖索引 | 写 `.aix/generated/`；不运行编译 |
| `wf preflight <flow>` | 检查 stage 所需能力 | required provider 缺失会非零退出 |
| `wf run <flow> ...` | 执行有输入绑定的流程 | 会按 action 写产物；须先确认授权、锁和 provider |
| `wf test --affected --repo <id>` | 影响分析 | 不等于执行 EDA 测试 |
| `repo commit <id> -m "..."` / `repo push <id>` | 提交已暂存文件、推送 | 需明确授权；不会自动 `git add` |

## 日常开始：只读巡检

```bash
uv run python bootstrap.py --ensure
uv run aix wf status
uv run aix wf doctor
uv run aix repo status ip
uv run aix repo diff ip
```

`--ensure` 按本地 canonical 内容增量物化；若 skill repo 不存在，会尝试下载。
已有可信物化副本且需要离线复用时使用 `uv run python bootstrap.py --skip-materialize aix wf status`。
`--skip-materialize` 不同步新的 Skill 修改，不能用陈旧副本验证刚修改的套件。
`--force` 可能拉取远端，不作为默认诊断步骤。

## Profile 选择

精确集合见 [Manifest profiles](../../manifests/default.yaml)；以下为当前配置的阅读摘要，不是第二份编辑源。

| Profile | 必选仓 ID | 可选附加 |
|---|---|---|
| `minimal` | hwif, tools | 无 |
| `ip-dev` | hwif, cbb, ip, dv-common, vip, tools | catalog, skills |
| `cbb-dev` | hwif, cbb, dv-common, tools | vip, catalog, skills |
| `soc-integration` | hwif, cbb, ip, dv-common, vip, tools, catalog, soc-integration | skills |
| `all` | 上述全部资产仓与 knowledge | skills |

`minimal` 不是“base 组全部仓”，也不是“无需私有仓”：tools 为私有必选仓。
skills 在 Profile 中 optional，不代表首次启动依赖它的 CLI runtime 也可缺省。
`init` 记录的 Profile 会被后续命令继承；只有在确实需要切换工作集合时再运行 init。

## Flow 调用模板

先执行 `uv run aix wf preflight ip-development`。当前标准领域 provider 未注册时应停止自动 Flow，详见 [当前限制](current-state.md)。
下面仅是 provider 就绪、输入已确认且选定资产写入已授权后的调用模板，本次文档检查未执行它：

```bash
uv run aix wf lock -o .aix/local.lock.yaml --mode workspace --no-fetch
uv run aix wf run ip-development --profile ip-dev \
  --lock .aix/local.lock.yaml \
  --input ip_name=<ip_name> \
  --input profile=ip-dev \
  --input mode=partial-task \
  --input tool_profile=<configured_tool_profile>
```

`--profile` 选择 CLI 工作区上下文，`--input profile=...` 显式绑定 Flow 占位输入；两者保持一致。
CBB 替换为 `cbb-development`、`cbb-dev` 和 `cbb_vlnv`；SoC 替换为 `soc-integration` 和 `soc_project`。
若转为人工/Agent 驱动的套件工作，应按 suite 前置条件执行并单独记录结果，不能宣称自动 Flow 已通过。

## 仓库交接的轻量检查

以下命令检查索引和 README，不运行 EDA，也不提升发布状态：

```bash
uv run python repos/aixsilicon_ip_repo/scripts/build_ip_registry.py --check-source
uv run python repos/aixsilicon_ip_repo/scripts/update_registry_readme.py --check
uv run python repos/aixsilicon_cbb_repo/scripts/build_cbb_structure.py
```

CBB README 刷新脚本当前的 `--check` 仍会调用写入逻辑，不列入只读巡检命令；修复前应在隔离副本中核对，不能仅凭参数名称假设无副作用。

不要从历史 README 猜测 FuseSoC VLNV/target；先生成聚合配置并核查资产实际 `.core`。
HWIF/VIP 的确定性入口及参数查看 [套件地图](repositories-and-skills.md)，正式运行前读取对应子 skill。

## 收尾与发布边界

```bash
make check
uv run pre-commit run --all-files
uv run aix repo diff workflow
```

`make check` 检查控制面 runtime 的 lint、Schema parity 和测试，不检查所有资产的 RTL。
pre-commit 可能修正空白/格式，应再次审查差异。子仓同样需要自己的领域测试。
需要提交时，只暂存本任务文件，再经 `aix repo commit`/`push`；不要将 `repos/`、`.aix/`、缓存或敏感证据提交到父仓。

正式发布需要明确版本、clean/locked 基线、领域证据和人工批准。
当前 `aix release publish` 写本地 `.aix/release-state.json`，不自动执行 tag/push、GitHub Release 或 Catalog PR；本地成功消息不是远端发布证明。

## 排障顺序

| 现象 | 先检查 | 不要做什么 |
|---|---|---|
| bootstrap/runtime 缺失 | skill repo 权限、选定 agent-dir、可信物化副本 | 把 optional 标记当作 CLI 已可用 |
| required provider unimplemented | preflight 和实际注册表 | 将 required 改 optional 来制造成功 |
| EDA/license 不可用 | 原生工具与许可证实际可用性 | 因 action 缺失就断言工具本体不存在 |
| dirty 或 NON-BASELINE | 各仓差异、local override、版本锁 | 自动 reset、覆盖用户修改 |
| 索引身份不一致 | registry 源、包元数据、`.core`、设计身份 | 只改一处名字或提高状态 |
| 派生视图漂移 | owner 源文件与生成器版本 | 手修生成 YAML/RTL 掩盖差异 |
| uv 缓存不可写 | 可写 `UV_CACHE_DIR`、已安装依赖 | 改 HOME、另建子仓环境、静默改 lock |

涉及破坏性操作、Schema owner 冲突或产品身份决策时，先报告范围并取得确认。
