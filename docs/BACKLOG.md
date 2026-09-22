# 本轮 minicalc 进展

当前主测试目标为 A 组 minicalc C2。E2 契约、配对评审、共享锁和 C2 镜像交接已经完成；真实 BuildChecker/EChecker、C0/C1 环境和跨机器产物读取保留为 E3/E12 待办。

# Backlog

“草案完成”指 AI 已生成并校验，不代表组员验收或 A 组同意。负责人姓名需在 TEAM 中认领。

| ID / 阶段 | 负责人角色 | 任务与产物 | 验收标准 | 状态 |
|---|---|---|---|---|
| E2-01 | A/B-CONTRACT | 统一 task.schema.json | 四类请求/查询记录通过，ABC 拒绝 | 已完成；A/B 校验通过 |
| E2-02 | B-DRAFT | DRAFT 样例、环境交接 | 对方能解释 repo/commit/image/命令与配置 | 已完成；A03 已拉取 C2 镜像并通过容器断言 |
| E2-03 | A-CONTRACT | 增量 baseline 样例 | 缺 baseline、提交/配置不匹配均拒绝 | 已完成；A03 27 个共享样例通过 |
| E2-04 | B-REPAIR | REPAIR 请求和固定报告 | 只接受 MD，错提交/配置拒绝 | 已完成；样例校验和修复验证通过 |
| E2-05 | A/B-CONTRACT | ADR-002、产物索引 | 双方解释 URI，本地哈希读取通过 | E2 已完成；跨机器读取保留 E12 |
| E2-06 | B-QA | 负例和 validate.py | manifest 预期结果全部一致 | 已完成；B03/A03 均记录通过结果 |
| E2-07 | 全体 | ADR、AI_USAGE、贡献记录 | 真实人工判断、SHA、Issue/PR 可追溯 | 已完成；成员、贡献和 SHA 已记录 |
| E2-08 | A/B 全体 | PAIR_REVIEW 签认 | 三轮讨论记录和未决项明确 | 已完成；A03/B03 记录已同步 |
| E3-01 | B-DRAFT | 真实 DRAFT 目标项目 | URL/许可/完整 SHA/构建说明确定，Docker 基线可构建 | C2 已完成；C0/C1 环境待 E3 补齐 |
| E3-02 | B-REPAIR | 固定 MD + 修复演示 | 漏依赖可复现，patch 可应用，修复后测试通过 | C2 演示已完成；真实 Checker 重检待 E3 |
| E3-03 | B-DRAFT | DRAFT 运行器 | 初始候选、构建日志、错误/上下文反馈、迭代上限和验证闭环 | 未实现 |
| E3-04 | B-REPAIR | MDFixer 运行器 | 显式规则后逐步支持宏/模式规则，风格说明及失败拒绝 | 未实现；仅样本演示 |
| E3-05 | A/B-CONTRACT | 图/稳定 finding_id Schema | 真实图节点边、跨提交 finding ID 可复用 | Schema/算法已对齐；真实 Checker 复用验证待 E3 |
| E3-06 | A/B-CONTRACT | 修复 overlay 身份协议 | A 组重检同 base+patch SHA 或修复提交，避免只检旧源码 | 待共同设计 |
| E3-07 | A/B-QA | 真实四服务联调 | 环境可运行、产物可下载、构建/测试/重检均有日志 | 未开始 |
| E12-01 | A/B-QA | 另一组读取证据 | 跨机器实际下载同一产物且 SHA-256 一致 | 未开始 |
