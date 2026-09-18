# CLI-8 · 做一张 portable prompt 对照卡

[← 返回 A2 手册](../README.md)

---

## 一、教材成果（原文）

> **成果：** 你能保留同一个任务核心，并清楚标出换工具时要修改的文件名、权限、命令和启用方式。

## 二、教材步骤（原文）

> 1. 共用核心只写四个字段：**任务、范围、禁止事项、成功条件**。
> 2. 在第一个 CLI 的干净 demo repo 中运行一次，记录 CLI 版本、模型/provider、权限设置和 `git diff`。
> 3. 恢复后再换第二个 CLI。不要让两个会写文件的 session 同时操作同一个目录。
> 4. 另外记下差异：**project-instructions 文件名、Skill 位置、shell/sandbox 权限、工具名称、登录和费用**。
>
> 「Portable」代表核心意思容易迁移，不代表整段文字和设置可以零修改复制。如果第二个工具没有同名功能，就回到成功条件，选择它真正支持的方法。

## 三、本目录的产物

| 文件 | 内容 |
|---|---|
| [`portable-prompt.md`](portable-prompt.md) | 四字段任务核心 +「哪些东西不 portable」逐项对照 |
| [`comparison-card.md`](comparison-card.md) | 跨工具对照表 + 两轮成功条件逐条判定 + 差异清单汇总 |
| [`evidence/aider-run1.patch`](evidence/aider-run1.patch) | Aider 的 `git diff` 原始证据 |
| [`evidence/opencode-run1.patch`](evidence/opencode-run1.patch) | OpenCode 的 `git diff` 原始证据 |
| [`proxy-probe.py`](proxy-probe.py) | 代理劫持诊断脚本（见下方「环境坑」） |

## 四、我们的操作

**四字段核心（两轮一字不改）**

```text
任务：给 README.md 补一段"如何运行测试"的说明，命令为 python test_calculator.py
范围：只修改 README.md；不新增文件、不改其他文件
禁止事项：不要 git commit、不要 git push、不要碰 data/ 目录
成功条件：README.md 中出现"如何运行测试"章节；git diff 只显示这一处改动；原有内容完好
```

**实验设计**：两轮都用同一个模型 `qwen2.5:3b` —— 这样**「工具」是唯一变量**。

| 轮次 | 工具 | 启动命令 |
|---|---|---|
| 第 1 轮 | Aider 0.86.2 | `aider --model ollama_chat/qwen2.5:3b --edit-format udiff --no-auto-commits --no-show-model-warnings README.md` |
| 第 2 轮 | OpenCode 1.18.31 | `opencode`（配置见 `a1-cli-agent/opencode.json`） |

两轮之间执行 `git restore -- README.md` 恢复到干净起点。

## 五、结果速览

| 成功条件 | Aider | OpenCode |
|---|---|---|
| 出现「如何运行测试」章节 | ✅ | ✅ 但写成 **H1**，且追加在文末 |
| `git diff` 只显示这一处改动 | ✅ 单文件单处 | ⚠️ 同一 hunk 里**还删掉了 2 个空行** |
| 原有内容完好 | ⚠️ 第 3 行多了 **2 个尾随空格** | ⚠️ 少了 2 个空行 + **全文换行符 CRLF→LF** |
| `git diff --check` | ❌ `exit=2` | ✅ `exit=0` |
| 未 commit / 未碰 `data/` / 无新增文件 | ✅ ✅ ✅ | ✅ ✅ ✅ |
| **真的跑了验证命令** | ❌ 完全没跑 | ❌ 声称要跑，**Bash 审批根本没弹 = 从未调用 Bash** |

> 结论：**两个工具都「完成了任务」，但没有一个是干净的。**

## 六、这次撞到的坑

### 1. ⚠️ 环境坑：Windows 系统代理劫持本地请求（502 Bad Gateway）

第一轮 Aider 直接起不来：

```
OllamaError: Error getting model info for gemma4:e4b.
Error: Server error '502 Bad Gateway' for url 'http://localhost:11434/api/show'
```

排查结论（三层客户端对照）：

| 客户端 | 读注册表代理? | 有绕过列表? | 结果 |
|---|---|---|---|
| `curl.exe` | ❌ 不读 | — | 直连 **200** ✅ |
| Python `requests` | ✅ 读 | ✅ 认 `ProxyOverride` 里的 `localhost;127.*` | **200** ✅ |
| **Python `httpx`** | ✅ 读（`urllib.request.getproxies()`） | ❌ **拿不到绕过列表** | 丢给 Clash:7890 → **502** ❌ |

**Aider 的 Ollama 客户端和 litellm 都走 httpx**，所以只有它中招。

```powershell
# 修复（只影响当前窗口）
$env:NO_PROXY = "localhost,127.0.0.1,::1"
$env:OLLAMA_API_BASE = "http://127.0.0.1:11434"
```

> 原理：`urllib.request.getproxies()` = `getproxies_environment() or getproxies_registry()`
> —— 设了 `NO_PROXY` 就短路，注册表代理整个被忽略。

### 2. ⚠️ 操作坑：判断 agent 改没改文件，要看**退出之后**的 `git status`

第一轮中途我查 `git status` 是**干净的**，于是误判「Aider 什么都没做」。
实际上 **Aider 是在答完 `Add file to the chat?` 提示符、会话继续之后才落盘的**。

> **中途看 = 看半成品。必须退出工具之后再看。**

### 3. Aider 侧：终端看不见的尾随空格

它打印的 diff 里有一对看起来一模一样的行：

```
-一个用于练习 CLI agent 的可丢弃小项目。
+一个用于练习 CLI agent 的可丢弃小项目。
```

真相：`+` 行末尾多了 **2 个空格**（Markdown 硬换行，渲染会变）。`git diff --check` 才揭示出来。

### 4. OpenCode 侧：工具选对了，参数填不出来

```
It seems that the string "{%include oldString%}" is not found in the file.
```

模型把工具 schema 里的**模板占位符**原样当成内容传给了 `Edit`，失败后**退回 `Write` 整文件覆写** → 换行符全改 + 空行丢失。

### 5. OpenCode 侧：自述内容和磁盘内容不是一回事

写完它报告说「Here's the new content: … **用途** … 测试使用 Python 标准库 unittest」——
那是 **`AGENTS.md`** 的正文，不是 README.md。**原生自动加载规则文件后，弱模型把两个文件混了。**

## 七、自查清单

- [x] 共用核心只写四个字段（任务 / 范围 / 禁止事项 / 成功条件）
- [x] 在**干净的** demo repo 里跑第一轮
- [x] 记录了 CLI 版本、模型/provider、权限设置和 `git diff`
- [x] 换工具前 `git restore` 恢复
- [x] 没有让两个会写文件的 session 同时操作同一个目录
- [x] 记下五项差异：project-instructions 文件名 / Skill 位置 / shell 权限 / 工具名称 / 登录与费用
- [x] 想清楚「如果第二个工具没有同名功能，回到成功条件，选它真正支持的方法」
