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

GitHub 首次成功、故意失败 PR、main 保护与实际拒绝合并、同一 PR 恢复及合并均已完成，见 [CI 完整记录](CI_RECORD.md)。

## 最终版本复验

固定源码 `c4c4f76ff79a0cb73a77da962be76eefb054211b`，工作区干净，原生服务器服务测试 31 passed、完整六场景全部通过、密钥扫描通过。新增的一项为 CI 演示恢复后的正确 version 测试；首次 30 项记录保持原样。原始结果与校验清单见 [最终服务器证据](../../artifacts/e7/linux-amd64-final-20261028/manifest.json)。

## 241250017 个人复跑（2026-11-01）

已从固定基线建立个人分支，新增 3 项输入/输出边界测试，重新构建后 34 项测试通过，E5、E6 和完整 gate 六场景通过。实际源码 SHA、贡献和原始证据见 [个人记录](STUDENT_241250017.md)。

## 241250075 个人复跑（2026-11-02）

已从固定基线建立个人分支，新增 3 项回放文件解析与入参边界测试，重新构建后 34 项测试通过，E5、E6 和完整 gate 六场景通过；CI 失败拦截与恢复直接引用小组共享记录，未重复配置仓库保护规则。实际源码 SHA、贡献和原始证据见 [个人记录](STUDENT_241250075.md)。

## 2026-11-02 合并后归档复核

- 朱玄的 [PR #6](https://github.com/Wangyuhan29/b-group-project/pull/6) 已合并，个人归档 `artifacts/e5-e7/241250017-20261101/` 的 404 项文件哈希复核一致。
- 靳滨硕的 [PR #7](https://github.com/Wangyuhan29/b-group-project/pull/7) 已合并；[PR #8](https://github.com/Wangyuhan29/b-group-project/pull/8) 从原件恢复两份 gate/results.csv 的 CRLF 换行，未改变实验内容或 manifest，414 项文件哈希复核一致。PR #8 四项 CI 检查通过，合并提交为 `859ccc7c8d65b0a0d6db158f9d482e0213fa1d70`。
- 两位成员个人服务器记录各为 34 项测试通过；汇总双方新增测试后，本地服务测试为 37 项通过。历史 30/31/34 项记录对应各自实测源码，不改写为当前数量。本次文档与证据复核未重新执行服务器 Docker 实验。
