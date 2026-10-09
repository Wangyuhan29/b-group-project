# 个人贡献记录



| 日期 | 姓名/学号 | 工作和文件                                                                                                                         | commit SHA | 提交说明 | Issue/PR | 验证结果 |
|---|---|------------------------------------------------------------------------------------------------------------------------------------|---|---|---|---|
| 2026-09-19—09-22 | 王宇晗（241250086） | 统筹 minicalc C2 接入、DRAFT 环境、GHCR 镜像、共享锁、A/B 联调和提交材料；`contracts/shared-lock.json`、镜像工作流、`fixtures/minicalc/project.json`、`docs/PAIR_REVIEW.md`、`docs/SUBMISSION.md` | `c458e7b88d86d8e1203f5e5d5280e0f6dbae71f4`、`da50ca9b24a775bf42a0e6d6c9563c5c4a656275`、`a5cd08dca0dc95f11ce787060ccf61c0afc2fe3d`、`0caf9beab227e52a194d2a1e85893bec0482c243`（实际作者均为 Wangyuhan29） | 建立 B03 仓库，完成共享契约、镜像交接和 A03 评审材料 | 无 Issue/PR；主线统一提交 | `make check`、33 文件锁校验和 C2 镜像交接证据通过 |
| 2026-09-20 | 朱玄（241250017） | MDFixer 分工；独立提交内容为贡献表和 AI_USAGE 中的核验说明，记录 Windows 编码、换行和源码快照检查未通过项 | `beb69e377c5fcdf81b42a77ada094d76ffb46760`（独立文档提交，作者 xuan zhu）；`5841b9df4d6c412106915b0bdba51b7c7386e264` 为 Wangyuhan29 的文档整理提交 | 记录 MDFixer 验证结果； | 无 Issue/PR | 修复前 4 MD/0 RD，修复后 0 MD/0 RD |
| 2026-09-19—22 | 靳滨硕（241250075） | 契约与质量方向：`graph.schema.json`、`finding-id-v1.json`、`shared-lock.json`、锁校验、测试和提交文档复核 | `da50ca9b24a775bf42a0e6d6c9563c5c4a656275`、`0caf9beab227e52a194d2a1e85893bec0482c243`（共同工作内容由王宇晗统一提交，Git 作者未冒充靳滨硕） | 完成共享契约同步、A/B 评审证据和质量复核 | 无 Issue/PR；本轮审阅确认见 AI_USAGE | 33 个共享文件哈希一致；26 项单元测试通过 |

可用 `git log --format='%H %an <%ae> %s'` 获取真实版本、作者和说明；截图仅辅助。

2026-09-22 人工审阅：根据朱玄提供的确认信息，王宇晗、朱玄、靳滨硕已确认各自分工范围内的文档审阅结论，详见 `AI_USAGE.md`。

## E3 补充记录（2026-10-09）

| 姓名/学号 | 工作与文件 | commit SHA | 提交说明 | Issue/PR | 验证结果 |
|---|---|---|---|---|---|
| 王宇晗（241250086） | 在 AI 辅助下组织 A03 基线互查、Ubuntu amd64 DRAFT Docker 验证，整理 E3 README、BACKLOG、验证记录及证据状态 | `10db4f8e535308488f1df213177e490eca771572`（作者 Wangyuhan29） | docs: record E3 peer review and native amd64 Docker validation | 无；直接提交 main | make check 通过：33 个共享文件锁、契约样例、26 项测试及 C2/历史检查；Ubuntu 失败/成功基线符合预期，原始日志待取回 |

此次没有其他成员新增提交或人工审阅的确认信息，因此未新增其完成记录。上表记录组织与文档工作；AI 参与范围见 AI_USAGE，不能将 Ubuntu 观察记录视为原始日志已归档。
