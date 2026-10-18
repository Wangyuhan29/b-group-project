# A03/B03 E4 双向互查（2026-10-18）

结论：两方向固定版本的 E4 工程环境互查均通过。B03 反向测试在王宇晗个人目录的独立克隆中原样执行，没有修改 A03 源码或原 B03 服务目录。范围是环境、构建、单测、冒烟与密钥检查，不代表 E5 Checker 算法或 E12 四服务联调已完成。

## A03 对 B03

A03 提供的实测 SHA：`8701f70d4a3f76592832eedde62b02bb59711ef4`。A03 环境 Ubuntu 22.04.5 x86_64，2 CPU，约 1.7 GiB 可见内存。归档来源是 A03 e4 分支文档/证据提交 `e6bdfe76ec26a1b1bbbc83804bfd629104d51ade`，不是把该分支头当作测试源码版本。

B03 已逐项静态核对其原始记录及 SHA256SUMS：自检 problems 为空，构建通过，6 passed，冒烟 build_exit_code=1、make_error_line 含 make: not found、passed=true，密钥扫描通过。此方向的实际执行由 A03 完成，B03 核验收到的证据，不冒充再次在 A03 服务器执行。

保留的对方原始文件及校验表见 [A03 原始校验表](../../artifacts/e4/a03-reviewed-b03-8701f70-20261018/SHA256SUMS.txt)。对方 metadata 中 origin 记录为传入的 Git bundle 路径，这与私有仓库离线交付说明一致，不改写原始 metadata。

## B03 对 A03

- 仓库：https://github.com/tang-yixin/devops_lab_a03.git，e4 分支。
- 固定实测 SHA：`6abc4d815b4a4baae7cc9d72fc221653a7897e19`，运行前后工作区干净。
- 复核人学号身份：241250086，Git 本地配置；AI 辅助执行。
- 独立克隆：`/root/241250086/a03-e4-cross-20261018`。
- 执行目录：上述克隆的 `e4-a03/`，按指定版本 README 原样执行 `make all`，没有修改源码或配置。
- 成功证据目录：`e4-a03/work/20261018-170959/`。
- 实际环境：B03 Ubuntu 24.04.4、x86_64、2 CPU、约 1.7 GiB 可见内存、Docker Engine 29.1.3。

| 检查 | 实际观察 | 判断 |
|---|---|---|
| doctor | problems=[]，身份 241250086 | PASS |
| build | 构建成功，依赖按哈希安装；pip 发生超时后原命令自行重试成功 | PASS |
| test | 3 passed in 0.01s | PASS |
| smoke | make_exit_code=0，app_output=1，trace_lines=1206，passed=true | PASS |
| 系统调用 | openat(AT_FDCWD, "config.h", O_RDONLY\|O_NOCTTY) = 4 | 正常记录到项目头文件打开 |
| scan | 仓库文件、Git 历史、镜像检查未发现问题 | PASS |
| .env | 权限 600，未被跟踪；内容未取回 | PASS |
| make all | 总退出码 0 | PASS |

完整原始日志和回执见 [本次证据清单](../../artifacts/e4/a03-cross-validation-6abc4d8-20261018/manifest.json)及[运行回执](../../artifacts/e4/a03-cross-validation-6abc4d8-20261018/receipt.json)。传输包 SHA-256 已与服务器核对一致。镜像 ID 是本地身份，不作为已发布 registry digest；基础 digest 与实际工具版本分别保留在 build.log 和 toolchain.lock。

本次原生 Linux E4 冒烟未出现此前 Mac 跨架构环境的系统调用解码异常，但它不等于补做了 E3 Minicalc 全部动态依赖推断。两台服务器的 Ubuntu 版本差异明确保留；双方固定提交、各自 README 下的预期结果一致。

## 收尾

B03 工程环境、三个学号目录复跑及 E4 双向环境互查现均有原始证据。给 A03 回传本次固定测试 SHA、环境、目录及归档位置即可完成记录交接，无需更改密码或提供密钥。B03 归档提交 SHA 由本次 Git 提交记录追溯并随回复提供；A03 测试 SHA 与 B03 归档 SHA 分别记录，不混用。
