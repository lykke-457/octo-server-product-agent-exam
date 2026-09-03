# 03 配置

## 已确认结论

### 1. 默认配置文件是 `configs/tsdd.yaml`
服务入口默认读取 `configs/tsdd.yaml`，也可以通过 `--config` 指定。读取后配置环境变量前缀为 `TS`，并把点号替换为下划线。

来源: main.go#L98-L105
来源: main.go#L138-L145

### 2. token 过期配置会在启动时校验并写入 `cfg.Cache.TokenExpire`
启动阶段调用 `validateTokenExpireConfig`，失败则 panic；成功后写入最终配置。

来源: main.go#L108-L110
来源: main.go#L145-L156

### 3. release 模式不允许保留测试短信验证码后门
启动时调用 `ValidateTestCodeConfig`，注释说明 release 模式禁止配置 `smsCode`。

来源: main.go#L158-L161
来源: configs/tsdd.yaml#L52-L68

### 4. 配置主要包含基础、Webhook、WuKongIM、DB、外网、日志、短信、文件、推送、注册、内置账户、头像、短号、机器人、第三方登录、缓存等段
这些段都在 `configs/tsdd.yaml` 中以注释模板形式给出。

来源: configs/tsdd.yaml#L1-L35
来源: configs/tsdd.yaml#L36-L68
来源: configs/tsdd.yaml#L69-L171
来源: configs/tsdd.yaml#L172-L259

### 5. Webhook HMAC 与 WuKongIM 配置是显式配置段
Webhook 可配置 HMAC-SHA256 密钥；WuKongIM 需要 `apiURL`，若 WuKongIM 配了 manager token 则需要配置 `managerToken`。

来源: configs/tsdd.yaml#L15-L24

## 待补充 / 不确定

- 哪些配置是“硬必填”取决于部署模式和 octo-lib 默认值；需继续读 `octo-lib/config` 或启动校验逻辑。
