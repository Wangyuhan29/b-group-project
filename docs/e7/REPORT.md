# E7 实验报告

王宇晗（241250086），B03，B 轨道 DRAFT。仓库：[b-group-project](https://github.com/Wangyuhan29/b-group-project)。

最终服务器实测源码：`c4c4f76ff79a0cb73a77da962be76eefb054211b`。实际运行日期为 2026-10-28，Ubuntu 24.04.4 LTS、linux/amd64、2 vCPU、可见内存 1.7 GiB、可用磁盘 68.3 GiB。此前按 2 核 2 GiB 配置实测，自检通过；新版最低内存要求为 4 GiB，原环境不满足该项，未按新版规格复跑。

## 1. 验证场景

| 场景 | 输入或故障注入 | 预期 | 实际状态与退出码 | 验收 | 证据 |
|---|---|---|---|---|---|
| unit-tests | 运行服务测试 | 退出 0 | 退出 / 0 | PASS | [场景目录](../../artifacts/e7/linux-amd64-final-20261028/e7-final/gate/unit-tests/) |
| success | 回放适配候选 | SUCCEEDED / 0 | SUCCEEDED / 0 | PASS | [场景目录](../../artifacts/e7/linux-amd64-final-20261028/e7-final/gate/success/) |
| wrong-output | 故意改错预期输出 | FAILED / 1 | FAILED / 1 | PASS | [场景目录](../../artifacts/e7/linux-amd64-final-20261028/e7-final/gate/wrong-output/) |
| invalid-candidate | 改写候选 CMD | FAILED / 1 | FAILED / 1 | PASS | [场景目录](../../artifacts/e7/linux-amd64-final-20261028/e7-final/gate/invalid-candidate/) |
| build-failed | 候选加入 RUN exit 23 | FAILED / 1 | FAILED / 1 | PASS | [场景目录](../../artifacts/e7/linux-amd64-final-20261028/e7-final/gate/build-failed/) |
| runtime-timeout | 注入 sleep，缩短运行预算 | TIMED_OUT / 1 | TIMED_OUT / 1 | PASS | [场景目录](../../artifacts/e7/linux-amd64-final-20261028/e7-final/gate/runtime-timeout/) |

## 2. 结果核对

正常场景首轮退出 1（MISSING_MAKE），第二轮构建退出 0；使用第二轮镜像 ID 禁网运行，退出 0，输出 hello E3。输出不符时 output_matches=false；无效候选在构建前拒绝；第二轮构建失败时不执行程序验证。超时场景第二轮构建成功后进入 TIMED_OUT，[清理日志](../../artifacts/e7/linux-amd64-final-20261028/e7-final/gate/runtime-timeout/evidence/cleanup-check/stderr.log)显示容器已不存在。

整体门禁退出 0，六项均通过：[gate-result.json](../../artifacts/e7/linux-amd64-final-20261028/e7-final/gate/gate-result.json)、[results.csv](../../artifacts/e7/linux-amd64-final-20261028/e7-final/gate/results.csv)。候选沿用[E6 候选来源记录](../e6/CANDIDATE_SOURCE.json)：回放教师保存的 DeepSeek 候选，并适配基础镜像固定摘要与下载源，本次未调用模型 API。

## 3. 自己新增的测试

[test_student_boundary.py](../../services/draft/tests/test_student_boundary.py)新增三项：候选 COPY 遗漏 Makefile 时拒绝；初始与候选的固定摘要相同时接受；候选更换既有摘要时拒绝。三项均通过。教师基线 24 项加本组保留的 E4 测试 3 项，新增前为 27 项；新增后重建为 30 项通过；加入正确的 CI 演示断言后，[最终服务器重建](../../artifacts/e7/linux-amd64-final-20261028/build-final/)为 31 项通过。另见[修改后重建及单测](../../artifacts/e6/linux-amd64-20261028/build-02/)。

## 4. CI 与合并门禁

| 阶段 | 运行链接 | 分支 head SHA | artifact 的 commit.txt | 结果 | 下载归档 |
|---|---|---|---|---|---|
| 正常 | [40647145632](https://github.com/Wangyuhan29/b-group-project/actions/runs/40647145632) | `849df98e03358201fd943a9b640d378717ebf0ab` | `849df98e03358201fd943a9b640d378717ebf0ab` | 通过 | [artifact](../../artifacts/e7/github-20261028/normal/artifact/) |
| 故意失败 | [40647276388](https://github.com/Wangyuhan29/b-group-project/actions/runs/40647276388) | `f015fc5fcd5c694162292b4a6a49530a6814da27` | `c0152bb6a086ec0c8a924815f6bff6d133c028b4` | 1 failed、30 passed | [artifact](../../artifacts/e7/github-20261028/rejection/artifact/) |
| 恢复 | [40647571082](https://github.com/Wangyuhan29/b-group-project/actions/runs/40647571082) | `7b6b69f22103c2a850fb57876e4d150aa8ee44a0` | `31d5da13ff2d2c83cbe6a40accfd5b5511f2a16d` | 31 项测试和六项门禁通过 | [artifact](../../artifacts/e7/github-20261028/recovery/artifact/) |

两次 PR 检查的 commit.txt 记录工作流实际测试的合并版本，运行元数据中的 head SHA 记录 PR 分支，两者分别保留。

[PR #2](https://github.com/Wangyuhan29/b-group-project/pull/2) 的必需检查为 e7-b-quality-gate，App ID 15368，strict 和 enforce_admins 均为 true。见[实际保护配置](../../artifacts/e7/github-20261028/rejection/protection.json)。普通合并退出 1，保存了[拒绝日志](../../artifacts/e7/github-20261028/rejection/merge-rejection.log)与[OPEN / BLOCKED 快照](../../artifacts/e7/github-20261028/rejection/PR-after.json)。同一 PR 将 version 退出码预期由 1 恢复为 0，最新检查通过后合并。mergeCommit 为报告开头的服务器实测 SHA，mergedAt 为 2026-10-28T07:05:59Z，见[最终合并记录](../../artifacts/e7/github-20261028/recovery/PR-merged.json)。

## 5. 文件索引

- [实现代码](../../services/draft/draft/)、[个人记录](STUDENT_241250086.md)、[贡献与提交](CONTRIBUTIONS.md)。
- [服务器原始证据](../../artifacts/e7/linux-amd64-final-20261028/manifest.json)索引输入副本、JSON/CSV、命令与 stdout/stderr；另存[环境自检](../../artifacts/e7/linux-amd64-final-20261028/final-doctor-console.log)和[含 Git 历史的密钥扫描](../../artifacts/e7/linux-amd64-final-20261028/final-secret-scan.txt)。
- [CI 证据清单](../../artifacts/e7/github-20261028/manifest.json)、[CI 详细记录](CI_RECORD.md)、[新版验收表](ACCEPTANCE.csv)。
