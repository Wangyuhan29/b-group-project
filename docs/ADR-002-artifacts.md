# ADR-002 产物通过 URI 交接

状态：Proposed，待 A/B 确认。

## Context
PPT 10、24 要求明确产物读取方法、提交和配置，E12 需另一组真实可读。

## Decision
E2 使用 artifact://demo/name 映射本地 artifacts/demo/name，索引包含来源与 SHA-256。双方共享同一仓库快照。日志、图、Patch 和报告均通过引用传递。

## Alternatives
把所有日志内嵌 JSON：简单但响应过大。立即部署对象存储：适合后期但增加 E2 运维工作。

## Consequences
离线校验可重复，但本地读取不等于跨机器可读。E3 后需确定远端存储、鉴权、生命周期与下载测试。artifact 解析器防止路径越界并验证哈希，不自动访问外网。
