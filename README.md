# B 组项目：minicalc 对接版

本仓库负责 DRAFT 环境生成和 MDFixer 缺失依赖修复；A 组负责 BuildChecker / EChecker。共同测试目标已切换为 A 组提供的 minicalc。这里仍是 B 组工具仓库，目标源码放在 fixtures/minicalc/source。

## 现在运行什么

需要 Python 3.10+、Git、GNU Make 和支持 -MM 的 gcc；不需要第三方 Python 包。

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
- C2 镜像已在 GitHub Actions 构建、通过容器断言并发布至私有 GHCR，见 [镜像交接](docs/IMAGE_HANDOFF.md)。A 组真实 Checker 联调仍待完成。

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
| docs/REPLY_TO_A.md | 可以发给 A 组的具体答复，未自动发送 |
| docs/MINICALC_HANDOFF.md | 读取方法、环境边界、三个版本的核验与边界 |

原 contracts/examples、artifacts/demo、fixtures/draft-project 及 scripts/demo.py 保留为旧教学样本与兼容性回归，**不是 minicalc 正式输入**。make demo 已改为 minicalc；make legacy-demo 可重放旧演示。公共 task.schema.json/OpenAPI/validate.py 没有改字段，不要求 A 组立刻升级公共模型。

contracts/minicalc 中的 *-response-local.json 是本机结果向公共模型的映射，不是 Docker/API 执行记录。当前 full-request / repair-request 已使用真实 C2 digest；旧本地响应保留当时的 NOT-BUILT 状态。共享 33 个文件的核对结果见 [SHARED_SYNC](docs/SHARED_SYNC.md)。

## 本地重新构建镜像

在本仓库根目录执行：

```bash
docker build -f draft/minicalc.Dockerfile -t minicalc-devops:c2 .
docker run --rm minicalc-devops:c2
```

已发布镜像的固定 digest 和拉取命令见 [IMAGE_HANDOFF](docs/IMAGE_HANDOFF.md)。重新构建可能产生不同 digest。此 Dockerfile 仅复制 C2 源码，C0/C1 的准确源码已在 history.bundle 中，Dockerfile 仍需按版本固定环境输入。

## 下一步

先与 A 组统一报告中的 `include/*.h` 路径、问题编号和产物读取位置，再进行真实 Checker 联调。

TEAM、贡献表及 B03 三人本轮审阅记录已填写；ADR-001～003 的双方确认仍需补齐。历史提交已同步 GitHub，本次本地修订的验证结果见 [VERIFICATION](docs/VERIFICATION.md)。

## Git 历史重放

已配置的 SSH 地址为 `git@github.com:hardtosleep/Minicalc-DevOps-Test.git`。接口 repository.url 仍保留原 HTTPS 标识以稳定 finding ID，clone_url 单独记录 SSH 传输地址。

`make history` 在临时目录离线 clone history.bundle，逐版本构建并比较发现，输出 work/minicalc-history。保存的真实扫描产物在 artifacts/minicalc-history，6 份任务样例在 contracts/minicalc-history。这里仍为逐版本全量扫描后比较，不声称实现 EChecker 增量算法；历史样例保留原占位值；本次发布仅覆盖 C2，不能直接用于 C0/C1 源码检测。
