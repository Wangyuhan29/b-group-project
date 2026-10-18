# 个人贡献记录



| 日期 | 姓名/学号 | 工作和文件                                                                                                                         | commit SHA | 提交说明 | Issue/PR | 验证结果 |
|---|---|------------------------------------------------------------------------------------------------------------------------------------|---|---|---|---|
| 2026-09-19—09-22 | 王宇晗（241250086） | 统筹 minicalc C2 接入、DRAFT 环境、GHCR 镜像、共享锁、A/B 联调和提交材料；`contracts/shared-lock.json`、镜像工作流、`fixtures/minicalc/project.json`、`docs/e2/PAIR_REVIEW.md`、`docs/e2/SUBMISSION.md` | `c458e7b88d86d8e1203f5e5d5280e0f6dbae71f4`、`da50ca9b24a775bf42a0e6d6c9563c5c4a656275`、`a5cd08dca0dc95f11ce787060ccf61c0afc2fe3d`、`0caf9beab227e52a194d2a1e85893bec0482c243`（实际作者均为 Wangyuhan29） | 建立 B03 仓库，完成共享契约、镜像交接和 A03 评审材料 | 无 Issue/PR；主线统一提交 | `make check`、33 文件锁校验和 C2 镜像交接证据通过 |
| 2026-09-20 | 朱玄（241250017） | MDFixer 分工；独立提交内容为贡献表和 AI_USAGE 中的核验说明，记录 Windows 编码、换行和源码快照检查未通过项 | `beb69e377c5fcdf81b42a77ada094d76ffb46760`（独立文档提交，作者 xuan zhu）；`5841b9df4d6c412106915b0bdba51b7c7386e264` 为 Wangyuhan29 的文档整理提交 | 记录 MDFixer 验证结果； | 无 Issue/PR | 修复前 4 MD/0 RD，修复后 0 MD/0 RD |
| 2026-09-19—22 | 靳滨硕（241250075） | 契约与质量方向：`graph.schema.json`、`finding-id-v1.json`、`shared-lock.json`、锁校验、测试和提交文档复核 | `da50ca9b24a775bf42a0e6d6c9563c5c4a656275`、`0caf9beab227e52a194d2a1e85893bec0482c243`（共同工作内容由王宇晗统一提交，Git 作者未冒充靳滨硕） | 完成共享契约同步、A/B 评审证据和质量复核 | 无 Issue/PR；本轮审阅确认见 AI_USAGE | 33 个共享文件哈希一致；26 项单元测试通过 |

可用 `git log --format='%H %an <%ae> %s'` 获取真实版本、作者和说明；截图仅辅助。

2026-09-22 人工审阅：根据朱玄提供的确认信息，王宇晗、朱玄、靳滨硕已确认各自分工范围内的文档审阅结论，详见 `AI_USAGE.md`。

## E3 补充记录（2026-10-09）

| 姓名/学号 | 工作与文件 | commit SHA | 提交说明 | Issue/PR | 验证结果 |
|---|---|---|---|---|---|
| 王宇晗（241250086） | 在 AI 辅助下组织 A03 基线互查、Ubuntu amd64 DRAFT Docker 验证，整理 E3 README、BACKLOG、验证记录及证据状态 | `10db4f8e535308488f1df213177e490eca771572`（作者 Wangyuhan29） | docs: record E3 peer review and native amd64 Docker validation | 无；直接提交 main | make check 通过：33 个共享文件锁、契约样例、26 项测试及 C2/历史检查；Ubuntu 失败/成功基线符合预期，原始日志待取回 |

此次没有其他成员新增提交或人工审阅的确认信息，因此未新增其完成记录。上表记录组织与文档工作；AI 参与范围见 AI_USAGE，不能将 Ubuntu 观察记录视为原始日志已归档。


## E3 证据归档与收尾（2026-10-09）

| 姓名/学号 | 工作与文件 | commit SHA | 提交说明 | Issue/PR | 验证结果 |
|---|---|---|---|---|---|
| 王宇晗（241250086） | AI 辅助取回 Ubuntu 21 个原始文件、核验哈希/退出码/源码，补齐 E3_SUBMISSION、Backlog、验证及阶段完成记录，重跑基线 | `497ff2e05757010c3097fb4d3f2ec0d89a1f0c5a`（作者与提交者 Wangyuhan29） | docs: archive Ubuntu Docker logs and complete B03 E3 checklist | 无；直接提交 main | Ubuntu 构建/运行证据校验通过；四类修复与拒绝恢复 PASS；make check 通过 |

上述记录更新前一轮“原始日志待取回”的历史状态：现已归档。其他成员保留已有分工和贡献，没有新增未经确认的工作或审阅声明。

## E4 服务器环境与首名组员运行（2026-10-15）

王宇晗（241250086）在 AI 辅助下接入课程模板、按教师 2 核 2G 配置调整自检容差、初始化服务器、处理下载源并完成个人 make all、假 Key 检查及原始证据归档。实际代码提交：`119ad88aa6fcd88a2638f020bb9d7ccf80674d46`（模板接入）、`8701f70d4a3f76592832eedde62b02bb59711ef4`（最终服务器实测版本，含 Debian 和 PyPI 适配），作者为学号 241250086；未使用 Issue/PR。结果见 docs/e4/SERVER_VERIFICATION.md；此为首名组员归档时状态，其他成员的后续记录见下表。

## E4 其他成员归档与对照（2026-10-15）

| 成员 | 工作和证据 | commit SHA 与真实作者 | 验证 |
|---|---|---|---|
| 朱玄（241250017） | 归档独立学号目录运行、假 Key 拒绝与恢复、同版本对比；docs/e4/MEMBER_COMPARISON_241250017.md | dc080d3090aca0b772d40b290d08d1c9e84516f3；作者 xuan zhu，2983618236@qq.com | 原始文件哈希通过；同 SHA、工具清单和 6 项单测一致，冒烟及扫描通过 |
| 靳滨硕（241250075） | 归档独立学号目录运行、假 Key 拒绝与恢复、三人结果对比；docs/e4/MEMBER_COMPARISON_241250075.md | 85fb8c021b845423e319fa3e3e8e0335486f5f06；作者靳滨硕，241250075@smail.nju.edu.cn | 原始文件哈希通过；同 SHA、工具清单和 6 项单测一致，冒烟及扫描通过 |

两份归档分别说明由 Codex、ZCode 代理辅助执行，不将学号身份等同于成员亲手操作。用户反馈全组完成测试，本次据真实 Git 提交与原始证据补录，不新增其他人工审阅声明。未使用 Issue/PR；既有提交作者不改写，后续按课程要求以学号提交。

## E4 双向互查收尾（2026-10-18）

王宇晗（241250086）：AI 辅助在本人学号目录复核 A03 固定 SHA 6abc4d815b4a4baae7cc9d72fc221653a7897e19，确认 make all、3 项单测、系统调用冒烟和扫描通过；复核 A03 对 B03 的固定 SHA 8701f70 原始日志及哈希，归档两方向证据并更新互查状态。材料见 docs/e4/A03_CROSS_VALIDATION_20261018.md。本次 B03 归档提交 SHA 随文档整理提交补录，与被测 A03 SHA 分开记录。
