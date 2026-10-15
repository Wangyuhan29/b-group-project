# B03 E4 可重复工程环境

来源：用户提供的 E4实验包.zip 中 B-draft/ 模板与 E4 B 组全流程命令手册。此处为模板接入及本地准备，服务器验收尚未执行。

## 项目结构

- services/draft/：服务 Dockerfile、draft CLI、pytest.ini、6 项单元测试（模板 4 项及超时 2 项）。
- fixtures/draft/：E4 模板指定的 Tiny Greeting，基础镜像按 digest 固定。fixtures/e3/ 保留先前 E3 的版本和证据，两个阶段不覆盖。
- compose.yaml、requirements-dev.in、requirements-dev.lock、.env.example：根目录按课程要求配置。
- scripts/doctor.py、scripts/secret_scan.py：环境和密钥检查。
- setup/bootstrap_ubuntu.sh：课程服务器初始化脚本，仅按需执行一次，本次未运行。
- work/<UTC时间>/：每次运行的本地证据，默认不提交。

## 在服务器正式运行

每位成员在自己的学号目录克隆相同提交；仅设置仓库本地 Git 身份，不更改全局配置。例如王宇晗：

```sh
git config --local user.name 241250086
git config --local user.email 241250086@smail.nju.edu.cn
make all
```

make all 串行执行 doctor、build、test、smoke、scan，即使传入 -j 也保持步骤顺序。所有步骤共享同一 RUN 证据目录。初次构建由示例生成权限 600 的 .env；无需填写真实 Key。镜像名与冒烟标签按学号区分。不要运行全局清理其他组员的镜像。

make doctor 仅在分配的 Linux 服务器上通过才计入环境验收。Mac 的非 Linux 自检失败属于预期限制，不能冒充服务器通过。

## 命令兼容

| 命令 | 作用 |
|---|---|
| make all | E4 全流程 |
| make doctor/build/test/smoke/scan | E4 单步验证 |
| make shell / make lock | E4 容器终端 / 更新依赖锁 |
| make check | 原 E2/E3 契约、26 项测试、Minicalc 演示和历史验证 |
| make regression-test | 原根 tests/ 单元测试（原 make test） |
| python3 scripts/verify_e3_baselines.py | 原 E3 人工参考基线 |

E4 make test 是容器内服务测试，不替代原回归。默认 make 已改为 E4 make all；旧 CI 显式执行 make check，仍验证原流程。

## 接入调整

保留模板的镜像 digest、依赖锁及四项测试，增加两项超时行为测试，确保超时不误判为预期构建失败。合并 Makefile 和忽略规则；服务镜像只复制 fixtures/draft，避免携带 Minicalc bundle 和历史产物。doctor 增加源码 SHA/dirty 状态；扫描器同时检查 Git 未忽略的新文件；冒烟镜像标签带学号。镜像的 socket 挂载和资源配置沿用模板，本次尚未运行服务器容器。

Docker socket 相当于控制宿主机 Docker。只构建课程样例，不开放远程 Docker API。密钥只在本地 .env，禁止进入源码、镜像或日志。

## 服务器交付待办

- [ ] Linux 服务器 make doctor：problems 为空，身份为学号。
- [ ] make build：保存 build.log、image.json、toolchain.lock，核对镜像 digest。
- [ ] make test：原模板四项及本组补充两项测试通过。
- [ ] make smoke：默认 app 用户能访问 Docker Server，预期失败错误含 make: not found。
- [ ] make scan：仓库/历史/镜像通过；假 Key 被拒绝、清理后通过。
- [ ] 另一名真实组员在独立学号目录克隆相同 SHA 并重跑，对比结论。

本地检查结果另见 LOCAL_CHECKS.md，不将本地模拟或本机预检计作上述服务器验收。

## 教师指定服务器配置（2026-10-15）

按用户提供的教师配置图，B03 使用 2 vCPU、2 GiB 内存、80 GiB 系统盘；无需为满足原模板阈值升级。用户实际服务器为 Ubuntu 24.04.4 x86_64，可见内存约 1.7 GiB，磁盘可用约 72 GiB；教师示例图使用 Ubuntu 22.04。

原模板 doctor.py 的最低可见内存 3.5 GiB 与教师指定规格不符，本组将该阈值调整为 1.5 GiB，作为标称 2 GiB 服务器的检查容差。CPU 最低 2 核、磁盘可用最低 40 GiB 保持不变；建议资源不足仍显示 warning，不阻止 E4 小样本运行。该调整不证明构建或测试成功，仍以实际日志验收。Compose 的 1 GiB 服务内存限制保持不变，宿主机构建不受该限制；按顺序运行，暂不同时启动多名组员的构建。本次未配置 Swap 或修改云服务器。

服务器首次构建停在 deb.debian.org 的 trixie Packages 下载，保留原日志后取消该次构建。已验证华为云 Debian 与 Debian Security 镜像 HTTPS 可达，服务 Dockerfile 通过 DEBIAN_MIRROR 改用该源，保留原 Debian 签名验证和固定镜像 digest；新增 apt 索引超时/重试参数。私有 GitHub 仓库在服务器无凭据，使用 SSH 传入 Git bundle 并核验完整 SHA，origin 仍记录真实 GitHub 地址；未传送 GitHub Token。
