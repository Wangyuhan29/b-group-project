# minicalc

一个极简的算术表达式计算器（C11），用作 **DevOps E2 实验 A 组 BuildChecker / EChecker 与 B 组 DRAFT / MDFixer 的共同测试目标项目**（A/B 配对联调使用同一仓库、同一 commit）。

- 构建系统：Makefile（`make`）
- 语言标准：C11（`-std=c11 -Wall -Wextra`）
- 支持：`+ - * /` 与括号，整数运算

## 构建与运行

```bash
make            # 构建 minicalc
make test       # 构建并跑三个冒烟用例
./minicalc "1+2*3"    # 7
./minicalc "10-4/2"   # 8
./minicalc "3*(4+5)"  # 27
./minicalc --version  # minicalc 1.0.0
```

> 注意：`make clean` 使用 Unix 风格的 `rm -f`。Windows 下请通过 Git Bash / WSL 运行，或直接在 Linux 中运行（BuildChecker 的 clean build 命令 `make clean && make -j2` 默认在 Linux 镜像中执行）。

## 目录结构

```text
minicalc/
├── Makefile          # 构建脚本（刻意未完整声明头文件依赖，见下）
├── src/
│   ├── main.c        # CLI 入口（打印版本、计算表达式）
│   ├── parser.c      # 递归下降求值
│   ├── token.c       # 词法分析
│   └── util.c        # 工具函数（die）
└── include/
    ├── config.h      # 版本等配置宏（C1 起新增 TOKEN_CAPACITY）
    ├── parser.h
    ├── token.h
    ├── util.h
    └── legacy.h      # 遗留头文件（C0/C1 无人引用 → REDUNDANT；C2 起被 util.c 重新使用）
```

## 口径约定：实际依赖 vs 声明依赖

- **实际依赖图（ACTUAL_GRAPH）**：编译每个目标时实际读取的源/头文件集合，**含传递包含**。获取方式：构建过程跟踪（如 ptrace）或编译器依赖输出（`gcc -MM` / `-H`）。
- **声明依赖图（DECLARED_GRAPH）**：Makefile 各目标规则声明的依赖。
- **MISSING**：实际需要、声明缺失；**REDUNDANT**：声明了但本配置未用。

## 刻意埋入的构建依赖缺陷（C0 基线，tag: `c0`）

下表是 **C0** 提交中「Makefile 声明依赖」与「实际构建读取依赖」的差异，即 BuildChecker 的预期发现：

| 类型 | target | 缺失/冗余的依赖 | 位置 | 证据 |
|---|---|---|---|---|
| MISSING | main.o | util.h | Makefile main.o 规则 | main.c `#include "util.h"`，规则未声明 |
| MISSING | main.o | token.h | Makefile main.o 规则 | main.c 经 parser.h **间接**包含 token.h，规则未声明 |
| MISSING | parser.o | token.h | Makefile parser.o 规则 | parser.c 经 parser.h 传递包含 token.h，规则未声明 |
| REDUNDANT | util.o | legacy.h | Makefile util.o 规则 | 规则声明了 legacy.h，但编译 util.o 时从未被读取 |

- 全量检测（FULL_CHECK @ C0）期望结果：`missing: 3, redundant: 1`
- 声明图（DECLARED_GRAPH）取自 `make -p`；实际图（ACTUAL_GRAPH）取自构建过程跟踪（如 ptrace）或编译器依赖输出（`gcc -MM` / `-H`，含传递包含）。

> 说明：`main.o → token.h` 是**传递依赖**（main.c → parser.h → token.h）。按“编译器实际读取”口径应计入 MISSING；本表已用 `gcc -H` 依赖输出核对。

## 增量检测场景（EChecker，C0 → C1 → C2）

### c0 → c1

- `c1`：新功能「可配置 token 容量」——`config.h` 新增 `TOKEN_CAPACITY`，`parser.c` 新增 `#include "config.h"` 并使用 `TOKEN_CAPACITY`，但 Makefile 未更新。
- 期望：`added: 1（parser.o → config.h, MISSING）, removed: 0`；c1 全量 `missing: 4, redundant: 1`。

### c1 → c2

- `c2`：新功能「恢复遗留兼容钩子」——`util.c` 开始包含并使用 `legacy.h`（调用 `legacy_die_hook`），使 C0 起即存在的冗余声明变为真实依赖。
- 期望：`added: 0, removed: 1（util.o → legacy.h, REDUNDANT 消除）`；c2 全量 `missing: 4, redundant: 0`。

### 汇总

| 提交 | MISSING | REDUNDANT | 相对上一提交新增 | 相对上一提交消除 |
|---|---|---|---|---|
| c0 | 3 | 1 | — | — |
| c1 | 4 | 1 | parser.o → config.h | — |
| c2 | 4 | 0 | — | util.o → legacy.h |

## Git 历史

```bash
git log --oneline --decorate
# <sha-c2> (HEAD, tag: c2) feat: restore legacy hook (resolves REDUNDANT)
# f863c2d (tag: c1) feat: configurable token capacity (adds MISSING)
# e3a1eda (tag: c0) chore: minicalc baseline (3 MISSING + 1 REDUNDANT)
```

完整 SHA 用 `git rev-parse c0 c1 c2` 获取；EChecker 的 baseline 必须使用 c0 的完整 SHA。

## 测试

```bash
make test
# == 1+2*3   => expect 7
# 7
# == 10-4/2  => expect 8
# 8
# == 3*(4+5) => expect 27
# 27
```
