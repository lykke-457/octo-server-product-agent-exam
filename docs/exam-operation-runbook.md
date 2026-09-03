# 考试运行手册

## 0. 冻结前检查

- [ ] GitHub 需求池仓库是 public。
- [ ] labels 已创建。
- [ ] issue templates 可用。
- [ ] Product Agent 已加载 `knowledge/` 与 `prompts/product-agent.md`。
- [ ] PM/Review Agent 已加载 `prompts/pm-review-agent.md` 与 `prd-template.md`。
- [ ] cron 或 scheduler 已启用，并能写 `run-log.md`。
- [ ] 群内回报模板已确认：有产出才发，必须 @ 主考。
- [ ] 所有 token/secret 仅在本地 secret store 或环境变量，不在仓库、不在群里。

## 1. 初始化 labels

如果使用 GitHub CLI，可按 `.github/labels.yml` 创建。不要把 token 写进命令历史或仓库。

## 2. 启动扫描

示例：

```bash
REPO=owner/name GITHUB_TOKEN=$GITHUB_TOKEN ./scripts/cron_tick.sh
```

cron 示例（每 10 分钟）：

```cron
*/10 * * * * cd /path/to/repo && REPO=owner/name GITHUB_TOKEN=$GITHUB_TOKEN ./scripts/cron_tick.sh >> state/cron.stdout.log 2>&1
```

## 3. 扫描后处理原则

- `changes` 为空：只写 run-log，不发群。
- 新 issue：Product Agent 分诊、补 label、必要时回群。
- PRD 需求：PM/Review Agent 补 PRD，状态改 `status/prd-drafting`。
- Review 打回：按原因修改，不得混淆结论。
- issue 关闭：检查关闭原因，回群时区分 done / wontfix / not reproduced。

## 4. 群内回报模板

```text
@主考 @相关同学
已处理需求池变化：

- Issue：#12
- 类型：feature
- 当前状态：status/reviewing
- 动作：已补 PRD，并请求 review
- 下一步：等待 review 结论
```

## 5. 红线

- 目标仓库只读。
- 不发 token / cookie / secret。
- 不编源码引用。
- 不发“无更新/正在检查/一切正常”。
- GitHub 限流后停止扫描，等待 reset。
