# Octo Agent 配置指南

> 这里是配置建议，不包含任何 token。实际建群/建 Agent 时，凭证必须走平台 secret 或本地环境变量。

## 推荐结构

### Agent 1：octo-server-product-agent

职责：
- 回答 octo-server 产品/源码问题
- 收 bug / feature / question
- 创建/更新需求池 issue
- 对关键结论给源码引用

加载文件：
- `prompts/product-agent.md`
- `knowledge/*.md`
- `issue-template.md`
- `labels.md`
- `docs/source-reference-policy.md`

### Agent 2：octo-server-pm-review-agent

职责：
- 根据 issue 补 PRD
- 请求 review
- 根据 review 修改
- 扫描状态变化并准备群内回报

加载文件：
- `prompts/pm-review-agent.md`
- `prd-template.md`
- `cron.md`
- `docs/exam-operation-runbook.md`

## 群内规则

- 有产出才说话。
- 每条回报必须 @ 主考。
- 需要 @ 相关人时一起 @。
- 不说“正在检查”“无更新”。
- 不暴露 token/secret/cookie。

## 工具权限建议

Product Agent：
- 读目标仓库源码
- 读/写需求池 issue
- 读 labels
- 不允许写目标仓库

PM/Review Agent：
- 读/写需求池 issue/comment
- 读 PRD 模板
- 可读知识库
- 不允许写目标仓库

## 冻结前测试

1. 问 Product Agent：`octo-server 的 Bot API token 认证怎么分流？给源码引用。`
2. 发一条 bug 文本，看是否创建 issue 并打 label。
3. 让 PM Agent 把 issue 补成 PRD，检查是否只写 What。
4. 手动触发 issue scan，确认 `run-log.md` 有记录。
5. 无变化时确认群里没有消息。
