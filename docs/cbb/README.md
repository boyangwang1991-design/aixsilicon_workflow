# CBB 仓设计契约

CBB 保存可参数化、可独立复用和可量化 PPA 的公共 RTL 构件。Owner 为 `hw-platform`；消费者主要是 IP 和 SoC 项目。

## 范围与边界

- 负责：功能契约、参数合法域、微架构变体、属性/验证、PPA 表征和成熟度；
- 不负责：带产品 CSR/中断/软件语义的完整 IP、通用接口事实、流程编排或工具实现；
- “有代码”不等于可复用；构件必须具备参数边界、质量证据、版本和至少一个真实消费者；
- 15 个种子构件是长期首期池，不应同时开工；先以 3 个 PPA 示范闭环验证平台。

## 资产模型

每个构件以领域、抽象层、接口契约、参数空间、实现变体和成熟度六维标识。PPA 结果必须绑定工艺/库、约束、工具版本、RTL SHA、参数和活动场景，禁止跨不可比环境直接排名。

## 目标能力与阶段

1. 冻结 metadata/result/PPA Schema 和 CBB Flow 契约；
2. 用 arbiter、ready/valid pipeline、FIFO 三个切片验证参数/形式/随机/PPA 全链；
3. 验证自动选型只给可解释建议，不自动改产品微架构；
4. 平台稳定后再扩到 15 个种子构件和更广 Catalog；
5. Qualification 复用 Workflow G0～G6，人工批准后的发布复用 G7、Lock、Evidence 和 Catalog PR。

## 验收出口

- 非法参数在生成/编译前失败；边界组合、随机/形式属性和 lint/build 全部有证据；
- PPA sweep 可重建、可比性字段完整、回归阈值经批准；
- 至少一个真实 IP/SoC 消费构件并锁定版本；
- 成熟度提升由 Gate/Evidence 驱动，不用主观百分比。

活动交付见 [`delivery.md`](delivery.md)，完整构件地图和历史设计见 [`design-reference.md`](design-reference.md)。
