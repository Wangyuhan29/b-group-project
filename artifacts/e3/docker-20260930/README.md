# Docker Desktop 实测记录

日期：2026-09-30；主机：macOS arm64；Docker Desktop 29.8.1；Docker Engine 29.8.1。

工作目录：`fixtures/e3/draft/`。

| 操作 | 命令 | 实际结果 | 日志 |
|---|---|---|---|
| 故意失败 | `docker build --progress=plain --platform linux/arm64 -f Dockerfile.broken -t b03-e3-draft-broken:20260930 .` | 顶层退出码 1；`RUN make` 退出码 127，`make: not found` | `broken-build.log` |
| 参考构建 | `docker build --progress=plain --platform linux/arm64 -f Dockerfile.reference -t b03-e3-draft-reference:20260930 .` | 退出码 0；镜像 ID `sha256:c67e26a89b12e4971dc7652754c8c0deb42e55f4a7ea041b3426e05d8a763ced` | `reference-build.log` |
| 功能验证 | `docker run --rm --platform linux/arm64 b03-e3-draft-reference:20260930` | 退出码 0；标准输出 `hello E3` | `reference-run.log` |

这些是实际 Docker Desktop 运行记录。`../<时间戳>/draft-missing-toolchain-local.log` 仍保留为早先的本地模拟失败记录，二者的来源标记不同。参考镜像仅保存在本机，没有发布到 GHCR。
