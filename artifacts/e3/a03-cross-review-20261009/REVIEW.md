# B03 对 A03 E3 基线的交叉复核

日期：2026-10-09。复核对象：A03 `e3` 分支提交 `555a262238c9bc2ac883a5ff74d5ae6b389895f1`。A03 仓库导出的 `devops_lab_a03-e3.zip` 内 `e3-a03/` 与该提交逐文件对比一致。

## 环境与来源

Apple Silicon macOS 上的 Docker Desktop，容器使用 Ubuntu 22.04、`--platform linux/amd64`；容器内报告 x86_64，GCC 11.4.0、GNU Make 4.3、strace 5.16。amd64 通过跨架构运行，不能等同于原生 x86_64 WSL。版本输出见 `environment.txt`。

共同目标仓库本次 HTTPS/SSH 连接失败，改用 B03 已保存的 `fixtures/minicalc/history.bundle` 克隆完整历史。实测的 c0/c1/c2 SHA 分别为 `e3a1eda0965e545d96467d275bccaf78c890fcac`、`f863c2deff1bd95e56f1578b872ae6aa26e3bfc8`、`e103bcb3726a3fd7253deb0d791ac74fac77cafe`，与 A03 一致。

## 结果

| 项目 | 实际结果 | 判断 |
|---|---|---|
| MD/RD 人工样例 | 初始输出 1；改 config.h 后增量仍 1；clean 后 2；改 unused.h 后重编译 | PASS，见 md-rd.log |
| 三版本人工演示 | C0 clean 10；C1 incremental/clean 12；只改 feature.h 不重建；C2 incremental 12、clean 19 | PASS，见 commits.log |
| Minicalc 三个固定提交 | 三版本 clean/build/test 均退出 0，逐项检查输出 7、8、27 | PASS，见 minicalc.log |
| Minicalc C0 依赖行为 | 改 util.h 重建 util.o、不重建 main.o；改 legacy.h 重建 util.o | PASS，与 A03 记录一致 |
| make -pn 声明关系 | 四个 .o 规则与 A03 一致 | PASS，见 strace-raw/make-pn.txt |
| strace 动态读取关系 | 命令退出 0，但出现大量 syscall_0x…、异常 execve，全部头文件统计为 0 | 未独立验证；不能将 0 次读取用于 RD 判定 |

`strace-run.log`、`strace-result.md` 与 `strace-raw/` 保存本次跟踪失败的原始观察。跨架构环境下的跟踪异常并不否定 A03 在原生 x86_64 WSL 采集的结果，应由原生环境复验。本次只核对 A03 摘要与源码及声明关系一致，未独立证明其动态读取结论。

## 可复现命令

在具有 Git、GCC、Make、strace 的原生 Linux 环境中，克隆上述 A03 提交及 Minicalc 完整历史后运行：

```bash
export MINICALC_REPO=/path/to/Minicalc-DevOps-Test
bash e3-a03/scripts/md_rd_check.sh
bash e3-a03/scripts/commits_check.sh
bash e3-a03/scripts/minicalc_check.sh
bash e3-a03/scripts/strace_check.sh
```

前三项必须逐项对照上表和实际日志，不能仅用脚本最终退出码作为判据。strace 项需确认具体编译进程的有效 openat/execve 和路径，不能仅凭 strace 退出码判断通过。

## 建议交给 A03 的补充项

1. 将 strace 的逐进程原始 trace 文件、make.stdout 和 make-pn.txt 一并保存；当前仓库主要保存摘要，原文件保留在临时目录。
2. 脚本目前仅 `set -u`，缺少关键步骤的失败终止及输出断言。建议补充，防止中间失败后脚本继续执行并最终返回 0。
3. 双方后续真实 Docker 构建继续统一 linux/amd64。本次完成 A03 行为样例的 amd64 复核，B03 原有 DRAFT Docker 镜像的 arm64 构建证据仍保留原平台标注。

这些是互查建议；本次没有修改 A03 的源码、人工答案或已有证据。
