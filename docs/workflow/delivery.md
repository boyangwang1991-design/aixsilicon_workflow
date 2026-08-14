# Workflow 交付台账

| ID | P | WP | 任务 | 依赖 | 验收 / Evidence | Owner | 状态 |
|---|---|---|---|---|---|---|---|
| WF-001 | P0 | WP0 | 审核并接受或修订 ADR-0007 | 方案评审 | Profile/依赖决策被批准 | workflow architect | `planned` |
| WF-002 | P0 | WP1 | 实现 exact Profile、有类型依赖及 v1 兼容 | WF-001 | exact-set、typed closure/DAG、旧配置测试 | workspace maintainer | `planned` |
| WF-003 | P0 | WP0 | 审核并接受或修订 ADR-0008 | 方案评审 | Action/Provider/Preflight 决策被批准 | workflow architect | `planned` |
| WF-004 | P0 | WP2 | 建立 capability registry、provider metadata 与 preflight | WF-003、TOOL-001 | action inventory 全覆盖；缺失能力 fail-closed | workflow + tools | `planned` |
| WF-005 | P0 | WP2 | 补齐 runner 控制语义和安全边界 | WF-004 | required/needs/timeout/retry/on_failure/gate/write_scope 负向测试 | workflow runtime | `planned` |
| WF-006 | P0 | WP2 | 加强 Lock、Run Manifest 与 Evidence 契约 | WF-002、WF-004 | repo/provider/tool/env/hash/seed 可校验并重放 | workflow runtime | `planned` |
| WF-007 | P0 | WP2 | 统一退出码与失败分类 | WF-004、TOOL-004 | CLI/Tool/Flow 契约测试无双口径 | workflow + tools | `planned` |
| WF-008 | P0 | WP3 | 固定 APB Flow 的 action/Gate/write scope/证据 | WF-004～006、APB 资产 | 固定 Lock 完成 G0～G6；故障注入无 false green | workflow + APB owners | `planned` |
| WF-009 | P0 | WP4 | 实现 Change Bundle 状态机和 PR HEAD 联验 | WF-005/006 | 多 PR checkout、联合 CI、merge order/SHA 可追溯 | collaboration maintainer | `planned` |
| WF-010 | P0 | WP4 | 实现 candidate/approval/G7/Tag/Release/Catalog PR | WF-006/009、CAT-004 | clean/lock/no-override、幂等、失败恢复 | release platform | `planned` |
| WF-011 | P1 | 工程化 | 统一 Windows/POSIX、UTF-8 和离线检查入口 | — | clean 环境双平台自检记录 | workflow maintainer | `planned` |
| WF-012 | P1 | 工程化 | 完成受控 PR 封装和凭据/权限负向测试 | WF-005 | 最小权限、secret redaction、失败可解释 | workflow maintainer | `planned` |
| WF-013 | P1 | M5 | 实现 CBB development/qualification Flow | WF-008、CBB-005 | 参数/PPA/影响/G0～G6 | workflow + cbb | `deferred` |
| WF-014 | P1 | M6 | 接入 SoC provider 与 baseline Flow | SOC-001～004、WF-006 | Golden/boot smoke/Lock/Evidence | workflow + soc/tools | `deferred` |

实现类风险和关闭条件见 [`../findings.md`](../findings.md)。任务进入 `in-progress` 前必须补齐具体负责人、目标日期和 PR/分支。
