# 07 Bot 与 Agent

## 已确认结论

### 1. Bot API 是统一的 bot gateway，路由集中在 `/v1/bot`
`BotAPI.Route` 注册 `/v1/bot/register`、`/v1/bot/heartbeat` 和 `/v1/bot` 组内 sendMessage、events、messages/sync、groups、threads、file、card、voice、OBO 等端点。

来源: modules/bot_api/bot_api.go#L297-L339
来源: modules/bot_api/bot_api.go#L341-L375
来源: modules/bot_api/bot_api.go#L400-L468
来源: modules/bot_api/bot_api.go#L479-L497

### 2. User Bot 与 App Bot 是两套身份，但在 Bot API 中统一成 `robot_id` / `bot_kind`
`authBot` 根据 token 前缀分流，最终都在上下文中写 `robot_id` 和 `bot_kind`。

来源: modules/bot_api/auth.go#L10-L23
来源: modules/bot_api/auth.go#L25-L43
来源: modules/bot_api/auth.go#L58-L61
来源: modules/bot_api/auth.go#L123-L129

### 3. App Bot 有 platform / space scope、发布状态、token、created_by 等字段
`appBotModel` 定义了 ID、UID、DisplayName、Scope、SpaceID、Status、Token、CreatedBy 等字段；管理路由区分平台和 Space。

来源: modules/app_bot/db.go#L28-L41
来源: modules/app_bot/app_bot.go#L38-L49
来源: modules/app_bot/app_bot.go#L116-L154

### 4. App Bot token registry 用 Redis 共享缓存支持多副本快速撤销
`NewAppBot` 初始化 `RedisAppBotRegistry` 并注入到 bot_api；注释说明共享 Redis store 让 token revocation 在所有副本即时生效。

来源: modules/app_bot/app_bot.go#L92-L102
来源: modules/bot_api/auth.go#L99-L120

### 5. BotFather 处理 DM 命令和 User Bot 管理生态
BotFather 注册消息监听器，只处理发给 BotFather 的单聊文本消息，并调用 command handler；同时提供 skill/CLI/setup 文档端点和 User API Key / Robot Apply 端点。

来源: modules/botfather/api.go#L68-L80
来源: modules/botfather/api.go#L83-L120
来源: modules/botfather/api.go#L156-L207

### 6. bot_provision 是 octo-server 与 octo-fleet/daemon 的新契约面
文件注释说明 `POST /v1/bot/mint` 用 web session mint bot；`GET /v1/bot/:uid/token` 用 daemon api_key 返回 bot token；JWT/JWKS 已移除。

来源: modules/bot_provision/bot_api.go#L1-L18
来源: modules/bot_provision/bot_api.go#L190-L218
来源: modules/bot_provision/jwt.go#L1-L10

## 待补充 / 不确定

- “agent 会话怎么起”的完整链路可能已经迁到 octo-fleet；本仓目前确认 runtime 模块已移除。
