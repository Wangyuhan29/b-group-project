# 本轮 minicalc 提交增量

当前主测试目标为 A 组 minicalc C2。新样例见 contracts/minicalc，实测结果与未完成项见 MINICALC_HANDOFF.md 和 VERIFICATION.md；图/ID 提案见 ADR-005，尚待 A 组确认。C0/C1/C2 SSH 历史及本地扫描已验证，Docker 镜像与 A 组重检未完成。下面保留 E2 初版说明，涉及 fixture://draft-project、artifacts/demo 和旧样本的内容仅供兼容回归。

# E2 提交清单

## 已随仓库提供

- [x] 四类请求、查询响应、系统错误、发现和产物样例。
- [x] Schema、OpenAPI 与可运行校验器。
- [x] ABC、缺少 baseline 等失败输入及预期结果。
- [x] Backlog、ADR、AI_USAGE 初稿。
- [x] B 组人工 DRAFT 样本、固定 MD 报告及本地修复演示。
- [x] 真实本地验证记录。

## 提交前由小组补齐

- [ ] TEAM：实际组号、配对组、姓名和学号。
- [ ] PAIR_REVIEW：同号 A 组解释同一份样例并实际确认。
- [ ] 将 Proposed ADR 更新为实际决策，未决项进入 Backlog。
- [ ] AI_USAGE：人工采纳、修改、拒绝和理由。
- [ ] CONTRIBUTIONS：真实个人提交及 Issue/PR 证据。
- [ ] 按课程材料核对是否有要求沿用的模板或仓库。
- [ ] 填写以下版本信息，并记录最终版本的校验结果。

| 字段 | 值 |
|---|---|
| 实际远端仓库 URL | 待填写 |
| 提交分支 | 待填写 |
| 提交完整 SHA（git rev-parse HEAD） | 待填写 |
| 组员作者与提交说明 | 见实际 git log，待核对 |
| Issue/PR | 待填写 |
| 本地验证结果 | 见 VERIFICATION.md，提交前重新运行 |
| 未完成项/原因/下一步 | 见 BACKLOG；身份与共同确认尚缺，运行器未实现 |

当前仓库可用于 E2 协商与校验，只有完成上述真实记录后才适合作为小组正式提交。
