# HWIF Development Suite（skill 设计）

> 当前唯一：本文件描述 `hwif-development-suite` skill 的**现行设计**（2026-08-17 起有效）。
> 落地实现位于 `aixsilicon_skill_repo/skills/hwif-development-suite/`（canonical 源码），
> 通过 `bootstrap.py --ensure` 物化到工作区 `.roo/skills/`。

## 1. 为什么把 HWIF 确定性能力放进 skill

HWIF 生成/校验/兼容/影响/打包属 **HWIF 领域专用方法与编排**，遵循工具归属原则：

> **市场级通用产品工具 → tool-repo；领域方法/判断 + 小型确定性辅助 → skill-repo；环境准备 → workspace-management。**

- `aixsilicon_tool_repo` 只承载整块、可复用的产品级工具（reg/address-map/dvsim/schema 等）；
- HWIF 领域能力统一收进 **`hwif-development-suite`** 内置 `scripts/`（唯一入口 `hwif_tool.py`）；
- 原 `aix-hwif-gen`（tool-repo）已标记 deprecated 并收敛（P4）；
- hwif 仓不再保存 `tools/`、`tests/`（P3，只留 SSOT + 结果）。

## 2. 套件结构（canonical）

```text
skills/hwif-development-suite/
├── SKILL.md                     # 生命周期路由 + 子 skill 路由表 + 触发冲突边界 + G0–G6
├── skills/                      # 9 个全生命周期子 skill
│   ├── hwif-spec-author/        # 接口规格 → 契约骨架
│   ├── hwif-contract-author/    # Contract/Profile/Binding 编写
│   ├── hwif-contract-validate/  # Schema + 正负样例校验（G0）
│   ├── hwif-view-generate/      # 多视图生成 + drift（G1）
│   ├── hwif-sv-consistency/     # SV↔YAML 一致性（G2）
│   ├── hwif-compatibility-check/# 兼容判定 DIRECT/ADAPTER/INCOMPATIBLE（G3）
│   ├── hwif-impact-analysis/    # 变更影响 + SemVer 建议
│   ├── hwif-fusesoc-pack/       # .core 校验/生成（G4）
│   └── hwif-release-package/    # Release 输入 + Catalog（G5）
├── scripts/
│   ├── hwif_tool.py             # 唯一确定性入口（7 子命令，fail-closed 退出码）
│   └── legacy/                  # 迁移自 hwif 仓 T2 的 6 脚本（frozen 快照）
├── references/                  # contract-authoring / compatibility / generation-checklist
├── evals/                       # evals.json（端到端断言）+ trigger-query.json（触发回归）
└── tests/                       # pytest（hwif_tool 冒烟 + golden 正负样例）
```

## 3. 子 skill 路由表（含冲突边界）

| 用户意图 | 子 skill | 什么时候**不**用 |
|---|---|---|
| "新增 APB 契约 / 加可选信号" | `hwif-contract-author` | 写 RTL Driver/VIP → vip skill |
| "校验 interface.yaml" | `hwif-contract-validate` | 不生成，只校验 |
| "生成 SV/ipxact/doc / 重跑" | `hwif-view-generate` | 不改契约语义 |
| "RTL 和 YAML 对不上" | `hwif-sv-consistency` | 纯 RTL bug → debug |
| "AXI 和 APB 能直连吗" | `hwif-compatibility-check` | 实现 adapter → cbb |
| "接口变更影响谁" | `hwif-impact-analysis` | 只分析不改 |
| "生成 .core / fileset" | `hwif-fusesoc-pack` | 编译仿真 → 工作区/DV |
| "HWIF Release / Catalog" | `hwif-release-package` | 直写 Catalog → 经流程 |

**跨套件冲突边界**：`hwif-contract-author` vs `ip-development-suite/03-hld-architect`
（IP 内部架构 → IP 套件；公共接口契约 → 本套件）；`hwif-view-generate` vs reg-tool
（CSR → reg-tool；接口视图 → 本套件）。

## 4. 唯一入口 CLI（`hwif_tool.py`）

```bash
uv run python ${SUITE_DIR}/scripts/hwif_tool.py <subcommand> [options]
```

| 子命令 | 门禁 | 说明 |
|---|---|---|
| `validate` | G0 | Schema + 语义（capability 引用 / width 受限表达式）；`semantic_check` 内建 |
| `generate` | G1 | View A/B/C/D + IP-XACT + docs；`--check-only` drift 门禁 |
| `consistency` | G2 | SV package/interface ↔ YAML 一致性 |
| `compat` | G3 | `--a/--b` 判定；AMBA 可桥族 → ADAPTER_REQUIRED |
| `impact` | — | 影响清单 + SemVer 建议 |
| `core` | G4 | `.core` CAPI=2 + `aix:` 命名空间 + 文件存在 |
| `package` | G5 | Release 必需输入 + 家族资产清单（`--dry-run` 防写库） |

- 退出码：`0` pass / `10` 验证失败 / `20` 用法 / `40` 内部（fail-closed）；
- **确定性**：同输入同 hash；`generated/` 禁止手改。

## 5. 生命周期门禁（G0–G6）

| Gate | 判定 |
|---|---|
| G0 contract-valid | `validate` 全绿（Schema + 正负样例 + semantic_check） |
| G1 view-fresh | `generate --check-only` 无漂移 |
| G2 sv-consistent | `consistency` 全绿 |
| G3 compat-pass | `compat` 消费者矩阵内均 DIRECT 或已记录 ADAPTER |
| G4 core-valid | `core` 全 `.core` 合法 |
| G5 package-ok | `package` 输入完整 |
| G6 evidence | Run Manifest/Evidence 记录契约 hash、生成 hash、工具版本 |

## 6. Eval 与触发测试（skill-creator 方法论）

- **端到端**（`evals/evals.json`）：每子 skill ≥2 真实 prompt + 1 负向；APB 为 fixture；
- **断言**：契约校验通过、生成哈希稳定、`--check-only` 拒绝手改、SV 一致、
  兼容判定正确、影响列表与依赖图一致、`.core` 合法、Release 输入完整；
- **触发回归**（`evals/trigger-query.json`）：20 条 should/should-not 查询覆盖近邻词，
  description 变更须过触发回归；
- **CI**：`validate.yaml`（pytest scripts）+ `eval.yaml`。

## 7. References

- Skill 落地实现：`aixsilicon_skill_repo/skills/hwif-development-suite/`
- 测试与样例：同套件 `tests/`（含自 hwif 仓迁移的 golden 正负样例）
- 收敛过程与决策：hwif-repo `archived/docs/aix-hwif-gen-unified-plan.md`