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

## 2026-09-13 IP/CBB 分类与管理清理

- 用户授权：按 tmp/ip_cbb_cleanup 原则及指导 YAML 整理 IP/CBB；补充强调由各 development-suite 主要管理。
- IP 355→292，CBB 410→298；APB 完整工程及 diversity comparator 契约迁仓，原实现/文件保留；退出记录与历史编号写入各资产仓 governance。
- 两仓 registry 统一编辑入口；canonical IP/CBB Skill、artifact contract、IP 00-workspace、CBB scaffold 与交接回归同步修改并重新物化。
- 验证：两套 Suite 测试/自检、registry/README、APB VCS 功能与变异回归、37 个受版本控制文件的字节一致性、make check、pre-commit 均通过。
- 临时诊断说明：发现根 AGENT.md 之前直接读取过子仓 git status；之后以 aix wf/repo status/diff 为状态证据。文件迁移完整性使用只读 git ls-tree/show（aix 无 Git blob 清单与读取接口），结果在 tmp/ip_cbb_cleanup/audit。
- 存量差异：两个 planned IP 的包身份警告、旧 axi_mpu Core 格式及本地 build 重复 Core；详见各仓 docs/cleanup-validation.md。未提交、推送或发布。

## 2026-09-13 过时材料与 CBB 报告边界复查

- 按用户要求归档 IP plan.md、空 OpenTitan 清单及 89 个已退出规划的纯空占位目录，恢复位置写入治理记录；有实质内容的工程保留。
- 归档 CBB 旧初始化脚本，旧入口仅报退役并返回 2；更新过时说明。将 CBB Skill 的旧 plan/design 移出 Skill 发布树，导航和校验指向现行合同。
- 用户指出 CBB 仓根 reports 泄漏：其混合运行日志逐字节归档至该仓 docs/archive/2026-09-ip-cbb-cleanup/repository-root-reports。
- 修复根因：log 不再默认 workspace=.；log/gate 写前校验具体 CBB 身份、登记路径和报告符号链接；registry 检查拒绝根 reports。Skill 合同区分仓根 --root 与工程 --workspace。
- CBB 全部 42 个测试通过（含新增报告边界回归），IP/CBB 套件自检和 registry/README 检查通过；canonical Skill 已重新物化。未修改 RTL 或提升 Gate，未提交推送。

## 2026-09-13 CBB 全量需求合同与 AXI 归属修正

- 按用户要求为当前 297 个 CBB 建立目录和需求合同：287 份规划草案、10 份现有 YAML 派生视图，统一 README 入口和 docs/requirement-contracts.md 导航。未生成占位 RTL 或提升实现/Gate 状态。
- 单通道 axi_channel_register_slice 按明确指示由 CBB AXI-001 迁入 IP MIG-IP-AXI-001，现 IP 293 条；原 ID 保留退出记录，两套 Skill 同步归属规则。
- 仓内新增只读合同覆盖/身份/源哈希校验并接入手动 CI；新增 5 项缺失/错配/源漂移/阶段交接回归。两 Suite 联合测试通过（272 passed, 1 skipped），registry/README 和套件自检通过，canonical 技能已物化。
- 已有工程文件按 Git HEAD 逐字节核对（README 和需求合同除外）；证据 tmp/cbb_requirements/preserved-files.json。popcount 的历史 profiles.yaml 存在未引用冒号导致的 YAML 语法问题，本轮合同仅派生 cbb/params/behavior，不据此宣称配置或 Gate 完成。未提交或推送。
- 收尾验证：make check（125 项 workflow 测试）与 pre-commit 全部通过。

## 2026-09-13 IP Suite 第一批 F01–F06：门禁真实性与证据保留

- 用户授权实施第一批 F01–F06；canonical 新增设计新鲜度/评审绑定、RTL 真实执行与摘要、模块 UT 源集合、文档/PPA 原始证据及内容寻址保留；quality/proof/release 消费者接入，已重新物化。
- 原评估反例在独立报告目录重跑，相关门禁均拒绝；有效完整样例 G0–G5 通过，清理 build、正式 ZIP 打包并迁移解包后重审结果一致。
- 验证：IP 211 passed / 1 skipped（商业 VCS）；工作区 make check（125 项）、完整 pre-commit、24 Skill 自检、quick_validate 和新增 Python Ruff F/E9 均通过。
- 环境诊断：沙箱内 uv 未回收已结束子进程；沙箱外探针及检查正常退出，经自动审批完成同一根 uv 环境检查。未创建第二环境。
- 保留原评估材料；skills 状态/差异通过 aix repo 获取。工作区有已有及并行 CBB/资产治理改动，本批不回滚或提交它们。无真实 IP 审批、提交、推送或发布；临时 Git 提交仅用于隔离发布测试夹具。
- 报告与证据：reports/ip-development-suite-f01-f06-2026-09-13/实施报告.md。

## 2026-09-13 CBB Suite F06–F12 优化实施

- 用户授权继续剩余优化项；修改 canonical CBB Skill 和 workflow ownership-map 的 CBB 包路径。
- 完成纯 YAML 计划、compact 文档/按族骨架、自动执行事件与哈希缓存、单点 PPA、工具 profile 能力 smoke、Formal 非空/有界判定、阶段一致性校验。
- 保留已有改动，不提交或推送。仅生成实施报告和测试证据，不对真实 CBB 作资格提升。
- 环境沿用 uv 管理的根 .venv；此前 uv 启动器发生等待，本轮直接调用该解释器。临时根 git status 仅作定位，正式状态证据用 aix repo。
- 最终验证和 pre-commit 等效入口的细节见 reports/cbb-skill-f06-f12-2026-09-13/report.md。

## 2026-09-13 CBB Skill 历史材料清理

- 用户授权清理/归档；将套件 docs 下 5 份历史报告移至 skill repo docs/archive/2026-09-cbb-suite/reports，修正相对链接并保留历史待办，不视为关闭。
- 删除限定于该 canonical 套件的 39 个生成型 Python 缓存文件；保留现行脚本、测试、规则和模板。
- 更新 README 与归档索引；重新物化，检查执行入口无归档依赖。清单与检查日志见 reports/cbb-suite-cleanup-2026-09-13/。

## 2026-09-13 IP Suite 剩余优化（主流程保持）

- 按用户要求继续完成主流程之外的优化：F07/F08/F15 契约修复，F09 RAL 生成与 G4 交接，F10 条件专项证据，以及 F13/F14/F16/F18 的字段视图、解析复用、PPA 固定版本与阶段内部执行续跑。
- lifecycle.yaml 与第一批基线 SHA-256 完全一致；未实施 F11 提前启动、F12 UT 裁剪、F17 oracle 策略变化或单点 PPA 签核放宽。
- 最终 IP 套件 243 项全部通过、0 跳过，本次新增合同用例 25 项。真实 VCS CSR W1C/字节使能/race/reset 仿真及 RAL package 编译通过；RAL 初次编译暴露 UVM 库顺序问题，已修正规范并复测。
- 工作区 make check 通过（125 项），24 Skill 自检无错误/警告，canonical 已物化；完整 pre-commit 日志与收尾校验保存在报告目录。
- 使用 workflow 根 uv 环境；沙箱外检查沿用已确认的 uv 回收问题处理方式。无真实 IP 审批或 Gate 提升，无提交、推送、发布；保留已有及并行改动。
- 报告：reports/ip-development-suite-remaining-2026-09-13/实施报告.md；含逐项完成/暂缓边界、真实工具日志、JUnit 与源码快照。

## 2026-09-14 IP Suite 历史材料清理

- 按用户授权将历史 docs/reports、演进路线、过时 evals 和离线 UVM 副本迁至 skill repo docs/archive/2026-09-ip-suite；178 个文件逐项校验 SHA-256、大小和权限，许可证及原始证据完整保留。
- 首次删除 59 个可再生缓存文件，收尾清除并行工作重建的 22 个缓存；移除退役 SpinalHDL 空目录。活动树为 192 个文件、1,618,344 字节。
- 本次只调整三个活动 Markdown 导航；保留现行脚本/测试/合同、主流程和共享工作区并行修改。canonical 经 bootstrap 物化，与分发副本逐文件一致。
- 回归 244 项全部通过（含 VCS，0 跳过）、24 Skill 自检、quick_validate、make check 通过；完整 pre-commit 结果随报告留存。根 uv 检查沿用沙箱外执行的既有环境处理方式。
- 报告：reports/ip-development-suite-cleanup-2026-09-13/清理报告.md。未提交、推送或发布。

## 2026-09-14 全仓提交推送 GitHub

- 用户指示 SUBMIT ALL TO GITHUB；状态证据：cbb（54 modified/deleted + 160 untracked）、ip（133 + 18）、skills（248 + 37）、workflow（2 modified），全部 aix repo status/diff 确认。
- cbb：requirement contracts 全量、IP/CBB 分类清理、报告边界修复与 adapters/registry 更新，`aix repo commit cbb` + push 成功。
- ip：planned-only 占位契约退役、axi_channel_register_slice 迁入、GPIO 证据流水线与 registry 脚本整合，`aix repo commit ip` + push 成功。
- skills：cbb/ip suite F01-F18 优化、requirement contracts、workflow policy 与证据强化，历史材料归档，`aix repo commit skills` + push 成功。
- 父仓：ownership-map.yaml 的 CBB allowed_paths 更新为 components/adapters；提交前 make check（125 项测试、ruff、schema parity）与 `uv run pre-commit run --all-files`（11 hooks）全部通过。
- 临时诊断说明：`aix` 无逐文件 diff 渲染接口，使用只读 `git status --porcelain` 查看变更明细；`pre-commit` 不在 PATH，改用 `uv run pre-commit`，未绕过任何门禁。
- 最终 `aix wf status` 全部 10 子仓 clean/sync，workflow 父仓提交推送完成。

## 2026-09-14 第二轮全仓提交与 139MB 证据内容审查

- 用户再次指示 SUBMIT ALL；cbb（constant_multiplier 全量 G0–G5 交付：model/profiles/trace/tools/verification/formal/PPA/quality）、ip（GPIO 全流程：UVM env/th/tc、synth/signoff/evidence 193 个内容寻址对象）、skills（pass_with_condition 门禁、release conditions、证据强化）三仓分别 commit+push 成功，全部 clean/sync。
- 用户质疑 ip 仓 139MB 内容是否为运行中间件；逐项分析如下（证据：reports/evidence/index.json，schema ip-retained-evidence/1.0，204 条目/238 对象/106.0MB）：
  - 38.58MB×2 = `build/ppa/n32_100mhz_*/synth.log`（12a7d930…）与 `reports/synth/fullflow_combined.log`（c4cf90b6…）：后者是前者的超集（前缀逐字节相同 + 约 2.9KB DC 尾部），为同一 DC run 的单步与 combined 两种身份重复保留，占总量 77MB/73%。
  - 1–5.4MB×13 = VCS UVM run manifest（fuseoc/uvm-vcs 索引文件，每 run 约 1.2MB×8）与覆盖率 urgReport 明细（modinfo/mod*.html×5）；其余 188 个对象共 3.6MB，为结构化 JSON/YAML 签核报告与解析器输出，属合理审计证据。
  - 判定：非"运行中间件数据库"（build/ 波形/EDA 库均被 .gitignore 拦截），而是 IP suite 证据保留合同（gate-evidence-retention.md）按设计复制"报告引用的日志闭包"；但大 EDA 日志以两种身份重复保留确有优化空间。
- 用户决定：方案 1 保持现状不动历史，仅评估政策改进建议。评估结论（供后续批次采纳，本批不实施）：
  - evidence_store.py 增加"同前缀超集检测"：新保留对象与已有对象 >10MB 且前缀相同时，保留 combined、单步日志以 offset/长度区间引用，预计可省约 38MB/次全流程；
  - index.json 对 >10MB 对象增加 `large: true` 标注与保留理由字段，供打包检查与人工审查显式豁免；摘要化（head/tail）违反现行"原始日志不改 SHA"合同，不建议；
  - 签核流程侧：synth 证据统一引用 combined 单一身份，避免同 run 双身份入库。
- 大文件均低于 GitHub 100MB 单文件限制，推送无阻断；未重写历史、未 force-push。
