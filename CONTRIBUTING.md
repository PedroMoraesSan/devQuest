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

## Publishing

See [PUBLISH.md](PUBLISH.md). Never commit PyPI tokens.
