# Codex Project Memory

**Codex Project Memory** is a Codex skill that gives one project a lightweight memory across multiple conversations. Each conversation can leave a short handoff, and the next conversation can read the project state first instead of rediscovering the whole repository from scratch.

**Codex 项目记忆** 是一个 Codex skill，用来加强同一个项目中不同对话之间的协作。每个对话结束时可以留下简短交接总结，新的对话开始时先读取项目状态，不必每次都重新扫描整个仓库。

## Why / 为什么

Codex is good at exploring code, but repeated exploration wastes time and context when several conversations work on the same project. This skill creates a small, structured memory folder inside each workspace:

Codex 很擅长读代码，但多个对话反复探索同一个项目会浪费时间和上下文。这个 skill 会在每个项目内创建一个轻量、结构化的记忆目录：

```text
.codex/project-memory/
  overview.md
  current-state.md
  decisions.md
  conversation-log/
```

## What It Does / 功能

- Reads project memory at the start of a task.
- Initializes memory files when a project does not have them yet.
- Appends timestamped handoff logs after meaningful work.
- Refreshes `current-state.md` so the next conversation has a clean starting point.
- Records durable decisions separately in `decisions.md`.

- 在任务开始时读取项目记忆。
- 项目还没有记忆时自动初始化相关文件。
- 在完成有意义的工作后追加带时间戳的交接日志。
- 自动刷新 `current-state.md`，让下个对话快速接手。
- 把长期有效的决策单独记录到 `decisions.md`。

## Installation / 安装

Clone this repository into your Codex skills directory:

把这个仓库克隆到 Codex 的 skills 目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/isclin123/codex-project-memory.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/project-memory-workflow"
```

Then start a new Codex conversation and invoke:

然后打开新的 Codex 对话并调用：

```text
Use $project-memory-workflow to continue this project.
```

中文也可以：

```text
用 $project-memory-workflow 继续这个项目，先读取项目记忆。
```

## Workflow / 工作流

At the beginning of a task, the skill runs:

任务开始时，skill 会运行：

```bash
python3 scripts/project_memory.py context --project-root "$PWD"
```

At the end of meaningful work, it writes a handoff:

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

## Files / 文件说明

- `SKILL.md`: Codex skill instructions.
- `scripts/project_memory.py`: deterministic helper for `init`, `context`, and `update`.
- `references/memory-format.md`: memory schema notes.
- `agents/openai.yaml`: Codex UI metadata.

- `SKILL.md`：Codex skill 的主说明。
- `scripts/project_memory.py`：负责 `init`、`context`、`update` 的确定性脚本。
- `references/memory-format.md`：项目记忆文件格式说明。
- `agents/openai.yaml`：Codex UI 元数据。

## Notes / 注意事项

This skill is intentionally lightweight. It does not replace reading code. It gives Codex a map before it starts, then Codex should still inspect the files that matter for the current task.

这个 skill 刻意保持轻量。它不是用来代替读代码，而是先给 Codex 一张地图；真正修改代码前，Codex 仍然应该检查和当前任务相关的文件。

Do not store secrets, tokens, private keys, or large pasted logs in project memory.

不要把密钥、token、私钥或大段日志放进项目记忆。
