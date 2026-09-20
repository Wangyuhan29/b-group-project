# 本轮 minicalc 进展

当前主测试目标为 A 组 minicalc C2。新样例见 contracts/minicalc，实测结果与剩余联调项见 MINICALC_HANDOFF.md 和 VERIFICATION.md；图/ID 已加入 shared-lock 并与 A 组文件核对。C2 Docker 镜像已构建发布，A 组 Checker 重检仍待完成。下面保留 E2 初版说明，涉及 fixture://draft-project、artifacts/demo 和旧样本的内容仅供兼容回归。

# Backlog

“草案完成”指 AI 已生成并校验，不代表组员验收或 A 组同意。负责人姓名需在 TEAM 中认领。

| ID / 阶段 | 负责人角色 | 任务与产物 | 验收标准 | 状态 |
|---|---|---|---|---|
| E2-01 | A/B-CONTRACT | 统一 task.schema.json | 四类请求/查询记录通过，ABC 拒绝 | 草案完成，待共同确认 |
| E2-02 | B-DRAFT | DRAFT 样例、环境交接 | 对方能解释 repo/commit/image/命令与配置 | 草案完成，待 A 组验证 |
| E2-03 | A-CONTRACT | 增量 baseline 样例 | 缺 baseline、提交/配置不匹配均拒绝 | 草案完成，待 A 组审阅 |
| E2-04 | B-REPAIR | REPAIR 请求和固定报告 | 只接受 MD，错提交/配置拒绝 | 草案完成，校验通过 |
| E2-05 | A/B-CONTRACT | ADR-002、产物索引 | 双方解释 URI，本地哈希读取通过 | 本地完成，跨组待验证 |
| E2-06 | B-QA | 负例和 validate.py | manifest 预期结果全部一致 | 完成，待人工复核 |
| E2-07 | 全体 | ADR、AI_USAGE、贡献记录 | 真实人工判断、SHA、Issue/PR 可追溯 | 模板已备，人工信息待补 |
| E2-08 | A/B 全体 | PAIR_REVIEW 签认 | 三轮讨论记录和未决项明确 | 待开展 |
| E3-01 | B-DRAFT | 真实 DRAFT 目标项目 | URL/许可/完整 SHA/构建说明确定，Docker 基线可构建 | 待选择；已有人工小样本 |
| E3-02 | B-REPAIR | 固定 MD + 修复演示 | 漏依赖可复现，patch 可应用，修复后测试通过 | 人工样本本地通过 |
| E3-03 | B-DRAFT | DRAFT 运行器 | 初始候选、构建日志、错误/上下文反馈、迭代上限和验证闭环 | 未实现 |
| E3-04 | B-REPAIR | MDFixer 运行器 | 显式规则后逐步支持宏/模式规则，风格说明及失败拒绝 | 未实现；仅样本演示 |
| E3-05 | A/B-CONTRACT | 图/稳定 finding_id Schema | 真实图节点边、跨提交 finding ID 可复用 | 待 A 组方案 |
| E3-06 | A/B-CONTRACT | 修复 overlay 身份协议 | A 组重检同 base+patch SHA 或修复提交，避免只检旧源码 | 待共同设计 |
| E3-07 | A/B-QA | 真实四服务联调 | 环境可运行、产物可下载、构建/测试/重检均有日志 | 未开始 |
| E12-01 | A/B-QA | 另一组读取证据 | 跨机器实际下载同一产物且 SHA-256 一致 | 未开始 |
