# ADR-005 minicalc 版本、图与 finding ID

状态：Accepted（A03/B03，2026-09-22）。

Context：A 组已提供目标项目与三个版本信息，并询问图结构、ID、镜像、配置。首次匿名 Git 读取失败；随后组员提供本机 SSH 地址，现已取得并核验三个真实版本。

Decision：以 C2 ZIP 文件清单哈希固定可复现实验；通过 SSH 核验 A 提供的三个 tag/SHA，并保存真实 Git bundle 和逐版本本地扫描。保留旧共享契约和例子，新 minicalc 数据单独命名。采用最小边列表图 Schema 与完整 SHA-256 finding ID；详细算法及向量随仓库交付。C2 Dockerfile 已有构建和发布记录，见 IMAGE_HANDOFF；不将其直接作为 C0/C1 源码环境。

Alternatives：从 C2 手动逆推旧版本无法证明真实 commit 内容，因此不采用。立即修改所有旧样例会破坏 A/B 已有一致性，因此保留兼容回归。

Consequences：C2 可本地演示修复并已由 A03 完成镜像冒烟验证；C0/C1 的源码和本地基线已可离线重放。真实 BuildChecker/EChecker 算法、C0/C1 环境和跨机器产物读取属于 E3/E12。
