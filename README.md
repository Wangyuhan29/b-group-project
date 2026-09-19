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
- 没有 Docker 命令，镜像未构建。没有执行 A 组真实 Checker，不能把本地重检说成跨组验收完成。

## 优先阅读与使用

| 文件/目录 | 作用 |
|---|---|
| fixtures/minicalc/project.json | C0/C1/C2 SHA、来源可信范围、C2 文件哈希、配置与镜像状态 |
| contracts/minicalc/ | DRAFT/FULL_CHECK/REPAIR 的 C2 请求、本地结果映射和固定 MD 报告 |
| artifacts/minicalc/c2/ | 真实本地日志、图、证据、MD 报告、Patch 及重检报告 |
| scripts/minicalc.py | 明确限定为 minicalc 显式规则的构建、扫描、修复和验证演示 |
| scripts/verify_minicalc.py | 三个算术结果与版本的自动断言，弥补上游 make test 只打印结果 |
| draft/minicalc.Dockerfile | 未构建的环境候选方案 |
| contracts/graph.schema.json | 本轮提出的最小图格式；待 A 组确认 |
| contracts/finding-id-v1.json | finding_id 算法与精确测试向量；待 A 组确认 |
| docs/REPLY_TO_A.md | 可以发给 A 组的具体答复，未自动发送 |
| docs/MINICALC_HANDOFF.md | 读取方法、环境边界、三个版本的核验与边界 |

原 contracts/examples、artifacts/demo、fixtures/draft-project 及 scripts/demo.py 保留为旧教学样本与兼容性回归，**不是 minicalc 正式输入**。make demo 已改为 minicalc；make legacy-demo 可重放旧演示。公共 task.schema.json/OpenAPI/validate.py 没有改字段，不要求 A 组立刻升级公共模型。

contracts/minicalc 中的 *-response-local.json 是本机结果向公共模型的映射，不是 Docker/API 执行记录。image 明确为 NOT-BUILT，占位请求不能用于真实镜像调度；执行模式和未完成项记录在 manifest 与验证文档中。

## Docker 可用后

在本仓库根目录执行：

```bash
docker build -f draft/minicalc.Dockerfile -t minicalc-devops:c2 .
docker run --rm minicalc-devops:c2
```

首次成功后记录实际镜像 digest、编译器版本和平台，并与 A 组确认获取方式，再替换请求的 NOT-BUILT 占位镜像。此 Dockerfile 仅复制 C2 源码，C0/C1 的准确源码已在 history.bundle 中，Dockerfile 仍需按版本固定环境输入。

## 下一步

给 A 组发送 docs/REPLY_TO_A.md 中的方案，确认图/ID/配置。Git 历史已核验，本地基线与跨版本样例已生成；下一步完成镜像构建和 A 组真实重检。

TEAM、贡献、人工 AI 判断仍需实际成员填写。你提供的本地目录目前没有 .git，因此本轮直接修改文件，没有冒充已完成 Git 提交或远端发布。

## Git 历史重放

已配置的 SSH 地址为 `git@github.com:hardtosleep/Minicalc-DevOps-Test.git`。接口 repository.url 仍保留原 HTTPS 标识以稳定 finding ID，clone_url 单独记录 SSH 传输地址。

`make history` 在临时目录离线 clone history.bundle，逐版本构建并比较发现，输出 work/minicalc-history。保存的真实扫描产物在 artifacts/minicalc-history，6 份任务样例在 contracts/minicalc-history。这里仍为逐版本全量扫描后比较，不声称实现 EChecker 增量算法；请求中的 Docker 镜像尚未构建。
