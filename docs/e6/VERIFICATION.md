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

## 241250017 个人复跑（2026-11-01）

已从固定基线建立个人分支，新增 3 项输入/输出边界测试，重新构建后 34 项测试通过，E5、E6 和完整 gate 六场景通过。实际源码 SHA、贡献和原始证据见 [个人记录](STUDENT_241250017.md)。

## 241250075 个人复跑（2026-11-02）

已从固定基线建立个人分支，新增 3 项回放文件解析与入参边界测试，重新构建后 34 项测试通过，E5、E6 和完整 gate 六场景通过。个人记录已按新模板补齐四项核心实现说明、本人候选来源表与验收表（补齐本轮提交建议第 2 点）。实际源码 SHA、贡献和原始证据见 [个人记录](STUDENT_241250075.md)。

## 2026-11-02 合并后归档复核

- 朱玄的 [PR #6](https://github.com/Wangyuhan29/b-group-project/pull/6) 已合并，个人归档 `artifacts/e5-e7/241250017-20261101/` 的 404 项文件哈希复核一致。
- 靳滨硕的 [PR #7](https://github.com/Wangyuhan29/b-group-project/pull/7) 已合并；[PR #8](https://github.com/Wangyuhan29/b-group-project/pull/8) 从原件恢复两份 gate/results.csv 的 CRLF 换行，未改变实验内容或 manifest，414 项文件哈希复核一致。PR #8 四项 CI 检查通过，合并提交为 `859ccc7c8d65b0a0d6db158f9d482e0213fa1d70`。
- 两位成员个人服务器记录各为 34 项测试通过；汇总双方新增测试后，本地服务测试为 37 项通过。历史 30/31/34 项记录对应各自实测源码，不改写为当前数量。本次文档与证据复核未重新执行服务器 Docker 实验。
