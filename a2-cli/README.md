# A2 动手练习手册 · 让 CLI agent 每次都按同一套方法做事

> **教材原文**：[`tracks/cli/A2-cli-workflow.zh-Hans.md`](https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/tracks/cli/A2-cli-workflow.zh-Hans.md)
> **这一站只解决一个问题**：怎么让 CLI agent 下次进入同一个 repo 时，还记得同一套做事方法？
> **目标**：把「每天都要重新交代」改成「墙上有守则，工具箱里有操作卡」。

---

## 一、三个核心词

| 核心词 | 它是什么、像什么 | A2 怎么用 | 不是什么 |
|---|---|---|---|
| **Project instructions（项目规则）** | 每次进入工作室都要看的守则 | 放项目用途、禁止事项、测试指令和交付格式 | 不放只用一次的任务或长篇参考资料 |
| **Skill（操作卡）** | 需要时才拿出的可复用操作卡 | 放 review、release、整理文档等重复流程 | 不是每家 CLI 都使用相同路径、权限或 frontmatter |
| **One-off prompt（单次提示）** | 只交代今天这一件事的便签 | 放本次任务、范围、输入和成功条件 | 不用它重复粘贴每次都相同的项目规则 |

## 二、四个动手练习

| # | 练习 | 教材成果（原话） | 我们的产物 | 状态 |
|---|---|---|---|---|
| **CLI-5** | 做一张最小项目规则卡 | CLI agent 每次进入 repo，都知道这个项目做什么、不能碰什么、怎么验证，以及完成时要回报什么 | [`a1-cli-agent/AGENTS.md`](../a1-cli-agent/AGENTS.md) → [练习卡](cli-5/README.md) | ✅ |
| **CLI-6** | 把重复 review 做成 Skill | 你能让 agent 执行同一套只读 review，输出 `PASS` 或具体问题，不会自己 commit、push 或部署 | [`a1-cli-agent/.agents/skills/review-changes/SKILL.md`](../a1-cli-agent/.agents/skills/review-changes/SKILL.md) → [练习卡](cli-6/README.md) | ✅ |
| **CLI-7** | 把大任务拆成看得见的小步骤 | 你能把一个可恢复的文档任务拆成「盘点 → 计划 → 修改 → 验证」，每一步都有看得见的结果 | [练习卡](cli-7/README.md)（含两次执行的事故复盘） | ✅ |
| **CLI-8** | 做一张 portable prompt 对照卡 | 你能保留同一个任务核心，并清楚标出换工具时要修改的文件名、权限、命令和启用方式 | [`portable-prompt.md`](cli-8/portable-prompt.md) + [`comparison-card.md`](cli-8/comparison-card.md) + [`evidence/`](cli-8/evidence/) → [练习卡](cli-8/README.md) | ✅ |

> 教材说明：「**时间**：先完成 CLI-5、CLI-6；CLI-7、CLI-8 可以之后再做，不必一次完成。」
> 我们的路线：CLI-5 → CLI-6 → CLI-7 → CLI-8，四个都做完了。

## 三、每张练习卡的结构

每个 `cli-N/README.md` 都按同一套结构写，方便照着复现：

1. **教材成果** —— 原文引用，「做到什么算成功」
2. **教材步骤** —— 原文引用，可照着复现
3. **我们的操作** —— 实际跑了什么命令、用了什么模型
4. **产物** —— 当时的文件快照 + 现行文件位置
5. **实测结果 / 踩到的坑** —— 我们真实撞出来的东西
6. **自查清单** —— 对照教材要求逐条勾

## 四、教材的 A2 自查清单（进 Stage 5 前，原文）

- [x] 我能用自己的话分清项目规则、Skill、单次 prompt。
- [x] 我的项目规则卡有用途、禁止事项、验证指令、交付格式，而且 agent 能读到。
- [x] 我的 review Skill 只读取变更，测试后 `git status --short` 没有多出非预期修改。
- [x] 我知道「共用核心」不等于「所有 CLI 的文件名和权限都一样」。

## 五、实验环境（A2 期间）

| 项 | 配置 |
|---|---|
| CLI Agent | Aider 0.86.2 / OpenCode 1.18.31 |
| 本地模型 | Ollama 0.33.2（`qwen2.5:3b` 为主；`gemma4:e4b` 因 6 GB 显存 + 32K 上下文会崩，降级使用） |
| demo repo | `E:\DSH\a1-demo`（可丢弃，全程用 git 当安全网） |
| 费用 | 全程 $0（纯本地模型） |

## 六、A2 期间撞到的四类失败（详见各练习卡）

| # | 失败 | 出自 | 一句话教训 |
|---|---|---|---|
| 1 | `Write` 整文件覆写 → **两个 README 内容被清空** | CLI-7 | 「追加内容」要用 `Edit`；`Write` 会清掉没提到的内容 |
| 2 | 口头说了三次「我将运行 `git diff --check`」，**从未调用 Bash** | CLI-7 | 验证步骤是弱模型最爱跳过的步骤 |
| 3 | `Edit` 的参数传成模板占位符 `{%include oldString%}` | CLI-8 | 工具选对了 ≠ 参数填得对 |
| 4 | 整文件重写导致**换行符 CRLF → LF** | CLI-8 | `Write` 的代价不止内容，还有换行符/编码 |

> **共同点**：四个坑都不是「模型不够聪明」，而是**流程纪律**问题 —— 每一个都能靠 `git diff` + 人独立验证抓出来。
