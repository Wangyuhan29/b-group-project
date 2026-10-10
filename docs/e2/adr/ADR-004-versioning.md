# ADR-004 严格 Schema 与版本变更

状态：Accepted（A03/B03，2026-09-22）。

## Context
PPT 26 提醒严格 Schema 可能拒绝新增字段。

## Decision
初版 schema_version 固定 1.0，所有对象 additionalProperties=false。当前消费者会拒绝未知字段。包括新增可选字段在内的任何 Schema 扩展，都需双方更新共享文件、样例和版本支持；在旧消费者升级前不发送新字段。字段改名、删字段、改语义或状态变更使用新的主版本。

## Alternatives
宽松接收未知字段：利于演进但易漏掉拼写错误。

## Consequences
契约变更需要 PR、ADR/CHANGELOG、双方校验记录。不能直接声称“新增字段总是兼容”。版本和组件结构更新需同时同步 OpenAPI；回归测试检查共享定义一致。
