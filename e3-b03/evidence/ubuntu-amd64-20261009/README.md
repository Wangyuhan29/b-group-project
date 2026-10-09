# B03 Ubuntu 原生 amd64 Docker 证据（2026-10-09）

已从 Windows VMware Ubuntu 取回 21 个原始文件，传输包 SHA-256 与虚拟机一致；逐文件哈希见 manifest.json。原始日志未改写。源码四个文件与 B03 基线提交 `9f39cc899b9e8136b89ebe32c90f74c00d912ec7` 完全一致。GitHub clone 当时失败，因此虚拟机使用字节核对后的文件，不声称成功克隆工作树。

## 预期与实际观察

| 场景 | 人工预期 | 原始观察 | 结论 |
|---|---|---|---|
| Dockerfile.broken | 缺少 make，构建非零退出 | RUN make 报 make: not found；退出码 127 | PASS（预期失败） |
| Dockerfile.mirror | 安装工具链，构建生成 hello 并通过断言 | 构建退出码 0，test -x 和输出断言均成功 | PASS |
| 运行参考镜像 | 退出码 0，标准输出 hello E3 | 退出码 0，hello E3 | PASS |

环境：Ubuntu 20.04.6 LTS，内核 5.15.0-139-generic，Docker 20.10.21，原生 x86_64；容器平台 linux/amd64。环境原文见 evidence/environment.txt；编译工具链的安装版本见 evidence/reference-build.log。

参考镜像本地 ID：`sha256:5ecded03dc4ec427a0d42fd2a2c0c6691a757e9eae2685897adaa4cedecca112`，平台由 evidence/reference-image.json 核对。镜像未发布，这不是 registry digest。

基础镜像通过 docker.1ms.run 拉取后重标为 python:3.13-slim，获取 digest 为 `sha256:70729b46c69b4f1e97c4822c1af3df53a1476cf5ddc6c087c0c10bc3a5678c2f`；见 evidence/1ms-pull.log 和 base-image.json。首次下载与原始 Debian 源尝试因网络停滞中止，日志分别保留，不能当成构建逻辑失败。

成功候选使用 draft/Dockerfile.mirror，只将参考 Dockerfile 中 Debian 下载域名替换为 mirrors.tuna.tsinghua.edu.cn；gcc/make/libc6-dev 和构建断言保持一致。未修改 Windows 代理，未关闭签名校验。失败到成功的差异见 dockerfile.diff。

## 重跑

在具有 Docker 的原生 Linux amd64 环境，从本证据目录开始。使用独立输出目录保留已有日志；以下失败构建的非零退出是验收目标。

```bash
cd draft
mkdir -p ../rerun
# 固定基础镜像；已归档的原始命令使用同一 digest 对应的标签
sudo docker pull docker.1ms.run/library/python@sha256:70729b46c69b4f1e97c4822c1af3df53a1476cf5ddc6c087c0c10bc3a5678c2f
sudo docker tag docker.1ms.run/library/python@sha256:70729b46c69b4f1e97c4822c1af3df53a1476cf5ddc6c087c0c10bc3a5678c2f python:3.13-slim
sudo docker build --platform linux/amd64 -f Dockerfile.broken -t b03-e3-draft-broken:amd64 . > ../rerun/broken-build.log 2>&1
echo $? > ../rerun/broken-build.exit
sudo docker build --platform linux/amd64 -f Dockerfile.mirror -t b03-e3-draft-reference:amd64 . > ../rerun/reference-build.log 2>&1
echo $? > ../rerun/reference-build.exit
sudo docker run --rm --platform linux/amd64 b03-e3-draft-reference:amd64 > ../rerun/reference-run.log 2>&1
echo $? > ../rerun/reference-run.exit
sudo docker image inspect b03-e3-draft-reference:amd64 > ../rerun/reference-image.json
```

对照上表检查三个退出码、失败错误、构建中的可执行文件/功能断言及运行输出。系统软件源版本可能随时间变化，重建镜像 ID 不保证相同。run-reference.sh/run-mirror.sh 是虚拟机实际执行脚本，保留原工作目录，不直接用于其他机器。

## 验证范围

本次证据满足 B03 E3 DRAFT 失败与参考成功基线。MDFixer 四类参考修复与拒绝恢复另见 E3 README；不声称自动 DRAFT/MDFixer 运行器或四服务联调完成，也不解决 A03 跨架构 strace 的独立复验待办。
