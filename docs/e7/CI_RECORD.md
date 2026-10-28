# E7 GitHub CI 与实际合并门禁记录

日期：2026-10-28；执行人：王宇晗（241250086），Codex 辅助。仓库：[Wangyuhan29/b-group-project](https://github.com/Wangyuhan29/b-group-project)。按用户确认公开仓库后完成门禁；公开前源码、Git 历史扫描未发现密钥，用户亲自完成 GitHub 身份验证。

## 首次正常 CI

贡献 [PR #1](https://github.com/Wangyuhan29/b-group-project/pull/1) 已通过并合并。首次 main 固定版本 `849df98e03358201fd943a9b640d378717ebf0ab`，[运行 40647145632](https://github.com/Wangyuhan29/b-group-project/actions/runs/40647145632) 成功；artifact 中 commit.txt 与源码 SHA 相同，六场景 passed=true。真实文件见 `artifacts/e7/github-20261028/normal/`。

首次分支 CI 40646144654 曾失败，原因是国内镜像源向 GitHub 托管机器返回错误元数据类型 application/octet-stream，不属于算法或测试断言错误。完整失败日志及 artifact 保留在 `artifacts/e7/github-initial-40646144654/`。CI 后续使用官方 registry、Debian/PyPI 源；服务构建和候选输入的 digest 保持不变，实际输入副本与哈希差异见各 artifact 的 inputs/adaptation.json。服务器继续使用已验证的镜像源。

## main 保护

实际检查：`e7-b-quality-gate`；App ID 为查询所得 15368，GitHub Actions。strict=true、enforce_admins=true；必须经 PR 合并，审批人数 0；禁止 force push 和删除分支，要求解决会话。配置请求与实际应用响应分别保存在 `protection-request.json`、`protection-applied.json`。未采用管理员绕过。

## 同一个 PR 的失败与恢复

演示 [PR #2](https://github.com/Wangyuhan29/b-group-project/pull/2)，分支 `e7/reject-241250086-20261028`。

| 步骤 | 源码 SHA / 结果 | 原始证据 |
|---|---|---|
| 故意失败 | `f015fc5fcd5c694162292b4a6a49530a6814da27`；将 version 成功退出码预期设为 1，实际返回 0；1 failed、30 passed | [失败运行 40647276388](https://github.com/Wangyuhan29/b-group-project/actions/runs/40647276388)；rejection/artifact/ 中单测日志 |
| 合并拒绝 | 普通 merge 返回 1，策略禁止；PR 仍 OPEN / BLOCKED | rejection/merge-rejection.log、merge-exit-code.json、PR-before.json、PR-after.json、protection.json |
| 同 PR 修复 | `7b6b69f22103c2a850fb57876e4d150aa8ee44a0`；断言恢复为实际成功码 0；31 项测试和六场景通过 | [恢复运行 40647571082](https://github.com/Wangyuhan29/b-group-project/actions/runs/40647571082)；recovery/artifact/ |
| 正常合并 | MERGED，合并提交 `c4c4f76ff79a0cb73a77da962be76eefb054211b` | recovery/PR-before-merge.json、PR-merged.json；PR2-merged.png |

本次修正的是故意错误的测试预期，不声称修正了算法缺陷。恢复运行的 headSha 与 PR 最新 headRefOid 一致后才执行普通合并。两个演示提交均保留在 Git 历史中，最终主线仅保留正确测试。

## 最终原生服务器复验

以合并提交 `c4c4f76ff79a0cb73a77da962be76eefb054211b` 在 `/root/241250086/e5-e7-20261028` 的干净源码状态复跑。31 项测试、完整六场景、镜像及源码密钥扫描通过；超时场景通过 inspect 确认容器不存在。证据位于 `artifacts/e7/linux-amd64-final-20261028/`，逐文件清单见 [manifest](../../artifacts/e7/linux-amd64-final-20261028/manifest.json)。云服务器与 GitHub 的下载源差异明确记录，未声称逐字节镜像可重复。

全部 GitHub artifact 已下载进项目目录，避免仅依赖 14 天保留期限；下载后逐文件 SHA-256 清单见 [CI manifest](../../artifacts/e7/github-20261028/manifest.json)。截图只辅助，实际退出码、报告、保护响应和 PR 状态均保留原件。
