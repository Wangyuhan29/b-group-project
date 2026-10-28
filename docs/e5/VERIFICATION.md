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
