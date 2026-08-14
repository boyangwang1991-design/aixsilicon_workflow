# CBB 交付台账

> 状态、负责人、日期和 Evidence 只在 [`../todo.md`](../todo.md) 维护。

| ID | P | 里程碑 | 任务 | 依赖 | 验收 / Evidence | Owner |
|---|---|---|---|---|---|---|
| CBB-001 | P0 | M5 | 冻结 metadata/params/result/PPA Schema 与成熟度 | HWIF-001、tools contract | Schema 正负样例和版本策略获批 | hw-platform |
| CBB-002 | P0 | M5 | 落地 arbiter 首个示范构件 | CBB-001 | 参数边界、形式/随机、lint/build、消费者证据 | cbb maintainer |
| CBB-003 | P0 | M5 | 落地 ready/valid pipeline 示范闭环 | CBB-001 | 延迟/吞吐契约与 PPA sweep 可重建 | cbb maintainer |
| CBB-004 | P0 | M5 | 落地 FIFO 存储映射示范闭环 | CBB-001 | depth/width/implementation 边界与 PPA 可比 | cbb maintainer |
| CBB-005 | P0 | M5 | 冻结 CBB Action/Flow 的领域验收契约 | CBB-002～004 | 参数矩阵、PPA、影响分析和 G0～G6 输入输出获批 | cbb + workflow |
| CBB-006 | P1 | M5 | 将三个示范构件发布并登记 Catalog | WF-010、CAT-003 | Tag/Release/Catalog/Evidence 完整 | hw-platform |
| CBB-007 | P1 | 扩展 | 从种子池按消费者需求逐项扩展 | CBB-006 | 每个新项有消费者、Owner 和验收切片 | hw-platform |

15 种子清单和完整领域地图保留在设计参考，不代表 15 项同时进入承诺。组合顺序见 [`../roadmap.md`](../roadmap.md)。
