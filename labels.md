# GitHub Label 体系建议

## 类型
- `type/bug`：缺陷反馈
- `type/feature`：新功能/增强
- `type/question`：产品或源码问题
- `type/prd`：需要补 PRD
- `type/review`：等待或正在评审

## 优先级
- `priority/P0`：阻塞考试/核心链路不可用
- `priority/P1`：重要功能或高影响问题
- `priority/P2`：普通需求/一般问题
- `priority/P3`：低优先级优化

## 状态
- `status/new`
- `status/triaged`
- `status/prd-drafting`
- `status/reviewing`
- `status/changes-requested`
- `status/approved`
- `status/wontfix`
- `status/done`

## 来源
- `source/exam-group`
- `source/examiner`
- `source/user-feedback`

## 处理原则

- bug 和 feature 必须至少有一个 `type/*`、一个 `priority/*`、一个 `status/*`。
- `wontfix`、`done`、`approved` 不可混用为同一状态。
- 关闭 issue 时必须保留最终结论：已修复 / 没复现 / 不做，不得混写。
