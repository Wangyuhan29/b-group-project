# B03 E7 验证、故障注入与 CI

| 本阶段记录 | 文件 |
|---|---|
| 小组与分工 | [TEAM.md](TEAM.md) |
| 任务与完成状态 | [BACKLOG.md](BACKLOG.md) |
| AI 使用与来源 | [AI_USAGE.md](AI_USAGE.md) |
| 个人贡献 | [CONTRIBUTIONS.md](CONTRIBUTIONS.md) |
| 验证与证据 | [VERIFICATION.md](VERIFICATION.md) |


## 本人新增边界测试

`services/draft/tests/test_student_boundary.py`：候选遗漏 Makefile 时在构建前拒绝；已有固定 digest 可直接使用；更换既有 digest 必须拒绝。后两项对应真实兼容修正，覆盖原包未固定输入的局限。新增测试 3 项通过，服务总数 30 项。

## 服务器完整门禁

```sh
python3 scripts/course.py gate --candidate fixtures/ci-candidates/B03-E5.Dockerfile --out work/e7-new --build-timeout 1200
```

六行结果全部 passed=true：服务测试、成功、错误输出、无效候选、第二轮构建失败、运行超时。故障场景的 FAILED/TIMED_OUT 是期望工具状态，不能据此判定场景失败。超时容器清理已单独 inspect 证明不存在。

## GitHub CI

工作流 `.github/workflows/e7-quality-gate.yml`，检查名 `e7-b-quality-gate`，执行语法检查、源码/镜像扫描、镜像构建、完整门禁并保留 14 天 artifact。当前远程 CI、main 保护、故意失败 PR、拒绝合并及同 PR 恢复证据仍在采集中，详见 [任务状态](BACKLOG.md)；未完成时不计为本阶段全部完成。
