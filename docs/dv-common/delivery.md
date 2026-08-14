# DV Common 交付台账

| ID | P | 里程碑 | 任务 | 依赖 | 验收 / Evidence | Owner | 状态 |
|---|---|---|---|---|---|---|---|
| DV-001 | P0 | M3 | 冻结 Run Manifest/Test Result/Failure/Metric Schema | WF-006 | 正负样例、版本和退出语义一致 | dv-platform | `planned` |
| DV-002 | P0 | M3 | 提供 RAL base 与 P0 CSR sequences | IP-001 | RW/RO/W1C/reset/非法地址测试 | dv-platform | `planned` |
| DV-003 | P0 | M3 | 提供 clock/reset/timeout/watchdog 最小服务 | — | 并发、reset epoch、timeout 负向单测 | dv-platform | `planned` |
| DV-004 | P0 | M3 | 完成 APB IP 穿刺适配 | DV-001～003、VIP-001 | 标准结果/Evidence 可被 Workflow 汇总 | dv + vip/ip | `planned` |
| DV-005 | P1 | M4 | 验证第二消费者与 API/SemVer 兼容 | DV-004 | 两个消费者矩阵、deprecated 测试 | dv-platform | `planned` |
| DV-006 | P2 | 扩展 | 按穿刺需求扩展 scoreboard/memory/fault 服务 | DV-005 | 每项有两个消费者或批准例外 | dv-platform | `deferred` |

完整组件清单是设计池，不等于全部进入当前承诺。
