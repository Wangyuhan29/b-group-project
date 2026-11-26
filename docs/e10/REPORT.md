# B03 E10 实验报告

王宇晗（241250086），B03，对应 A03，鼓楼校区。2026-11-26。
仓库：https://github.com/Wangyuhan29/b-group-project 。实测源码：`27148bdc052bb8c66be92c7aaf2a18dc1301608f`。
服务器执行目录：`/root/241250086/e10-e12.ImtOKA/final-repo`，最终检出干净。
环境镜像 ID：`sha256:539db8e5e11ccfd66a243c27ff68fd1df4f618585dc500f5d260dd1421305cc6`。课程 Ubuntu x86_64 服务器，2 CPU、约 1.7 GiB 可见内存；容器由本人既有课程镜像扩展 strace 和教师 BuildChecker。初次原版镜像构建网络阻塞，适配 Dockerfile 和日志保留在证据中。实验运行包含 SYS_PTRACE；E11/E12 构建服务挂载 Docker socket，最终 DRAFT 程序运行禁网。

教师实现与本组修改分开记录：参考 pipeline/server/vendor DRAFT、E8-E10 的 scan/patch/validate 为教师代码；本人增加 E10 编译失败回滚测试、契约及重启测试、Minicalc 专用适配、构建目标选择和环境配置。AI 辅助见 [AI_USAGE.md](AI_USAGE.md)。

## 场景与个人扩展
错误测试预期 99 而程序实际输出 1：accepted=false，test=false，rollback=true，原 Makefile 字节不变。
恢复正确预期后，patch_applies/build/test/header_change/no_missing 全部 true，accepted=true；验证副本 config.h 的 VALUE 从 1 改为 2，实际触发重编译，输出 2；源项目仅写回已通过的 Makefile。
随后无效补丁被拒，已接受版本字节保持不变。最终真实 BuildChecker 重检无 MD，RD 可以保留。

新增 labs/e8e10/test_e10_241250086.py：候选编译参数引入不存在的 absent.h，预期编译失败、不得写回、回滚保持源字节；1 项通过。

## 命令与证据

容器内执行 python3 labs/e8e10/lab.py e10 --track B --out work/e10-final，以及 unittest test_e10_241250086。
[本阶段结果](../../artifacts/e10-e12/241250086-final-20261126/work/e10-final)；[测试、镜像与版本记录](../../artifacts/e10-e12/241250086-final-20261126/work/run-metadata)；[数据集与 job/trace 索引](../../artifacts/e10-e12/241250086-final-20261126/dataset.csv)。

## CI

[专项 CI](https://github.com/Wangyuhan29/b-group-project/actions/runs/45807638172)已通过；原始 artifact 见 [CI 归档](../../artifacts/e10-e12/ci-45807638172)。此轮 CI 在源码 27148bdc052bb8c66be92c7aaf2a18dc1301608f 上运行 E10、E11-B 和 E12；E11-A 参考适配器回归也已通过，见 [CI_RECORD.md](CI_RECORD.md)。
