# E2 Backlog

本阶段负责接口契约、样例、设计与交接。角色对应见 [小组信息](TEAM.md)。

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
