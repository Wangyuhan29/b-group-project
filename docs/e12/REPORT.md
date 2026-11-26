# B03 E12 实验报告

王宇晗（241250086），B03，对应 A03，鼓楼校区。2026-11-26。
仓库：https://github.com/Wangyuhan29/b-group-project 。实测源码：`27148bdc052bb8c66be92c7aaf2a18dc1301608f`。
服务器执行目录：`/root/241250086/e10-e12.ImtOKA/final-repo`，最终检出干净。
环境镜像 ID：`sha256:539db8e5e11ccfd66a243c27ff68fd1df4f618585dc500f5d260dd1421305cc6`。课程 Ubuntu x86_64 服务器，2 CPU、约 1.7 GiB 可见内存；容器由本人既有课程镜像扩展 strace 和教师 BuildChecker。初次原版镜像构建网络阻塞，适配 Dockerfile 和日志保留在证据中。实验运行包含 SYS_PTRACE；E11/E12 构建服务挂载 Docker socket，最终 DRAFT 程序运行禁网。

教师实现与本组修改分开记录：参考 pipeline/server/vendor DRAFT、E8-E10 的 scan/patch/validate 为教师代码；本人增加 E10 编译失败回滚测试、契约及重启测试、Minicalc 专用适配、构建目标选择和环境配置。AI 辅助见 [AI_USAGE.md](AI_USAGE.md)。

## 固定样例及真实项目
固定样例的 draft、full-check、incremental-check、repair、recheck 五阶段成功，统一 job_id/trace_id；full-check 属于 base，其余目标阶段属于 target，MDFixer 消费本轮 incremental-check.json 并校验 SHA。
真实 Minicalc 来源：git@github.com:hardtosleep/Minicalc-DevOps-Test.git 。通过本人已授权 SSH 身份在电脑拉取，Git bundle 传服务器，不复制私钥或 Token。
base：e3a1eda0965e545d96467d275bccaf78c890fcac；target：f863c2deff1bd95e56f1578b872ae6aa26e3bfc8。保留上游真实历史，C1 在 token 容量配置中新增头文件依赖；不将生成样例或适配代码提交冒充上游提交。
适配 labs/e11e12/minicalc.py 使用四个真实对象目标、src/include 路径、上游 GNU Make 展开和 GCC -MM 观测；变化时保守刷新全部对象，不声称细粒度性能提升。pipeline 的动态检查使用上游 make 默认目标。
DRAFT 工作副本额外加入 Dockerfile.broken，不改上游源仓库；候选 COPY src/include/Makefile，输出测试 1+2*3=7。沙箱验证另外检查 10-4/2=8、3*(4+5)=27，变更 config.h 后 main.o 的更新时间增加，并重新扫描无 MD。最终真实 BuildChecker 重检无 MD，仍保留 legacy.h 的 RD。输出报告未声称消除 RD。

## API 与重启
API 仅绑定服务器 127.0.0.1:18087，不开放公网端口。真实 HTTP 提交后轮询 SUCCEEDED；相同键和输入返回同一 job_id，同键改变 target 返回 409；下载 candidate.patch 并核对 X-Content-SHA256 一致。
服务实际停止并重启后，先前已完成的真实任务仍可查询；另外受控写入的一条持久化 RUNNING 探针被标为 FAILED/SERVER_RESTARTED。这是状态恢复探针，不声明在构建中强杀真实业务任务。
服务内核 schema、旧 commit、失败上游、错误 artifact 类型、产物篡改拒绝，以及重启恢复共 12 项契约测试通过。入口 run_e11e12.py 与服务适配代码已提交固定版本。

## A03 尚需参与
B03 单机与本机 HTTP 链路已经通过，但尚未由 A03 在另一台机器通过 SSH 转发提交并下载。A03 实际操作、时间、请求和确认记录不得由本组代写；见 HANDOFF_TO_A03.md。

## 命令与证据

在个人服务器检出根目录执行 python3 run_e11e12.py run --request data/integration-sample/e12.json --out work/e12-final。另执行宏风格或 real-config 请求及 API 操作。
[本阶段结果](../../artifacts/e10-e12/241250086-final-20261126/work/e12-final)；[测试、镜像与版本记录](../../artifacts/e10-e12/241250086-final-20261126/work/run-metadata)；[数据集与 job/trace 索引](../../artifacts/e10-e12/241250086-final-20261126/dataset.csv)。
[真实项目结果](../../artifacts/e10-e12/241250086-final-20261126/work/e12-real-final)；[HTTP 与重启记录](../../artifacts/e10-e12/241250086-final-20261126/work/api-final)。

## CI

[专项 CI](https://github.com/Wangyuhan29/b-group-project/actions/runs/45807638172)已通过；原始 artifact 见 [CI 归档](../../artifacts/e10-e12/ci-45807638172)。此轮 CI 在源码 27148bdc052bb8c66be92c7aaf2a18dc1301608f 上运行 E10、E11-B 和 E12；E11-A 参考适配器回归也已通过，见 [CI_RECORD.md](CI_RECORD.md)。
