# A03 跨机联调待办

B03 已独立通过固定样例、真实 Minicalc C0→C1，以及 HTTP 幂等、409 冲突、下载 SHA 和重启恢复。需要 A03 实际参与的仅为跨机访问和双方确认。

1. 双方固定同一源码提交，核对 docs/e12/CONTRACT.md、dataset.csv 中 base/target 和请求。
2. B03 在自己的服务器目录执行 python3 run_e11e12.py serve --port 18087。测试前由 B03 确认监听正常，无需开放公网 8080/18087。
3. A03 使用自己有权使用的服务器登录方式建立 SSH 转发，例如本地端口 18080 转至 API 服务器 127.0.0.1:18087；不在报告填写密码或 Token。
4. A03 访问 /health，POST 双方确认的 input（路径使用 API 服务器 /course/data），轮询任务，下载 candidate.patch 并核对 SHA。
5. A03 返回实际请求、job_id/trace_id、运行时间、下载哈希、结果与证据提交 SHA；B03 再填写双方联调结果。

服务器工作路径和请求以本阶段报告为准。未完成上述操作前不勾选 A03 跨机联调完成。
