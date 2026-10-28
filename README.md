# B03 · DRAFT / MDFixer

南京大学 DevOps 课程 B03 小组项目，对应 A03，鼓楼校区。成员：王宇晗（241250086）、朱玄（241250017）、靳滨硕（241250075）。

B03 负责 DRAFT 构建环境与 MDFixer 缺失依赖修复，A03 负责 BuildChecker / EChecker。服务代码统一维护，文档与运行证据按实验阶段归档。

## 阶段概览

| 阶段 | 主要内容 | 当前进展与详细记录 |
|---|---|---|
| E2 · 需求与接口契约 | 统一任务模型、请求/响应、错误与产物格式，完成配对评审和 Minicalc 镜像交接。 | 契约、样例和交接材料已归档；[E2 文档](docs/e2/README.md)。 |
| E3 · 并行测试基线 | 准备 DRAFT 成功/失败输入，以及四种 Makefile 风格的 MDFixer 参考补丁。 | 基线、原生 amd64 Docker 复验与互查记录已归档；[E3 文档](docs/e3/README.md)。 |
| E4 · 可重复工程环境 | 固定服务镜像与依赖，执行环境自检、构建、测试、冒烟和密钥扫描。 | 三个学号目录运行对照及 A03/B03 双向互查已完成；[E4 文档](docs/e4/README.md)。 |
| E5 · DRAFT 方法复现 | 从真实缺 make 失败生成提示，选择候选并手工构建、运行验证。 | 已按教师允许的记录候选回放路线实测，保留来源及环境适配；[E5 文档](docs/e5/README.md)。 |
| E6 · 核心工作流 | 自动执行初始失败、候选构建，再以构建所得镜像 ID 验证程序。 | 两轮构建和证据一致性校验通过；[E6 文档](docs/e6/README.md)。 |
| E7 · 验证与 CI | 新增边界测试，覆盖成功和故障场景，验证 CI 拦截与恢复。 | 最终 31 项服务测试、六场景门禁及同 PR 失败/恢复验证通过；[E7 文档](docs/e7/README.md)、[CI 记录](docs/e7/CI_RECORD.md)。 |

E5—E7 现有证据对应王宇晗的个人轨道与小组共享 CI。其他成员须各自新增测试、保存运行记录并提交个人 PR；实际贡献见各阶段的 CONTRIBUTIONS.md。

## 常用命令

以下命令均在仓库根目录执行。E4—E7 正式实验使用 Linux 服务器与 Docker；每名成员使用自己的学号目录、本仓库 Git 身份和镜像标签。

### E5—E7

组员统一从已验证基线 `2dc97ff3b9dd8d00a9c49dddf1efdab0ee75bdf7` 建立个人分支 `student/学号/e5-e7`。阶段文档记录各次实际测试 SHA，新增测试后重新构建并运行门禁。

```sh
python3 scripts/course.py doctor
python3 scripts/course.py build --out work/build-01 --build-timeout 1200
python3 scripts/course.py e5 --candidate fixtures/ci-candidates/B03-E5.Dockerfile --out work/e5-01 --build-timeout 1200
python3 scripts/course.py e6 --candidate fixtures/ci-candidates/B03-E5.Dockerfile --out work/e6-01 --build-timeout 1200
python3 scripts/course.py gate --candidate fixtures/ci-candidates/B03-E5.Dockerfile --out work/e7-01 --build-timeout 1200
```

每一步成功后再执行下一步；输出目录必须全新，复跑时递增编号，保留原日志。E5 的候选手工构建与同镜像运行步骤见 [E5 说明](docs/e5/README.md)，E6 证据核验见 [E6 说明](docs/e6/README.md)。

### 前序实验与回归

| 命令 | 用途 |
|---|---|
| `make all` | E4 环境自检、服务构建、测试、冒烟与扫描；默认 make 也执行此流程。 |
| `make check` | E2/E3 共享契约校验、Minicalc 测试、修复演示及三版本历史验证。 |
| `python3 scripts/verify_e3_baselines.py` | E3 DRAFT / MDFixer 独立测试基线。 |
| `make regression-test` | 原根目录 tests/ 回归；`make test` 执行服务镜像内的测试。 |

## 项目结构

维护中的主要目录如下。原始日志保留在各阶段的运行目录中，目录树只展开到用途清晰的层级。

```text
b-group-project/
├── README.md                         项目说明、阶段概览与常用命令
├── Makefile                          E4 全流程及前序回归入口
├── compose.yaml                      服务资源限制与 Docker socket 配置
├── requirements-dev.in               直接测试依赖
├── requirements-dev.lock             带哈希的依赖锁
├── .env.example                      本地配置示例
├── validate.py                       接口契约与产物引用校验
├── CHANGELOG.md                      项目变更记录
├── .github/
│   ├── workflows/
│   │   ├── check.yml                 契约与 Minicalc 回归
│   │   ├── minicalc-image.yml        C2 镜像构建与发布
│   │   └── e7-quality-gate.yml       E7 构建、扫描、六场景门禁与证据上传
│   └── PULL_REQUEST_TEMPLATE.md
├── services/draft/
│   ├── Dockerfile                    服务镜像与工具链
│   ├── draft/
│   │   ├── cli.py                    version / smoke / auto-build 入口
│   │   ├── smoke.py                  冒烟验证
│   │   └── autobuild.py              两轮构建与程序验证
│   ├── tests/                        服务测试与个人边界测试
│   └── pytest.ini
├── scripts/
│   ├── course.py                     学号隔离的 E5—E7 入口
│   ├── lab_cloud.py                  云端实验调度
│   ├── prepare_e5_prompts.py         从实际失败日志生成两类提示
│   ├── verify_e6_b_evidence.py       构建与运行证据一致性校验
│   ├── run_e7_b_gate.py              完整六场景门禁
│   ├── prepare_e7_ci_inputs.py       CI 下载源适配与输入哈希记录
│   ├── doctor.py                     环境与 Git 身份检查
│   ├── secret_scan.py                源码、历史与镜像密钥扫描
│   ├── check_shared_lock.py          共享契约锁校验
│   ├── minicalc.py                   Minicalc 扫描与修复演示
│   ├── verify_minicalc.py            功能断言
│   ├── verify_history.py             C0/C1/C2 历史验证
│   ├── verify_e3_baselines.py        E3 基线验证
│   └── demo.py                       旧教学演示
├── contracts/                        与 A03 共享的接口契约
│   ├── task.schema.json              公共 Job 模型
│   ├── graph.schema.json             依赖图格式
│   ├── finding-id-v1.json            稳定发现 ID 规则
│   ├── openapi.json                  API 定义
│   ├── shared-lock.json              共享文件哈希锁
│   ├── examples/                     请求、响应与错误样例
│   ├── minicalc/                     C2 任务与固定报告
│   └── minicalc-history/             C0/C1/C2 任务样例
├── fixtures/                         固定实验输入与参考答案
│   ├── draft/                        E4—E7 Tiny Greeting 项目
│   ├── ci-candidates/                教师候选、B03 适配与来源
│   ├── e3/
│   │   ├── draft/                    E3 DRAFT 成功/失败样本
│   │   └── mdfixer/                  四种 Makefile 风格与参考补丁
│   ├── minicalc/
│   │   ├── source/                   固定 C2 源码
│   │   ├── history.bundle            C0/C1/C2 离线 Git 历史
│   │   └── project.json              版本、配置与源码哈希
│   ├── draft-project/                旧教学项目
│   └── md-report.json / source.*     旧教学输入
├── course-support/
│   ├── import-receipt.json           教师参考文件导入记录
│   ├── e5-recorded-source/           原始记录候选、提示和选择过程
│   ├── ci/                           门禁配置及失败/恢复演示模板
│   └── templates/                    教师报告与验收模板
├── docs/                             各阶段独立文档
│   ├── e2/                           接口、评审、ADR 与交接
│   │   ├── README.md
│   │   ├── AI_USAGE.md
│   │   ├── BACKLOG.md
│   │   ├── CONTRIBUTIONS.md
│   │   ├── IMAGE_HANDOFF.md
│   │   ├── INTERFACE.md
│   │   ├── MINICALC_HANDOFF.md
│   │   ├── PAIR_REVIEW.md
│   │   ├── REPLY_TO_A.md
│   │   ├── REQUIREMENTS.md
│   │   ├── SHARED_SYNC.md
│   │   ├── SUBMISSION.md
│   │   ├── TEAM.md
│   │   ├── VERIFICATION.md
│   │   ├── adr/
│   │   └── records/
│   ├── e3/                           测试基线与提交核对
│   │   ├── README.md
│   │   ├── AI_USAGE.md
│   │   ├── BACKLOG.md
│   │   ├── CONTRIBUTIONS.md
│   │   ├── SUBMISSION.md
│   │   ├── TEAM.md
│   │   └── VERIFICATION.md
│   ├── e4/                           服务器、成员对照与跨组互查
│   │   ├── README.md
│   │   ├── A03_CROSS_VALIDATION_20261018.md
│   │   ├── AI_USAGE.md
│   │   ├── BACKLOG.md
│   │   ├── CONTRIBUTIONS.md
│   │   ├── LOCAL_CHECKS.md
│   │   ├── MEMBER_COMPARISON_241250017.md
│   │   ├── MEMBER_COMPARISON_241250075.md
│   │   ├── PEER_REVIEW.md
│   │   ├── SERVER_VERIFICATION.md
│   │   ├── TEAM.md
│   │   └── VERIFICATION.md
│   ├── e5/                           失败复现、候选与手工验证
│   │   ├── README.md
│   │   ├── ACCEPTANCE.csv
│   │   ├── AI_USAGE.md
│   │   ├── BACKLOG.md
│   │   ├── CONTRIBUTIONS.md
│   │   ├── TEAM.md
│   │   └── VERIFICATION.md
│   ├── e6/                           两轮工作流与证据核验
│   │   ├── README.md
│   │   ├── ACCEPTANCE.csv
│   │   ├── AI_USAGE.md
│   │   ├── BACKLOG.md
│   │   ├── CONTRIBUTIONS.md
│   │   ├── TEAM.md
│   │   └── VERIFICATION.md
│   └── e7/                           故障门禁、CI 拦截与恢复
│       ├── README.md
│       ├── ACCEPTANCE.csv
│       ├── AI_USAGE.md
│       ├── BACKLOG.md
│       ├── CI_RECORD.md
│       ├── CONTRIBUTIONS.md
│       ├── TEAM.md
│       └── VERIFICATION.md
├── artifacts/                        已归档的运行产物与原始证据
│   ├── e3/                           基线、平台复验与 A03 互查
│   ├── e4/                           本地准备、三人运行与双向互查
│   ├── e5/                           初始失败、提示及候选手工验证
│   ├── e6/                           两轮构建、报告与镜像信息
│   ├── e7/                           初次/最终服务器门禁与 GitHub 全流程证据
│   ├── minicalc/                     C2 图、报告、Patch 与重检日志
│   ├── minicalc-history/             三版本扫描与比较
│   ├── demo/                         旧教学演示产物
│   └── index.json                    产物 URI 索引
├── tests/                            原契约与 Minicalc 回归测试
├── draft/minicalc.Dockerfile          E2 Minicalc C2 镜像
├── mdfixer/README.md                  MDFixer 说明
├── setup/bootstrap_ubuntu.sh          服务器初始化脚本
└── work/                             本地运行输出，不提交 Git
```

各阶段分别保存 TEAM、BACKLOG、AI_USAGE、CONTRIBUTIONS、VERIFICATION；新增阶段沿用相同组织方式。运行结果以对应原始日志、源码 SHA 和哈希清单为准。

`main` 已启用 `e7-b-quality-gate` 必需检查，后续修改通过个人分支发 PR。已有产物保留原始内容；本地配置 `.env`、密钥和临时 work/ 不提交。
