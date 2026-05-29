---
name: project-memory-workflow
description: Maintain lightweight cross-chat project memory for Codex workspaces. Use when starting work in an existing project, continuing work from another Codex conversation, finishing a task that should leave a handoff, initializing project memory, updating project summaries/decisions, or when the user says things like "read project memory", "update project memory", "write a handoff", "continue from last conversation", "跨对话", "项目记忆", or "交接总结".
---

# Project Memory Workflow

## Overview

Use this workflow to share concise project state across Codex conversations without rereading the entire repository every time. Store memory inside the project at `.codex/project-memory/`, then read that memory first and update it at the end of meaningful work.

## Core Workflow

1. At the start of a project task, run the bundled `scripts/project_memory.py context` command from the project root and read its output before broad repo exploration.
2. If memory does not exist yet, run `scripts/project_memory.py init`, then inspect the repository just enough to write a first useful `overview.md`.
3. During the task, keep normal notes mentally: changed files, decisions, validation, open questions, and useful next steps.
4. Before finishing the turn, run `scripts/project_memory.py update` with a concise handoff. Do this for completed implementation, debugging, research, architecture, planning, or review work that future conversations would benefit from.
5. If the task was tiny and created no durable project knowledge, skip the update unless the user explicitly asked to write memory.

## Script Usage

Resolve the skill directory, then call the script with Python:

```bash
python3 /path/to/project-memory-workflow/scripts/project_memory.py context --project-root "$PWD"
```

Useful commands:

- `init`: create `.codex/project-memory/` and template memory files.
- `context`: print `overview.md`, `current-state.md`, `decisions.md`, and recent conversation logs.
- `update`: append a timestamped conversation log and refresh `current-state.md`.

Example update:

```bash
python3 /path/to/project-memory-workflow/scripts/project_memory.py update \
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

## Memory Quality Rules

Keep memory short, factual, and useful for handoff. Prefer durable project facts over transcript summaries.

- `overview.md`: stable project purpose, architecture, commands, and important entry points.
- `current-state.md`: latest useful state and what a new conversation should know first.
- `decisions.md`: architecture/product decisions with dates and reasons.
- `conversation-log/*.md`: one short log per meaningful conversation.

Do not store secrets, access tokens, private keys, or large pasted outputs. Do not rewrite memory to hide uncertainty; record unclear items as open threads.

## When Reading Memory

Use memory as a map, not as proof. After reading memory, inspect only the files needed for the current task or to verify claims that affect code changes.

If memory conflicts with the repository, trust the repository and update memory at the end with the correction.

## Resources

- Use `scripts/project_memory.py` for deterministic memory file creation and updates.
- Read `references/memory-format.md` only when changing the memory schema or writing custom tooling around these files.
