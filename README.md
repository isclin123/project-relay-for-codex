# Project Relay for Codex

[English](#english) | [中文](#中文)

## English

**Project Relay for Codex** is a lightweight handoff workflow for AI coding projects. It helps Codex and Claude Code carry project state across separate conversations by writing short, structured relay notes inside each workspace.

## Why

AI coding agents are good at exploring code, but repeated exploration wastes time and context when several conversations work on the same project. Project Relay creates a small memory folder inside each workspace:

```text
.codex/project-memory/
  overview.md
  current-state.md
  decisions.md
  conversation-log/
```

## What It Does

- Reads project memory at the start of a task.
- Initializes memory files when a project does not have them yet.
- Appends timestamped handoff logs after meaningful work.
- Refreshes `current-state.md` so the next conversation has a clean starting point.
- Records durable decisions separately in `decisions.md`.
- Works as a Codex skill and as a Claude Code skill.

## Install for Codex

Clone this repository into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/isclin123/project-relay-for-codex.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/project-relay"
```

Then start a new Codex conversation and invoke:

```text
Use $project-relay to continue this project.
```

## Install for Claude Code

Claude Code supports skills with a `SKILL.md` entrypoint. Install Project Relay as a personal Claude Code skill:

```bash
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/isclin123/project-relay-for-codex.git \
  "$HOME/.claude/skills/project-relay"
```

Then invoke it inside Claude Code:

```text
/project-relay
```

Or ask naturally:

```text
Use project relay to read the project memory before continuing.
```

For a project-local Claude Code install, copy this repository into:

```text
<your-project>/.claude/skills/project-relay/
```

## Workflow

At the beginning of a task, the skill runs:

```bash
python3 scripts/project_memory.py context --project-root "$PWD"
```

At the end of meaningful work, it writes a handoff:

```bash
python3 scripts/project_memory.py update \
  --project-root "$PWD" \
  --title "Add OAuth callback handling" \
  --project-summary "Next.js app for internal account management." \
  --work-summary "Implemented callback route, token exchange helper, and failure states." \
  --files-changed "app/auth/callback/route.ts" \
  --files-changed "lib/auth/oauth.ts" \
  --decision "Keep token exchange server-side to avoid exposing client secrets." \
  --validation "npm test -- auth passed" \
  --open-thread "Add integration coverage for expired authorization codes."
```

## Files

- `SKILL.md`: skill instructions for Codex and Claude Code.
- `scripts/project_memory.py`: deterministic helper for `init`, `context`, and `update`.
- `references/memory-format.md`: memory schema notes.
- `agents/openai.yaml`: Codex UI metadata.

## Notes

Project Relay is intentionally lightweight. It does not replace reading code. It gives the agent a map before it starts, then the agent should still inspect the files that matter for the current task.

Do not store secrets, tokens, private keys, or large pasted logs in project memory.

---

## 中文

**Project Relay for Codex** 是一个面向 AI 编程项目的轻量交接工作流。它可以让 Codex 和 Claude Code 在不同对话之间延续项目状态：每次完成工作后写入简短、结构化的接力记录，下次对话先读取这些记录再开始工作。

## 为什么

AI 编程助手很擅长读代码，但多个对话反复探索同一个项目会浪费时间和上下文。Project Relay 会在每个项目内创建一个轻量的记忆目录：

```text
.codex/project-memory/
  overview.md
  current-state.md
  decisions.md
  conversation-log/
```

## 功能

- 在任务开始时读取项目记忆。
- 项目还没有记忆时自动初始化相关文件。
- 在完成有意义的工作后追加带时间戳的交接日志。
- 自动刷新 `current-state.md`，让下个对话快速接手。
- 把长期有效的决策单独记录到 `decisions.md`。
- 同时支持 Codex skill 和 Claude Code skill。

## Codex 安装

把这个仓库克隆到 Codex 的 skills 目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/isclin123/project-relay-for-codex.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/project-relay"
```

然后打开新的 Codex 对话并调用：

```text
用 $project-relay 继续这个项目，先读取项目记忆。
```

## Claude Code 安装

Claude Code 支持以 `SKILL.md` 为入口的 skills。可以把 Project Relay 安装成个人 Claude Code skill：

```bash
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/isclin123/project-relay-for-codex.git \
  "$HOME/.claude/skills/project-relay"
```

然后在 Claude Code 里调用：

```text
/project-relay
```

也可以自然语言触发：

```text
Use project relay to read the project memory before continuing.
```

如果想作为某个项目专用的 Claude Code skill，可以复制到：

```text
<your-project>/.claude/skills/project-relay/
```

## 工作流

任务开始时，skill 会运行：

```bash
python3 scripts/project_memory.py context --project-root "$PWD"
```

完成有意义的工作后，它会写入交接总结：

```bash
python3 scripts/project_memory.py update \
  --project-root "$PWD" \
  --title "Add OAuth callback handling" \
  --project-summary "Next.js app for internal account management." \
  --work-summary "Implemented callback route, token exchange helper, and failure states." \
  --files-changed "app/auth/callback/route.ts" \
  --files-changed "lib/auth/oauth.ts" \
  --decision "Keep token exchange server-side to avoid exposing client secrets." \
  --validation "npm test -- auth passed" \
  --open-thread "Add integration coverage for expired authorization codes."
```

## 文件说明

- `SKILL.md`：Codex 和 Claude Code 的 skill 主说明。
- `scripts/project_memory.py`：负责 `init`、`context`、`update` 的确定性脚本。
- `references/memory-format.md`：项目记忆文件格式说明。
- `agents/openai.yaml`：Codex UI 元数据。

## 注意事项

Project Relay 刻意保持轻量。它不是用来代替读代码，而是先给 AI 编程助手一张地图；真正修改代码前，仍然应该检查和当前任务相关的文件。

不要把密钥、token、私钥或大段日志放进项目记忆。
