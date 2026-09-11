# Workflow 控制面运行日志

本文件记录在 `aixsilicon_workflow`（多仓工作区控制面）执行的**跨仓/元操作**：
skill repo 变更、物化、校验、发布协调等。IP 工作区内的阶段动作日志
（`reports/quality/run_log.md`）由对应 Skill 管理，不在此记录。

格式：`时间(UTC)` | 阶段 | 动作 | 结果 | 证据/哈希

- `2026-09-11` | **workflow / 全仓提交推送（第二轮）** | 用户再次 submit all to GitHub：
  skills（1 commit：apb-secure-demux 流程改进文档更新）、ip（1 commit：apb_secure_demux
  lint/synth 进度与 rtl_leaves 证据、gpio 约束三件套与 UT/synth 脚本、watchdog
  sgdc/spyglass 约束与 malloc-retry 覆盖率证据）快照提交推送；并行 codex 会话仍在
  ip 仓持续写入，本快照包含其截至提交时刻的最新产出 | PASS |
  其余 8 仓 clean+sync；skills push 后自动重新物化 11 skills。

- `2026-09-11` | **workflow / 全仓提交推送** | submit all to GitHub：skills、ip、workflow 三仓
  commit + push 到 origin/main，其余 7 子仓（hwif/cbb/dv-common/vip/tools/catalog/soc-integration/
  knowledge）本就 clean+sync 无需提交 | PASS |
  ip（3 commits：GPIO IP 全套+apb_secure_demux 契约+watchdog 更新+registry 刷新 1022 文件
  `22c5b33`；GPIO ut_gpio_regfile.sv `a965a5cb`；GPIO lint waivers/synth target+lint review
  +watchdog tc_fault UVM manifest）；skills（1 commit：ip-dev-suite 结构化参数契约与
  param-space 验证改进）；workflow（1 commit：docs/cbb_repo_diff.md CBB/IP 分类分析）。
  `make check`（ruff/schema parity/124 tests）与 `uv run pre-commit run --all-files`
  （11 hooks）全绿。构建/仿真产物（.log/.vcd/csrc/simv 等）经各仓 .gitignore 屏蔽未入库；
  reports 质量证据沿用仓内跟踪先例提交。期间 watchdog tc_fault UVM 回归在后台运行持续产生
  reports/uvm 时间戳目录，等回归结束后补交其 manifest 作为证据。
  注意：`aix repo commit/push` 必须在 workflow 根执行（子仓内执行报 manifest not found）；
  子仓内 `git add` 属例外的暂存操作（aix repo commit 不自动 add）。
  收尾 `aix repo status` 确认其余 9 仓 clean + remote sync；ip 仓遗留 dirty 系另一个并行
  codex agent 会话正在该仓活跃开发（GPIO 单测/synth 脚本、watchdog lint 约束、
  apb_secure_demux quality 报告等持续写入，mtime 距检查仅数十秒），属未完成中间状态，
  本任务不代为提交，由该会话完成后自行提交推送。

- `2026-09-10` | **workflow / 全仓提交推送** | submit all to GitHub：skills、cbb、ip、vip、
  workflow 五仓全部 commit + push 到 origin/main | PASS |
  workflow 五仓全部 commit + push 到 origin/main | PASS |
  skills（2 commits：suite 校准/AHB findings/SPI 优化报告 + SAF-005 回顾，head `0874bb0bf76f`）；
  cbb（3 commits：packet_locking_arbiter + lockstep_comparator 新增、SAF-005 质量证据与
  结构检查、PPA 更新，head `ac34181283d2`）；ip（2 commits：spi_master 全生命周期 G0-G5
  交付 + watchdog 契约更新，head `fb403e8a8e26`）；vip（1 commit：AHB VIP 全套交付，
  head `ac4bfad02ce2`）；workflow（1 commit：pyproject+uv.lock 依赖锁定，head 已推送）。
  `make check`（ruff/schema parity/124 tests）与 `uv run pre-commit run --all-files`
  （11 hooks）全绿。构建产物（simv.daidir/csrc/.alib/SpyGlass DB）经各仓 .gitignore
  屏蔽未入库；待添加文件核查无凭据、无 >1MB 文件。收尾 `aix wf status` 11 仓全部
  clean + remote sync。全部 git 操作经 `aix repo status/diff/commit/push` 执行。

- `2026-09-10` | **workflow / 协作文档** | 核对 Manifest、三条 Flow、六类核心资产仓和 canonical suite；新增架构、仓库与技能地图、交付流程、操作手册、当前限制五篇文档及三张 Mermaid 图，更新导航 | PASS |
  `docs/index.md` 为入口；11 个 Markdown 文件、109 个本地链接及代码围栏检查无错误；
  `make check`（根既有 uv 环境、`--no-sync`）通过：ruff、6 个 Schema parity、124 项测试；
  `pre-commit run --all-files` 全通过。未重新同步依赖或证明 lock 安装一致性，未运行领域 EDA。
  doctor 通过；IP/CBB/SoC preflight 均因 required 领域 provider 未注册而 BLOCKED，已如实记录。
  初始普通 git status 仅用于读取工作方法前的只读基线诊断；后续正式状态经 aix。
  沙箱 uv 输出后收尾阻塞，经授权在沙箱外完成诊断与验证；未修改资产仓实现、未提交或发布。

- `2026-09-10` | **workflow / 全仓提交准备** | 用户授权将全部改动提交到 GitHub；
  范围为 skills、cbb、ip、workflow，各仓保留 main 分支，使用 aix repo commit/push。
  make check、IP/CBB 106 项回归、两套 suite validator、CBB/IP 索引和 README 同步检查通过。
  IP SEC-015 仍有 planned 包名称/版本一致性警告，不提升交付状态。
  普通 git diff/ls-files 仅补充 aix diff --stat 未提供的内容审阅、未跟踪文件明细和空白检查。

- `2026-09-10` | **skills / IP suite 复查** | 先记录六项改进，再统一修复日志判定、
  运行退出状态、超时输出、参数传递和触发范围；补负向回归，重新物化 | PASS |
  suite validator 24 skills / 0 errors；scripts/tests 88 passed；make check 与
  pre-commit 全通过。改进与结果见 skill repo
  `skills/ip-development-suite/docs/review-2026-09-10.md`。
  初始普通 git status 仅用于加载工作方法前的只读诊断；后续状态和差异使用 aix。
  沙箱 uv 收尾阻塞，经批准在沙箱外重跑检查，正常退出；保留已有未提交改动。

---

- `2026-09-08 03:18:28` | **skill-repo / ip-development-suite** | 固化核心原则 1：
  Markdown 是人和 Agent 的唯一设计事实源（Design Source of Truth），
  YAML/JSON/RTM 均为 extractor 自动抽取的派生数据 | PASS |
  源仓 `aixsilicon_skill_repo` commit `489b4e245efe`；
  修改 10 个 Markdown 文档（SKILL.md、artifact-contract.md、README.md、glossary.md、
  01-lrs/03-hld/05-lld/06-verification/07-rtl/16-trace 子 skill）
- `2026-09-08 03:18:45` | **workflow / 物化** | `bootstrap.py --ensure` 重新物化
  skills 到 `.roo/skills/`（源仓 head 已更新，指纹变化触发全量复制） | PASS |
  materialize OK 11 skill(s)
- `2026-09-08 03:15:42` | **workflow / 校验** | `validate_suite.py` 于源仓执行：
  仅存预先存在基线差异（expected 23 SKILL.md files, found 26；05-lld 536 行警告），
  与本次改动无关 | INFO | 源仓基线 pre-existing
- `2026-09-08 03:16:13` | **workflow / 校验** | `pytest scripts/tests` 全绿 | PASS |
  19 passed
- `2026-09-08 03:31:04` | **skill-repo / ip-development-suite** | 固化核心原则 3：
  四份文档职责边界切干净（LRS=WHAT / HLD=ARCH / LLD=HOW / VPLAN=HOW TO VERIFY）。
  修复越界：LRS 5.4 子模块划分→功能能力概述；HLD 16.2 RTL 实现约束→架构级约束、
  17 删除断言建议；LLD 7.2 验证要点→设计验证关注点（给 VPLAN）、附录D 验证用例→
  关注点摘要、修复 06_verification.md 断链；VPLAN 补充不包含 RTL 实现设计声明 | PASS |
  源仓 commit `346495f569fd`；9 个 Markdown 文档
- `2026-09-08 03:31:12` | **workflow / 物化** | `bootstrap.py --ensure` 重新物化
  skills（源仓 head 更新触发全量复制） | PASS | materialize OK 11 skill(s)
- `2026-09-08 03:30:41` | **workflow / 校验** | `pytest scripts/tests` 全绿；
  `validate_suite.py` 仅存预先存在基线差异（expected 23 found 26），与本次改动无关 | PASS |
  19 passed
- `2026-09-10 07:58:00` | **workflow / 提交推送** | 全仓变更提交并推送 GitHub：
  - `ip`（388 文件）：memory_protection_controller 全生命周期交付 G0–G5 + MPC .gitignore
    屏蔽 Verdi/VCS 产物（AN.DB、ucli.key、vc_hdrs.h、csrc）+ 清理 ips/ 根旧占位 .MD；
    commit `50f9f1561f38` → origin/main
  - `skills`（118+1 文件）：ip/vip suite 演进（python-hw-ir 生成器、render_dc_setup、
    analyze_sweep、qualify.py、模板精简）+ cbb suite weighted_rr_arbiter 反查记录；
    门禁 pytest 52+6 全绿、validate_suite.py 通过；commit `6457d01f206a`、
    `a773a9ce17fc` → origin/main；物化 11 skills
  - `workflow`（1 文件）：根 .gitignore 屏蔽 novas.conf/novas.rc/AN.DB/ucli.key 等
    EDA 产物；门禁 `make check` 全绿（ruff + schema 同步 + 104 pytest）、
    `pre-commit run --all-files` 全绿；commit `dc4e037` → origin/main
    （连同此前本地领先的 4 个提交一并推送）
  - 诊断豁免说明：变更甄别阶段使用普通 `git status/check-ignore/log` 只读命令
    （`aix repo status` 无法展开 untracked 明细、`aix repo shell` 为交互式），未做写操作；
    commit/push 全部走 `aix repo commit|push` 入口 | PASS |
    最终 `aix wf status`：10 仓 clean，remote 全部 sync

- `2026-09-10 08:45:08` | **workflow / 本地清理** | 将 218 组 smoke/ctl-test/sec-flow 测试残留及根 `.pytest_cache/`、`__pycache__/` 归档到 `tmp/cleanup-20260910T084508Z/`；原路径与报告 SHA-256 记录于该目录 `manifest.json`，移动后核验哈希。保留审查报告、`.venv/`、`repos/`、`.aix/`、Skill 运行目录及安装元数据。修复 canonical workflow tests 中 13 个 runner 测试的工作目录隔离，重新物化；Makefile 集中缓存输出 | PASS | `make check` 通过（ruff、6 个 schema、124 个测试）；普通 Git 只读诊断用于展开父仓文件及忽略明细，aix CLI 不提供这些明细，未执行 Git 写操作
- `2026-09-10` | **workflow / 清理复核** | `pre-commit run --all-files` 全绿；归档与缓存均被 Git 忽略；完整测试后 `reports/` 仅保留套件审查报告，根 `.pytest_cache/`、`__pycache__/` 未再生成，`.venv/bin/python` 仍可用 | PASS | 沙箱 hook 停滞后在获批环境完成检查

- `2026-09-10` | **skills / chipdraw-skill-suite** | 修复 canonical 绘图套件的错误阻断、QA 状态、适配器、视图投影、多视图报告、Manifest diff、wheel 资源打包与技能入口；共享 uv 环境安装 chipdiagram。新增 20 项回归（共 71），5 个 SKILL 校验通过，24 个视图生成检视。补充物化忽略 node_modules，避免复制依赖树；workflow make check 125 测试通过。完整工程验收仍受真实 PDK/Xschem/ngspice、Draw.io 导出工具和原始建设方案缺失限制，未标记全部功能 verified | PARTIAL | 证据 `reports/chipdraw-acceptance/`；make / pre-commit 通过 uv 选定的根解释器执行，解决嵌套 uv 子命令退出停滞，未跳过 hook。普通 Git 仅一次只读检查父仓是否有意外变更，主状态与 diff 证据仍使用 aix；未提交或推送，保留其他技能已有变更。

- `2026-09-10` | **skills / chipdraw 后端复核** | 完成 WaveDrom 3.2.0 本地安装和依赖锁定；APB 示例真实导出 WaveJSON/SVG/PNG，ERROR=0、WARNING=0；FSM 与 APB PNG 已打开检视。工程 PDK/Xschem/ngspice 与 Draw.io 导出验收仍未完成 | PASS（时序导出） | `reports/chipdraw-acceptance/timing-export.log`

- `2026-09-10` | **skills / chipdraw 中等复杂度用例测试** | 新建架构级异步 DMA 测试规格（128→32 位、双时钟域、3 FIFO、寄存器、流水线、CDC/RDC、安全机制），通过真实 CLI 抽取 SystemRDL 并生成 7 个视图；17 项检查中 14 通过、3 失败。发现虚假转换器引用和 FIFO/通路位宽不匹配漏检，以及 FIFO 图缺少深度/位宽标签；再次运行复现相同结果。未修改技能源，未把草稿绘图结果视为硬件签核 | FAIL（3 项） | `reports/chipdraw-medium-dma/report.md`、`run_case.py`、`latest.json` 与独立 runs 目录保存输入、命令日志、产物和哈希。

- `2026-09-10` | **chipdraw / 测试 PNG 统一输出** | DMA 两次测试运行的 20 个已生成图数据统一导出 PNG；最新图册包含正常用例 7 张及错误注入/版本变体 3 张。基于原 graph.json 使用 Graphviz 渲染，逐图验证可解码、尺寸与 SHA-256，打开检视数据通路图。测试脚本已接入自动 PNG 输出，报告入口改为 PNG；原测试 3 项失败结论保持不变 | PASS（PNG 导出） | `reports/chipdraw-medium-dma/png-gallery.html`、`png-gallery.md`、`export_png.py` 与各运行 `png-manifest.json`

- `2026-09-10` | **skills / chipdraw 固定 PNG 契约** | 全图型统一强制输出 diagram.png；缺失、损坏、旧文件不能满足构建，纳入 Manifest 与哈希。增加确定性 Graphviz/Pillow 后备渲染及 Pillow 完整解码校验，更新全部技能入口与 CLI 格式说明。套件 80 项测试通过；24 视图 PNG 解码/哈希通过；DMA 10 PNG 通过，原有 3 项功能失败保留 | PASS（PNG） | `reports/chipdraw-required-png/report.md`；完成物化，make check（125 测试）与完整 pre-commit 检查，未提交或推送。

- `2026-09-10` | **skills / chipdraw 两个精选框图** | 根据用户反馈将展示收敛为 SoC 总览、IP 数据通路两例，重写 canonical YAML；SoC 分区及总线层次清晰，IP 独立读写通路，明确单时钟 payload 范围。修复孤立元数据投影、FIFO 参数标签，补充分组与正交 PNG 渲染。两张 PNG 打开检视并核验解码/Manifest 哈希，82 项套件测试通过；make check 125 项与完整 pre-commit 通过，已物化 | PASS（示例绘图） | `reports/chipdraw-showcase/index.html`、`review.md`；保留 IP 未绑定 RTL 警告，不声明硬件签核，未提交/推送。
