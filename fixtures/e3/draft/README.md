# Tiny Greeting：B03 DRAFT 测试基线

来源：B03 根据 E3 课件准备的课程人工样例，版本由本仓库提交 SHA 固定。

构建：`make`，成功判据是退出码 0 且生成可执行文件 `hello`。
功能验证：`./hello`，成功判据是退出码 0 且标准输出恰为 `hello E3`。

`Dockerfile.broken` 故意使用缺少 `make`/C 编译工具链的基础镜像，预期 `RUN make` 失败；`Dockerfile.reference` 安装工具链并在构建阶段运行功能断言。两份 Dockerfile 都只复制本目录源码。
