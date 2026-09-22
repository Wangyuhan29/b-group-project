# 个人贡献记录



| 日期 | 姓名/学号 | 工作和文件                                                                                                                         | commit SHA | 提交说明 | Issue/PR | 验证结果 |
|---|---|------------------------------------------------------------------------------------------------------------------------------------|---|---|---|---|
| 2026-09-19—09-22 | 王宇晗（241250086） | 统筹 minicalc C2 接入、DRAFT 环境、GHCR 镜像、共享锁、A/B 联调和提交材料；`contracts/shared-lock.json`、镜像工作流、`fixtures/minicalc/project.json`、`docs/PAIR_REVIEW.md`、`docs/SUBMISSION.md` | `c458e7b88d86d8e1203f5e5d5280e0f6dbae71f4`、`da50ca9b24a775bf42a0e6d6c9563c5c4a656275`、`a5cd08dca0dc95f11ce787060ccf61c0afc2fe3d`、`0caf9beab227e52a194d2a1e85893bec0482c243`（实际作者均为 Wangyuhan29） | 建立 B03 仓库，完成共享契约、镜像交接和 A03 评审材料 | 无 Issue/PR；主线统一提交 | `make check`、33 文件锁校验和 C2 镜像交接证据通过 |
| 2026-09-20 | 朱玄（241250017） | MDFixer 方向：4 条 MD 的修复逻辑、Patch、修复后构建与重检结果复核；补充 MDFixer 验收说明和 Windows 编码/源码快照检查记录 | `beb69e377c5fcdf81b42a77ada094d76ffb46760`（独立提交，作者 xuan zhu）；相关整理 `5841b9df4d6c412106915b0bdba51b7c7386e264`（统一提交） | 记录 MDFixer 验证结果并完善修复材料 | 无 Issue/PR | 修复前 4 MD/0 RD，修复后 0 MD/0 RD |
| 2026-09-19—22 | 靳滨硕（241250075） | 契约与质量方向：`graph.schema.json`、`finding-id-v1.json`、`shared-lock.json`、锁校验、测试和提交文档复核 | `da50ca9b24a775bf42a0e6d6c9563c5c4a656275`、`0caf9beab227e52a194d2a1e85893bec0482c243`（共同工作内容由王宇晗统一提交，Git 作者未冒充靳滨硕） | 完成共享契约同步、A/B 评审证据和质量复核 | 无 Issue/PR；个人参与需以课堂记录/审阅记录佐证 | 33 个共享文件哈希一致；26 项单元测试通过 |

可用 `git log --format='%H %an <%ae> %s'` 获取真实版本、作者和说明；截图仅辅助。
