# awesome-agentic-ai-zh 学习记录

> 跟随 [WenyuChiou/awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh) 学习 AI Agent 的过程记录:
> 每个阶段的动手练习、踩过的坑、实测数据与结论。
>
> **学习路线**:Track A — CLI Power User(本地 Ollama 零费用路径)
> **学习版本**:简体中文(`*.zh-Hans.md`)

---

## 📍 当前进度

| 阶段 | 内容 | 状态 |
|---|---|---|
| **Stage 0** | 基础准备(Python / API / JSON / Git / CLI) | ✅ |
| **Stage 1** | LLM 基础(token / context window / temperature / 成本与延迟) | ✅ |
| **Stage 2** | Prompt 设计(四部分 Prompt / Few-Shot / Eval 驱动迭代) | ✅ |
| **A1 · CLI-1** | CLI Agent 实操:读取 → 计划 → 编辑 → `git diff` → 撤销 | ✅ |
| **A1 · CLI-2** | 项目规则文件与边界守护(`AGENTS.md` + 三组对照实验) | ✅ |
| **A1 · CLI-3** | 第二个 harness 公平对比(Aider vs OpenCode) | ✅ |
| **A1 · CLI-4** | 推送通道排查(实战替代):HTTPS 被阻断 → SSH 可用 → 推送成功 | ✅ |
| **A2 · CLI-5** | 四字段规则卡(用途 / 不可做 / 验证 / 回报) | ✅ |
| **A2 · CLI-6** | 只读 review Skill(`.agents/skills/review-changes/`) | ✅ |
| **A2 · CLI-7** | 任务拆解(盘点 → 修改 → 验证 → 回报) | ✅ |
| **A2 · CLI-8** | portable prompt 对照卡 | ⬜ 可选 |
| **Stage 5** | Claude Code 生态:MCP / Skills / Plugins / Hooks / Subagents | ⬜ 下一站 |

> 📖 **完整学习总结见 [`learning-log.md`](learning-log.md)** —— 包含每个 bug 的现象 / 原因 / 解决 / 教训,以及 12 条核心教训与可复用工具箱。

---

## 📂 目录结构

```text
.
├── README.md                       # 本文件：进度总览
├── learning-log.md                 # 完整学习总结（12 条核心教训 + 工具速查）
├── stage0-foundations/             # Stage 0：GitHub API 数据小工具
│   ├── github-profile.py
│   └── result.txt
├── stage1-llm-basics/              # Stage 1：本地 LLM 调用实测
│   ├── practice_1.py               #   一个工具、一次调用 + usage 读取
│   ├── practice_2.py               #   中英文 token 差异 + temperature 影响
│   └── practice_3.py               #   延迟 / tokens-per-second / 成本估算
├── stage2-prompt-engineering/      # Stage 2：Prompt 设计与 Eval 迭代
│   ├── practice_2_1.py             #   模糊 vs 四部分 Prompt 对比
│   ├── practice_2_2.py             #   Zero-Shot vs Few-Shot（六题评分）
│   ├── practice_2_3.py             #   边界题 + Iterative Refinement
│   └── practice_2_4.py             #   多轮统计版（3 轮平均分对比）
└── a1-cli-agent/                   # A1 / A2：CLI Agent 实操的演示仓库
    ├── AGENTS.md                   #   项目规则（四字段：用途/不可做/验证/回报）
    ├── .aider.conf.yml             #   让 Aider 自动加载 AGENTS.md
    ├── opencode.json               #   OpenCode 配置（Ollama provider + 权限）
    ├── .agents/skills/review-changes/SKILL.md   # A2：只读 review Skill
    ├── calculator.py               #   被测代码
    ├── test_calculator.py          #   单元测试
    ├── data/                       #   受保护目录（禁止 agent 修改）
    └── experiments/                #   Aider 会话原始记录
```

---

## 🔬 实测数据摘要

### Stage 1 — 本地 LLM 的真实数字

| 指标 | 实测值 |
|---|---|
| 单次调用 usage | `prompt_tokens=22` / `completion_tokens=353`(推理模型,含"思考") |
| 延迟 | min 7.95s / max 12.18s / **mean 9.67s** |
| 生成速度 | **67 tokens/sec** |
| 1000 次本地运行 | **$0,但需 161 分钟** |
| 同规模云端估算 | 约 **$0.003262/次**(按 Haiku $1/$5 与实测 token 计) |

**中英文 token 对比**(同一语义):中文 25 tokens vs 英文 26 tokens —— **几乎相同,不能靠字数猜 token**。

### Stage 2 — Eval 驱动的 Prompt 改进

| 版本 | 三轮分数 | 平均 |
|---|---|---|
| 基线 Prompt | [5, 5, 5] | **5.00 / 6** |
| 加"边界规则"后 | [6, 6, 6] | **6.00 / 6** |

### A1 — 规则文件与权限门的三组实验

| # | 规则措辞 | 权限提示 | 模型行为 | 结果 |
|---|---|---|---|---|
| 2a | 基础("不要修改 `data/`") | 批准 | ❌「由于您明确要求,我将执行」 | **数据被破坏** |
| 2b | 强化(优先级 + 拒绝话术) | 拒绝 | ✅ 引用规则拒绝 | 零破坏 |
| 3 | 强化(同上) | **批准** | ✅ **仍然拒绝** | 零破坏 |

---

## 💡 核心结论(摘自学习总结)

1. **`max_tokens` 是预算上限,不是输出长度**;推理模型的"思考"会吃掉大部分预算。
2. **Token 不能按字数估**;`temperature` 是真实的"稳定性旋钮"(实测输出长度可差 32 倍)。
3. **Eval 要同一组题 + 多次运行**;而且 **Eval 代码自身也要被验证**(评分器 bug 会伪造出满分)。
4. **不信 agent 的自述,只信 `git diff`**;机制(只读、权限门、版本控制)> 自觉。
5. **垃圾进,垃圾出**:每一步都要验证"我交给 agent 的,是不是我以为的那个"。
6. **agent 不会说"这活不用干"**:"什么都不做"必须由人或指令明确给出。
7. **规则文件的效果取决于措辞**:优先级声明 + 堵住例外 + 固定拒绝话术,三者缺一不可。
8. **规则管"想不想做",权限门管"能不能做"**;权限门与 git 才是硬边界。
9. **"能复述规则" ≠ "会遵守规则"**:知道与做到之间隔着"指令遵循能力"。
10. **默认参数是隐藏的坑**:Ollama `num_ctx` 默认 4096,而模型支持 131072 —— 上下文不够时,模型会"看不见"你的指令。
11. **零费用本地栈的瓶颈是硬件**:6GB 显存跑不动"8B 多模态模型 + 32K 上下文"。

---

## 🖥 实验环境

| 项 | 配置 |
|---|---|
| 系统 | Windows + PowerShell |
| Python | 3.13 |
| 本地推理 | Ollama 0.33.2(`gemma4:e4b` / `qwen2.5:3b`) |
| GPU | NVIDIA RTX 3060 Laptop(6 GB 显存) |
| CLI Agent | Aider 0.86.2 / OpenCode 1.18.31 |
| API 费用 | **全程 $0**(纯本地模型) |

---

## 🔗 相关链接

- 学习地图原项目:[WenyuChiou/awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh)
- 在线文档站:[wenyuchiou.github.io/awesome-agentic-ai-zh](https://wenyuchiou.github.io/awesome-agentic-ai-zh/)

---

## ⚠️ 说明

- 本仓库是**个人学习记录**,不是教程;代码为练习产物,可能包含刻意保留的"错误示范"。
- 所有实验均在**可丢弃的 demo 仓库**中进行,并全程使用 git 作为安全网。
- 未包含任何 API key / 凭据;`opencode.json` 中的 `apiKey: "ollama"` 是本地 Ollama 的占位值。
