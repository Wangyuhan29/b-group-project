# A/B 配对评审记录

状态：已完成 E2 配对评审；真实 Checker 联调留待 E3。

| 项目 | 实际记录 |
|---|---|
| 日期、A/B 组号、参会成员 | 2026-09-22；A03 / B03，鼓楼校区；A：唐一心、李翔宇、王子贤、刘馨蔓；B：王宇晗、朱玄、靳滨硕 |
| 评审的完整 commit SHA | C0 `e3a1eda0965e545d96467d275bccaf78c890fcac`；C1 `f863c2deff1bd95e56f1578b872ae6aa26e3bfc8`；C2 `e103bcb3726a3fd7253deb0d791ac74fac77cafe` |
| 第一轮：A 的环境/基线需求，B 的交付是否足够 | B 提供 C2 私有 GHCR 镜像、`cc-default`、构建/验证命令；A 已拉取并 `docker run` 三个算术用例和版本断言全部通过 |
| 第二轮：B 的 MD 报告需求，A 如何生成并交付 | A 提供 C0 的 `md-only-report`，包含 3 个 MISSING，供 B 的 REPAIR 请求消费 |
| 第三轮：选择哪条失败输入，预期状态/错误码 | 缺少 baseline 的增量请求，预期 `INPUT_1001` 和 HTTP 400 |
| A 组执行 validate.py 的结果 | 27 个共享样例：19 个有效、8 个预期拒绝；Minicalc 7 个样例全部通过 |
| B 组执行 validate.py 的结果 | B 组共享锁校验通过，33 个共享文件 SHA-256 一致；`make check` 通过 |
| 产物读取方式和实际读取证据 | 使用 `artifact://` 映射和 `artifacts/index.json` SHA-256 注册；A03 压缩包记录 C2 镜像 4 个断言通过 |
| 采纳/修改的 ADR | ADR-004 版本变更策略；ADR-005 Minicalc、图格式和 `finding_id` |
| 未决问题、负责人、截止日期 | C0/C1 环境、真实 BuildChecker/EChecker 联调和修复后重检，由 A/B 在 E3 完成 |
| A 组确认人与 B 组确认人 | 唐一心（241250061）／王宇晗（241250086） |
