# 04b 模块职责速查表（初版）

> 说明：本表用于考试快速定位。职责描述基于模块名、`1module.go` 注册、公开路由文件与已读注释整理；没有完全核验的模块标为“待细化”。

## 启动注册机制

模块通过 `internal/modules.go` blank import 触发各模块 `init()` 注册；migration 排序按 SQL 文件名时间戳，不按 import 顺序。

来源: internal/modules.go#L1-L18
来源: internal/modules.go#L22-L78

## 核心模块

| 模块 | 初步职责 | 证据 |
|---|---|---|
| `base` | 基础 app/event 能力与基础 SQL | 来源: internal/modules.go#L24-L27 |
| `user` | 用户、好友、管理端用户相关能力；也提供 user datasource | 来源: internal/modules.go#L62-L63 |
| `group` | 群、群成员、群 ACL、群 IM datasource | 来源: modules/group/1module.go#L43-L55 |
| `thread` | 群内子区 / CommunityTopic，父群 ACL 继承 | 来源: modules/thread/1module.go#L53-L73 |
| `channel` | 会话/频道详情、单聊/群/子区资料读取鉴权 | 来源: internal/modules.go#L35-L38 |
| `message` | 消息、会话、侧边栏相关 API 和 SQL | 来源: modules/message/1module.go#L28-L53 |
| `file` | 文件上传/下载、文件服务适配 | 来源: internal/modules.go#L39-L40 |
| `space` | Space/知识空间与成员边界 | 来源: modules/space/1module.go#L32-L48 |

## Bot / Agent 相关模块

| 模块 | 初步职责 | 证据 |
|---|---|---|
| `robot` | User Bot/机器人基础资料与 IM token 相关历史能力 | 来源: modules/robot/1module.go#L18-L26 |
| `botfather` | BotFather DM 命令、User Bot 管理、User API Key、Robot Apply、文档端点 | 来源: modules/botfather/api.go#L83-L120 |
| `bot_api` | Bot 外部 API 网关：sendMessage/events/groups/threads/file/card/voice/OBO/search/webhook 管理 | 来源: modules/bot_api/bot_api.go#L400-L497 |
| `app_bot` | App Bot 管理：platform/space scoped bot、发布、token、用户 opt-in | 来源: modules/app_bot/app_bot.go#L116-L154 |
| `bot_provision` | octo-fleet/daemon 新契约：mint bot、用 api_key 换 bot_token；JWT/JWKS 已移除 | 来源: modules/bot_provision/bot_api.go#L1-L18 |
| `botidentity` | card/action 等场景解析 bot 身份 | 来源: main.go#L551-L569 |
| `bot_mention` | 文档评论/mention bot 入口（待细化） | 来源: internal/modules.go#L32-L33 |
| `agentmailgateway` | Agent mail gateway（待细化） | 来源: internal/modules.go#L24-L25 |
| `voice_adapter` | 语音转写/voice context 适配 | 来源: modules/bot_api/bot_api.go#L455-L459 |

## 集成 / 通知 / 管理模块

| 模块 | 初步职责 | 证据 |
|---|---|---|
| `incomingwebhook` | 群入站 webhook 管理与投递 | 来源: modules/bot_api/bot_api.go#L491-L493 |
| `webhook` | 接收 IM/webhook/github 回调、推送通知 | 来源: modules/webhook/api.go#L148-L159 |
| `notify` | 系统通知/卡片通知发送 | 来源: main.go#L601-L620 |
| `notification` | 通知暂停等用户通知设置（待细化） | 来源: internal/modules.go#L47-L48 |
| `oidc` | OIDC 登录/绑定 | 来源: internal/modules.go#L49-L49 |
| `integration` | 第三方 integration | 来源: internal/modules.go#L42-L43 |
| `openapi` | Open API | 来源: internal/modules.go#L50-L51 |
| `messages_search` | 消息搜索，web/bot/user-key 多入口共享 handler | 来源: modules/bot_api/bot_api.go#L185-L189 |
| `card_template_catalog` | 卡片模板运行时 catalog | 来源: main.go#L393-L402 |
| `backup` | 备份与 WuKongIM 数据目录相关能力 | 来源: internal/modules.go#L24-L25 |

## 其他模块（待细化）

`category`、`common`、`conversation_ext`、`internal_resolve`、`opanalytics`、`qrcode`、`report`、`search`、`statistics`、`sticker`、`usersecret`、`workplace`。

来源: internal/modules.go#L35-L78

## 明确不用 / 已迁移

`modules/runtime` 已移除，runtime/bot orchestration 由 octo-fleet 负责。

来源: internal/modules.go#L54-L57
