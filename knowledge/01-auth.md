# 01 认证与身份

## 已确认结论

### 1. 普通用户 REST 认证主要依赖 octo-lib 的 AuthMiddleware，octo-server 在启动时注入自定义 TokenParser
`runAPI` 中创建 server/route 后，把 `pkg/auth.NewCacheTokenParser` 注入到路由的 TokenParser。这个 parser 支持 v2 JSON envelope 与旧的 `uid@name[@role]` 格式，并额外解析语言与角色。

来源: main.go#L193-L227
来源: pkg/auth/parser.go#L59-L72
来源: pkg/auth/parser.go#L130-L227

### 2. REST 用户 token 同时兼容 `token` 头和 `Authorization: Bearer <token>`
`BearerTokenCompat` 会在 `token` 头缺失时，把 `Authorization: Bearer` 回填到 `token` 头，供 octo-lib AuthMiddleware 使用。它不接受 query 参数兜底，避免凭证进 URL 历史和 Referer。

来源: main.go#L279-L288
来源: pkg/wkhttp/bearer_compat.go#L17-L43
来源: pkg/wkhttp/bearer_compat.go#L44-L75

### 3. Bot API 认证按 Bearer token 前缀分流
`/v1/bot` 系列使用 `authBot`：`app_` 前缀走 App Bot，`bf_` 或 legacy token 走 User Bot。User Bot 查 `robot` 表；App Bot 先查共享 registry/cache，miss 后查 `app_bot` 表，并要求 `status == 1`。

来源: modules/bot_api/auth.go#L25-L43
来源: modules/bot_api/auth.go#L45-L62
来源: modules/bot_api/auth.go#L64-L130
来源: modules/bot_api/auth.go#L143-L150

### 4. Bot Provision 的 daemon token 获取走 `Authorization: Bearer uk_...` api_key，不走普通 session middleware
`GET /v1/bot/:uid/token` 要求 Bearer api_key，解析出调用者 UID 和绑定 Space 后，再校验 bot 存在、启用、创建者匹配、bot 也属于该 Space。

来源: modules/bot_provision/bot_api.go#L8-L18
来源: modules/bot_provision/bot_api.go#L96-L109
来源: modules/bot_provision/bot_api.go#L110-L171
来源: modules/bot_provision/bot_api.go#L190-L218

### 5. Webhook/IM 回调有独立认证机制
普通 HTTP webhook 路由包括 `/v1/webhook/message/notify`；配置文件说明可通过 `TS_WEBHOOK_SECRET_KEY` 启用 HMAC-SHA256 签名校验。gRPC webhook 还提供 `auth_token` metadata 拦截器。

来源: configs/tsdd.yaml#L15-L19
来源: modules/webhook/api.go#L49-L50
来源: modules/webhook/api.go#L137-L138
来源: modules/webhook/api.go#L148-L159
来源: modules/webhook/api.go#L162-L175

## 待补充 / 不确定

- WebSocket 握手的具体 token/cookie/DH-sealed frame 实现需要继续在 octo-lib 或相关 websocket handler 中定位；当前仓库 README 提到认证步骤，但实现可能在依赖库里。

## 第二轮补充

### 6. octo-server 依赖 octo-lib 提供 AuthMiddleware / WKHttp，当前依赖版本固定在 go.mod
普通用户认证中间件来自 octo-lib，octo-server 本仓主要负责在 `main.go` 注入自定义 parser、错误 renderer、Bearer 兼容中间件。若考官要求 AuthMiddleware 内部细节，需要说明该实现位于依赖库 `github.com/Mininglamp-OSS/octo-lib`，不是 octo-server 本仓代码。

来源: go.mod#L9-L9
来源: main.go#L193-L227
来源: main.go#L279-L288

### 7. 当前 octo-server 本仓没有定位到 WebSocket 握手实现
README 说服务提供 REST + WebSocket API，但本仓本轮扫描未定位到 WebSocket 握手认证 handler；从代码证据看，REST/Bot/Webhook 认证路径更明确。如果被问到 WebSocket 握手细节，不能编，应回答：需要继续核验 octo-lib 或 WuKongIM 客户端侧实现。

来源: README.md#L26-L39
来源: go.mod#L9-L9
