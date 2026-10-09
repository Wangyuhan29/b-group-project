> 2026-09-17 更新：C2 镜像已构建、验证并发布到私有 GHCR；真实 digest 与获取方式见 [IMAGE_HANDOFF.md](IMAGE_HANDOFF.md)，共享锁核对见 [SHARED_SYNC.md](SHARED_SYNC.md)。以下本地验证记录保留原执行时的环境状态，A 组真实 Checker 验收仍待完成。

# 当前验证记录

日期：2026-09-16。本机 macOS，gcc 命令对应的具体编译器见 artifacts/minicalc/c2/evidence.json。

- 旧公共契约的 27 个正反样例与原有测试继续保留。
- 26 项单元测试通过（18 项原有、8 项 minicalc）。
- 新 C2 源码文件 SHA-256、6 份 minicalc 契约样例、全部新旧产物 URI/hash 均校验。
- C2 构建与四个输出断言通过；初始 4 MD / 0 RD。
- 生成 Patch、git apply --check/应用通过；修复后构建和四个输出断言通过；本地重检为 0 MD / 0 RD。
- 四条缺失依赖在修复前不会触发对应目标重建，修复后会触发，使用 make -q -W 检查。
- 补丁 SHA 和汇总见 minicalc-verification.json；日志和证据见 artifacts/minicalc/c2。
- SSH clone 成功；C0/C1/C2 的 tag/完整 SHA 已核验，C2 ZIP 文件哈希与 Git 完全一致。三个版本均构建及结果断言通过，实测 MD/RD 为 3/1、4/1、4/0。
- Docker 未安装，镜像构建未执行；A 组真实 Checker、跨机器联调未执行。

复现：make check。脚本仅在临时副本应用补丁，work/minicalc-run 保存新结果；不修改固定源文件或冒充已合入上游。

## A03 E2 交接证据（2026-09-22）

- A03 已使用私有 C2 镜像运行容器，三个算术用例和版本断言通过。
- A03 `validate.py`：27 个共享样例（19 个有效、8 个预期拒绝）及 7 个 Minicalc 样例全部通过。
- A03 与 B03 核对后确认 33 个共享文件 SHA-256 一致。
- 以上是 E2 契约和镜像交接证据；真实 BuildChecker/EChecker 算法和跨机器 Checker 联调仍属于 E3/E12。

## E3 互查与 Ubuntu 复验（2026-10-09）

- A03 固定提交的人工 MD/RD、三版本行为和 Minicalc 三提交测试通过，原始本地互查日志见 `e3-b03/evidence/a03-cross-review-20261009/`；strace 解码异常未作为通过证据。
- Ubuntu 原生 amd64 的 DRAFT Docker 失败候选退出码 127；镜像源参考候选构建/运行退出码 0，输出 hello E3。
- Ubuntu 结果已根据取回的原始日志、退出码和镜像 inspect 再次核对；21 个原始文件已归档并生成哈希清单。详见 `e3-b03/evidence/ubuntu-amd64-20261009/README.md`。

本次文档提交前重新执行 `make check`：33 个共享文件锁校验、27 个公共契约正反例、Minicalc 固定源码与样例、26 项单元测试、C2 修复演示及三版本历史检查均通过。

证据归档后再次执行 E3 基线与 make check 均通过；本次新目录为 `e3-b03/evidence/20261009T134348322944Z/`，Ubuntu manifest.json 全部文件哈希校验通过。
