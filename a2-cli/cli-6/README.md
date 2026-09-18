# CLI-6 · 把重复 review 做成 Skill

[← 返回 A2 手册](../README.md)

---

## 一、教材成果（原文）

> **成果：** 你能让 agent 执行同一套只读 review，输出 `PASS` 或具体问题，不会自己 commit、push 或部署。
>
> Claude Code 使用 `.claude/skills/review-changes/SKILL.md`；Codex、Gemini CLI、OpenCode 可以使用 `.agents/skills/review-changes/SKILL.md`。

## 二、教材步骤（原文）

> 1. 先完整读完 `SKILL.md`，确认没有下载陌生程序、读取秘密或改变外部系统的步骤。
> 2. 在 demo repo 做一个小文档改动，但不要 commit。请 agent「review my local changes」，观察它是否找到 Skill；也可以按照工具文档手动启用。
> 3. 对照 `git diff` 检查回报。测试后执行 `git status --short`，确认 Skill 没有偷偷改文件。
> 4. 想在多个 CLI 共用时，先共用上面的核心内容，再根据每个工具调整文件夹、权限和工具专属 frontmatter。未知字段可能会被忽略，不要假设每个设置在所有地方都有效。

## 三、产物

**Skill 文件（快照）** —— 现行文件在 [`../../a1-cli-agent/.agents/skills/review-changes/SKILL.md`](../../a1-cli-agent/.agents/skills/review-changes/SKILL.md)：

```markdown
---
name: review-changes
description: Review the current git diff and report concrete risks. Use when the user asks to review local changes.
---

1. Read `git diff --no-ext-diff HEAD` without changing files.
2. Check for secrets, unsafe commands, broken links, and missing verification.
3. Report `PASS` when no problem is found; otherwise list each problem with its file and reason.
4. Do not edit, commit, push, deploy, or send messages.
```

**目录位置**：

```text
a1-cli-agent/
└── .agents/
    └── skills/
        └── review-changes/
            └── SKILL.md
```

## 四、OpenCode Skill 机制要点（官方文档核对）

- **搜索位置**：`.opencode/skills/`、`.claude/skills/`、`.agents/skills/`（项目级）+ 对应全局目录
- **frontmatter 只识别**：`name`（必需）、`description`（必需，≤1024 字符）、`license`、`compatibility`、`metadata`
- **`name` 必须与目录名一致**，且符合 `^[a-z0-9]+(-[a-z0-9]+)*$`
- **按需加载**：skill 列表出现在 `skill` 工具的 description 里，agent 需要时调用 `skill({ name: "..." })`
- **权限**：`"permission": { "skill": { "*": "allow", "internal-*": "deny" } }`

> ⚠️ **Aider 完全没有 Skill 机制** —— 这是 CLI-8 对照卡里的一行硬差异。

## 五、实测结果（能力边界）

| 环节 | `qwen2.5:3b` 表现 |
|---|---|
| Skill 被发现 | ✅ |
| **自动选择该用哪张 Skill** | ❌ 发起 `Skill ""`（**空参数**） |
| 显式指定名称后加载 | ✅ `Skill "review-changes"` |
| **按 Skill 步骤选对工具** | ❌ 把 `git diff --no-ext-diff HEAD` 当成**文件名**，陷入 `Read git_diff.txt` 死循环 |
| **明确指定「用 Bash 执行」后** | ✅ 成功执行，并报出假密钥 `sk-test-…` 与危险命令 `rm -rf` |
| 严格遵循输出格式 | ⚠️ 同时输出 `PASS` 和问题清单（逻辑矛盾） |

> **关键结论：Skill 失败的瓶颈不是「分析能力」，而是「工具选择能力」。**
> 同一个 diff，模型能发现密钥和危险命令；但它无法从自然语言步骤推断出「这一步该用 Bash 而不是 Read」。
> **Skill 是给「指令遵循能力足够强」的模型设计的机制。**

## 六、自查清单

- [x] 完整读过 `SKILL.md`，确认没有下载程序 / 读秘密 / 改外部系统的步骤
- [x] 文件放在工具认得的位置（`.agents/skills/review-changes/SKILL.md`）
- [x] frontmatter 的 `name` 与目录名一致，且匹配 `^[a-z0-9]+(-[a-z0-9]+)*$`
- [x] 在 demo repo 做了未提交的小改动，请 agent review
- [x] 对照 `git diff` 检查过它的回报
- [x] 测试后 `git status --short` 确认 **Skill 没有偷偷改文件** ✅（只读确实是只读）
- [x] 知道 Skill 正文里明确写出工具名（如「用 Bash 执行」）能显著提升弱模型成功率
