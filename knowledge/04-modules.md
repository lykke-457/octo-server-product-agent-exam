# 04 业务模块清单

## 已确认结论

### 1. 模块通过 `internal/modules.go` 的 blank import 注册
注释说明 migration 执行顺序由 SQL 文件名时间戳决定，不由 import 顺序决定；Go init 顺序由依赖图决定。

来源: internal/modules.go#L1-L18

### 2. 当前启用模块清单
`internal/modules.go` 注册了如下模块：agentmailgateway、backup、base、robot、bot_mention、botfather、card_template_catalog、category、channel、common、conversation_ext、file、group、incomingwebhook、integration、internal_resolve、message、messages_search、notification、notify、oidc、opanalytics、openapi、qrcode、report、search、space、statistics、sticker、thread、user、usersecret、bot_api、app_bot、bot_provision、voice_adapter、webhook、workplace。

来源: internal/modules.go#L22-L78

### 3. runtime 模块已移除，runtime/bot orchestration 由 octo-fleet 负责
代码注释明确说明 `modules/runtime` 已移除，相关编排归 octo-fleet，历史 migration 表记录保留。

来源: internal/modules.go#L54-L57

### 4. BotFather 不再处理 `/v1/bot/*` API 主体
BotFather 路由注释说明 `/v1/bot/*` 已迁移到 `modules/bot_api`；BotFather 现在负责文档、User Bot 管理命令、User API Key、Robot Apply。

来源: modules/botfather/api.go#L83-L108

## 待补充 / 不确定

- 每个模块的完整职责可以继续从各模块 `1module.go` / README / Route 方法补齐。
