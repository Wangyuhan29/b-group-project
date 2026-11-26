# B03 E11 实验报告

王宇晗（241250086），B03，对应 A03，鼓楼校区。2026-11-26。
仓库：https://github.com/Wangyuhan29/b-group-project 。实测源码：`27148bdc052bb8c66be92c7aaf2a18dc1301608f`。
服务器执行目录：`/root/241250086/e10-e12.ImtOKA/final-repo`，最终检出干净。
环境镜像 ID：`sha256:539db8e5e11ccfd66a243c27ff68fd1df4f618585dc500f5d260dd1421305cc6`。课程 Ubuntu x86_64 服务器，2 CPU、约 1.7 GiB 可见内存；容器由本人既有课程镜像扩展 strace 和教师 BuildChecker。初次原版镜像构建网络阻塞，适配 Dockerfile 和日志保留在证据中。实验运行包含 SYS_PTRACE；E11/E12 构建服务挂载 Docker socket，最终 DRAFT 程序运行禁网。

教师实现与本组修改分开记录：参考 pipeline/server/vendor DRAFT、E8-E10 的 scan/patch/validate 为教师代码；本人增加 E10 编译失败回滚测试、契约及重启测试、Minicalc 专用适配、构建目标选择和环境配置。AI 辅助见 [AI_USAGE.md](AI_USAGE.md)。

## 轨道内集成
按 data/integration-sample/e11-b.json 运行 DRAFT→fixed-md→repair→recheck。DRAFT 首轮真实缺 make，第二轮构建成功，按同镜像 ID 运行输出 1；固定 MD envelope 与 data.commit 都对应 target。
macro 扩展使用独立 repo 和提交，修改 DEPS 而保留目标宏引用，最终 accepted=true 且动态重检无 MD。
将固定报告 commit 改为全零的单独请求返回 STALE_REPORT、入口退出 1，未生成 repair 阶段。该拒绝为预期测试通过。

新增 labs/e11e12/test_student_241250086.py：产物在计算哈希后被篡改必须返回 ARTIFACT_HASH_MISMATCH；持久化 RUNNING 状态在重启恢复后变为 FAILED/SERVER_RESTARTED，已完成任务保持 SUCCEEDED。教师 10 项加本人 2 项，12 项通过。

## 命令与证据

在个人服务器检出根目录执行 python3 run_e11e12.py run --request data/integration-sample/e11-b.json --out work/e11-final。另执行宏风格或 real-config 请求及 API 操作。
[本阶段结果](../../artifacts/e10-e12/241250086-final-20261126/work/e11-final)；[测试、镜像与版本记录](../../artifacts/e10-e12/241250086-final-20261126/work/run-metadata)；[数据集与 job/trace 索引](../../artifacts/e10-e12/241250086-final-20261126/dataset.csv)。
[宏风格](../../artifacts/e10-e12/241250086-final-20261126/work/e11-macro-final)；[旧报告拒绝](../../artifacts/e10-e12/241250086-final-20261126/work/e11-stale-final)。

## CI

[专项 CI](https://github.com/Wangyuhan29/b-group-project/actions/runs/45807638172)已通过；原始 artifact 见 [CI 归档](../../artifacts/e10-e12/ci-45807638172)。此轮 CI 在源码 27148bdc052bb8c66be92c7aaf2a18dc1301608f 上运行 E10、E11-B 和 E12；E11-A 参考适配器回归也已通过，见 [CI_RECORD.md](CI_RECORD.md)。
