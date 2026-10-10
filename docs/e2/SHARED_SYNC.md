# A/B 共享契约同步记录

日期：2026-09-17。

依据：A 组提供的 REPLY_TO_B.md，及实际读取的 A 组仓库 `tang-yixin/devops_lab_a03` 的 e2 分支，提交 `b75b40f89708bc577e223081631a2c17e68c1fa8`。

B 组首次建立 contracts/shared-lock.json，沿用最初共同模型的 31 个文件及哈希，追加 graph.schema.json 和 finding-id-v1.json。锁文件的 b_source_commit 保留初始模型来源，不是当前仓库 HEAD；锁本身不能加入自身哈希。

实际核对结果：33 个文件在 A/B 两侧逐字节一致。两个新增文件的 SHA-256 为：

| 文件 | SHA-256 |
|---|---|
| contracts/graph.schema.json | 18820800b1f9e38ec040c81fdbf8d002a42f2353b66de5088c667bc533bb7b60 |
| contracts/finding-id-v1.json | dc2f196d3fb3f7c89db6b6d31743960c970c10e92aae3bb02cf05c6ceb505347 |

运行 `python3 scripts/check_shared_lock.py` 或 `make validate` 检查锁。A 组可以直接取 B 组锁文件对齐；此记录不表示已修改或提交 A 组仓库。

根据 A 组回复，图格式与 ID 算法已获得 A 方采纳。为了不改变已匹配文件的字节和哈希，Schema 标题及 ID 文件中的旧 PROPOSED 标记保留，由本同步记录说明当前确认情况。若后续要清理这些说明字段，应双方一起重新生成锁。

镜像交接详见 IMAGE_HANDOFF.md。构建需要真实通过容器测试才能填写 digest；图/ID 已一致不代表镜像验证自动成立。
