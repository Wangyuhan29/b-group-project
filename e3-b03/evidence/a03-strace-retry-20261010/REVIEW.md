# A03 最新 strace 更新重试（2026-10-10）

复核提交：d27a0a3f7aeeb6e702e46fec2125925846d93db9。结论：A03 原生 WSL 原始证据可正常读取；B03 Apple Silicon Docker 的 amd64 跨架构重跑仍出现系统调用解码异常，英文 stdout 未解决。

## 原始证据静态复核

A03 新增 raw/ 包含 16 个 trace 及 make.stdout、make-pn.txt、generation-info.txt。生成环境 Ubuntu GCC 11.4.0、Make 4.3、strace 5.16、x86_64，Minicalc C0 SHA 正确。syscall_0x 数为 0，编译器 cc1 读取关系见 a03-raw-analysis.json：main.c 读取 config/parser/token/util；parser.c 读取 parser/token；token.c 读取 token；util.c 读取 util。证据与 C0 人工预期一致。这是独立读取 A03 产物，不是 B03 原生重跑。

## 最新脚本实际重跑

在 Apple Silicon Docker 中使用 Ubuntu 22.04 linux/amd64（跨架构），工具版本与前次一致。以 MINICALC_REPO 指向已核验完整历史，执行原样 strace_check.sh。脚本 stdout 已为英文；strace 和 make -pn 均报告退出 0，但 local-rerun-raw/ 中 16 个 trace 存在 8650 条 syscall_0x，正常成功 execve 为 0，五个项目头文件的正常成功 openat 均为 0。异常路径为空、参数不合理，不能用 0 次读取判断 RD。详见 retry-run.log、local-analysis.json 和原始 trace。

纯英文最小测试 `/bin/echo ASCII_OK` 输出 ASCII_OK，退出 0；限定 execve/openat 的 trace 仅包含 exited with 0，未出现应有的 execve。这也表明 stdout 编码不是充分解释。

当前证据更符合跨架构系统调用跟踪兼容问题，具体机制尚未进一步确定。后续应在原生 x86_64 Ubuntu/WSL 重跑；容器的 linux/amd64 标记不代表物理 CPU 为 x86_64。

## 附加发现

新版脚本向已有仓库 raw/ 直接复制新 PID 文件而未分运行目录：原有 16 个 trace 加上本次 16 个导致 raw/ 共 32 个。为避免混用，本复核先保存 a03-original-raw/，仅用当次 /tmp/e3-strace-a03-out 拷出的 local-rerun-raw/ 分析。建议 A03 每次创建新时间目录。

本次记录及原始日志归档到 B03 仓库；未修改 A03 仓库。按用户决定，跨架构解码异常暂不继续排查，保留失败证据，不影响 B03 已完成的 E3 必交基线。
