# Techlib 候选仓提案

建议状态：暂不建仓，M5 复审。

## 拟解决的问题

统一 Generic/FPGA/ASIC primitive、memory、clock/reset 和物理约束适配，使 HWIF/CBB/IP 不硬编码工艺或厂商库。

## 边界

- 拟负责：抽象 primitive contract、目标库 mapping/profile、支持矩阵和适配验证；
- 不负责：PDK/商业库文件、CBB 算法、IP 产品逻辑、综合/PPA 引擎；
- 私有 PDK 内容留 T3 Overlay，公共仓只保存不敏感契约和 adapter 接口。

## 建仓触发与首个切片

同时出现至少两类目标适配（如 FPGA + ASIC）和两个真实消费者；首个切片以同一 FIFO/memory primitive 在两类目标下完成功能等价、参数合法域、PPA/约束和版本锁定。未触发时 adapter 留在消费者或私有 Overlay。

## 需要的决策

Owner 候选为 hw-platform；需 ADR 决定 Schema Owner、与 CBB/tools 的边界、私有/公共拆分、VLNV 和 Catalog 类型。
