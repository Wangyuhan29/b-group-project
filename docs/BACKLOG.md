# 本轮 minicalc 进展

当前主测试目标为 A 组 minicalc C2。E2 契约、配对评审、共享锁和 C2 镜像交接已经完成。E3 独立测试基线新增在 `docs/e3/`、`fixtures/e3/` 和 `artifacts/e3/`：Tiny Greeting DRAFT 样本、固定 MD 报告、四种 Makefile 风格的参考补丁及本地运行日志。真实运行器与跨组联调仍按后续实验推进。

# Backlog

“草案完成”指 AI 已生成并校验，不代表组员验收或 A 组同意。负责人角色与姓名已在 TEAM 中对应。

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
| E3-01 | B-DRAFT | 真实 DRAFT 目标项目与独立样本 | 记录版本、构建命令、功能断言、失败和参考输入 | Minicalc C2 镜像已验证；Tiny Greeting 在 Mac arm64 和 Ubuntu 原生 amd64 均完成 Docker 失败/成功实跑；Ubuntu 原始日志已取回并校验归档 |
| E3-02 | B-REPAIR | 固定 MD + 四类修复样本 | 漏依赖可复现，patch 可应用，改头文件后自动重建；无效候选被拒绝并恢复 | Target/Macro/Hybrid/Implicit 四种本地行为验证及拒绝恢复已通过，日志见 `artifacts/e3/` |
| E3-03 | B-DRAFT | DRAFT 运行器 | 初始候选、构建日志、错误/上下文反馈、迭代上限和验证闭环 | 后续 E5 实现；本次提供人工参考基线 |
| E3-04 | B-REPAIR | MDFixer 运行器 | 显式规则后逐步支持宏/模式规则，风格说明及失败拒绝 | 后续 E8 实现；本次提供人工参考补丁和验证脚本 |
| E3-05 | A/B-CONTRACT | 图/稳定 finding_id Schema | 真实图节点边、跨提交 finding ID 可复用 | Schema/算法已对齐；真实 Checker 复用验证待 E3 |
| E3-06 | A/B-CONTRACT | 修复 overlay 身份协议 | A 组重检同 base+patch SHA 或修复提交，避免只检旧源码 | 待共同设计 |
| E3-07 | A/B-QA | 真实四服务联调 | 环境可运行、产物可下载、构建/测试/重检均有日志 | 未开始 |
| E12-01 | A/B-QA | 另一组读取证据 | 跨机器实际下载同一产物且 SHA-256 一致 | 未开始 |

## 2026-10-09 互查与平台复验

| ID | 工作 | 完成情况与下一步 |
|---|---|---|
| E3-09 | B03 复核 A03 e3 基线 | MD/RD、三版本演示及 Minicalc 三提交行为通过；跨架构 strace 解码异常已留档，动态读取仍待原生环境复验 |
| E3-10 | B03 原生 linux/amd64 DRAFT Docker 基线 | Ubuntu 实测符合失败/成功预期；镜像源变体和结果已记录，原始日志已取回并校验归档 |
| E3-11 | Ubuntu 原始证据归档 | 已完成；21 个原始文件已取回，传输包及逐文件 SHA-256 校验通过，见 artifacts/e3/ubuntu-amd64-20261009/ |

## E4 工程环境（2026-10-15）

| 任务 | 状态 |
|---|---|
| B-draft 模板接入与旧成果兼容 | 已接入，按课件 services/ 与根目录配置组织 |
| 本地脚本/单元测试/锁文件与安全检查 | 本地验证见 docs/e4/LOCAL_CHECKS.md |
| 服务器完整 make all 和镜像扫描 | 王宇晗在 8701f70 完整运行通过，原始证据已归档 |
| 真实组员相同 SHA 重跑对照 | 待组员分别执行，不由本地模拟代替 |
