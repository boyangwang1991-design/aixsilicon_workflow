# Tools 仓设计契约

Tools 仓提供跨仓复用的确定性生成、检查、转换、解析和打包能力。Owner 为 `engineering-platform`；Workflow 通过稳定 Action/Provider 契约调用工具。

> **可见性：私有**。Tools 仓源码不直接开源；其确定性生成/检查产出的**交付件**（HWIF/CBB/IP/DV Common/VIP 契约与资产、生成 RTL/Header/Core、Catalog 条目、文档）写入对应公开资产仓随资产仓开源。Workflow/资产仓按已发布 Action/Provider 契约调用工具，不依赖其私有源码。

## 边界

- T1 跨仓产品化工具归本仓（私有）；T2 单仓测试/CI 脚本留资产仓；T3 商业 EDA/PDK/Memory adapter 留私有 Overlay；T4 项目胶水留项目仓；
- Tool 实现领域算法，Workflow 编排顺序/Gate，Skill 辅助判断，资产仓保存事实；
- 不允许双重实现同一确定性能力；迁移采用双入口 → `aix tool` → deprecated；
- Tool 不直接判业务 Gate，只返回结构化 Result/Diagnostic/Artifact 和可审计退出码。

## Provider 契约

每个 provider 必须声明 action 名、版本、输入/输出 Schema、capability、availability reason、权限/路径、确定性、超时/重试和证据字段。版本/hash 与外部工具/容器/EDA 摘要进入 Lock/Evidence。

## 建设顺序

现有 core/schema/hwif/reg 基线先完成 provider 化和 APB 实跑；再按 M5/M6 需要建设 param/PPA、socgen/connect；report/rtm/package 等只在有端到端消费者时启动。工具地图是选择池，不是同时开发清单。

## 验收出口

- 单元、golden、negative、安全和跨平台测试通过；
- 缺可选依赖返回明确 unavailable，不伪装成功；
- 相同输入/版本得到稳定输出 hash；
- Workflow preflight 能发现、约束和锁定 provider；
- 真实 APB Flow 在固定 Lock 下调用，不依赖仓内隐式脚本路径。

活动交付见 [`delivery.md`](delivery.md)，完整工具地图、CLI/API 和历史设计见 [`design-reference.md`](design-reference.md)。
