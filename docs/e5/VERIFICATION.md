# E5 验证记录

日期：2026-10-28；源码 SHA：`7a5a01622da340e59a15090a2b5167ae832b8398`。Ubuntu 24.04.4、linux/amd64、2 CPU、约 1.7 GiB 可见内存。服务器共用 root，操作范围仅本人学号目录。

证据目录：[linux-amd64-20261028](../../artifacts/e5/linux-amd64-20261028/manifest.json)。本地下载包 SHA-256：`0c9982bc1e02e5042fc26552cbc2f659df072dba8987c889ca9cc4b808bd103b`，传输后匹配。

| 步骤 | 实际结果 | 原始文件（上述归档下） |
|---|---|---|
| 首次直连 | Docker Hub 元数据连接超时；不算缺 make 复现 | e5-01/iter-01/build/stderr.log |
| 调整后初始失败 | Docker build 退出 1；RUN make 内部退出 127，make: not found | e5-02/iter-01/build-retry.log、result-retry.json |
| 两类提示 | 根据真实日志与 README 生成；模型调用次数 0 | e5-02/iter-01/prompt-error-driven.txt、prompt-context-driven.txt |
| 手工候选构建 | 退出 0 | e5-02/candidate-build.log、candidate-build-exit-code.txt |
| 按同一 ID 验证 | 输出 hello E3，退出 0，禁网运行 | e5-02/candidate-image-id.txt、verify.log、verify-exit-code.txt |

手工候选镜像 ID：`sha256:5daf7cc34a0ef35cc4ecddd6dbe56c1825a3edc3e33ea21373aa4d1c87240844`。本地 image ID 不等于已发布仓库的 registry digest。

## 241250017 个人复跑（2026-11-01）

已从固定基线建立个人分支，新增 3 项输入/输出边界测试，重新构建后 34 项测试通过，E5、E6 和完整 gate 六场景通过。实际源码 SHA、贡献和原始证据见 [个人记录](STUDENT_241250017.md)。

## 241250075 个人复跑（2026-11-02）

已从固定基线建立个人分支，新增 3 项回放文件解析与入参边界测试，重新构建后 34 项测试通过，E5、E6 和完整 gate 六场景通过；另附本人候选手工构建与同镜像禁网运行的独立记录。实际源码 SHA、贡献和原始证据见 [个人记录](STUDENT_241250075.md)。

## 2026-11-02 合并后归档复核

- 朱玄的 [PR #6](https://github.com/Wangyuhan29/b-group-project/pull/6) 已合并，个人归档 `artifacts/e5-e7/241250017-20261101/` 的 404 项文件哈希复核一致。
- 靳滨硕的 [PR #7](https://github.com/Wangyuhan29/b-group-project/pull/7) 已合并；[PR #8](https://github.com/Wangyuhan29/b-group-project/pull/8) 从原件恢复两份 gate/results.csv 的 CRLF 换行，未改变实验内容或 manifest，414 项文件哈希复核一致。PR #8 四项 CI 检查通过，合并提交为 `859ccc7c8d65b0a0d6db158f9d482e0213fa1d70`。
- 两位成员个人服务器记录各为 34 项测试通过；汇总双方新增测试后，本地服务测试为 37 项通过。历史 30/31/34 项记录对应各自实测源码，不改写为当前数量。本次文档与证据复核未重新执行服务器 Docker 实验。
