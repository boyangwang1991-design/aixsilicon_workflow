# AIXSILICON 统一 Todo 台账

更新时间：2026-08-17。本文是全部活动任务状态、负责人、日期、Evidence、下一动作和阻塞的唯一事实源。任务定义、依赖和验收条件仍在各仓 `delivery.md`；跨仓顺序见 [`roadmap.md`](roadmap.md)，里程碑汇总见 [`progress.md`](progress.md)。

## 1. 维护规则

- 状态只在本文件更新；`delivery.md` 不再保存状态；
- `in-progress` 必须同时有具体负责人或已批准责任角色、目标日期和下一证据动作；
- `blocked` 必须填写阻塞原因、解除条件、解除 Owner 和复审日期；
- `done` 必须填写 PR/SHA/run-id/Evidence/Release 链接之一，不能只写文字结论；
- `deferred` 必须绑定重新评审里程碑，未到触发点不得暗中启动；
- 每周更新本表，每两周按 Roadmap 里程碑评审；完成项在 Evidence 稳定后移入 Git/Release 历史。

状态：`planned`、`in-progress`、`blocked`、`done`、`deferred`。每个阶段标题中的目标日期默认适用于该阶段全部任务；如需单独调整，在“下一动作 / 阻塞”中记录覆盖日期。目标日期按当前 Roadmap 建议窗口初始化，方案批准日期变化时整体重排。

## 2. 当前执行队列

| 顺序 | 任务 | 当前动作 | 出口 |
|---|---|---|---|
| 1 | WF-001 | ✅ 决策完成（2026-08-17） | ADR-0007 已接受（含 REV-1/REV-2），证据见 `evidence/profile-diff.md` |
| 2 | WF-003 | ✅ 决策完成（2026-08-17） | ADR-0008 已接受（含 REV-1/REV-2/REV-3），证据见 `evidence/action-inventory.md` |
| 3 | M0 Findings 审核 | ✅ 完成（2026-08-17） | F-001～F-013 已逐项确认 Owner/关闭阶段/关联任务，见 `docs/findings.md` §6 |
| 4 | WF-002（M1） | ✅ 完成（2026-08-17） | exact Profile + typed DAG/closure 已实现并测试通过（`tests/unit/test_exact_profile.py`，65 项测试全绿） |
| 5 | WF-004 / TOOL-001（M1） | ✅ 完成（2026-08-17） | capability registry + preflight 已实现（`src/aixworkflow/capability.py`），preflight CLI 接入 `aix wf` |
| 6 | WF-005～007、WF-011～012、TOOL-003/004（M1） | ✅ 完成（2026-08-17） | runner fail-closed/控制语义 + Lock/Evidence 增强 + 退出码/安全 + 跨平台入口均已实现，95 项测试全绿 |

WF-001～WF-007、WF-011/WF-012 及 TOOL-001/003/004 已全部实现（2026-08-17）；M1 剩余：SKILL-001/002、KNOW-001～003（P1 可选），以及 M2 APB 穿刺。

## 3. M0 — 方案与决策冻结（目标 2026-08-28）

| ID | P | 任务 | 定义 | 状态 | 负责人 | Evidence | 下一动作 / 阻塞 |
|---|---|---|---|---|---|---|---|
| WF-001 | P0 | 审核 ADR-0007 | [workflow](workflow/delivery.md) | `done` | boyang wang | ADR-0007 accepted（2026-08-17，REV-1/REV-2）；[`evidence/profile-diff.md`](evidence/profile-diff.md) | 移交 WF-002 实施 exact Profile + typed DAG/closure 测试 |
| WF-003 | P0 | 审核 ADR-0008 | [workflow](workflow/delivery.md) | `done` | boyang wang | ADR-0008 accepted（2026-08-17，REV-1/REV-2/REV-3）；[`evidence/action-inventory.md`](evidence/action-inventory.md) | 移交 WF-004/TOOL-001 实施 action inventory + capability registry + preflight |

## 4. M1 — 控制面安全底座（目标 2026-09-25）

| ID | P | 任务 | 定义 | 状态 | 负责人 | Evidence | 下一动作 / 阻塞 |
|---|---|---|---|---|---|---|---|
| WF-002 | P0 | exact Profile、有类型依赖与 v1 兼容 | [workflow](workflow/delivery.md) | `done` | boyang wang | exact Profile + typed DAG/closure 实现（[`tests/unit/test_exact_profile.py`](tests/unit/test_exact_profile.py)，2026-08-17，65 项测试全绿） | 移交 WF-004/TOOL-001；后续 WF-006 复用 typed deps 计算操作闭包 |
| WF-004 | P0 | capability registry、provider metadata、preflight | [workflow](workflow/delivery.md) | `done` | boyang wang | [`../src/aixworkflow/capability.py`](../src/aixworkflow/capability.py)（6 态 + preflight），2026-08-17；[`../tests/unit/test_capability.py`](../tests/unit/test_capability.py) | 移交 TOOL-001 实现公共包 provider metadata |
| WF-005 | P0 | runner 控制语义与安全边界 | [workflow](workflow/delivery.md) | `done` | boyang wang | runner fail-closed/required 阻断/timeout/retry/write_scope（2026-08-17）；[`../tests/unit/test_runner_controls.py`](../tests/unit/test_runner_controls.py) | 覆盖 F-001/F-002/F-007 负向矩阵 |
| WF-006 | P0 | Lock、Run Manifest、Evidence 契约 | [workflow](workflow/delivery.md) | `done` | boyang wang | Run Manifest 增 provider/tool/env/hash；Lock tools 段生成（2026-08-17） | 复用 typed deps 计算操作闭包 |
| WF-007 | P0 | 退出码与失败分类 | [workflow](workflow/delivery.md) | `done` | boyang wang | 退出码分段契约测试（[`../tests/unit/test_security.py`](../tests/unit/test_security.py)），2026-08-17 | 对齐 CLI/Tool/Flow 契约 |
| WF-011 | P1 | Windows/POSIX、UTF-8、离线检查入口 | [workflow](workflow/delivery.md) | `done` | boyang wang | Makefile/pre-commit 跨平台入口 + UTF-8 修复（F-013，2026-08-17）；pre-commit 11/11 全绿 | 双平台 clean-environment 记录 |
| WF-012 | P1 | 受控 PR、凭据和权限负向测试 | [workflow](workflow/delivery.md) | `done` | boyang wang | 事件循环 guard/secret redaction/force-push 拒绝（[`../tests/unit/test_pr_controls.py`](../tests/unit/test_pr_controls.py)），2026-08-17 | 冻结最小权限语义 |
| TOOL-001 | P0 | 公共包 provider metadata/capability | [tools](tools/delivery.md) | `done` | boyang wang | capability registry 契约（2026-08-17）；inventory 见 [`../evidence/action-inventory.md`](../evidence/action-inventory.md) | tool_repo 落地 provider metadata |
| TOOL-003 | P0 | 锁定包、外部工具、容器/EDA | [tools](tools/delivery.md) | `done` | boyang wang | Lock tools 段 schema/生成（2026-08-17） | 工具版本/hash 重放用例 |
| TOOL-004 | P0 | 工具退出码、参数和路径安全 | [tools](tools/delivery.md) | `done` | boyang wang | 参数/路径/越界负向测试（[`../tests/unit/test_security.py`](../tests/unit/test_security.py)），2026-08-17 | 注入/缺依赖测试设计 |
| SKILL-001 | P1 | Suite validator 与脚本单测 | [skills](skills/delivery.md) | `planned` | boyang wang | — | 指派负责人；建立可复现 Python 环境 |
| SKILL-002 | P1 | Context Pack/Change Plan/Skill Result | [skills](skills/delivery.md) | `planned` | boyang wang | — | 对齐 WF-006 与 ownership scope |
| KNOW-001 | P1 | 术语、metadata、来源和敏感分级 | [knowledge](knowledge/delivery.md) | `planned` | boyang wang | — | 提交 Schema/模板/负向样例评审 |
| KNOW-002 | P1 | 活动主题 Owner/Reviewer/复审日期 | [knowledge](knowledge/delivery.md) | `planned` | boyang wang | — | 建立无人负责内容清单并分配角色 |
| KNOW-003 | P1 | 可搜索知识索引 | [knowledge](knowledge/delivery.md) | `planned` | boyang wang | — | 定义 10 个检索用例和断链/重复检查 |

## 5. M2 — APB 最短穿刺（目标 2026-10-23）

| ID | P | 任务 | 定义 | 状态 | 负责人 | Evidence | 下一动作 / 阻塞 |
|---|---|---|---|---|---|---|---|
| HWIF-001 | P0 | 冻结 APB Contract/Profile/Binding | [hwif](hwif/README.md) | `planned` | boyang wang | — | 选定 APB3/APB4 profile；提交正负样例 |
| HWIF-002 | P0 | 生成三视图与 drift check | [hwif](hwif/README.md) | `planned` | boyang wang | — | 依赖 tools provider；冻结输入/输出 hash |
| IP-001 | P0 | APB IP 规格、SystemRDL、验收矩阵 | [ip](ip/delivery.md) | `planned` | boyang wang | — | 依赖 HWIF-001；冻结 CSR/功能/负向范围 |
| IP-002 | P0 | 生成 RTL/RAL/Header/Core | [ip](ip/delivery.md) | `planned` | boyang wang | — | 依赖 IP-001/TOOL-002；建立 drift 负向样例 |
| DV-001 | P0 | Run/Test/Failure/Metric Schema | [dv-common](dv-common/delivery.md) | `planned` | boyang wang | — | 与 WF-006 对齐版本和退出语义 |
| DV-002 | P0 | RAL base 与 P0 CSR sequences | [dv-common](dv-common/delivery.md) | `planned` | boyang wang | — | 覆盖 RW/RO/W1C/reset/非法地址 |
| DV-003 | P0 | clock/reset/timeout/watchdog 服务 | [dv-common](dv-common/delivery.md) | `planned` | boyang wang | — | 建立 reset epoch/并发/timeout 单测 |
| DV-004 | P0 | APB IP 穿刺适配 | [dv-common](dv-common/delivery.md) | `planned` | boyang wang | — | 依赖 DV-001～003/VIP-001；输出标准 Result |
| VIP-001 | P0 | APB VIP MVP | [vip](vip/delivery.md) | `planned` | boyang wang | — | 完成 driver/monitor/checker/coverage/negative/RAL |
| VIP-002 | P0 | 故意违规负向套件 | [vip](vip/delivery.md) | `planned` | boyang wang | — | 定义每类协议错误和预期 Failure Signature |
| TOOL-002 | P0 | schema/hwif/reg/core 接入 APB Flow | [tools](tools/delivery.md) | `planned` | boyang wang | — | 依赖 TOOL-001/WF-004；首次真实 provider 调用 |
| CAT-001 | P0 | Catalog asset/lifecycle/compatibility Schema | [catalog](catalog/delivery.md) | `planned` | boyang wang | — | 冻结发布索引最小字段和负向迁移样例 |
| CAT-003 | P0 | APB HWIF/VIP/IP 条目模板 | [catalog](catalog/delivery.md) | `planned` | boyang wang | — | 对齐 Release/Evidence/SBOM/RTM 字段 |
| CAT-004 | P0 | Catalog diff/PR 接口 | [catalog](catalog/delivery.md) | `planned` | boyang wang | — | 冻结权限、幂等键、输入输出和失败语义 |
| KNOW-004 | P1 | APB 端到端知识路径 | [knowledge](knowledge/delivery.md) | `planned` | boyang wang | — | 以真实 APB 契约/Evidence 做技术评审 |

## 6. M3 — APB 完整资格（目标 2026-11-27）

| ID | P | 任务 | 定义 | 状态 | 负责人 | Evidence | 下一动作 / 阻塞 |
|---|---|---|---|---|---|---|---|
| HWIF-003 | P0 | APB VIP/IP/CBB 消费者联验 | [hwif](hwif/README.md) | `planned` | boyang wang | — | 固定各消费者 SHA 和兼容报告 |
| IP-003 | P0 | APB lint/build/unit/regression | [ip](ip/delivery.md) | `planned` | boyang wang | — | 固定 Lock；完成 G0～G6 和全部负向场景 |
| VIP-003 | P0 | APB VIP 达 V3 Qualified | [vip](vip/delivery.md) | `planned` | boyang wang | — | 在代表性 IP 上关闭回归/coverage/Evidence |
| WF-008 | P0 | APB Flow action/Gate/write scope/Evidence | [workflow](workflow/delivery.md) | `planned` | boyang wang | — | M2 启动；完成故障注入且无 false green |
| DV-005 | P1 | 第二消费者与 API/SemVer 兼容 | [dv-common](dv-common/delivery.md) | `planned` | boyang wang | — | 选择第二消费者并建立 deprecated 测试 |
| SKILL-003 | P1 | 8 个端到端 Eval 与安全负向 | [skills](skills/delivery.md) | `planned` | boyang wang | — | 依赖 SKILL-001/002；保存失败样本与评分 |
| SKILL-004 | P1 | APB Author/Verifier 双角色 | [skills](skills/delivery.md) | `planned` | boyang wang | — | 禁用 Skill 仍可运行；候选变更经 G0～G6 |

## 7. M4 — 协作与发布（目标 2026-12-25）

| ID | P | 任务 | 定义 | 状态 | 负责人 | Evidence | 下一动作 / 阻塞 |
|---|---|---|---|---|---|---|---|
| WF-009 | P0 | Change Bundle 状态机与 PR HEAD 联验 | [workflow](workflow/delivery.md) | `planned` | boyang wang | — | 建立多 PR checkout/CI/merge-order E2E |
| WF-010 | P0 | approval/G7/Tag/Release/Catalog PR | [workflow](workflow/delivery.md) | `planned` | boyang wang | — | 依赖 WF-009/CAT-004；完成幂等/恢复测试 |
| CAT-002 | P0 | 清查现有 Catalog 条目 | [catalog](catalog/delivery.md) | `planned` | boyang wang | — | 标记可追溯、legacy 或 unverified |
| CAT-005 | P1 | resolve/compatibility 检查 | [catalog](catalog/delivery.md) | `planned` | boyang wang | — | 覆盖冲突/yanked/不兼容负向用例 |
| CAT-006 | P0 | Release→Catalog PR 闭环 | [catalog](catalog/delivery.md) | `planned` | boyang wang | — | 验证不直写 main、审批、幂等和恢复 |
| IP-004 | P0 | APB IP 发布与 Catalog 登记 | [ip](ip/delivery.md) | `planned` | boyang wang | — | 生成 G7/Tag/Release/SBOM/RTM/Catalog PR |
| IP-005 | P1 | ipkg/Core/Release 边界 | [ip](ip/delivery.md) | `planned` | boyang wang | — | 收敛 auto-push、legacy VLNV 和双事实源 |
| HWIF-004 | P0 | 发布 APB 接口资产 | [hwif](hwif/README.md) | `planned` | boyang wang | — | 形成 SemVer/Tag/Release/Catalog/Evidence |
| VIP-004 | P1 | 发布 APB VIP | [vip](vip/delivery.md) | `planned` | boyang wang | — | 登记兼容/能力矩阵和已知限制 |

## 8. M5 — CBB 产品化（目标 2027-02-19）

| ID | P | 任务 | 定义 | 状态 | 负责人 | Evidence | 下一动作 / 阻塞 |
|---|---|---|---|---|---|---|---|
| CBB-001 | P0 | metadata/params/result/PPA Schema | [cbb](cbb/delivery.md) | `planned` | boyang wang | — | M4 后启动；冻结 Schema/成熟度/版本策略 |
| CBB-002 | P0 | arbiter 示范构件 | [cbb](cbb/delivery.md) | `planned` | boyang wang | — | 参数边界、属性/随机、PPA 和消费者证据 |
| CBB-003 | P0 | ready/valid pipeline 示范 | [cbb](cbb/delivery.md) | `planned` | boyang wang | — | 延迟/吞吐/背压与 PPA sweep |
| CBB-004 | P0 | FIFO 示范闭环 | [cbb](cbb/delivery.md) | `planned` | boyang wang | — | depth/width/overflow/underflow/mapping/CDC |
| CBB-005 | P0 | CBB Action/Flow 验收契约 | [cbb](cbb/delivery.md) | `planned` | boyang wang | — | 从三个示范提炼参数/PPA/Gate 输入输出 |
| CBB-006 | P1 | 三示范 Release/Catalog | [cbb](cbb/delivery.md) | `planned` | boyang wang | — | 至少一个达到 C4，三个均达到 C3 |
| TOOL-005 | P1 | param-matrix/PPA provider | [tools](tools/delivery.md) | `deferred` | boyang wang | — | M4 出口后激活；支持三示范可重建 |
| WF-013 | P1 | CBB development/qualification Flow | [workflow](workflow/delivery.md) | `deferred` | boyang wang | — | M4 出口+CBB-005 后激活 |
| HWIF-005 | P1 | 按真实需求补 L0/L1 契约 | [hwif](hwif/README.md) | `deferred` | boyang wang | — | 有两个消费者或批准例外时激活 |
| SKILL-005 | P2 | CBB Suite | [skills](skills/delivery.md) | `deferred` | boyang wang | — | WF-013 稳定后复审，不复制 Tool |

## 9. M6 — 最小 SoC（目标 2027-04-02）

| ID | P | 任务 | 定义 | 状态 | 负责人 | Evidence | 下一动作 / 阻塞 |
|---|---|---|---|---|---|---|---|
| SOC-001 | P1 | 最小 SoC Schema | [soc](soc-integration/delivery.md) | `planned` | boyang wang | — | 冻结 instance/address/IRQ/CRG/connect 正负样例 |
| SOC-002 | P1 | 已发布 APB 资产最小 Golden | [soc](soc-integration/delivery.md) | `planned` | boyang wang | — | 依赖 Catalog resolve/IP C4 |
| SOC-003 | P1 | socgen/connect provider 契约 | [soc](soc-integration/delivery.md) | `planned` | boyang wang | — | 冻结生成区/手写区和 Result/Artifact |
| SOC-004 | P1 | 地址/IRQ/连接/接口负向检查 | [soc](soc-integration/delivery.md) | `planned` | boyang wang | — | 覆盖冲突/缺端点/不兼容 |
| SOC-005 | P1 | compile/sim/boot/baseline | [soc](soc-integration/delivery.md) | `planned` | boyang wang | — | 固定 Lock 形成 G0～G6 Evidence |
| TOOL-006 | P1 | socgen/connect provider | [tools](tools/delivery.md) | `deferred` | boyang wang | — | M4/Catalog 稳定后激活 |
| WF-014 | P1 | SoC provider 与 baseline Flow | [workflow](workflow/delivery.md) | `deferred` | boyang wang | — | SOC-001～004 和 WF-006 完成后激活 |
| SKILL-006 | P2 | SoC Suite | [skills](skills/delivery.md) | `deferred` | boyang wang | — | WF-014 稳定后复审，不复制 socgen |

## 10. M7 — 规模化与候选仓（M6 后重新排期）

| ID | P | 任务 | 定义 | 状态 | 负责人 | Evidence | 下一动作 / 阻塞 |
|---|---|---|---|---|---|---|---|
| CBB-007 | P1 | 按消费者扩种子池 | [cbb](cbb/delivery.md) | `deferred` | boyang wang | — | CBB-006 后逐项评审消费者/Owner/出口 |
| DV-006 | P2 | 扩 scoreboard/memory/fault 服务 | [dv-common](dv-common/delivery.md) | `deferred` | boyang wang | — | DV-005 后按两个消费者门禁评审 |
| VIP-005 | P1 | AXI4-Lite/Stream MVP 评审 | [vip](vip/delivery.md) | `deferred` | boyang wang | — | APB C4 和真实消费者出现后评审 |
| VIP-006 | P2 | 双 simulator/cocotb | [vip](vip/delivery.md) | `deferred` | boyang wang | — | 可用 provider 且不变成 required 时评审 |
| TOOL-007 | P2 | report/rtm/package/catalog 工具 | [tools](tools/delivery.md) | `deferred` | boyang wang | — | 有首个真实消费者且无重复能力时启动 |
| CAT-007 | P2 | deprecated/yanked/替代审计 | [catalog](catalog/delivery.md) | `deferred` | boyang wang | — | CAT-005 稳定后建立运营周期 |
| IP-006 | P2 | Bridge/PIC 下一切片评审 | [ip](ip/delivery.md) | `deferred` | boyang wang | — | APB C4、真实消费者和资源满足后评审 |
| KNOW-005 | P2 | MAC 完整案例 | [knowledge](knowledge/delivery.md) | `deferred` | boyang wang | — | Owner/工具环境和复现出口明确后启动 |
| KNOW-006 | P2 | 季度知识审计 | [knowledge](knowledge/delivery.md) | `deferred` | boyang wang | — | KNOW-002/003 完成后建立 SLA |
| KNOW-007 | P2 | 按需求扩卷 01～18 | [knowledge](knowledge/delivery.md) | `deferred` | boyang wang | — | 每批有真实问题、Reviewer 和质量出口 |
| HWIF-006 | P2 | techlib 建仓门禁 | [hwif](hwif/README.md) | `deferred` | boyang wang | — | 两类适配、两个消费者后提交 ADR |
| SOC-006 | P2 | sw 仓门禁 | [soc](soc-integration/delivery.md) | `deferred` | boyang wang | — | SoC C3 后评审独立生命周期/消费者 |
| SOC-007 | P2 | reference-soc 建仓门禁 | [soc](soc-integration/delivery.md) | `deferred` | boyang wang | — | Golden 稳定并需独立 Release 后提交 ADR |

## 11. 每周更新模板

更新任务行时至少填写：

```text
ID：
状态：planned | in-progress | blocked | done | deferred
负责人：具体人
目标日期：YYYY-MM-DD
Evidence：PR / SHA / run-id / report / release
下一证据动作：
阻塞：原因 / 解除条件 / 解除 Owner / 复审日期
```

如果外部 Issue Tracker 投入使用，本文件仍保留 ID、状态、Owner、日期和链接；详细讨论可以迁出，但不能让本表失去可审计的组合视图。
