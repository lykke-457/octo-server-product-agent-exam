# GitHub 需求池初始化指南

## 1. 创建 public 仓库

建议仓库名：`octo-server-product-agent-exam`

必须 public，方便考官当天读取。

## 2. 推送本备考包

```bash
cd agent-exam-pack
REMOTE=git@github.com:<owner>/octo-server-product-agent-exam.git ./scripts/bootstrap_repo.sh
git branch -M main
git push -u origin main
```

## 3. 创建 / 更新 labels

```bash
cd agent-exam-pack
GITHUB_TOKEN=$GITHUB_TOKEN python3 scripts/apply_labels.py --repo <owner>/octo-server-product-agent-exam
```

要求 token 只放环境变量，不写入文件、不发群。

## 4. 启用定时扫描

仓库内已有 `.github/workflows/issue-scan.yml`，每 10 分钟执行一次。

它只会：
- 扫描 issue 状态
- 更新 `state/last-scan.json`
- 追加 `run-log.md`
- 提交执行记录

它不会自动发群，避免“无更新”刷屏。群内回报由 Agent 读取 `state/last-scan-output.json` 或 workflow diff 后判断是否有有效产出。

## 5. 考试展示方式

可以展示：
- Actions 运行记录
- `run-log.md` 最近几次扫描记录
- issue label / 状态变化
- Agent 回群记录
