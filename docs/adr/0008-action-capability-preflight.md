# ADR-0008：Action Capability Preflight 与 Provider 锁定

- 状态：建议
- 日期：2026-08-13

## 背景

当前 Flow YAML 已引用大量 `tool.*`、`release.*`、`catalog.*`、`soc.*`、`eda.*` 和 `skill.*` action，但标准 runner 只注册少量基础实现。Flow 能通过 Schema 校验并不表示能够执行，且 Lock/Evidence 尚不能完整记录 action provider 版本。

## 决策

1. 分离 Flow、Action Contract 和 Provider；
2. Action registry 返回稳定名称、provider、版本、输入输出 Schema、确定性、环境要求、写入范围和证据要求；
3. 新增 Flow preflight，在执行前产生 capability matrix；
4. 统一状态为 `available/optional-unavailable/unimplemented/version-mismatch/environment-unavailable`；
5. 未实现或版本不匹配的必需 action 必须在 Stage 执行前阻断；
6. 实际 provider 包版本、hash、容器/EDA 摘要写入 Lock 和 Evidence；
7. Flow 只有在 preflight、代表性端到端测试和 Evidence 均通过后才能标记 active。

## 备选方案

- 遇到未注册 action 时运行期再失败：反馈太晚，无法形成可靠计划；
- 在 Flow 中写脚本路径：破坏安全边界、插件替换和版本锁；
- 所有缺失能力都 skipped：会产生假通过；
- 仅记录 Python 包版本：不能覆盖容器、EDA、私有 Overlay 和生成器实现。

## 结果

正向影响：Flow 的可运行性可在执行前判断；公共/私有 provider 使用统一契约；Evidence 可重建；规划完成度不再依赖 YAML 数量。

负向影响：需要 provider metadata、版本约束、preflight 命令、Lock/Evidence Schema 和测试；私有 EDA/PDK adapter 也必须提供最小公开元数据。
