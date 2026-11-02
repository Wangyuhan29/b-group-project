# E7 个人贡献

| 成员 | 本阶段工作 | 代码提交 | 验证 |
|---|---|---|---|
| 王宇晗（241250086） | 助接入并理解本阶段教师参考实现、处理现有固定 digest 与下载环境兼容问题，组织本人目录实际测试和原始证据归档 | `b85f6d2c8ebd131b65c39e6d42cad2603c000da5`（参考接入）；`7a5a01622da340e59a15090a2b5167ae832b8398`（固定 digest 修正与个人测试）；[PR #1](https://github.com/Wangyuhan29/b-group-project/pull/1)（实现与个人测试）、[PR #2](https://github.com/Wangyuhan29/b-group-project/pull/2)（失败拦截与恢复）、[PR #3](https://github.com/Wangyuhan29/b-group-project/pull/3)（证据与验收归档） | [个人记录](STUDENT_241250086.md)、[验证记录](VERIFICATION.md) |
| 朱玄（241250017） | 个人边界测试与镜像重建、运行证据归档；补齐本阶段个人说明 | `c220521c078a2b32f28fa70def896197f986c8a7`（实测源码）；[PR #6](https://github.com/Wangyuhan29/b-group-project/pull/6) | [个人记录](STUDENT_241250017.md)，个人 34 项测试、六场景通过 |
| 靳滨硕（241250075） | 个人边界测试与镜像重建、运行证据归档；补齐个人材料并恢复两份 CSV 原始换行 | `b1643f47ba4e15af562768b76d97ad7d0608560f`（实测源码）；[PR #7](https://github.com/Wangyuhan29/b-group-project/pull/7)、[PR #8](https://github.com/Wangyuhan29/b-group-project/pull/8) | [个人记录](STUDENT_241250075.md)，个人 34 项测试、六场景通过；414 项文件哈希一致 |

执行目录：`/root/241250086/e5-e7-20261028`。测试代码 SHA 与之后文档归档提交 SHA 分开记录。三项新增边界测试的作者为本地学号身份，AI 参与见 [AI_USAGE.md](AI_USAGE.md)；其他成员的实际测试与提交见上表和各自个人记录，各次实测源码 SHA 分开保留。

## CI 与收尾贡献

王宇晗（241250086）：

- `5f9652ff0f85d6863c175b7e6a0347aac015efa1`：定位 GitHub 托管镜像源元数据错误，保留失败证据，增加同 digest 的显式 CI 输入适配。贡献 PR #1 已合并。
- `f015fc5fcd5c694162292b4a6a49530a6814da27`：故意错误的 version 断言，CI 实际失败且合并被拒绝。
- `7b6b69f22103c2a850fb57876e4d150aa8ee44a0`：同一 PR #2 恢复正确断言，31 项测试及完整 gate 通过后正常合并。
- 源码里程碑 `c4c4f76ff79a0cb73a77da962be76eefb054211b`：本人服务器目录最终复验，原始日志、CI artifact、保护规则及 PR 状态按阶段归档。

[PR #1](https://github.com/Wangyuhan29/b-group-project/pull/1)、[PR #2](https://github.com/Wangyuhan29/b-group-project/pull/2)。此记录不新增其他成员的提交、亲手操作或审阅声明。

## 241250017 个人复跑（2026-11-01）

已从固定基线建立个人分支，新增 3 项输入/输出边界测试，重新构建后 34 项测试通过，E5、E6 和完整 gate 六场景通过。实际源码 SHA、贡献和原始证据见 [个人记录](STUDENT_241250017.md)。

## 241250075 个人复跑（2026-11-02）

已从固定基线建立个人分支，新增 3 项回放文件解析与入参边界测试，重新构建后 34 项测试通过，E5、E6 和完整 gate 六场景通过；CI 失败拦截与恢复直接引用小组共享记录，未重复配置仓库保护规则。实际源码 SHA、贡献和原始证据见 [个人记录](STUDENT_241250075.md)。
