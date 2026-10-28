# E7 个人贡献

| 成员 | 本阶段工作 | 代码提交 | 验证 |
|---|---|---|---|
| 王宇晗（241250086） | AI 辅助接入并理解本阶段教师参考实现、处理现有固定 digest 与下载环境兼容问题，组织本人目录实际测试和原始证据归档 | `b85f6d2c8ebd131b65c39e6d42cad2603c000da5`（参考接入）；`7a5a01622da340e59a15090a2b5167ae832b8398`（固定 digest 修正与个人测试） | 见 [验证记录](VERIFICATION.md) |

执行目录：`/root/241250086/e5-e7-20261028`。测试代码 SHA 与之后文档归档提交 SHA 分开记录。三项新增边界测试的作者为本地学号身份，AI 参与见 [AI_USAGE.md](AI_USAGE.md)；其他成员个人贡献与 PR 尚待其实际完成，不复用王宇晗提交冒充其独立提交。

## CI 与收尾贡献

王宇晗（241250086），AI 辅助完成：

- `5f9652ff0f85d6863c175b7e6a0347aac015efa1`：定位 GitHub 托管镜像源元数据错误，保留失败证据，增加同 digest 的显式 CI 输入适配。贡献 PR #1 已合并。
- `f015fc5fcd5c694162292b4a6a49530a6814da27`：故意错误的 version 断言，CI 实际失败且合并被拒绝。
- `7b6b69f22103c2a850fb57876e4d150aa8ee44a0`：同一 PR #2 恢复正确断言，31 项测试及完整 gate 通过后正常合并。
- 源码里程碑 `c4c4f76ff79a0cb73a77da962be76eefb054211b`：本人服务器目录最终复验，原始日志、CI artifact、保护规则及 PR 状态按阶段归档。

[PR #1](https://github.com/Wangyuhan29/b-group-project/pull/1)、[PR #2](https://github.com/Wangyuhan29/b-group-project/pull/2)。此记录不新增其他成员的提交、亲手操作或审阅声明。
