# 本轮 minicalc 接口提案

当前主测试目标为 A 组 minicalc C2。新样例见 contracts/minicalc，实测结果与未完成项见 MINICALC_HANDOFF.md 和 VERIFICATION.md；图/ID 提案见 ADR-005，尚待 A 组确认。C0/C1/C2 SSH 历史及本地扫描已验证，Docker 镜像与 A 组重检未完成。下面保留 E2 初版说明，涉及 fixture://draft-project、artifacts/demo 和旧样本的内容仅供兼容回归。

# 接口与交接约定（待 A/B 确认）

## 请求与查询

| 操作 | 端点 | job_type |
|---|---|---|
| DRAFT | POST /v1/dockerfile-jobs | DRAFT |
| BuildChecker | POST /v1/full-check-jobs | FULL_CHECK |
| EChecker | POST /v1/incremental-check-jobs | INCREMENTAL_CHECK |
| MDFixer | POST /v1/repair-jobs | REPAIR |
| 状态查询 | GET /v1/jobs/{job_id} | 查询结果包含类型 |

创建请求必填 schema_version、trace_id、job_type、execution、input、idempotency_key。服务端生成 job_id，HTTP 202 返回 job_id + QUEUED，GET 返回完整公共任务单。公共任务单没有 idempotency_key，包含 input/output/error。

拟定幂等范围是“创建端点 + 调用方身份 + idempotency_key”。相同 key、相同规范化请求返回同一 job_id；相同 key、不同内容返回 409/INPUT_1001。规范化指对象键排序后 JSON 序列化，数组顺序保留。保留期暂定 24 小时；鉴权、存储、并发锁都留待服务实现，当前脚本不模拟服务器。

## 状态、执行错误和分析发现

正常迁移 QUEUED → RUNNING → SUCCEEDED/FAILED/TIMED_OUT；QUEUED 或 RUNNING 可由后续运行器取消为 CANCELLED。终态不可回退。本期只定义取消状态，没有设计取消 HTTP 端点。

QUEUED/RUNNING/CANCELLED 的 output 和 error 都为 null。FAILED/TIMED_OUT 的 output 为 null、error 必填。SUCCEEDED 的 output 必填、error 为 null。发现 MD/RD 属于 ERROR_REPORT.findings，检测成功仍为 SUCCEEDED。修复流程正常完成但判定候选无效，返回 SUCCEEDED + accepted=false + rejection_reason；工具自身无法执行则 FAILED。将来实现运行器时需另外验证迁移顺序，静态 Schema 只能验证单个快照。

| code | 含义 | 使用位置 |
|---|---|---|
| INPUT_1001 | 结构/值不合法、幂等键冲突 | HTTP 400/409；不创建 Job |
| INPUT_1002 | 仓库或完整提交不匹配 | HTTP 422；或受理后 FAILED |
| INPUT_1003 | 构建配置/工作目录不匹配 | HTTP 422；或受理后 FAILED |
| INPUT_1004 | 非 MD-only、空报告或位置不在 Makefile 范围 | HTTP 422；或受理后 FAILED |
| ARTIFACT_2001 | 产物不存在、不可读、哈希错误 | 受理后 FAILED |
| ENV_3002 | 镜像构建失败（PPT） | job.error |
| EXEC_4002 | 超时（PPT） | TIMED_OUT 的 job.error |
| ANALYSIS_5001 | 分析器失败（PPT） | job.error |
| REPAIR_6001 | 修复验收结果自相矛盾 | 校验拒绝；正常候选拒绝不用此错误 |

超时单位秒，必须正整数；timeout_seconds 表示整个任务上限，max_iterations 表示 DRAFT 总候选尝试上限。运行器尚未实现超时控制。404 响应沿用 INPUT_1001、message 说明 job 不存在，这是待确认的本组约定。

## 环境交接

DRAFT 输入给出 repository.url/commit、build.command/clean_command/verify_command/working_directory、max_iterations 和 execution.timeout_seconds。完整 40 位 Git SHA 绑定版本。

DRAFT 成功输出包含 Dockerfile URI、environment、每轮 index/log_uri/changes/selection_reason，以及最终 build_result/verify_result。下游沿用该 repository、build 和 environment，保持 environment.project_root 与 working_directory 相同；configuration_id 标识编译器、构建选项等同一配置。配置改变必须新分配 ID，不能只更改 ID 而复用不匹配的产物。

生产交接建议 image 使用不可变 digest；当前契约允许 tag，但演示 tag 是占位名称。本地 fixture://draft-project 对应 fixtures/source.bundle，用 git clone 读取；它只用于离线样例。真实任务应替换为双方可访问的仓库 URL 和已存在的 SHA。

## 检测和修复交接

FULL_CHECK 输出实际图、声明图、ERROR_REPORT 和证据 URI；报告可有 MD/RD 两类 finding。位置包含 Makefile 路径和一基行号，evidence 包含实际/声明关系、描述及 URI。示例图格式仅供本地演示，真实图中节点、边、进程模型属于后续共同待决项，不算已冻结算法图 Schema。

INCREMENTAL_CHECK 必须包含 base_commit、baseline 两张图 URI、baseline.commit/configuration_id；baseline.commit 必须等于 base_commit，配置必须等于当前环境；图的产物元数据必须匹配同一仓库、旧提交和配置。当前仓库 commit 可与 base 不同；输出为当前图、报告和新增/消除 finding IDs。跨提交 finding_id 的稳定生成方案需 A 组决定。

REPAIR 必须消费非空 MD-only ERROR_REPORT；混合报告由上游先拆分，RD 从不提交给修复器。报告和每条 finding 的提交、报告仓库 URL、configuration_id 必须与请求一致；位置必须落在 makefiles 列表中。只通过 URI 字符串校验还不够，因此 validate.py 读取实际报告并核对内容与哈希。

修复产物包含 patch、declaration_style、accepted、rejection_reason、build/test/recheck。accepted=true 必须构建、测试、重检全通过，且 remaining_missing_count=0。重检发现数要与引用报告一致。修复针对 base commit 上的 patch overlay；当前示例以原 commit 标识基底，patch URI 与产物 sha256 标识修改。E3 真实重检必须同时传递 overlay 的 patch hash，或创建修复提交后给 A 组该提交，具体扩展见 BACKLOG，当前不能拿仅含基底 commit 的示例代替真实 overlay 身份证明。

## 产物读取

artifact://demo/name 映射到本仓库 artifacts/demo/name。文件在 artifacts/index.json 注册；解析器验证目录边界、存在性和 SHA-256，拒绝联网 URI 和未注册产物。E2 双方收到同一份仓库即可读取。真实运行建议双方共享 HTTPS 下载地址或共同对象存储，必须补充鉴权/保留期与跨机器实测；E12 的跨组读取证据当前未完成。

metadata 包含 artifact_id、type、uri、media_type、producer_job_id、repository、configuration_id、sha256。大日志仅存 URI。PPT 将 sha256 列为按需选项，本方案把它设为必填以便离线校验。

## 校验器边界

task.schema.json 是标准 Draft 2020-12；validate.py 为零依赖实现，仅支持该文件实际使用的关键字，启动会拒绝未知关键字。它不是完整 JSON Schema 引擎，其 URI 校验也只做基础绝对 URI 检查。结构符合后还执行提交、配置、报告、验收状态语义检查。将来升级 Schema 可切换到标准 jsonschema 实现，保留语义层与回归样例。
