# 文档图片资产

本目录保存用于概念解释的项目图片。图片不是规范源：精确字段、依赖、Gate 和状态仍以相邻正文、Mermaid、表格及机器可读配置为准。

## 资产清单

| 文件 | 用途 | 插入位置 | 尺寸 |
|---|---|---|---|
| [`documentation-map.png`](documentation-map.png) | 解释文档五层结构与阅读关系 | `docs/index.md` | 1672×941 |
| [`control-plane-ecosystem.png`](control-plane-ecosystem.png) | 解释 Workflow、Tools、独立资产仓、EDA、Evidence 与 Catalog 的关系 | `docs/architecture/overview.md` | 1672×941 |
| [`evidence-release-lifecycle.png`](evidence-release-lifecycle.png) | 解释从 Manifest/Lock 到 Gate/Evidence/人工批准/发布的闭环 | `docs/workflow/release.md` | 1672×941 |

## 生成记录

- 生成日期：2026-08-13；
- 生成方式：Codex 内置 imagegen，`infographic-diagram` 用例；
- 风格：16:9、企业技术信息图、暖白背景、navy/teal/amber/gray；
- 文档地图提示主题：五层材料 `ENTRY & STATUS / ARCHITECTURE / WORKFLOW CONTRACTS / REPO EXECUTION / REFERENCE`；
- 控制面提示主题：可选 Skill、Workflow 控制面、Tools、六类独立资产仓、EDA、Evidence 和 Catalog；初稿的仓间串行箭头已通过一次定向编辑改为公共总线；
- 发布闭环提示主题：`MANIFEST → LOCK → PREFLIGHT → FLOW + PROVIDER → GATES → EVIDENCE → human approval → RELEASE + CATALOG`，Gate 失败回到执行层；
- 约束：无品牌 Logo、无水印、无额外文案；所有标签均在落库前人工目视检查。

## 维护规则

- 新图片必须有有意义的 Markdown alt 文本和紧邻图片的文字说明；
- 图片中的箭头若可能简化真实语义，正文必须明确说明；
- 架构变化时优先更新可维护的 Mermaid/表格，再决定是否重新生成图片；
- 不允许仅凭图片判定依赖、所有权、Gate 或完成状态；
- 替换现有图片时使用可审阅的新文件或明确记录重新生成原因。
