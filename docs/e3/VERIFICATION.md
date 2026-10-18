# E3 验证记录

## 互查与 Ubuntu 复验（2026-10-09）

- A03 固定提交的人工 MD/RD、三版本行为和 Minicalc 三提交测试通过，原始本地互查日志见 `artifacts/e3/a03-cross-review-20261009/`；strace 解码异常未作为通过证据。
- Ubuntu 原生 amd64 的 DRAFT Docker 失败候选退出码 127；镜像源参考候选构建/运行退出码 0，输出 hello E3。
- Ubuntu 结果已根据取回的原始日志、退出码和镜像 inspect 再次核对；21 个原始文件已归档并生成哈希清单。详见 `artifacts/e3/ubuntu-amd64-20261009/README.md`。

本次文档提交前重新执行 `make check`：33 个共享文件锁校验、27 个公共契约正反例、Minicalc 固定源码与样例、26 项单元测试、C2 修复演示及三版本历史检查均通过。

证据归档后再次执行 E3 基线与 make check 均通过；本次新目录为 `artifacts/e3/20261009T134348322944Z/`，Ubuntu manifest.json 全部文件哈希校验通过。

## 历史归档差异（2026-10-15 核对）

本次核对发现 E3 历史 a03-strace-retry-20261010/REVIEW.md 的哈希与旧 manifest 不一致，该差异已存在于接入前的 HEAD；文件与当前 HEAD 完全一致。本次不改写 E3 历史报告或锁清单，E4 本地证据使用独立 manifest。
