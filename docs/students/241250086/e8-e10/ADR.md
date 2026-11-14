# ADR：按 Make 声明风格增补缺失依赖

保留参考实现的 direct/macro/mixed 选点，只处理 MISSING；同一目标与依赖去重。补丁生成不写回原项目，并先核对报告版本。纯变量定义被多个目标共用时，修改可能扩大范围；本次仅验证固定样例，未扩展到复杂或隐式 Make 规则。macOS 仅排除 Apple Clang 返回的 SDKSettings.json 元数据，保留其他路径检查。
