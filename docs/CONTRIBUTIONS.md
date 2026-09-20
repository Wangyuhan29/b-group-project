# 个人贡献记录



| 日期 | 姓名/学号 | 工作和文件 | commit SHA | 提交说明 | Issue/PR | 验证结果 |
|---|---|---|---|---|---|---|
| 2026-09-17 | 王宇晗（241250086） | 统筹 minicalc C2 接入、DRAFT 环境、GHCR 镜像、A/B 联调材料；`README.md`、`fixtures/minicalc/project.json`、`docs/IMAGE_HANDOFF.md` | `a5cd08d`（统一提交） | 完成 C2 镜像交接与当前请求更新 | 无独立 Issue/PR；仓库提交记录可核对 | `make check` 通过；C2 镜像构建和容器断言通过 |
| 2026-09-17 | 朱玄（241250017） | MDFixer 方向：4 条 MD 的修复逻辑、Patch、修复后构建与重检结果复核 | `a5cd08d`（统一提交） | 完成 C2 修复验收材料 | 无独立 Issue/PR；需补充个人审阅记录 | 修复前 4 MD/0 RD，修复后 0 MD/0 RD |
| 2026-09-17 | 靳滨硕（241250075） | 契约与质量方向：`graph.schema.json`、`finding-id-v1.json`、`shared-lock.json`、锁校验和提交文档复核 | `a5cd08d`（统一提交） | 完成共享契约同步与验证材料 | 无独立 Issue/PR；需补充个人审阅记录 | 33 个共享文件哈希一致；26 项单元测试通过 |

可用 `git log --format='%H %an <%ae> %s'` 获取真实版本、作者和说明；截图仅辅助。

## 2026-09-20：朱玄（241250017）工作记录

- MDFixer 核验材料：核对四条 MD 与补丁的对应关系，补充 Windows 编码、换行及源码快照检查未通过的结果；本轮不标记整套验收通过。
- 个人提交作者：`xuan zhu <2983618236@qq.com>`；提交编号可用 `git log -1 --format=%H -- docs/CONTRIBUTIONS.md` 查询。
