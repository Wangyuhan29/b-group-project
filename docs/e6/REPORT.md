# E6 实验报告 · B03 / 王宇晗

| 信息 | 实际记录 |
|---|---|
| 姓名 / 学号 / 小组 / 轨道 | 王宇晗 / 241250086 / B03（对应 A03）/ B：DRAFT |
| 仓库地址 | https://github.com/Wangyuhan29/b-group-project |
| 本次材料依据 | DevOps_E6_Student_Cloud.zip（包内整理日期 2026-10-29，2026-10-30 核对） |
| 压缩包 SHA-256 | `c25e34bd4eb8a836ee7ec9052636b1491bcfea4e316bcff47af63bbce37a40a0` |
| 实际实验日期 | 2026-10-28；本报告按新模板整理于 2026-10-30，未将旧日志写成本日新运行 |
| 实测源码提交 SHA | `7a5a01622da340e59a15090a2b5167ae832b8398` |
| 个人代码提交 | `b85f6d2c8ebd131b65c39e6d42cad2603c000da5`、`7a5a01622da340e59a15090a2b5167ae832b8398` |
| 服务镜像标签 / ID | course1027-draft:241250086 / `sha256:589d27819c3ef552c2839a4fc0cfd7a8f10b011b172464c0df5a5a59e34a641d` |
| 服务器环境 | Ubuntu 24.04.4 LTS，x86_64，2 CPU，约 1.7 GiB 可见内存；Docker 29.1.3，Python 3.12.3（宿主机） |

本次报告、验收表及候选来源均位于 docs/e6/，实际构建输出保存在 artifacts/e6/。工作区源码与提交材料的后续版本可通过 Git 历史和 PR 追溯；上表 SHA 专指产生该次原始运行记录的代码。

## 1. 实验目标与输入

复现 DRAFT 的两轮 MVP：先真实构建缺少 make 的初始 Dockerfile，确认 MISSING_MAKE；再构建记录候选，并使用刚构建的同一镜像 ID 验证程序退出码和输出。

- 样例：`fixtures/draft/` 的 Tiny Greeting，源码 main.c 与 Makefile，目标输出 hello E3。
- 初始输入：`fixtures/draft/Dockerfile.broken`；本次实际副本保存在 `e6-01/evidence/iter-01/Dockerfile`。
- 核心实现：`services/draft/draft/autobuild.py`；CLI 为 `services/draft/draft/cli.py`。
- 候选：`fixtures/ci-candidates/B03-E5.Dockerfile`，基于教师记录 DeepSeek 候选进行下载源与既有固定基础摘要适配。
- 来源：采用新版指南允许的包内候选回放路线，无本次模型 API 调用；[完整候选来源](CANDIDATE_SOURCE.json)。初始与候选使用同一固定 FROM，但该摘要并非新包默认的 70729b…，具体环境差异保留在来源记录中。

核对今天包内 autobuild、CLI、候选约束测试、故障测试、lab_cloud 和证据校验脚本，均与 10 月 28 日教师合并包的对应原文相同；本组保留既有固定 digest 兼容修正，未用新包覆盖已经验证的工程代码。

## 2. 实际运行

执行目录：`/root/241250086/e5-e7-20261028`。下列命令对应 2026-10-28 的真实记录；course.py 将本人镜像名传递给 lab_cloud.py。证据路径均以 `artifacts/e6/linux-amd64-20261028/` 为根。

| 步骤 | 完整命令 | 实际退出码与结果 | 原始记录 |
|---|---|---|---|
| 修改后镜像构建与服务测试 | `python3 scripts/course.py build --out work/build-02 --build-timeout 1200` | build 0；服务测试 0、30 passed | build-02/build/exit-code.json、stderr.log；build-02/unit-tests/exit-code.json、stdout.log |
| 两轮构建及运行 | `python3 scripts/course.py e6 --candidate fixtures/ci-candidates/B03-E5.Dockerfile --out work/e6-01 --build-timeout 1200` | 入口 0；第一轮 build 1；第二轮 build 0；程序运行 0 | e6-01/runner/command.json、exit-code.json；e6-01/evidence/result.json 与 iter-01/、iter-02/ |
| B 证据校验 | `python3 scripts/verify_e6_b_evidence.py --run-dir work/e6-01/evidence` | 0、passed=true | e6-01/verification.json |
| 新增测试定向核验 | `docker run --rm --network none course1027-draft:241250086 pytest tests/test_student_boundary.py -q` | 0、三项边界测试通过 | student-boundary-test.log |

三项新增测试与修正已在实测提交中。build-02 在修改后重新构建镜像，随后 e6-01 重新执行原始样例。build-01 为较早试运行，本报告不以该轮日志代替修改后验证。

## 3. 结果解释

| 项目 | 实测 |
|---|---|
| 整体状态 / trace_id | SUCCEEDED / `e6-b-ea506cdf96a84d8b8b006fc8995a0d6c` |
| 第一轮 | build_exit_code=1，failure_class=MISSING_MAKE；日志包含 /bin/sh: 1: make: not found，RUN make 内部退出 127 |
| 第二轮 | build_exit_code=0；候选增加 build-essential，提供 make 与 C 编译工具 |
| 本次候选 SHA-256 | `4e3c2b003ad9b04a53be424ba0fc86c727613f00f0246e85f0195d3769ebea6d` |
| 第二轮镜像 ID | `sha256:23eab3f1095fe0aea1abf8f47b33b34da9aef5c739a7bbb61070913dcf9b8960` |
| 运行验证 | 按上述 image ID 禁网运行；exit_code=0，actual_output 为 `hello E3\n`，output_matches=true |

四项代码阅读与实际结果的对应关系：

1. **固定 FROM 和必需指令**：prepare_candidate（autobuild.py 第 28—49 行）先折叠续行，要求单阶段、带摘要的 FROM，再按原顺序逐项匹配必需指令，只允许增加 RUN。第 36 行兼容本组已经固定摘要的初始输入，仍拒绝替换已有摘要。
2. **第一轮分类与停止条件**：classify_failure（第 61—66 行）识别 shell 的 make 不存在错误，网络问题归为 INFRASTRUCTURE，其余为 OTHER_BUILD_ERROR。auto_build 第 107—112 行只在第一轮非零且分类 MISSING_MAKE 时进入第二轮；初始成功或其他错误均停止。第二轮非零也在第 113—114 行停止，不执行功能验证。
3. **构建镜像与运行镜像一致**：第 115—122 行执行 docker image inspect，将其 Id 写入第二轮 image_id，并作为 docker run 最后一个参数。报告、image-inspect.json 与 verification.command 中三处 ID 一致。
4. **退出码与输出同时检查**：第 123—128 行记录运行退出码和标准输出，去掉末尾换行后比较 hello E3。必须 exit_code=0 且 output_matches=true，才转为 SUCCEEDED；退出正常但输出错误仍为 FAILED。

以上行号对应上表实测提交的文件。原始日志、候选和输入文件哈希经 verify_e6_b_evidence.py 核验一致。网络失败不冒充 MISSING_MAKE；镜像构建成功与程序功能正确分别验收。

## 4. 自己的代码修改与新增测试

本人在 Codex 辅助下进行环境兼容修正和测试，教师实现来源与本人修改分别记录，不声明从零独立实现论文全部方法。

代码修改：autobuild.py 第 36 行允许初始 FROM 与候选带摘要 FROM 完全相同，解决既有 E4 固定摘要输入被教师未固定标签比较规则拒绝的问题；仍拒绝不同摘要。lab_cloud.py 的 E5 候选选择兼容用于既有环境，E6 构建路径保留参考行为。

新增测试：`services/draft/tests/test_student_boundary.py`。

| 测试函数 | 输入 | 预期 | 实际 |
|---|---|---|---|
| test_candidate_cannot_silently_drop_makefile | 候选 COPY 列表删去 Makefile，其余增加正常依赖安装 | 构建前 ValueError，禁止丢失关键项目输入 | 通过 |
| test_existing_pinned_baseline_is_supported | 初始与候选已有相同固定摘要 | 接受并返回保持摘要的初始轮内容 | 通过 |
| test_existing_baseline_digest_cannot_change | 候选替换既有摘要 | ValueError，拒绝更换基础输入 | 通过 |

新增测试并重建后的服务测试数量为 30：教师基线 24 项、本组保留的 E4 测试比原包多 3 项、本次边界测试 3 项。定向日志与完整服务测试日志均保留；后续 E7 增加的版本退出码演示测试属于另一阶段，不混入本次 E6 的 30 项结果。

## 5. 提交文件索引

| 内容 | 项目内位置 |
|---|---|
| 本报告 / 新版验收表 / 候选来源 | docs/e6/REPORT.md、ACCEPTANCE.csv、CANDIDATE_SOURCE.json |
| 实测源码 / 环境身份 | artifacts/e6/linux-amd64-20261028/source-commit.txt、source-status.txt、environment-20261028.json |
| 运行入口与完整调用 | artifacts/e6/linux-amd64-20261028/e6-01/invocation.json、runner/ |
| 修改后镜像构建与服务测试 | artifacts/e6/linux-amd64-20261028/build-02/ |
| 实际输入、两轮 Dockerfile 和完整日志 | artifacts/e6/linux-amd64-20261028/e6-01/evidence/project/、iter-01/、iter-02/ |
| 结构化报告与程序原始输出 | artifacts/e6/linux-amd64-20261028/e6-01/evidence/result.json、verify.log、verify-stderr.log |
| 证据一致性结果 / 定向测试 | artifacts/e6/linux-amd64-20261028/e6-01/verification.json、student-boundary-test.log |
| 完整性清单 | [原始证据 manifest](../../artifacts/e6/linux-amd64-20261028/manifest.json) |

全部证据来自本人服务器目录，不使用新包 reference_results 冒充个人运行。原始 work/ 继续忽略，需保留的输出已按运行目录原样归档到 artifacts/e6/；按用户要求本次不另行打包。本人实测已覆盖新版 B 验收项；其他成员仍须提交其本人新增测试、运行结果及贡献。
