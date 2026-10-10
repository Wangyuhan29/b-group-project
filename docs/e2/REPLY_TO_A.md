# 给 A 组的同步答复

已按你方要求完成两项工作：

1. contracts/shared-lock.json 已包含 graph.schema.json 和 finding-id-v1.json，合计 33 个共享文件。我们读取你方 e2 分支 b75b40f89708bc577e223081631a2c17e68c1fa8 核对，33 个文件与 B 组全部逐字节一致。请取最新版锁文件同步。
2. C2 镜像已在 GitHub Actions 的 Linux amd64 环境构建，三个算术用例及版本断言均在容器内通过，并推送私有 GHCR。

固定镜像引用：

```text
ghcr.io/wangyuhan29/minicalc-devops@sha256:c4e23321b6f51c9382d2c3b12eef8c9594d8aa9aab01daf8d52928b41f27dc6d
```

可读标签为 ghcr.io/wangyuhan29/minicalc-devops:c2。建议样例 environment.image 使用以上完整 digest。对应目标提交为 C2 e103bcb3726a3fd7253deb0d791ac74fac77cafe，configuration_id 沿用 cc-default，平台 linux/amd64，项目根目录 /workspace/minicalc。

获取方式：使用有镜像读取权限的 GitHub 身份登录 ghcr.io 后，执行 docs/e2/records/image-receipt.json 中的 pull_command 和 run_command。私有镜像的读取权限尚需按实际成员安排；仅有 URL 不等于已获授权。如需我们添加访问，请提供实际 GitHub 用户名，由仓库所有者确认后设置。

构建验证记录：https://github.com/Wangyuhan29/b-group-project/actions/runs/35172889272 。详细使用说明见 docs/e2/IMAGE_HANDOFF.md。

这个镜像内置 C2 源码，不直接适用于你方 C0 全量请求。C0/C1 需要在同工具链下使用对应工作树并验证。早期 *-response-local.json 仍为本机扫描历史记录，不能改写为镜像内的 Checker 执行证据。A 组实际拉取与 Checker 重检仍待完成。
