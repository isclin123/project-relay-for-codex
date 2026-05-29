#!/usr/bin/env python3
"""Project memory helper for cross-chat Codex handoffs."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path


MEMORY_DIR = Path(".codex") / "project-memory"


def now_stamp() -> str:
    return dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug[:48] or "handoff"


def project_root(args: argparse.Namespace) -> Path:
    return Path(args.project_root).expanduser().resolve()


def memory_root(root: Path) -> Path:
    return root / MEMORY_DIR


def ensure_memory(root: Path) -> Path:
    mem = memory_root(root)
    (mem / "conversation-log").mkdir(parents=True, exist_ok=True)

    files = {
        "overview.md": """# Project Overview

## Purpose
TODO: Summarize what this project is for.

## Architecture
TODO: Note the main technologies, folders, and entry points.

## Common Commands
TODO: Add build, test, lint, and run commands as they become known.

## Important Files
TODO: Add stable file landmarks future conversations should know.
""",
        "current-state.md": """# Current State

No project handoff has been written yet.
""",
        "decisions.md": """# Decisions

Record durable project, product, and architecture decisions here.
""",
    }

    for name, content in files.items():
        path = mem / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")
    return mem


def read_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def recent_logs(mem: Path, limit: int) -> list[Path]:
    logs = sorted((mem / "conversation-log").glob("*.md"), reverse=True)
    return logs[:limit]


def cmd_init(args: argparse.Namespace) -> int:
    root = project_root(args)
    mem = ensure_memory(root)
    print(f"Project memory initialized at {mem}")
    return 0


def cmd_context(args: argparse.Namespace) -> int:
    root = project_root(args)
    mem = ensure_memory(root)

    sections = [
        ("overview.md", read_if_exists(mem / "overview.md")),
        ("current-state.md", read_if_exists(mem / "current-state.md")),
        ("decisions.md", read_if_exists(mem / "decisions.md")),
    ]

    print(f"# Project Memory Context\n\nRoot: {root}\nMemory: {mem}\n")
    for name, text in sections:
        print(f"\n--- {name} ---\n")
        print(text or "(empty)")

    logs = recent_logs(mem, args.logs)
    print(f"\n--- recent conversation logs ({len(logs)}) ---\n")
    for log in logs:
        print(f"\n### {log.name}\n")
        print(read_if_exists(log) or "(empty)")
    return 0


def bullet_list(items: list[str]) -> str:
    cleaned = [item.strip() for item in items if item and item.strip()]
    if not cleaned:
        return "- None recorded."
    return "\n".join(f"- {item}" for item in cleaned)


def append_decisions(mem: Path, decisions: list[str]) -> None:
    cleaned = [decision.strip() for decision in decisions if decision.strip()]
    if not cleaned:
        return
    path = mem / "decisions.md"
    with path.open("a", encoding="utf-8") as f:
        f.write(f"\n\n## {now_stamp()}\n")
        for decision in cleaned:
            f.write(f"- {decision}\n")


def update_overview(mem: Path, project_summary: str | None) -> None:
    if not project_summary:
        return
    path = mem / "overview.md"
    current = read_if_exists(path)
    if "TODO: Summarize what this project is for." in current:
        current = current.replace("TODO: Summarize what this project is for.", project_summary.strip())
    else:
        current += f"\n\n## Latest Project Summary\n{project_summary.strip()}\n"
    path.write_text(current.rstrip() + "\n", encoding="utf-8")


def cmd_update(args: argparse.Namespace) -> int:
    root = project_root(args)
    mem = ensure_memory(root)
    stamp = now_stamp()
    slug = slugify(args.title)
    log_name = f"{dt.datetime.now().astimezone().strftime('%Y%m%d-%H%M%S')}-{slug}.md"
    log_path = mem / "conversation-log" / log_name

    update_overview(mem, args.project_summary)
    append_decisions(mem, args.decision)

    log = f"""# {args.title}

Date: {stamp}

## Work Summary
{args.work_summary.strip()}

## Files Changed
{bullet_list(args.files_changed)}

## Decisions
{bullet_list(args.decision)}

## Validation
{bullet_list(args.validation)}

## Open Threads
{bullet_list(args.open_thread)}

## Next Steps
{bullet_list(args.next_step)}
"""
    log_path.write_text(log, encoding="utf-8")

    state = f"""# Current State

Last updated: {stamp}

## Latest Work
{args.work_summary.strip()}

## Files Changed Recently
{bullet_list(args.files_changed)}

## Validation
{bullet_list(args.validation)}

## Open Threads
{bullet_list(args.open_thread)}

## Suggested Next Steps
{bullet_list(args.next_step)}

## Latest Log
`{log_path.relative_to(root)}`
"""
    (mem / "current-state.md").write_text(state, encoding="utf-8")
    print(f"Wrote handoff log: {log_path}")
    print(f"Updated current state: {mem / 'current-state.md'}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maintain .codex/project-memory handoff files.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create project memory files.")
    init.add_argument("--project-root", default=".")
    init.set_defaults(func=cmd_init)

    context = sub.add_parser("context", help="Print project memory context.")
    context.add_argument("--project-root", default=".")
    context.add_argument("--logs", type=int, default=3, help="Number of recent logs to include.")
    context.set_defaults(func=cmd_context)

    update = sub.add_parser("update", help="Append a handoff log and refresh current state.")
    update.add_argument("--project-root", default=".")
    update.add_argument("--title", required=True)
    update.add_argument("--project-summary")
    update.add_argument("--work-summary", required=True)
    update.add_argument("--files-changed", action="append", default=[])
    update.add_argument("--decision", action="append", default=[])
    update.add_argument("--validation", action="append", default=[])
    update.add_argument("--open-thread", action="append", default=[])
    update.add_argument("--next-step", action="append", default=[])
    update.set_defaults(func=cmd_update)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
