# Cron / 长时闭环机制

## 扫描频率
建议每 10 分钟扫描一次需求池 GitHub issues。

## 扫描范围
- 新 issue
- label 变化
- issue close / reopen
- review 评论
- `wontfix` / `feature` / `bug` 状态变化
- PRD 是否被打回、是否已更新

## 触发动作
- 新 bug/feature：归档并打 label
- 需要 PRD：转给 PM/Review Agent 补 PRD
- review 打回：按打回原因修改 PRD
- issue 关闭或状态变化：回报考试群，并 @ 主考和相关人

## 静默原则
- 无新增、无变化时，不向群里发送任何消息。
- 可以写入本地 `run-log.md` 证明 cron 自己醒过。
- 禁止群里发“正在检查”“本次扫描无更新”“一切正常”。

## 考试时要能展示的证据
- 最近几次定时执行记录
- 每次扫描的 issue 数量
- 发现变化后的动作
- 是否回报群、回报给谁
