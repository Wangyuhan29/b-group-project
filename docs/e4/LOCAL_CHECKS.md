# E4 本地准备验证（2026-10-15）

历史结论（本地准备时）：模板接入和本地检查通过；当时尚未完成服务器正式验收。后续结果见 [服务器验证](SERVER_VERIFICATION.md) 和 [本阶段验证汇总](VERIFICATION.md)。本次在 macOS arm64、Python 3.13.14、Make 3.81 下执行，没有初始化服务器或构建/运行 E4 服务镜像。

| 检查 | 实际结果 | 证据 |
|---|---|---|
| 依赖锁按哈希安装 | 隔离 venv 的 pip install --require-hashes 成功，保留模板锁文件原文 | dependency-install.log |
| 服务单元测试 | 6 passed：原模板 4 项，加超时拒绝及部分输出保留 2 项 | service-tests.log |
| 原项目回归 | make check：33 个共享文件锁、契约样例、26 项单测、C2 演示和三版本历史验证通过 | regression.log |
| Compose 解析 | --no-env-resolution 静态解析成功；模拟学号 241250086 和组号 0，仅验证配置，不代表实际 socket 组号 | compose.json |
| 工作区和 Git 历史扫描 | 未发现问题，包含未忽略的新文件 | repository-secret-scan.log |
| 假 Key 检出及恢复 | 一次性临时仓库：未跟踪假 Key 被拒绝；工作树清除后通过；仅在历史保留假 Key 时被拒绝 | scanner-self-test.log |
| 忽略规则 | .env 未跟踪；.env、.env.local、private.key、work/ 均忽略 | 本地断言通过 |
| 环境自检 | exit 1，Mac 非 Linux、Docker Server 不可用；本仓库已设置学号本地身份 | env.json、doctor.log |

上述文件已挑选归档到 [本地检查证据](../../artifacts/e4/local-20261015/manifest.json)，含模板 ZIP 和逐文件 SHA-256。运行时源码包含未提交的 E4 修改，manifest 和 env.json 明确记录 source_dirty=true，不声称是某个干净提交的服务器验收。

## 不需要服务器的重跑

在仓库根目录执行（本地环境命令；虚拟环境放在忽略的 work/）：

```sh
python3 -m venv work/e4-local-venv
work/e4-local-venv/bin/python -m pip install --require-hashes -r requirements-dev.lock
work/e4-local-venv/bin/python -m pytest -c services/draft/pytest.ini services/draft/tests
make check
python3 scripts/secret_scan.py . --history
STUDENT_ID=241250086 DOCKER_GID=0 docker compose --env-file .env.example config --no-env-resolution -q
```

假 Key 测试使用一次性临时 Git 仓库，未向本组真实历史写入假 Key；已在 work/e4-local-checks-20261015/ 中保留测试副本，保持忽略。本机未生成 .env、未填写 API Key；未改变全局 Git 身份。服务器 clone 后仍须运行 make all，进行镜像扫描及两名真实组员的重跑对比。
