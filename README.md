# octo-server Agent 实操考核备考包

目标：为 `octo-server` 搭建可在 Octo 群里工作的产品管家 Agent/Agents，完成源码问答、需求归档、PRD、Review、定时扫描与群内回报。

## 源码版本

- 目标仓库：`https://github.com/Mininglamp-OSS/octo-server`
- 本地源码：`../octo-server`
- 当前 commit：`543776488b86cf995aeadc2ce12aac9ba789c671`

## 推荐 Agent 分工

1. **产品管家 Agent**
   - 回答 octo-server 产品/源码问题
   - 收集 bug / feature / question
   - 创建或更新需求池 issue
   - 所有关键结论必须给源码引用

2. **PM/Review Agent**
   - 把 issue 补成 PRD
   - 发起 review、接收打回意见
   - 修改 PRD 并回写 issue
   - 扫描 issue 状态变化，有实际产出才回群

## 文件结构

```text
knowledge/      九块知识库初稿
prompts/        两个 Agent 的 system prompt
labels.md       建议 GitHub label 体系
issue-template.md
prd-template.md
cron.md         定时扫描机制
run-log.md      扫描记录模板
```

## 考试硬规则

- 目标仓库只读，不能写。
- 凭证不能出现在群里，也不能进 git。
- 代码引用必须可核验：`来源: <相对路径>#L<起>-L<止>`。
- 找不到证据就说“不确定”，不能编路径、函数名、行号。
- PRD 只写 What，不写 How。
- 没有产出不要往群里发“无更新/正在检查”。
