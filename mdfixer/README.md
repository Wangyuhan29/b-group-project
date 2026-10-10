# MDFixer 修复准备

当前运行 python3 scripts/minicalc.py。它仅对固定 minicalc C2 的显式对象规则，消费四条 MD、生成 Patch，并在临时源码副本中构建/验证/重检。报告和真实日志在 artifacts/minicalc/c2，重跑结果在 work/minicalc-run。

这不是通用 Makefile 修复器，也不是论文完整实现。宏/模式规则拒绝处理。真实 A 组重检和修复源码身份协议仍待对接；本机 gcc -MM 的重检不能替代最终 A 组验收。

E3 的四类声明风格人工参考补丁与拒绝恢复样本在 `fixtures/e3/mdfixer/`，使用 `python3 scripts/verify_e3_baselines.py` 验证；说明见 [E3 文档](../docs/e3/README.md)。这些样本不代表通用修复器已实现。
