# 本轮目标项目适配

当前主测试目标为 A 组 minicalc C2。新样例见 contracts/minicalc，实测结果与剩余联调项见 MINICALC_HANDOFF.md 和 VERIFICATION.md；图/ID 已加入 shared-lock 并与 A 组文件核对。C2 Docker 镜像已构建发布，A 组 Checker 重检仍待完成。下面保留 E2 初版说明，涉及 fixture://draft-project、artifacts/demo 和旧样本的内容仅供兼容回归。

# E2 要求对照

依据：《E2_需求与接口契约_20260910.pptx》，共 27 页。以下为原始 PPT 文本核对结果，不依据之前助手关于“课程一定有现成仓库”的推断。四篇论文供后续算法复现，本交付按 E2 验收范围构建。

| PPT 页 | 明确要求 | 本仓库落实 | 状态                                                                                          |
|---|---|---|-----------------------------------------------------------------------------------------------|
| 2、3 | 同号 A/B 配对，B 做 DRAFT/MDFixer | TEAM、PAIR_REVIEW | 已完成                                                                                        |
| 5、19 | 环境、基线、修复、验证交接和公共字段 | Schema、INTERFACE | 公共模型已对齐；报告路径/编号及跨仓读取约定待补                                                                                    |
| 7、27 | 四个创建接口及查询，E2 不要求部署 | openapi.json | 已定义，未部署                                                                                |
| 8、9 | 六种状态；系统错误与 MD/RD 分离 | 查询记录及错误/发现样例 | 已校验                                                                                        |
| 10、23 | MD 报告有版本、位置、证据；只修 MD | 固定报告、REPAIR 语义校验 | 已校验                                                                                        |
| 12 | 负责人、产物、验收条件 | BACKLOG | 角色与 TEAM 姓名已对应；跨组待办需双方确认                                                                    |
| 13、14 | ADR、AI 建议与人工判断 | ADR-001~004、AI_USAGE | B03 三人本轮审阅已确认；ADR-001～003 的双方确认待补                                                                     |
| 15、17 | Git、作者、Issue/PR、完成及未完成 | CONTRIBUTIONS、SUBMISSION、VERIFICATION | 已有 Git、历史验证和本轮审阅记录； |
| 20 | DRAFT 仓库、命令、迭代/时限、每轮日志/修改/理由及结果 | draft 请求/响应 | 契约已定义；C2 镜像已有构建与冒烟记录                                                                      |
| 21 | 完整提交、配置、全量图、MD/RD/证据 | full 请求/响应及两类报告 | 契约已定义                                                                                    |
| 22 | 历史图、base commit、配置匹配、发现变化 | incremental 请求/响应、语义校验 | 已校验                                                                                        |
| 23 | Patch、风格、构建/测试/重检，拒绝失败候选 | repair 成功/拒绝样例及本地演示 | 真正 A 组重检待接入                                                                           |
| 24 | 产物元数据、读取方式；E12 证明另一组可读 | index、resolver、ADR-002 | 各仓内部读取通过；跨仓读取位置/同名 URI 处理待约定                                                                    |
| 25 | 四类样例、ABC 拒绝、无 baseline 拒绝 | validate.py、manifest、tests | 通过 |
| 26 | 版本兼容与变更 | ADR-004、CHANGELOG | 严格 Schema 策略已说明                                                                        |
| 17 | B 组 E3 DRAFT 项目和固定 MD | fixtures、demo | Minicalc C2 和固定 MD 已提供；C0/C1 环境待补                                                                |

## 本组自主决定，须 A 组审阅

所有对象严格拒绝未知字段；创建请求不包含服务端 job_id；时间限制放 execution.timeout_seconds；所有构建配置使用完整 commit；REPAIR 接受非空 MD-only 报告，混合报告先由上游拆分；拒绝候选可作为 SUCCEEDED 的分析结果；本地 artifact URI 映射到仓库文件。它们是实现选择，不是 PPT 原文强制的字段形式。
