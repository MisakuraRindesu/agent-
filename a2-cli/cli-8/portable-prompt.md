# CLI-8 · Portable Prompt（跨工具任务核心）

> **教材定义**：共用核心只写四个字段 —— **任务、范围、禁止事项、成功条件**。
> 这四个字段里**不带任何工具特有的设置**：不写编辑格式、不写权限开关、不写命令行参数、不写规则文件名。

---

## 一、四字段核心（两轮一字不改）

```text
任务：给 README.md 补一段"如何运行测试"的说明，命令为 python test_calculator.py
范围：只修改 README.md；不新增文件、不改其他文件
禁止事项：不要 git commit、不要 git push、不要碰 data/ 目录
成功条件：README.md 中出现"如何运行测试"章节；git diff 只显示这一处改动；原有内容完好
```

## 二、每个工具各自要补的部分（**这部分不 portable**）

教材原话：「"Portable" 代表**核心意思容易迁移**，不代表整段文字和设置可以零修改复制。」

| 工具特有的东西 | Aider | OpenCode |
|---|---|---|
| 怎么限定"只能改这个文件" | 命令行末尾带上 `README.md`；只有出现在 chat 里的文件才可编辑 | 待测 |
| 模型输出要符合什么格式 | `--edit-format udiff`（模型必须吐 `\`\`\`diff` 围栏块） | 无此开关，agent 自己调用工具 |
| 怎么禁用自动提交 | `--no-auto-commits` | 待测（`permission: {edit: ask, bash: ask}`） |
| 项目规则怎么被读到 | `.aider.conf.yml` 里 `read: [AGENTS.md]`，显式加载 | 待测（原生读 `AGENTS.md`？） |
| 怎么避免被追问"要不要加入这个文件" | 答 `n` | 待测 |

## 三、两轮共用的环境前置条件

```powershell
$env:NO_PROXY = "localhost,127.0.0.1,::1"   # 关掉 Python 对 Windows 注册表代理的读取
$env:OLLAMA_API_BASE = "http://127.0.0.1:11434"
```

> 为什么需要：`httpx` 通过 `urllib.request.getproxies()` 读 Windows 注册表代理，但**拿不到绕过列表**，
> 于是把 `http://localhost:11434/...` 也丢给系统代理（Clash @ 127.0.0.1:7890），拿到 **502 Bad Gateway**。
> 详见 `../../learning-log.md` 的「CLI-8 环境排查」一节。

## 四、执行纪律（教材指定）

1. 在第一个 CLI 的**干净** demo repo 中跑一次，记录 CLI 版本、模型/provider、权限设置和 `git diff`。
2. **恢复后**再换第二个 CLI。
3. 不要让两个会写文件的 session **同时**操作同一个目录。
