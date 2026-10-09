# B03 Ubuntu amd64 Docker 验证（2026-10-09）

通过 UU 远程桌面操作 Windows VMware Ubuntu 虚拟机，实际执行 DRAFT Docker 基线。结果由远程终端输出核对；原始证据尚未取回 Mac，不应将本说明视为原始日志。

环境：Ubuntu 20.04.6 LTS，x86_64，Docker 20.10.21；构建明确指定 linux/amd64。

| 场景 | 实际结果 | 验收 |
| --- | --- | --- |
| Dockerfile.broken | RUN make 报 make: not found，构建退出码 127 | 符合预期 |
| Dockerfile.mirror | 安装 gcc/make/libc6-dev 后构建退出码 0 | 通过 |
| 参考镜像运行 | 退出码 0，输出 hello E3 | 通过 |

原始 Dockerfile.reference 的 Debian 下载尝试因网络停滞被中止；成功构建使用 Dockerfile.mirror，仅将 deb.debian.org 替换为 mirrors.tuna.tsinghua.edu.cn。基础镜像通过 docker.1ms.run 拉取并重标为 python:3.13-slim。未修改 Windows 代理设置，未绕过签名校验。

参考镜像本地 ID：`sha256:5ecded03dc4ec427a0d42fd2a2c0c6691a757e9eae2685897adaa4cedecca112`。此值是 image ID，不能作为已发布镜像的 registry digest。

虚拟机源文件 main.c、Makefile、Dockerfile.broken、Dockerfile.reference 的 SHA256 已与 B03 本地文件逐一核对一致。由于 GitHub clone 失败，虚拟机使用核对后的文件，不是成功克隆的 Git 工作树。

完整文件位于 Ubuntu `/home/hp/b03-e3-validation/`，其中 `evidence/` 包含环境、源文件哈希、构建日志、运行日志、退出码及镜像 inspect JSON；`draft/` 包含输入文件和镜像源变体；根目录包含执行脚本。

待完成：将上述目录取回 Mac 后加入 B03 仓库并复核原始日志，再给 A03 回发证据。本次未 commit 或 push，也未验证完整 Checker/MDFixer 联调。临时 HTTP 文件服务已停止。
