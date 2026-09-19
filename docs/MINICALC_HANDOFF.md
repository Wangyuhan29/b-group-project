# minicalc 对接状态

## 版本

| 版本 | 完整 SHA | 预期 MD/RD | 本轮证据 |
|---|---|---|---|
| C0 | e3a1eda0965e545d96467d275bccaf78c890fcac | 3/1 | SSH 核验真实 tag/SHA；本机构建、断言、依赖扫描通过 |
| C1 | f863c2deff1bd95e56f1578b872ae6aa26e3bfc8 | 4/1 | SSH 核验真实 tag/SHA；本机构建、断言、依赖扫描通过 |
| C2 | e103bcb3726a3fd7253deb0d791ac74fac77cafe | 4/0 | SSH 核验；ZIP 全文件与 Git 一致；本机编译器扫描 |

不能用 C2 的图当作 C0 baseline。不能把现有 synthetic source.bundle 当作 A 组真实 Git 历史。SSH clone 已成功；真实历史存于 fixtures/minicalc/history.bundle，可离线 clone。

## 本轮 C2 固定 MD

main.o → include/token.h；main.o → include/util.h；parser.o → include/config.h；parser.o → include/token.h。报告 detector=COMPILER_MM_LOCAL，并附实际命令、规则行号、编译器输出。排除 macOS SDK 等绝对外部路径并记录到 evidence；图范围只覆盖项目内对象文件编译依赖，不是完整进程/链接依赖图。

产物 URI artifact://minicalc/c2/name 对应本仓库 artifacts/minicalc/c2/name，使用合并后的 artifacts/index.json 校验 SHA-256。不要覆盖 A 自己的 index；接收者应复制对应产物并合并索引，或将 resolver 指向整份收到的 B 仓库。

## 图格式提案 v1

schema_version、commit、configuration_id、edges；边为 [target,dependency]，含传递读取，全部采用仓库相对路径和 /。两张图共用结构，图类型由 artifact.type 区分。不得用绝对路径、.. 路径或重复边。真实检测器如需节点/进程属性，由 A 组提出扩展并共同定版。该最小图 Schema 是新提案，没有单方面宣布双方已冻结。

## finding_id 提案 v1

字段顺序固定：[repository.url, configuration_id, type, target, dependency]。按 UTF-8 JSON 数组序列化，ensure_ascii=false，separators=(',',':')，不加换行；SHA-256 完整 64 位小写 hex，前缀 finding-。排除 commit、行号和时间。仓库 URL 使用 project.json 中带 .git 的精确字符串，不自行增删后缀或大小写。路径使用 /，不加 ./。公共实现为 scripts/minicalc.py 的 finding_id，测试向量见 contracts/finding-id-v1.json。

这与先前人工小样本的 NUL 分隔/截断 ID 不同；旧样本不改。A 组确认提案后，双方真实 minicalc 报告统一生成，不能混用旧临时 ID。

## 配置与镜像

cc-default 暂为逻辑配置名称，需 A 组确认。固定选项为 -std=c11 -Wall -Wextra -Iinclude -g；clean/build 为 make clean && make -j2；项目目录 /workspace/minicalc。实际本地编译器版本在 evidence.json 内，可执行测试通过不意味着 Linux Docker 配置已验证。

Docker 候选使用 gcc:14-bookworm + python3/make，拟定 tag minicalc-devops:c2。当前未构建，也没有 digest、注册表或下载位置，禁止向 A 宣称镜像已可用。验证命令 python3 /opt/b-group/verify_minicalc.py . 依赖本仓库 Dockerfile 放入该脚本；不能在未安装脚本的任意镜像中直接运行。

## 修复验收

本地生成的 fix.patch 只补 main.o/parser.o 的四条 MD，不改 RD 或功能源码。git apply --check、clean build、四个结果断言、gcc -MM 重检及四条依赖的 make -q -W 行为检查均通过。重检报告 commit 表示 base，recheck-evidence 额外记录 patch_sha256，明确是 base+overlay。真实 A 组重检仍需双方把 overlay 身份纳入正式交接，或创建修复后的真实提交。
