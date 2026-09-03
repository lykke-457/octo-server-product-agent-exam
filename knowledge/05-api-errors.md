# 05 API 与错误约定

## 已确认结论

### 1. 服务对每次 HTTP 请求生成或透传 `X-Request-ID`
`runAPI` 中的全局中间件读取入站 `X-Request-ID`，没有则生成；写入 gin.Context、request context 和响应头。

来源: main.go#L239-L252

### 2. 错误响应优先走本仓的 localized error facade
`httperr.ResponseErrorL` 会校验错误码注册、保持 legacy HTTP/body status=400 兼容，并交给注入的 ErrorRenderer 渲染 envelope。

来源: main.go#L197-L204
来源: pkg/httperr/respond.go#L13-L24
来源: pkg/httperr/respond.go#L53-L81

### 3. 新端点或特定端点可以保留语义 HTTP 状态码
`ResponseErrorLWithStatus` body envelope 与 `ResponseErrorL` 相同，但 transport status 使用错误码的 `HTTPStatus`，适合没有 legacy 依赖的新端点。

来源: pkg/httperr/respond.go#L26-L49
来源: pkg/httperr/respond.go#L53-L81

### 4. 错误码集中注册在 `pkg/errcode/*`
例如 thread 错误码定义了 bad request、forbidden、not found、gone、conflict、internal 等分类，并通过 `codes.Register` 注册。

来源: pkg/errcode/server.go#L1-L16
来源: pkg/errcode/server.go#L47-L80
来源: pkg/errcode/server.go#L110-L121

### 5. Bot API 错误码按 validation / permission / not found 等分组
`pkg/errcode/bot_api.go` 注释说明 Bot API 面向外部 bot adapter / integration，部分端点已经依赖真实 HTTP status，因此用 status-preserving 响应。

来源: pkg/errcode/bot_api.go#L9-L20
来源: pkg/errcode/bot_api.go#L22-L68
来源: pkg/errcode/bot_api.go#L114-L205

## 待补充 / 不确定

- 成功响应的统一 envelope 形状多处使用 `c.Response(...)` 和 `c.JSON(...)`，具体封装在 octo-lib，需要继续看依赖库。
