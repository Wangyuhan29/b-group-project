# B03 E5 DRAFT 论文方法复现

| 本阶段记录 | 文件 |
|---|---|
| 小组与分工 | [TEAM.md](TEAM.md) |
| 任务与完成状态 | [BACKLOG.md](BACKLOG.md) |
| AI 使用与来源 | [AI_USAGE.md](AI_USAGE.md) |
| 个人贡献 | [CONTRIBUTIONS.md](CONTRIBUTIONS.md) |
| 验证与证据 | [VERIFICATION.md](VERIFICATION.md) |


本次选择手册允许的“包内已保存 DeepSeek 候选”路线，完成失败采集、两类提示生成、候选比较与环境适配、手工构建及程序验证。没有新发起网页/API 模型对话，不将记录候选写成本次模型生成。

## 输入和候选选择

项目为 `fixtures/draft/` 的 Tiny Greeting：`make` 构建，`./hello` 预期输出 `hello E3`。原始教师候选及其原有来源字段保留在 `fixtures/ci-candidates/DeepSeek-E5.Dockerfile` 和 `provenance.json`，模型具体版本原包未记录。

采用 `fixtures/ci-candidates/B03-E5.Dockerfile`：保留安装 build-essential、COPY、RUN make 与 CMD；使用已有 E4 项目的准确固定 digest 和华为 Debian 镜像源，差异见 `B03-provenance.json`。这些属于本组环境适配，不是 DeepSeek 原始回复。

R1：本次此前未手工构建该适配候选；R2：本次回放采用教师已选的候选 1。原资料中候选 1 和 3 折叠续行并去除边界空白后逻辑指令相同，候选 2 改变 COPY/RUN 顺序；三份原文件、来源、教师选择记录和两种提示已保存在 `course-support/e5-recorded-source/`，属于教师历史记录，不是本组新生成的六份回复；R3：build-essential 包含缺少的 make 与 C 编译工具，符合失败原因；R4：不适用，无额外模型裁决。两类提示从真实失败日志生成，保存在本次证据中。若教师额外要求新模型交互与每类三个候选，该扩展仍需另行完成，不能用本次回放替代。

## 复跑

```sh
python3 scripts/course.py e5 --candidate fixtures/ci-candidates/B03-E5.Dockerfile --out work/e5-new --build-timeout 1200
docker build --progress=plain -f fixtures/ci-candidates/B03-E5.Dockerfile -t course1027-e5-candidate:241250086 work/e5-new/project
```

成功构建后查询该标签实际 image ID，再以该 ID 禁网运行，分别保存构建退出码、镜像 ID、程序输出及运行退出码。实际结果与原始路径见 [验证](VERIFICATION.md)。

## 方法边界

本次只验证一个小项目及一个记录候选，未实现自动模型调用、多轮搜索或论文完整基准评测。通过真实失败和真实程序行为验证环境修复，不能仅凭 Dockerfile 文本认定成功。
