# E6 验证记录

源码 SHA：`7a5a01622da340e59a15090a2b5167ae832b8398`；环境与 E5 相同，服务镜像：`course1027-draft:241250086`。

- 服务构建通过，30 项单元测试通过（原教师 24 项；保留本仓库已有 E4 测试多 3 项；本次新增边界 3 项）。
- 第一轮真实 build 退出 1，failure_class=MISSING_MAKE。
- 第二轮真实 build 退出 0。
- 同一镜像 ID `sha256:23eab3f1095fe0aea1abf8f47b33b34da9aef5c739a7bbb61070913dcf9b8960` 运行退出 0，stdout 为 `hello E3\n`，output_matches=true，终态 SUCCEEDED。
- `verify_e6_b_evidence.py` 检查候选哈希、原始日志、镜像 ID、输入文件哈希和输出一致性，passed=true。
- 源码与镜像密钥扫描通过。构建使用已有缓存；不声明从零下载或性能提升。

原始记录：[本阶段证据清单](../../artifacts/e6/linux-amd64-20261028/manifest.json)，关键路径 e6-01/evidence/result.json、e6-01/verification.json、build-02/unit-tests/stdout.log。build-01 是首次参考接入试运行，之后已修正提交身份与兼容代码；正式结论以 build-02 和 `7a5a01622da340e59a15090a2b5167ae832b8398` 为准。

## 2026-10-30 新材料核对

本日按单独 E6 包核对验收项，沿用上述本人实测原件。新版报告、四项实现解释和指定列验收表见 [REPORT.md](REPORT.md) 与 [ACCEPTANCE.csv](ACCEPTANCE.csv)，候选来源见 [CANDIDATE_SOURCE.json](CANDIDATE_SOURCE.json)。本日仅离线重算证据哈希、核验报告一致性与源码对应关系，不记作新的 Docker 运行。
