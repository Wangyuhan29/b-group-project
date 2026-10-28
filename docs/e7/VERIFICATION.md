# E7 验证记录

本地服务测试与原生 Ubuntu 服务测试均为 30 项通过，个人定向边界测试 3 项通过。原 E2/E3 make check 回归通过。正式源码 SHA：`7a5a01622da340e59a15090a2b5167ae832b8398`。

| 场景 | 工具退出/终态 | 场景判定 |
|---|---|---|
| unit-tests | 0 | PASS，30 项 |
| success | 0 / SUCCEEDED | PASS，同一构建镜像输出 hello E3 |
| wrong-output | 1 / FAILED | PASS，输出不符被拒绝 |
| invalid-candidate | 1 / FAILED | PASS，构建前拒绝且无 attempts |
| build-failed | 1 / FAILED | PASS，RUN exit 23 后停止程序验证 |
| runtime-timeout | 1 / TIMED_OUT | PASS，运行容器已移除 |

真实 gate 返回 0，passed=true。证据：[逐文件清单](../../artifacts/e7/linux-amd64-20261028/manifest.json)，完整门禁结果 e7-01/gate/gate-result.json、results.csv；超时清理证据 e7-01/gate/runtime-timeout/evidence/cleanup-check/。

GitHub 的首次成功、故意失败 PR、main 保护与拒绝合并、同一 PR 恢复与合并记录将在真实执行后另行归档，当前不以服务器门禁替代远程门禁。
