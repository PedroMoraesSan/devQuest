<p align="center">
  <img src="assets/banner.png" alt="DevQuest — Gamify your developer journey" width="100%"/>
</p>

<p align="center">
  <strong>DevQuest is not a Git wrapper.</strong><br/>
  It is a terminal RPG where programming <em>is</em> the gameplay.
</p>

<p align="center">
  <a href="https://pypi.org/project/devquest/"><img src="https://img.shields.io/pypi/v/devquest?color=22d3ee&label=pypi&logo=pypi&logoColor=white" alt="PyPI"/></a>
  <a href="https://pypi.org/project/devquest/"><img src="https://img.shields.io/pypi/pyversions/devquest?color=34d399" alt="Python"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-a78bfa" alt="License"/></a>
  <img src="https://img.shields.io/badge/cli-hero-f472b6" alt="CLI"/>
  <img src="https://img.shields.io/badge/status-playable-fbbf24" alt="Status"/>
</p>

---

## The world

```text
  Git is a sword.
  Deploy is a battle.
  Bug is an enemy.
  Merge Conflict is a boss.
```

Every real developer action becomes a quest. XP and Gold only drop when the work actually lands.

Commit and push open with short **ASCII sprite intros** — enemy summon on commit, fortress breach on push. Toggle with `hero config --animations off` (also auto-off when `CI=true`).

---

## Install

Global (recommended):

```bash
pip install --user devquest
# or, isolated: pipx install devquest
```

Then awaken your hero:

```bash
hero init
```

Pause / resume / update anytime:

```bash
hero disable   # skip gameplay until you want it back
hero enable
hero update    # pip install -U devquest
```

`hero --help` also lists these.
---

## Gameplay loop

```text
┌─────────────────────────────────────────────────────────────┐
│  hero commit                                                │
│                                                             │
│  ╭─────────────────────╮                                    │
│  │ Prepare for battle! │                                    │
│  ╰─────────────────────╯                                    │
│                                                             │
│  Merge Conflict                                             │
│  HP [████████████░░░░░░░░] 48/80                            │
│                                                             │
│  Attack 1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%     │
│  CRITICAL HIT! 42 damage!                                   │
│                                                             │
│  ╭──────────────────────────────╮                           │
│  │ Victory!                     │                           │
│  │ Enemy Defeated: Merge Conflict│                          │
│  │ +40 XP   +20 Gold            │                           │
│  ╰──────────────────────────────╯                           │
│                                                             │
│  ╭──────────────────────────────╮                           │
│  │ LEVEL UP!                    │                           │
│  │ Level 5 · Bug Hunter         │                           │
│  ╰──────────────────────────────╯                           │
└─────────────────────────────────────────────────────────────┘
```

```text
hero push   →  siege the fortress (origin/<branch>)
hero pull   →  call reinforcements from the remote
hero status →  XP bar, title, equipped gear, quests
hero quests →  daily missions that reset with the sun
```

---

## Commands

| Command | What happens |
|---|---|
| `hero init` | Create your hero profile |
| `hero status` | Sheet: level, XP bar, gold, gear |
| `hero commit [-m msg]` | Battle an enemy, then commit |
| `hero push` | Assault the remote fortress |
| `hero pull [remote] [ref]` | Call reinforcements (`git pull`) |
| `hero achievements` | Trophy hall |
| `hero quests` | Daily quest board |
| `hero inventory` | Cosmetic loot (`--equip <key>`) |
| `hero shop` | Spend gold (`--buy <key>`) |
| `hero dashboard` | Full Textual menu (arrows + `q`) |
| `hero config` | Settings (`--animations`, `--sounds`, `--theme`) |
| `hero theme` | List or switch color themes |
| `hero remotes` | Scout fortresses (`git remote -v`) |
| `hero branches` | Map all paths (`git branch -a`) |
| `hero branch <name>` | Forge a new branch (+XP) |
| `hero checkout <name>` | Travel to another branch |
| `hero disable` | Pause DevQuest (gameplay no-ops) |
| `hero enable` | Resume after disable |
| `hero update` | Upgrade from PyPI |

---

## Branch control

```bash
hero remotes
hero branches
hero branch feature/loot
hero checkout main
hero pull
hero pull origin
hero pull origin main
```

Creating a branch awards XP/Gold and can complete the daily Pathfinder quest.

---

## Themes & Sounds

Config lives at `~/.devquest/config.toml`:

```toml
theme = "cyberpunk"
animations = true
sounds = false
enabled = true
```

Themes: `cyberpunk`, `matrix`, `retro`, `nord`, `dracula`, `catppuccin`, `windows95`

```bash
hero theme matrix
hero config --sounds on
hero config --animations off   # fast mode: no sprites, battle rounds, or loading bars
```

With animations off (or in CI), `commit` / `push` / `pull` run git first and print rewards in one shot afterward.

```bash
# CI / pipelines
export CI=true
# or:
export DEVQUEST_ANIMATIONS=off
hero commit -m "ship it"
```

Sounds are optional and off by default (level up, crit, achievement, quest, victory).

---

## Progression

```text
Titles
  Code Apprentice  →  Bug Hunter  →  Senior Warrior  →  Legendary Engineer

Combat
  Hit · Miss · Critical · Boss encounters

Economy
  Gold from real commits/pushes → cosmetic shop only
  (no pay-to-win, ever)
```

---

## Quick start

```bash
pip install --user devquest
cd your-repo
hero init
hero status
hero commit
hero push
hero dashboard
```

Local development:

```bash
pip install -e .
```

---

## Philosophy

> The terminal should feel like a game world.  
> Programming should feel like an adventure.

Read more in [`vision.md`](vision.md).

---

## Docs

| File | Purpose |
|---|---|
| [`vision.md`](vision.md) | Product vision |
| [`ROADMAP.md`](ROADMAP.md) | Release plan |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute |
| [`PUBLISH.md`](PUBLISH.md) | PyPI release guide |

---

<p align="center">
  <sub>⚔ May your builds be green and your merges conflict-free.</sub>
</p>
