# 06 IM 控制面 / WuKongIM 分工

## 已确认结论

### 1. octo-server 对外是 REST + WebSocket API，同时驱动 WuKongIM IM core
README 明确说 octo-server 是 Go backend，提供 REST + WebSocket API，做 Lobster agent orchestration，并作为 WuKongIM 的 control plane。

来源: README.md#L26-L39
来源: README.md#L44-L47

### 2. Bot API 发送消息最终通过 `ctx.SendMessageWithResult` 交给 WuKongIM
`dispatchMsgSendReq` 注释说明生产路径通过 `ba.ctx.SendMessageWithResult` 发到 WuKongIM；`sendMessage` 组装 `MsgSendReq` 后调用该函数。

来源: modules/bot_api/bot_api.go#L207-L214
来源: modules/bot_api/send.go#L426-L447

### 3. DM 的 channel_id 对 WuKongIM 是裸 uid，Space 前缀主要用于 IM whitelist
`resolveSpaceChannelID` 注释明确：DM 频道在 WuKongIM 中使用裸 uid；Space 前缀只用于 IM whitelist 操作。

来源: modules/bot_api/bot_api.go#L502-L509

### 4. 群解散时 MySQL 是权威状态源，随后推送 WuKongIM disband flag
群解散流程先在 MySQL 事务内写 `group.status=Disband`，提交后再推送 WuKongIM disband；推送失败时 fail-closed，客户端可重试。

来源: modules/group/api.go#L238-L246
来源: modules/group/api.go#L274-L313
来源: modules/group/api.go#L315-L348
来源: modules/group/api.go#L351-L354

### 5. Webhook 接收 IM 消息通知
`modules/webhook` 注册 `/v1/webhook/message/notify`，注释说明这是接收 IM 的消息通知，并可通过 HMAC-SHA256 签名认证。

来源: modules/webhook/api.go#L148-L159
来源: configs/tsdd.yaml#L15-L19

## 待补充 / 不确定

- WebSocket 客户端直连 IM 与 server 控制面的边界，需要继续读 octo-lib 的 IM client / websocket 代码。

## 第二轮补充

### 6. octo-server 对 WuKongIM 管理面访问来自 octo-lib config.Context
本仓通过 `ctx.SendMessageWithResult`、`ctx.IMWhitelistAdd`、`ctx.IMCreateOrUpdateChannelInfo` 等方法操作 IM；这些方法定义在依赖库 octo-lib。octo-server 本仓可核验证据是调用点和配置项，具体 HTTP 路径实现不在本仓。

来源: go.mod#L9-L9
来源: modules/bot_api/bot_api.go#L207-L214
来源: modules/bot_api/send.go#L426-L447
来源: modules/app_bot/app_bot.go#L1139-L1158
来源: configs/tsdd.yaml#L21-L24

### 7. 群/子区控制面典型边界：业务状态先落 MySQL，再同步给 WuKongIM
群解散是一个典型例子：业务侧用 MySQL 的 `group.status` 作为权威状态源，提交后再推送 WuKongIM disband flag；如果 IM 推送失败，API 返回错误让客户端重试，避免业务以为成功但 IM 仍可写。

来源: modules/group/api.go#L238-L246
来源: modules/group/api.go#L274-L313
来源: modules/group/api.go#L315-L348
