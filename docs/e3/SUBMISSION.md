# B03 E3 提交核对（2026-10-09）

依据《E3_并行测试基线_20260930.pptx》第 6、9、10 页及 B 组操作附录核对，B03 本阶段必交基线材料已完成。E3 要求独立测试输入、人工预期与实际观察；运行器在 E5/E8，真实跨组数据联调在 E12。

| 必交项 | 文件及证据 | 状态 |
|---|---|---|
| DRAFT 项目、构建与功能条件 | fixtures/e3/draft/：main.c、Makefile、README；make 退出 0，生成 hello，运行输出 hello E3 且退出 0 | 完成 |
| 可定位的真实失败构建 | artifacts/e3/ubuntu-amd64-20261009/evidence/broken-build.log、broken-build.exit；RUN make 报错，退出 127 | 完成 |
| 参考成功、差异、镜像身份和功能日志 | 同目录 draft/Dockerfile.mirror、dockerfile.diff、reference-build.log、reference-run.log、退出码及 reference-image.json；构建/运行均 0 | 完成 |
| 固定 MD 报告与对应 Makefile | fixtures/e3/mdfixer/fixed-md.json；INSTRUCTOR_ORACLE_ADAPTED_BY_B03；对应四种 before.mk，限定 main.o → config.h | 完成 |
| 参考 Patch、依据与修复判据 | target/macro/hybrid/implicit.patch、after.mk；main.c 包含 config.h，原规则缺声明；修复后再次改头文件自动重建输出 3 | 完成 |
| 无效候选拒绝与恢复 | scripts/verify_e3_baselines.py；evidence/20260930T035836430577Z/summary.json 和 rejection 日志，失败退出 2，恢复输出 1 | 完成 |
| 环境、版本、命令与实际日志 | E3 README、Docker 两个平台历史记录、Ubuntu environment.txt、源码哈希、manifest.json 和重跑步骤 | 完成 |
| 仓库、SHA 与个人贡献 | https://github.com/Wangyuhan29/b-group-project，main；原样本固定提交 9f39cc899b9e8136b89ebe32c90f74c00d912ec7；贡献见 docs/CONTRIBUTIONS.md；最终提交版本用 git rev-parse HEAD 获取 | 完成 |
| 小组与设计说明 | docs/TEAM.md：B03/A03、鼓楼校区、三名成员与联系人；docs/BACKLOG.md、docs/AI_USAGE.md 及已有 ADR | 已填写 |
| 相互检查、失败及后续说明 | A03 复核 B03 的结果见 A03 提供的回复；B03 实测互查日志见 artifacts/e3/a03-cross-review-20261009/；strace 异常及下一步明确记录 | 完成记录 |

## 证据和边界

- Ubuntu 原始包与虚拟机 SHA-256 一致，21 个原始文件已归档；四个原始输入文件与固定基线提交一致。镜像源变体另存，不冒充原版网络条件。
- MDFixer 报告和 Patch 是人工参考答案，行为日志是实际执行；没有把它们写成真实自动工具结果。
- A03 strace 动态关系尚未独立证明，失败日志已保存。它不属于 B03 本阶段必交项，仍留在后续互查待办。
- ADR-001～003 的双方确认状态继续保留 Proposed，不代替 A03 签认；这是既有设计待办，本次不声称新增双方确认。
- 本次贡献由王宇晗统一提交；没有已确认的新工作证据的成员不新增完成声明。历史分工与提交 SHA 保留原记录。

## 提交前最终验证

2026-10-09 重跑 verify_baselines.py：DRAFT 本地行为、Target/Macro/Hybrid/Implicit 四类修复和无效候选拒绝恢复均 PASS，证据见 `artifacts/e3/20261009T134348322944Z/`。同目录 project-check.log 保存 make check 的通过记录（33 文件锁、契约、26 项测试及 C2/历史检查）。Ubuntu 21 个原始文件哈希再次逐一校验通过。

E3 材料与最终验证对应提交：`497ff2e05757010c3097fb4d3f2ec0d89a1f0c5a`；之后的贡献记录提交仅补充此 SHA。仓库最终 HEAD 同时包含材料与贡献记录。

2026-10-10 互查收尾：A03 新增原生 trace 已独立读取复核，符合 C0 预期；B03 跨架构重跑异常已留档，暂不继续排查。详见 `artifacts/e3/a03-strace-retry-20261010/REVIEW.md`。这是 A03 产物复核通过，不冒充 B03 原生 strace 重跑通过。
