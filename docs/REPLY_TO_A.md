# 给 A 组的答复草案（尚未发送）

收到最新版 minicalc，我们已按 C2 压缩包完成 B 组适配。C2 本地实测为 4 MD / 0 RD，四条 MD 补齐后的构建、结果断言和本地依赖重检已通过。已使用本机 SSH 成功获取 Git 历史，三个 tag 的完整 SHA 均与你们给出的相同。C2 ZIP 与 Git 源码一致。逐版本本地扫描为 C0=3MD+1RD、C1=4MD+1RD、C2=4MD+0RD；变化数量也符合预期。

针对待确认问题，B 组提出以下方案，请确认或提出修改：

1. 图格式先用 schema_version、commit、configuration_id、edges；每条边为 [target, dependency]，统一仓库相对路径，包含传递头文件依赖。完整结构见 contracts/graph.schema.json；实测样例在 artifacts/minicalc/c2/actual.json、declared.json。图只覆盖项目内对象编译依赖，完整进程图如需扩展请给出需求。
2. finding_id 用 [repository.url, configuration_id, type, target, dependency] 的紧凑 UTF-8 JSON 数组做完整 SHA-256，前缀 finding-。不含 commit/行号/时间。精确算法和测试向量见 contracts/finding-id-v1.json。先前人工演示 ID 不作为正式 minicalc 规范。
3. 镜像暂未构建。拟定 minicalc-devops:c2，Dockerfile 已准备，构建成功后再提供实际 digest 和传递方式。目前请求里 NOT-BUILT 镜像仅供契约核对。
4. configuration_id 建议暂用 cc-default，同时记录编译器/平台和 -std=c11 -Wall -Wextra -Iinclude -g。本地 macOS 结果不能直接视为 Linux Docker 环境已验证。

当前交接产物为 B 本机 gcc -MM 的辅助验证结果，不冒充 A 的 BuildChecker/EChecker 输出。待你们确认图和 ID 后，再生成双方一致的真实报告。A 给 MDFixer 的报告只包含 MISSING，且仓库、commit 和 configuration_id 必须一致。
