# B03 E4 服务器验证（2026-10-15）

三个学号目录的真实服务器全流程均通过，实测源码 SHA 相同。241250017、241250075 的归档提交及逐文件哈希已核验，工具清单与单测日志均与 241250086 逐字节一致，冒烟和密钥检查结论一致。详见 [朱玄运行对比](MEMBER_COMPARISON_241250017.md)和[靳滨硕运行对比](MEMBER_COMPARISON_241250075.md)。跨组 README 重跑互查已于 2026-10-18 双向通过，见 A03_CROSS_VALIDATION_20261018.md。

## 固定版本和环境

- 实测源码 SHA：`8701f70d4a3f76592832eedde62b02bb59711ef4`，运行前工作区干净。
- Ubuntu 24.04.4 x86_64，2 vCPU，实际可见内存约 1.7 GiB，80 GiB 系统盘；依教师指定 2 核 2G 运行。
- Docker Engine 29.1.3、Compose 2.40.3、Buildx 0.30.1；宿主机 Git 2.43.0、Make 4.3、Python 3.12.3。
- 个人克隆：`/root/241250086/b-group-project`，本地 Git 身份为学号。
- 成功证据：`work/20261015T113739788827Z/`。
- 服务镜像：`e4-draft:241250086`，linux/amd64，默认用户 app，本地 image ID 为 `sha256:2a708b2e44f4589340ccf8aa961985cae3c9fea1a2f7f1da1f64031b837ef999`。未发布服务镜像，不将 image ID 当作 registry digest。

## 实际结果

| 步骤 | 结果 |
|---|---|
| 环境自检 | problems 为空，建议资源 warning 保留 |
| 镜像构建 | 成功，固定 Python/Docker CLI digest，按锁文件哈希安装依赖，工具版本已导出 |
| 容器单测 | 6 passed |
| 默认 app 用户冒烟 | Docker Server 29.1.3，样本构建退出 1，错误 make: not found，passed=true；RUN make 内部退出 127 |
| 仓库、Git 历史、镜像扫描 | 未发现问题 |
| 假 Key 检查 | 一次性未跟踪测试文件被检出，make scan 退出 2；清理后退出 0；未提交假 Key |
| .env | 权限 600，未跟踪，未归档其内容 |

完整原始日志、安装记录、两次网络失败及成功记录见 [证据清单](../../artifacts/e4/server-20261015/manifest.json)。源码版本、镜像 ID 和假 Key 检查路径见 [服务器回执](../../artifacts/e4/server-20261015/e4-server-receipt.json)。传输包 SHA-256 已与服务器一致性核对。

## 网络适配和源码交付

服务器对私有 GitHub 仓库没有读取凭据；使用已认证 SSH 传入完整 Git bundle，保留固定提交和真实 origin 地址，未保存 GitHub Token。首次 Debian 下载停滞后仅取消本次构建；随后 pip 无法取得 pytest 版本。两次日志均保留，最终统一提交使用已验证的华为云 Debian/Security 和 PyPI HTTPS 镜像，保留签名验证、依赖版本及哈希要求。

没有创建新 Linux 账号或设置初始密码；依手册共用 root，仅创建 `/root/241250086`、`/root/241250017`、`/root/241250075`。未重装系统、配置 Swap、变更代理或开放远程 Docker API。

## 首次归档时的其他成员接续（历史状态）

朱玄或靳滨硕需亲自在自己的学号目录操作。服务器已保存本组离线 Git 来源 `/root/e4-group-setup/b-group-project`，可用它克隆后固定上述实测 SHA。例如朱玄：

```sh
cd /root/241250017
git clone --branch main /root/e4-group-setup/b-group-project b-group-project
cd b-group-project
git remote set-url origin https://github.com/Wangyuhan29/b-group-project.git
git checkout --detach 8701f70d4a3f76592832eedde62b02bb59711ef4
git config --local user.name 241250017
git config --local user.email 241250017@localhost
make all
```

操作前确认自己的目标克隆目录不存在，已有目录不要覆盖。只在各自目录运行，按顺序执行，避免同时构建。记录真实运行人、SHA、证据目录，对比 toolchain.lock、test.log 和 smoke.json 结论；缓存、镜像 ID 或时间差异应说明。首次归档时其他成员目录为空、尚未重跑；后续 241250017 已在 `/root/241250017/draft` 完成授权复跑，勿照上述历史示例另建重复克隆。241250075 后续也已在 `/root/241250075/draft` 完成复跑，详见其运行对比文档。

本文件和后续证据归档提交仅增加记录，服务器实测版本仍为上述 SHA；不要把文档提交 SHA 当作已实际运行的源码版本。

## 三人证据汇总（2026-10-15 更新）

统一实测 SHA：`8701f70d4a3f76592832eedde62b02bb59711ef4`，三个运行前的工作区均干净，Git 本地身份均为对应学号。

| 成员 | 成功证据目录 | 归档提交 | 结果 |
|---|---|---|---|
| 王宇晗 241250086 | /root/241250086/b-group-project/work/20261015T113739788827Z | e2a89833a1285b532e043c2a72c858ca145eb56b | 自检、6 项测试、预期失败冒烟和扫描通过 |
| 朱玄 241250017 | /root/241250017/draft/work/20261015T115106982116Z | dc080d3090aca0b772d40b290d08d1c9e84516f3 | 同上；假 Key 拒绝、清理恢复通过 |
| 靳滨硕 241250075 | /root/241250075/draft/work/20261015T121458530171Z | 85fb8c021b845423e319fa3e3e8e0335486f5f06 | 同上；假 Key 拒绝、清理恢复通过 |

本次重新计算三套归档 manifest 中的所有文件哈希，均匹配。三套 toolchain.lock 与 test.log 逐字节相同。镜像 ID、耗时与缓存使用差异已在两份对比文档解释，不能将缓存构建视为从零下载验证或性能改进。

两位组员的归档提交作者姓名分别为 xuan zhu、靳滨硕，运行时 Git 身份为学号。按课件后续提交应在各自克隆使用学号身份；本次不重写他人已推送历史。个人贡献记录分别注明真实提交作者。

B03 服务环境与同服务器重跑证据已齐；已完成的课堂相邻组互查见 [E4 跨组互查清单](PEER_REVIEW.md)。
