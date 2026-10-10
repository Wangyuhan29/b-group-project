# ADR-003 MDFixer 只消费 MD

状态：Proposed，待 A/B 确认。

## Context
PPT 12、23 明确 REPAIR 只消费 Missing Dependency，失败候选要被拒绝。

## Decision
请求 finding_types 固定 [MISSING]，实际读取的报告也必须非空且只有 MISSING。混合报告由上游拆分。验证同仓库、同提交、同配置，构建/测试/重检全部通过才接受候选。算法正常完成但候选不合格可返回 SUCCEEDED + accepted=false。

## Alternatives
忽略混合报告中的 RD：便利，但容易掩盖错误对接。把候选拒绝统一视为 FAILED：会混淆验收结论和执行故障。

## Consequences
A 组需提供 MD-only 报告或增加过滤层。当前本地演示仅处理一个人工显式规则，不处理宏、模式规则或通用 Makefile。真实 patch overlay 的重检身份在 E3 扩展协议中补足。
