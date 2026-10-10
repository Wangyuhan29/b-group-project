# B03 E2 文档入口

E2 的接口设计、配对评审、需求对照、共享契约核对和提交材料集中于本目录。文档保留当时验证和待办状态，不代替双方签认。

| 内容 | 入口 |
|---|---|
| 需求与提交清单 | [要求对照](REQUIREMENTS.md)、[提交材料](SUBMISSION.md) |
| 接口与配对评审 | [接口说明](INTERFACE.md)、[评审记录](PAIR_REVIEW.md) |
| 共享文件一致性 | [共享锁核对](SHARED_SYNC.md)；实际契约仍在 contracts/ |
| Minicalc 和镜像交接 | [目标项目交接](MINICALC_HANDOFF.md)、[镜像交接](IMAGE_HANDOFF.md)、[历史回复](REPLY_TO_A.md) |
| 设计决策 | adr/ 中五份 ADR，原确认状态保持不变 |
| 历史机器可读记录 | records/ 中镜像回执、演示和历史验证 JSON，文件内容保持不变 |

跨阶段资料保留在 docs/：TEAM.md、BACKLOG.md、AI_USAGE.md、CONTRIBUTIONS.md、VERIFICATION.md。E3 材料见 [E3 入口](../e3/README.md)。

本次目录调整仅迁移文档和说明性 JSON；contracts/、fixtures/ 与 artifacts/ 的 E2 输入、URI 和共享锁保持不变，避免影响 A03 读取及回归验证。仓库根目录执行 make check。
