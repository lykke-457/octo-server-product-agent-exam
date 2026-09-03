# 08 存储与外部依赖

## 已确认结论

### 1. 默认 dev 运行需要 MySQL-compatible DB、Redis、WuKongIM、对象存储等外部依赖
README quickstart 说明默认 dev config 期待本地 WuKongIM 和 MySQL-compatible database；CI 注释还说明 MySQL、Redis、WuKongIM 是 E2E/integration-style tests 需要的服务。

来源: README.md#L52-L58
来源: .github/workflows/ci.yml#L136-L172

### 2. 数据库和 Redis 配置在 `configs/tsdd.yaml` 的 db 段
DB 段包括 `mysqlAddr`、`redisAddr`、`redisPass`、Redis TLS、异步任务 Redis 地址。

来源: configs/tsdd.yaml#L26-L35

### 3. SQL migration 分散在各模块 `sql/` 目录
仓库里大量模块都有 `sql` 目录，例如 app_bot、bot_api、botfather、common、group、message、space、thread、user 等。

来源: internal/modules.go#L1-L18
来源: internal/modules.go#L22-L78

### 4. 启动时在 module.Setup 前做 legacy migration ID 修复和 thread schema 兼容
`runAPI` 在 `module.Setup(ctx)` 前调用 `RewriteLegacyMigrationIDs` 和 `ReconcileThreadSchemaRecords`，避免旧数据库 migration ledger 与当前 SQL 文件不一致导致启动失败。

来源: main.go#L454-L479
来源: main.go#L481-L486

### 5. Redis 覆盖 session、rate limit、bot registry、用户/群/Space auth 等控制面
`main.go` 注释说明 Redis 指标覆盖共享缓存、限流、OIDC、bot registry、user/group/space auth、health、Lua 锁等。

来源: main.go#L426-L444

### 6. 文件服务支持 MinIO、Tencent COS、Aliyun OSS、Qiniu、SeaweedFS，不同后端 presigned 能力不同
配置注释给出 presigned PUT/GET 能力矩阵，并说明浏览器直传需要 bucket CORS。

来源: configs/tsdd.yaml#L69-L104
来源: configs/tsdd.yaml#L105-L171

## 待补充 / 不确定

- 各核心表结构需要按模块 SQL 逐表整理，当前只完成了依赖与 migration 机制层面的初稿。
