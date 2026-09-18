---
name: review-changes
description: Review the current git diff and report concrete risks. Use when the user asks to review local changes.
---

1. Read `git diff --no-ext-diff HEAD` without changing files.
2. Check for secrets, unsafe commands, broken links, and missing verification.
3. Report `PASS` when no problem is found; otherwise list each problem with its file and reason.
4. Do not edit, commit, push, deploy, or send messages.