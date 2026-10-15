# B03 项目：DRAFT / MDFixer

## E4 可重复工程环境

已接入课程 B-draft 模板，正式 Linux 服务器运行 `make all`。服务位于 `services/draft/`，运行参数在根目录 `compose.yaml`，依赖锁和 `.env.example` 均按课件放在根目录。王宇晗已在服务器完成全流程，241250017、241250075 目录也已按用户授权完成实际复跑，对比结论一致，执行方式和边界见 [复跑对比](docs/e4/MEMBER_COMPARISON_241250017.md)、[复跑对比（241250075）](docs/e4/MEMBER_COMPARISON_241250075.md)。完整步骤与当前验收状态见 [E4 文档](docs/e4/README.md)。原 E2/E3 验证继续使用 `make check`，原根目录单测改名为 `make regression-test`。


## E3 并行测试基线（2026-09-30）

B03 的 DRAFT 失败与参考成功样本、固定 MD 报告、四种 Makefile 风格补丁、重跑命令和实际日志见 [docs/e3/README.md](docs/e3/README.md)。E3 本地基线执行命令：`python3 scripts/verify_e3_baselines.py`。Tiny Greeting 的两次 Docker 构建及容器验证已在本机完成，证据见 `artifacts/e3/docker-20260930/`；原有 C2 镜像证据另见 `docs/e2/IMAGE_HANDOFF.md`。

本仓库负责 DRAFT 环境生成和 MDFixer 缺失依赖修复；A 组负责 BuildChecker / EChecker。共同测试目标已切换为 A 组提供的 minicalc。这里仍是 B 组工具仓库，目标源码放在 fixtures/minicalc/source。

## 现在运行什么

原 E2/E3 回归需要 Python 3.10+、Git、GNU Make 和支持 -MM 的 gcc，不需要第三方 Python 包。E4 服务测试另使用 requirements-dev.lock，正式环境由 Docker 构建。

```bash
make check
```

它校验原有公共契约和新增 minicalc 样例，运行测试，再在临时副本上完成 C2 构建、四条 MD 检测、补丁生成/应用、构建与结果断言、本地依赖重检和增量重建检查。真实输出在 work/minicalc-run，不修改固定源码。


## 当前材料与验证边界

- 目标仓库：https://github.com/hardtosleep/Minicalc-DevOps-Test.git
- 当前源码为收到的 main.zip，ZIP comment 记录 C2：e103bcb3726a3fd7253deb0d791ac74fac77cafe。源码文件逐一固定 SHA-256。
- 已通过本机 SSH 成功 clone 并独立核验 c0/c1/c2；C2 ZIP 的全部源码文件与 Git C2 完全一致。
- 三个真实版本已构建和扫描，C0/C1/C2 分别为 3/1、4/1、4/0（MD/RD）；完整历史保存在 fixtures/minicalc/history.bundle。
- 本地 C2 实测 4 MD / 0 RD；补齐 4 条依赖后，本机编译器依赖对照为 0 MD / 0 RD。
- C2 镜像已在 GitHub Actions 构建、通过容器断言并发布至私有 GHCR，见 [镜像交接](docs/e2/IMAGE_HANDOFF.md)。A 组真实 Checker 联调仍待完成。

## 优先阅读与使用

| 文件/目录 | 作用 |
|---|---|
| fixtures/minicalc/project.json | C0/C1/C2 SHA、来源可信范围、C2 文件哈希、配置与镜像状态 |
| contracts/minicalc/ | DRAFT/FULL_CHECK/REPAIR 的 C2 请求、本地结果映射和固定 MD 报告 |
| artifacts/minicalc/c2/ | 真实本地日志、图、证据、MD 报告、Patch 及重检报告 |
| scripts/minicalc.py | 明确限定为 minicalc 显式规则的构建、扫描、修复和验证演示 |
| scripts/verify_minicalc.py | 三个算术结果与版本的自动断言，弥补上游 make test 只打印结果 |
| draft/minicalc.Dockerfile | 已在 GitHub Actions 验证的 C2 环境 |
| contracts/graph.schema.json | 已与 A 组文件核对并加入共享锁 |
| contracts/finding-id-v1.json | finding_id 算法与测试向量；已加入共享锁 |
| docs/e2/REPLY_TO_A.md | 可以发给 A 组的具体答复 |
| docs/e2/MINICALC_HANDOFF.md | 读取方法、环境边界、三个版本的核验与边界 |

原 contracts/examples、artifacts/demo、fixtures/draft-project 及 scripts/demo.py 保留为旧教学样本与兼容性回归，**不是 minicalc 正式输入**。make demo 已改为 minicalc；make legacy-demo 可重放旧演示。公共 task.schema.json/OpenAPI/validate.py 没有改字段，不要求 A 组立刻升级公共模型。

contracts/minicalc 中的 *-response-local.json 是本机结果向公共模型的映射，不是 Docker/API 执行记录。当前 full-request / repair-request 已使用真实 C2 digest；旧本地响应保留当时的 NOT-BUILT 状态。共享 33 个文件的核对结果见 [SHARED_SYNC](docs/e2/SHARED_SYNC.md)。

## 本地重新构建镜像

在本仓库根目录执行：

```bash
docker build -f draft/minicalc.Dockerfile -t minicalc-devops:c2 .
docker run --rm minicalc-devops:c2
```

已发布镜像的固定 digest 和拉取命令见 [IMAGE_HANDOFF](docs/e2/IMAGE_HANDOFF.md)。重新构建可能产生不同 digest。此 Dockerfile 仅复制 C2 源码，C0/C1 的准确源码已在 history.bundle 中，Dockerfile 仍需按版本固定环境输入。

## 下一步

先与 A 组统一报告中的 `include/*.h` 路径、问题编号和产物读取位置，再进行真实 Checker 联调。

TEAM、贡献表及 B03 三人本轮审阅记录已填写；ADR-001～003 的双方确认仍需补齐。历史提交已同步 GitHub，本次本地修订的验证结果见 [VERIFICATION](docs/VERIFICATION.md)。

## Git 历史重放

已配置的 SSH 地址为 `git@github.com:hardtosleep/Minicalc-DevOps-Test.git`。接口 repository.url 仍保留原 HTTPS 标识以稳定 finding ID，clone_url 单独记录 SSH 传输地址。

`make history` 在临时目录离线 clone history.bundle，逐版本构建并比较发现，输出 work/minicalc-history。保存的真实扫描产物在 artifacts/minicalc-history，6 份任务样例在 contracts/minicalc-history。这里仍为逐版本全量扫描后比较，不声称实现 EChecker 增量算法；历史样例保留原占位值；本次发布仅覆盖 C2，不能直接用于 C0/C1 源码检测。

## E3 进展（2026-10-09）

已完成 A03 基线的构建与行为互查，并在原生 Ubuntu x86_64 完成 B03 DRAFT Docker 失败/参考成功验证。详见 [E3 文档](docs/e3/README.md)。Ubuntu 成功构建使用 Debian 镜像源变体，原始日志已取回并校验归档；A03 strace 动态关系尚未独立验证，四服务联调未完成。

## 项目结构

以下展示维护中的主要目录和文件。原始日志按运行目录归档，不逐一展开；本地缓存和 IDE 文件不列入项目结构。

```text
b-group-project/
├── README.md                         项目入口、运行方法与当前进展
├── Makefile                          E4 all/test/smoke/scan；旧 check/regression-test
├── validate.py                       公共契约与产物引用校验
├── CHANGELOG.md                      契约与项目变更记录
├── .gitignore                        本地缓存、密钥和临时输出忽略规则
├── .github/
│   ├── workflows/
│   │   ├── check.yml                 项目持续集成检查
│   │   └── minicalc-image.yml        C2 镜像构建、验证与发布
│   └── PULL_REQUEST_TEMPLATE.md      PR 说明模板
├── compose.yaml                      E4 运行限制与 Docker socket 挂载
├── requirements-dev.in               E4 直接测试依赖
├── requirements-dev.lock             E4 带哈希依赖锁
├── .env.example                      空密钥运行配置示例
├── services/draft/                   E4 及后续 DRAFT 服务
│   ├── Dockerfile                    固定基础镜像与 Docker CLI digest
│   ├── draft/                        version 与 smoke CLI
│   ├── tests/                        服务单元测试
│   └── pytest.ini
├── setup/bootstrap_ubuntu.sh         课程服务器初始化脚本（按需）
├── draft/
│   ├── README.md                     DRAFT 说明
│   └── minicalc.Dockerfile           Minicalc C2 构建环境
├── mdfixer/
│   └── README.md                     MDFixer 说明与实现范围
├── contracts/                        A/B 共享接口契约，路径保持稳定
│   ├── task.schema.json              公共任务模型
│   ├── graph.schema.json             依赖图结构
│   ├── finding-id-v1.json            稳定发现 ID 算法与测试向量
│   ├── openapi.json                  API 定义
│   ├── shared-lock.json              共享文件 SHA-256 锁
│   ├── examples/                     公共请求、响应和错误正反例
│   ├── minicalc/                     C2 任务、固定报告及本地结果样例
│   └── minicalc-history/             C0/C1/C2 历史任务样例
├── fixtures/                         固定测试输入与人工参考答案
│   ├── minicalc/                     共同目标项目
│   │   ├── source/                   固定 C2 源码
│   │   ├── history.bundle            C0/C1/C2 完整 Git 历史
│   │   └── project.json              版本、配置及源码哈希
│   ├── draft/                        E4 模板固定 digest 的 Tiny Greeting
│   ├── e3/
│   │   ├── draft/                    Tiny Greeting 源码、Makefile、失败/参考 Dockerfile
│   │   └── mdfixer/                  固定 MD、四种声明风格与参考 Patch
│   ├── draft-project/                旧教学项目，保留兼容回归
│   ├── md-report.json                旧教学固定报告
│   ├── source.json                   旧教学源码描述
│   └── source.bundle                 旧教学源码历史
├── scripts/
│   ├── doctor.py                     E4 环境与提交身份自检
│   ├── secret_scan.py                工作区、历史和镜像密钥扫描
│   ├── check_shared_lock.py          校验共享文件锁
│   ├── minicalc.py                   Minicalc 构建、依赖扫描与修复演示
│   ├── verify_minicalc.py            功能与版本断言
│   ├── verify_history.py             三个固定提交的历史验证
│   ├── verify_e3_baselines.py        E3 基线、补丁与拒绝恢复验证
│   └── demo.py                       旧教学演示
├── artifacts/                        实际运行产物与原始证据
│   ├── index.json                    产物 URI 索引
│   ├── minicalc/c2/                  C2 图、报告、Patch、构建与重检日志
│   ├── minicalc-history/             三版本扫描与比较记录
│   ├── e4/
│   │   ├── local-20261015/            E4 本地准备记录
│   │   └── server-20261015/           服务器成功、失败日志及验收回执
│   ├── e3/
│   │   ├── <UTC运行时间>/            E3 基线 summary.json 与逐命令日志
│   │   ├── docker-20260930/          Mac arm64 Docker 构建与运行证据
│   │   ├── ubuntu-amd64-20261009/    Ubuntu 原生 amd64 原始日志和哈希清单
│   │   ├── a03-cross-review-20261009/ A03 基线互查与跟踪异常记录
│   │   └── a03-strace-retry-20261010/ A03 新增原始 trace 复核和本地重跑证据
│   └── demo/                         旧教学演示产物
├── docs/
│   ├── TEAM.md                       B03/A03、成员与联系人
│   ├── BACKLOG.md                    跨阶段任务与完成状态
│   ├── AI_USAGE.md                   AI 参与和采纳记录
│   ├── CONTRIBUTIONS.md              成员贡献与真实提交 SHA
│   ├── VERIFICATION.md               跨阶段验证记录
│   ├── e2/
│   │   ├── README.md                 E2 文档入口
│   │   ├── REQUIREMENTS.md           课件要求对照
│   │   ├── INTERFACE.md              接口与交接约定
│   │   ├── PAIR_REVIEW.md            A/B 配对评审
│   │   ├── SHARED_SYNC.md            共享契约核对记录
│   │   ├── SUBMISSION.md             E2 提交清单
│   │   ├── MINICALC_HANDOFF.md        目标项目交接
│   │   ├── IMAGE_HANDOFF.md           私有镜像 digest 与获取方式
│   │   ├── REPLY_TO_A.md              历史交接回复
│   │   ├── adr/                      ADR-001～005 及其确认状态
│   │   └── records/                  镜像回执与历史验证 JSON
│   ├── e4/                           E4 步骤、本地验证与服务器待办
│   └── e3/
│       ├── README.md                 E3 基线、命令和验证范围
│       └── SUBMISSION.md             E3 必交材料核对
├── tests/
│   ├── test_contracts.py             公共契约测试
│   └── test_minicalc.py              Minicalc 验证与修复测试
└── work/                             本地临时输出，不提交 Git
```


E2 文档已集中在 [E2 入口](docs/e2/README.md)，设计决策位于 docs/e2/adr/，历史说明性 JSON 位于 docs/e2/records/。团队、Backlog、AI 使用、贡献与跨阶段验证仍由 docs/ 下的公共文件统一维护。共享 contracts/ 和既有产物位置不变。

旧 draft/minicalc.Dockerfile 保留为 C2 镜像兼容入口；E4 及后续服务实现以 services/draft/ 为准。
