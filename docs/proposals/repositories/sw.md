# Software 候选仓提案

建议状态：M6 前评审，当前不建仓。

## 拟解决的问题

当多个 SoC/IP 共享 BSP、boot、HAL、driver 或生成的软件接口，并需要独立版本/发布时，提供明确的软件资产 Owner。

## 边界

- 拟负责：公共 BSP/HAL/driver、boot 接口、构建/测试和发布；
- IP 寄存器 Header 仍由 IP 的 SystemRDL 派生；项目专用 firmware 留项目仓；
- SoC 配置事实归项目仓，生成器归 tools，候选 sw 仓只消费稳定接口。

## 建仓触发与首个切片

最小 SoC boot smoke 已稳定，且至少两个目标共享同一软件资产并要求独立 SemVer。首个切片为 APB IP driver + 最小 boot/HAL，在仿真或 FPGA 上绑定精确硬件 Release/Lock 验证。

## 需要的决策

Owner、语言/构建系统、硬软版本兼容、生成代码边界、许可证和安全更新策略需 ADR 批准。
