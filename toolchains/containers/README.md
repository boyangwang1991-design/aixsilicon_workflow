# 容器 / 环境定义

- 开源工具流程可提供容器镜像；
- 商业 EDA 环境通常由受控 Runner/module 加载，**不把许可证写入镜像**；
- blue-zone 与 red-zone 使用相同 Schema 和 Flow 语义，但具体工具路径与网络策略分离；
- CI 只记录工具版本和 Profile ID，不回显敏感环境变量；
- 生成器版本必须锁定，不能只锁 RTL 仓库。

## 约定

本目录存放容器构建说明与基础镜像引用（不含商业 EDA 二进制与许可证）：

- `aix-base/`：Python + FuseSoC + Verilator 开源基础镜像。
- 商业 EDA 镜像由受控基础设施提供，不在本开源仓维护。
