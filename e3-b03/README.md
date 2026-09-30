# B03 E3 并行测试基线

依据课程课件《E3_并行测试基线_20260930.pptx》准备。这里保存人工预期、可运行样本、实际观察和失败记录。E3 当前目标是独立准备测试基线；真实 DRAFT/MDFixer 运行器在后续实验实现。

## 环境与版本

- 项目：本仓库内 `e3-b03/fixtures/` 的课程人工样例。用提交本目录的 Git SHA 固定版本；提交前以 `git rev-parse HEAD` 和文件 SHA-256 确认快照。
- 关联真实目标：Minicalc C2 `e103bcb3726a3fd7253deb0d791ac74fac77cafe`，原有 B03 C2 修复、Patch 和镜像记录仍在 `artifacts/minicalc/c2/`、`docs/IMAGE_HANDOFF.md`。
- 本次本地环境：macOS arm64，GNU Make 3.81、Apple clang 21.0.0、Python 3.13.14、Git 2.54.0。
- Docker Desktop 29.8.1 已于 2026-09-30 在本机安装并运行。Tiny Greeting 的失败候选和参考镜像已在本机实测，证据见 `evidence/docker-20260930/`。此前 C2 镜像已在 GitHub Actions 构建、推送并由 A03 拉取验证，两套镜像分别记录。

## DRAFT 基线

`fixtures/draft/README.md` 给出 `make` 和 `./hello` 的成功判据。`Dockerfile.broken` 故意缺少 `make` 和 C 工具链；`Dockerfile.reference` 安装工具链并在构建中断言输出。

在本目录运行 `python3 verify_baselines.py`，脚本会生成新的 `evidence/<UTC 时间>/`，保留原有证据。本机实际结果：缺少工具命令的模拟失败退出码 127，正常 `make` 构建退出码 0，`./hello` 输出 `hello E3` 且退出码 0。模拟失败日志标有 `LOCAL_FAILURE_SIMULATION`，不能当作 Docker 构建失败日志。

在有 Docker 的 Linux 环境中，从 `fixtures/draft/` 运行：

```bash
docker build -f Dockerfile.broken -t b03-e3-draft-broken .
docker build -f Dockerfile.reference -t b03-e3-draft-reference .
docker run --rm b03-e3-draft-reference
```

本机实际结果：第一条退出码 1，内部 `RUN make` 退出码 127，日志明确显示 `/bin/sh: 1: make: not found`；第二条退出码 0；第三条输出 `hello E3`、退出码 0。参考镜像 ID 为 `sha256:c67e26a89b12e4971dc7652754c8c0deb42e55f4a7ea041b3426e05d8a763ced`，平台 `linux/arm64`。完整日志和命令见 `evidence/docker-20260930/`。此镜像尚未推送到远端。

## MDFixer 基线

`fixtures/mdfixer/fixed-md.json` 是人工参考答案，限定 `main.o` 对项目头文件 `config.h` 的一条 MISSING。它不是 Checker 运行输出。四种 Makefile 声明风格分别为 Target、Macro、Hybrid、Implicit；每种都有 `before.mk`、`after.mk` 和可用 `git apply --check` 验证的参考补丁。

`verify_baselines.py` 在临时副本逐种检查：原始输出 1；只改头文件为 VALUE 2 后增量构建仍输出旧值 1；应用补丁并完整构建输出 2；再改头文件为 VALUE 3 后增量构建输出 3。Implicit 风格额外检查编译器生成的 `main.d` 包含 `config.h`。脚本还故意加入构建失败候选，确认非零退出，再恢复原 Makefile 并重新构建成功。原始样本不会被脚本改动。

本次通过的摘要和各命令日志在最新 `evidence/` 目录。具体源码快照可用下列哈希核对：

```text
mdfixer/main.c           a1bbac023098d5bdd6302977e565b57c4959ee2c34d0787c1c5b2ea5c208ee9f
mdfixer/config.h         ac32a92f4af359517c993d6e8583ea2d9b053c2ad171b4c602bc242894bd9696
mdfixer/target.before.mk e99d68627e6a99dfa90469063633cb06fff1dc024425a88b2c33521799519116
```

## 未完成与下一步

- 如需在课堂统一的 `linux/amd64` 环境比较结果，应在该平台再次运行；当前容器证据来自本机 `linux/arm64`。
- 后续 E5/E8 实现 DRAFT 与 MDFixer 运行器时，用本目录人工答案判定其输出；不能将参考补丁直接当作自动工具结果。
- 与 A03 的真实 Checker、跨机器产物读取和修复后重检安排在后续实验联调。
