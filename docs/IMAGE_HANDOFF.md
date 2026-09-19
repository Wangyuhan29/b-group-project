# C2 镜像交接

2026-09-17 已完成构建、容器运行断言并发布。成功记录：https://github.com/Wangyuhan29/b-group-project/actions/runs/35172889272 。机器可读信息见 image-receipt.json。

实际注册表 digest：`sha256:c4e23321b6f51c9382d2c3b12eef8c9594d8aa9aab01daf8d52928b41f27dc6d`。

登录 GHCR 后按固定 digest 获取：

```bash
docker pull --platform linux/amd64 ghcr.io/wangyuhan29/minicalc-devops@sha256:c4e23321b6f51c9382d2c3b12eef8c9594d8aa9aab01daf8d52928b41f27dc6d
docker run --rm --platform linux/amd64 ghcr.io/wangyuhan29/minicalc-devops@sha256:c4e23321b6f51c9382d2c3b12eef8c9594d8aa9aab01daf8d52928b41f27dc6d
```

对应源码为 C2 `e103bcb3726a3fd7253deb0d791ac74fac77cafe`。不能把此镜像中的 C2 源码当作 C0/C1 的工作树；那些版本需要在相同工具链下替换为准确源码并重新验证。

本机没有 Docker，因此使用 GitHub Actions 的 Linux amd64 runner 构建并运行镜像。工作流先验证固定源码与共享锁，再构建、运行三个算术用例和版本断言，全部通过才推送 GHCR。

- 工作流：`.github/workflows/minicalc-image.yml`（Build and publish minicalc C2）。
- 镜像标签：`ghcr.io/wangyuhan29/minicalc-devops:c2`。
- 不可变版本标签：`c2-<B组构建提交SHA>`。
- 实际 digest：见本页及成功工作流的 `minicalc-c2-image-handoff` 产物。
- 平台：linux/amd64，A 组若使用 ARM 机器需显式指定 `--platform linux/amd64`。

成功摘要会提供 `docker pull` 和 `docker run` 的完整 digest 命令，避免后来 c2 标签移动导致环境不一致。digest 是注册表清单摘要，不是本地 image ID。

GHCR 镜像不自动公开。接收者需要有包的读取权限，并在自己的机器完成 `docker login ghcr.io`（GitHub 用户名及具备 read:packages 权限的凭据）。不要在回复或仓库里发送访问令牌。包权限与仓库协作者访问是否继承，以 GitHub 包设置为准。

目前源码和编译测试由 B 组工作流验证；A 组仍需实际拉取，并执行 Checker 才能确认交接完成。仓库中的 `*-response-local.json` 继续表示早期本机扫描，不改写为容器执行记录。
