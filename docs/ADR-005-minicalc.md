# ADR-005 minicalc 版本、图与 finding ID

状态：Proposed，待 A/B 确认。日期：2026-09-16。

Context：A 组已提供目标项目与三个版本信息，并询问图结构、ID、镜像、配置。首次匿名 Git 读取失败；随后用户提供 SSH 地址，现已取得并核验三个真实版本。

Decision：以 C2 ZIP 文件清单哈希固定可复现实验；通过 SSH 核验 A 提供的三个 tag/SHA，并保存真实 Git bundle 和逐版本本地扫描。保留旧共享契约和例子，新 minicalc 数据单独命名。提出最小边列表图 Schema 与完整 SHA-256 finding ID；详细算法及向量随仓库交付。Dockerfile 作为尚未执行的候选。

Alternatives：从 C2 手动逆推旧版本无法证明真实 commit 内容，因此不采用。立即修改所有旧样例会破坏 A/B 已有一致性，因此保留兼容回归。

Consequences：C2 可本地演示修复；C0/C1 的源码和本地基线已可离线重放，Docker 与真实增量算法仍待执行。新 ID/图格式是共同待审方案。真实镜像、跨机器产物读取和 A 组重检尚未完成。
