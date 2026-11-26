# e11e12-1 接口契约

| 接口 | 输入／输出 | 状态码 |
|---|---|---|
| POST /v1/jobs | idempotency_key、input；返回 job_id/status | 202；错误输入 400；同键不同输入 409 |
| GET /v1/jobs/{job_id} | status、trace_id、error | 200；不存在 404 |
| GET /v1/jobs/{job_id}/artifacts | 实际阶段和 artifact URI/SHA256 | 200；未就绪 409 |
| GET /v1/jobs/{job_id}/files/{path} | bytes 与 X-Content-SHA256 | 200；不存在或越界 404 |

input 包含 mode、repo、base、target、candidate、fixed_report（E11-B）、expected_output、build_timeout。真实 Minicalc 扩展 profile=minicalc，并提供 data/ 下的 broken_dockerfile；repo/candidate/fixed_report/broken_dockerfile 仅允许服务器 data/ 路径。基础样例和真实项目使用不同请求。
状态：QUEUED、RUNNING、SUCCEEDED、FAILED、TIMED_OUT。envelope：schema_version/job_id/trace_id/kind/commit/status/data/artifacts。
URI artifact://job/path 通过 files 接口下载。消费者核对 kind、target commit、status 和内容哈希。full-check 的 base commit 与目标阶段不同是正常的。
API 只绑定回环，通过 SSH 转发访问。参考编排器在一台服务器串行执行四组件，不声称四套独立服务。
