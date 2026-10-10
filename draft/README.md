# DRAFT 环境准备

当前主目标为 fixtures/minicalc/source（C2）。候选文件 minicalc.Dockerfile 的构建上下文是 B 项目根目录，复制 minicalc 源码及结果断言脚本。运行方法见根 README。C2 镜像已构建、验证并发布至私有 GHCR，获取方式见 [镜像交接](../docs/e2/IMAGE_HANDOFF.md)。E3 Tiny Greeting 已完成 Mac arm64 和 Ubuntu 原生 amd64 的失败/参考成功 Docker 验证，见 [E3 文档](../docs/e3/README.md)。自动生成与迭代的 DRAFT 服务仍未实现。C0/C1 源码已在 history.bundle 中，仍需按版本固定对应 Docker 输入。旧 artifacts/demo/Dockerfile 仅属于人工回归样本。
