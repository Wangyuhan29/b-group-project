# B03 E6 两轮构建核心工作流

| 本阶段记录 | 文件 |
|---|---|
| 新版提交材料 | [实验报告](REPORT.md)、[验收表](ACCEPTANCE.csv)、[候选来源](CANDIDATE_SOURCE.json) |
| 小组与分工 | [TEAM.md](TEAM.md) |
| 任务与完成状态 | [BACKLOG.md](BACKLOG.md) |
| AI 使用与来源 | [AI_USAGE.md](AI_USAGE.md) |
| 个人贡献 | [CONTRIBUTIONS.md](CONTRIBUTIONS.md) |
| 验证与证据 | [VERIFICATION.md](VERIFICATION.md)、[验收表](ACCEPTANCE.csv) |


2026-10-30 已按单独发布的 DevOps_E6_Student_Cloud.zip 对齐提交材料，实际运行日期保留为 2026-10-28。报告逐项解释四项代码阅读任务，记录新增测试、重建及重新运行；详细内容见 [实验报告](REPORT.md)。

已接入教师 `services/draft/draft/autobuild.py`、CLI 和云端入口。第一轮必须真实复现缺 make，第二轮构建已保存候选，随后按第二轮镜像 ID 启动禁网程序并比较输出。报告、CLI 退出码与验证日志分别保存，不把候选回放称作自动模型生成。

## 本组修改

教师 prepare_candidate 只接受未固定的原始 FROM，与本仓库 E4 已固定的 FROM 不兼容。本组允许原始与候选 FROM 完全相同，继续拒绝更换既有 digest；没有放宽 COPY、RUN make、CMD 的保留约束。E5 入口支持显式候选，以便记录真实环境适配。

## 复跑与核验

```sh
python3 scripts/course.py build --out work/build-new --build-timeout 1200
python3 scripts/course.py e6 --candidate fixtures/ci-candidates/B03-E5.Dockerfile --out work/e6-new --build-timeout 1200
python3 scripts/verify_e6_b_evidence.py --run-dir work/e6-new/evidence
```

项目副本、两轮 Dockerfile、构建日志、image inspect、程序验证及 result.json 全部保存在 work 的本次目录。正式执行环境须为 Linux，并可访问宿主 Docker。已有证据见 [验证记录](VERIFICATION.md)。
