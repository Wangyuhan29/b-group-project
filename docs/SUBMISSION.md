# 本轮 minicalc 提交增量

当前主测试目标为 A 组 minicalc C2。新样例见 contracts/minicalc，实测结果与边界见 MINICALC_HANDOFF.md 和 VERIFICATION.md；图/ID 已纳入共享锁并与 A 组版本核对。C2 镜像已构建并发布到私有 GHCR，A 组 Checker 的实际重检仍待联调完成。下面保留 E2 初版说明，涉及 fixture://draft-project、artifacts/demo 和旧样本的内容仅供兼容回归。

# E2 提交清单

## 已随仓库提供

- [x] 四类请求、查询响应、系统错误、发现和产物样例。
- [x] Schema、OpenAPI 与可运行校验器。
- [x] ABC、缺少 baseline 等失败输入及预期结果。
- [x] Backlog、ADR、AI_USAGE 初稿。
- [x] B 组人工 DRAFT 样本、固定 MD 报告及本地修复演示。
- [x] 真实本地验证记录。

## 提交前由小组补齐

- [x] TEAM：已补录 B03、A03、鼓楼校区、双方联系人和成员学号。
- [x] PAIR_REVIEW：A03 已提供三轮评审记录和验证结果，已同步到 `docs/PAIR_REVIEW.md`。
- [x] ADR-004/005 已按 A03/B03 评审更新为 Accepted；ADR-001/002/003 仍保留 Proposed 状态，待双方逐项确认。
- [x] AI_USAGE：已记录人工采纳、修改、拒绝和理由。
- [x] CONTRIBUTIONS：已按三人分工填写；个人讨论/审阅证据仍需成员核对补充。
- [x] 按课程材料核对是否有要求沿用的模板或仓库。
- [x] 填写以下版本信息，并记录最终版本的校验结果。

| 字段 | 值 |
|---|---|
| 实际远端仓库 URL | https://github.com/Wangyuhan29/b-group-project |
| 提交分支 | main |
| 提交完整 SHA（git rev-parse HEAD） | 以本次同步完成后的 `git rev-parse HEAD` 输出为准 |
| 组员作者与提交说明 | 三人分工见 `docs/CONTRIBUTIONS.md`；Git 提交由 Wangyuhan29 统一推送 |
| Issue/PR | 无；本轮未使用 Issue/PR 流程 |
| 本地验证结果 | `make check` 通过；33 个共享文件锁校验、26 项测试和 C2 历史验证通过 |
| 未完成项/原因/下一步 | 真实 BuildChecker/EChecker、C0/C1 环境和跨机器产物读取属于 E3/E12；A03 已完成 C2 镜像冒烟验证 |

当前仓库可用于 E2 协商与校验，只有完成上述真实记录后才适合作为小组正式提交。

## E3 提交增量（2026-10-09）

B03 E3 必交基线已完成，逐项核对见 [E3_SUBMISSION](E3_SUBMISSION.md)。Ubuntu 原生 amd64 的原始构建/运行证据已取回并校验归档。请提交 main 最终 SHA；E2 初版和后续 E5/E8/E12 待办保留原阶段，不混作 E3 未完成必交项。
