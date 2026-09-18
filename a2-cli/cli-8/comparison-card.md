# CLI-8 · Portable Prompt 对照卡

同一份四字段 prompt（见 `portable-prompt.md`），在两个 CLI 上各跑一次，记录差异。

- demo repo：`E:\DSH\a1-demo`（干净起点 = commit `c3ca88c`）
- 执行日期：2026-09-18
- 模型：两轮都是 `qwen2.5:3b`（**故意保持一致**，这样"工具"是唯一变量）

---

## 一、对照表（教材指定的五个差异项 + 实测补充）

| 维度 | Aider（第一轮） | OpenCode（第二轮） |
|---|---|---|
| **CLI 版本** | v0.86.2 | 1.18.31 |
| **模型 / provider** | `ollama_chat/qwen2.5:3b` / Ollama 本地 | `qwen2.5:3b (local)`（TUI 状态栏：`▣ Build · qwen2.5:3b (local)`） |
| **project-instructions 文件名** | `AGENTS.md` —— ⚠️ **非原生**，靠 `.aider.conf.yml` 的 `read: [AGENTS.md]` 显式加载（启动打印 `Added AGENTS.md to the chat (read-only)`） | `AGENTS.md` —— ✅ **原生自动加载**，无需任何配置 |
| **Skill 位置** | ❌ **完全不支持** Skill 机制 | `.agents/skills/`（本轮任务未触发） |
| **shell / sandbox 权限** | ❌ **无运行时门禁**。约束是"配置 + 约定"：`--no-auto-commits` 禁自动提交；文件必须出现在 chat 里才可编辑（`Readonly: AGENTS.md` / `Editable: README.md`） | ✅ **运行时门禁**。动作发生前弹 `△ Permission required` → `Allow once`。来源：`opencode.json` 的 `permission: {edit: ask, bash: ask}` |
| **工具名称** | ❌ 无工具调用概念。编辑 = **编辑格式契约**：模型吐 diff → Aider 解析 → 写盘 | ✅ 真工具调用序列：`→Read README.md` → `←Edit README.md` → `←Write README.md` |
| **登录 / 费用** | 无需登录；本地 **$0** | 无需登录；本地 **$0** |
| **执行结果（git diff）** | ✅ 落盘，见 `evidence/aider-run1.patch` | ✅ 落盘，见 `evidence/opencode-run1.patch` |
| **有没有越界** | 无 | 无 |

---

## 二、成功条件并排判定

| 成功条件 | Aider | OpenCode |
|---|---|---|
| README.md 中出现"如何运行测试"章节 | ✅ | ✅ 但写成 **H1**，且追加在文末 |
| `git diff` 只显示这一处改动 | ✅ 单文件、单处 | ⚠️ 同一个 hunk 里**还删掉了 2 个空行** |
| 原有内容完好 | ⚠️ 第 3 行多了 **2 个尾随空格**（Markdown 硬换行） | ⚠️ 删了 `## 功能` / `## 文件` 后的空行；且**全文换行符 CRLF → LF** |
| （附加）`git diff --check` | ❌ `exit=2`：`README.md:3: trailing whitespace.` | ✅ `exit=0` |
| （附加）有没有自动 commit | ✅ 无，HEAD 仍在 `c3ca88c` | ✅ 无 |
| （附加）有没有碰 `data/` | ✅ 未动 | ✅ 未动 |
| （附加）有没有新增 / 删除文件 | ✅ 无 | ✅ 无（`docs/README.md` 也未动） |
| （附加）有没有跑验证命令 | ❌ 没跑 | ❓ 声称要跑（`Next, I will run the git diff...`），是否真跑见下 |

**结论：两个工具都"完成了任务"，但各自踩了不同的坑，没有一个是干净的。**

---

## 三、Aider 的坑

### 1. 尾随空格 —— 终端看不见，diff 看得见

Aider 打印的 diff 里有一对看起来完全一样的行：

```
-一个用于练习 CLI agent 的可丢弃小项目。
+一个用于练习 CLI agent 的可丢弃小项目。
```

当时误判为"模型吐了假改动"。实际 `git diff --check` 揭示：`+` 那行末尾多了 **2 个尾随空格**。
在 Markdown 里这是**硬换行**，渲染会变 —— 严格说"原有内容完好"不成立。

### 2. 没跑 AGENTS.md 要求的验证

`AGENTS.md` 的「验证」栏明确写了「修改文档或代码后，执行 `git diff --check` 确认没有空白错误」。
模型一次都没跑 —— 而它恰恰就是会失败的那个。

### 3. ⚠️ 时间陷阱（本次实验最大的操作教训）

在 `Add file to the chat?` 提示符**还挂着**的时候去 `git status`，会看到**干净的工作区**，从而误判"agent 什么都没做"。
实际上 **Aider 是在答完 `n`、会话继续之后才把编辑落盘的**。

> **教训**：判断 agent 有没有改文件，必须在**退出工具之后**再看 `git status`。中途看 = 看半成品。

---

## 四、OpenCode 的坑

### 1. 弱模型连工具参数都填不对

```
It seems that the string "{%include oldString%}" is not found in the file.
```

模型把工具 schema 里的**模板占位符 `{%include oldString%}` 原样当成内容**塞进了 `Edit`。

它**工具选对了**（定点修改确实该用 Edit），但**填不出合法参数**。
这是 CLI-6 那个 `Skill({name: ""})`（空参数）的升级版：**工具识别 ≠ 参数构造**。

### 2. 又一次退回 `Write` 整文件覆写

`Edit` 失败后，模型没有换参数重试，而是直接整文件覆写 —— 正是 CLI-7 里把两个 README 一起 wipe 掉的那个动作。

这次没 wipe 内容，但代价是**全文件级的副作用**：

| 测量项 | HEAD 原始 | OpenCode 写完 |
|---|---|---|
| CRLF 行数 | 12 | **0** |
| bare-LF 行数 | 0 | **15** |
| 字节数 | 258 | 301 |

```
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
```

`core.autocrlf=true` 把这层差异**盖住了** —— 如果这个仓库没有开 autocrlf，`git diff` 会显示**几乎每一行都改了**。

> **教训**：`Write`（整文件覆写）的破坏力不止"内容可能丢"，还包括**换行符、编码、文件末尾换行**这些看不见的东西。

### 3. 新章节写成 H1、位置在文末

```
## 文件
- `calculator.py` — 运算函数
- `test_calculator.py` — 单元测试

# 如何运行测试          ← H1，和文档主标题同级，把文档劈成两半
```

教材的成功条件写的是"出现'如何运行测试'**章节**" —— 字面满足，结构上错。

### 4. 自述内容与磁盘内容不符（跨文件混淆）

写入成功后，模型报告说：

> "The README.md file has been updated successfully. Here's the new content:
> Demo Calculator / 一个用于练习 CLI agent 的**可丢弃 Python 小项目** / - 提供四个基础运算函数 / - **测试使用 Python 标准库 unittest** / **用途** / ..."

这不是 README.md 的内容 —— 这是 **`AGENTS.md`** 的内容！
模型把"项目规则文件"和"要改的目标文件"**混在一起**了。

> **教训**：`AGENTS.md` 原生自动加载是有代价的 —— 弱模型会把规则文件的正文当成自己的产出复述。
> **永远以磁盘上的 `git diff` 为唯一事实。**

---

## 五、差异清单汇总（CLI-8 的核心产出）

| # | 差异维度 | Aider | OpenCode |
|---|---|---|---|
| 1 | project-instructions 文件名 | `AGENTS.md`（**要显式配置** `.aider.conf.yml` 的 `read:`） | `AGENTS.md`（**原生**） |
| 2 | Skill 位置 | ❌ 无 | `.agents/skills/` |
| 3 | shell / sandbox 权限 | 无门禁，靠命令行开关 + chat 文件白名单 | `permission: {edit: ask, bash: ask}` → 运行时弹窗 |
| 4 | 工具名称 | 无；编辑走"编辑格式契约" | `Read` / `Edit` / `Write` |
| 5 | 登录和费用 | 无需登录，$0 | 无需登录，$0 |
| 6 | **编辑实现方式** | 模型吐 diff 文本 → 工具解析 → 写盘 | 模型挑工具 → 传参数 → 工具执行 |
| 7 | **换行符处理** | 保持 CRLF | 整文件重写为 LF |
| 8 | **验证行为** | 完全没跑 | 声称要跑（待确认是否真跑） |

---

## 六、CLI-8 的最终结论

> 教材原话：「"Portable" 代表**核心意思容易迁移**，**不代表整段文字和设置可以零修改复制**。
> 如果第二个工具没有同名功能，就**回到成功条件，选择它真正支持的方法**。」

**实证结论：**

1. **四字段 prompt 一字不改，两个工具都跑通了** —— "任务核心"确实是 portable 的。
2. **但"设置"完全不 portable**：同一个编辑动作，Aider 要的是"编辑格式契约"（`--edit-format udiff`），OpenCode 要的是"权限授权"（`permission.edit: ask`）。**这两个开关在两个工具里根本不存在对应物。**
3. **同一个弱模型，在两个 harness 下暴露的短板不一样**：
   - Aider 下：能产出可用内容，但**输出契约（diff 围栏）**和**空白字符**不过关
   - OpenCode 下：能调对工具，但**参数构造**和**自述准确性**不过关
   - → **harness 会改变模型的行为表现**，不只是"换个壳"。
4. **两个工具都没做到"自我验证"**，而"验证"恰恰是四字段规则卡里最容易被忽略、也最值钱的一栏。
