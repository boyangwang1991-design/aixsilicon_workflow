# Local Overrides

Local Override 让开发者临时覆盖某个仓库的分支，例如“VIP 暂时依赖尚未合入的 HWIF 分支”，而不修改公共 Manifest。

## 规则

- override 默认只在本地生效，且 `overrides/local.yaml` 被 `.gitignore` 忽略；
- CLI 状态页必须显著显示 `NON-BASELINE / OVERRIDDEN`；
- Evidence 和 Run Manifest 必须记录实际 SHA，不能只记录分支名；
- Release Gate 默认拒绝存在 local override；
- 需要团队共享的跨仓变更改用 **Change Bundle**，而不是提交个人 override。

## 示例

```yaml
# overrides/local.yaml（被忽略，仅供本地使用）
schema_version: aix.workspace-override/v1
repositories:
  hwif:
    revision:
      branch: feature/axi-user-contract
  vip:
    revision:
      branch: feature/axi-user-support
```

## 添加本地覆盖

```bash
cp overrides/local.yaml.example overrides/local.yaml
# 编辑后执行
aix wf sync
aix wf status   # 应显示 OVERRIDDEN 标记
```
