# Contributing to DevQuest

## Setup

```bash
git clone <repo-url>
cd devquest
python -m venv venv
source venv/bin/activate
pip install -e .
```

## Testing

Run manual scenarios in the playground:

```bash
cd /Users/pedromoraes/anything/devquest-playground
hero init
hero status
hero commit
hero push
```

Test edge cases in isolated `/tmp` folders (no git, no remote, clean repo).

## Principles

Read [vision.md](vision.md) before contributing.

- Simplicity over architecture
- UX first — the terminal is the game world
- One complete mechanic per sprint
- No XP for fake actions

## Code style

- Functions over classes
- Rich for UI, SQLite for data
- Files under 250 lines
- Do not break existing CLI commands
