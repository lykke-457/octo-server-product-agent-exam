# 02 鉴权模型

## 已确认结论

### 1. 系统管理角色不是单一 admin/superAdmin，还存在固定角色能力分层
`pkg/auth/manager_roles.go` 定义了 `dashboardReader` 和 `marketAdmin`，并用 `IsManagerConsoleRole`、`CanAdminMarketplace`、`CanReadManagerDashboard` 分别控制可进入管理台、市场管理、仪表盘读取。

来源: pkg/auth/manager_roles.go#L5-L24
来源: pkg/auth/manager_roles.go#L63-L90

### 2. App Bot 管理有平台级和 Space 级两套路由
平台管理路由 `/v1/admin/app_bot` 需要登录，并在 handler 里做 admin/superAdmin 检查；Space 管理路由 `/v1/space/:space_id/app_bot` 需要登录，并在 handler 里做 Space admin 检查。

来源: modules/app_bot/app_bot.go#L116-L154
来源: modules/app_bot/app_bot.go#L156-L169

### 3. App Bot 的路由作用域需要和 bot 自身 scope 匹配，防 IDOR
`botInRouteScope` 要求平台路由只能管理 platform-scoped bot，Space 路由只能管理自己 Space 的 bot，注释明确说明这是为了防止通过全局 id 读/轮换其它 Space bot token。

来源: modules/app_bot/app_bot.go#L171-L183

### 4. Channel/Group ACL：群与子区读取要校验成员关系
频道详情里，群频道要求登录用户是群成员；社区子区继承父群 ACL，要求登录用户是父群活跃成员。

来源: modules/channel/api.go#L180-L194
来源: modules/channel/api.go#L231-L250

### 5. OBO 授权必须校验 grantor 对目标频道有读取权，防止 wiretap
创建 OBO scope 前会验证 grantor 能读对应频道：群要求群成员，子区继承父群成员，单聊要求本人或好友关系。

来源: modules/bot_api/obo_api.go#L699-L725
来源: modules/bot_api/obo_api.go#L732-L763
来源: modules/bot_api/obo_api.go#L765-L790

### 6. Bot 发送权限按 BotKind 和频道类型分支
App Bot 只能 DM；Space App Bot 还要求目标用户仍是绑定 Space 成员。User Bot 的群、子区、单聊规则还需继续补完整证据。

来源: modules/bot_api/send.go#L459-L500

## 待补充 / 不确定

- User Bot 对群/子区/单聊的完整 `checkSendPermission` 分支还需继续补全行号。
- org 级 RBAC 的完整模型可能在 octo-lib 或管理模块里，需要继续定位。

## 第二轮补充

### 7. User Bot 群发送：群被解散时先 fail-closed；非 OBO 时要求 bot 自己是群成员
`checkSendPermission` 对 User Bot 的群消息先查 group.status，解散则拒绝；不是 OBO 上下文时，再查 bot 是否为群成员。

来源: modules/bot_api/send.go#L503-L537

### 8. User Bot 子区发送：子区继承父群状态和父群成员关系
社区子区 channel_id 需要拆成 `<parent_group_no>____<short_id>`；先校验父群是否解散；非 OBO 时要求 bot 是父群成员。

来源: modules/bot_api/send.go#L538-L587

### 9. User Bot 单聊发送：创建者可直接和自己的 bot 说话；其他人需要好友关系，OBO 只在明确上下文下才可绕过 friend gate
这避免普通 bot 发送、typing、readReceipt、messages-sync 借 OBO grant 绕过用户 opt-in。

来源: modules/bot_api/send.go#L588-L620

### 10. App Bot 是 DM-only；Space App Bot 还要校验目标用户仍在绑定 Space
App Bot 不支持群/子区发送；DM 也要先有好友/会话关系，Space scope 下还要检查对端 Space membership。

来源: modules/bot_api/send.go#L468-L501
