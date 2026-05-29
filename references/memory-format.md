# Project Memory File Format

Project memory lives in `.codex/project-memory/` inside each repository.

## Files

- `overview.md`: stable project purpose, architecture, commands, and important files.
- `current-state.md`: latest handoff state, refreshed by `scripts/project_memory.py update`.
- `decisions.md`: dated durable decisions appended over time.
- `conversation-log/*.md`: timestamped per-conversation handoff logs.

## Log Shape

Each log should include:

- Work summary
- Files changed
- Decisions
- Validation
- Open threads
- Next steps

## Editing Rules

Keep entries concise and factual. Remove stale TODOs from `overview.md` once the project is understood. Prefer adding corrections to rewriting history, unless fixing an obvious factual error.
