import subprocess

import typer
from rich.panel import Panel

from devquest.achievements import check_achievements
from devquest.animations import (
    achievement_unlocked,
    battle_spin,
    level_up,
    loading,
    quest_complete,
    victory_panel,
)
from devquest.combat import run_battle
from devquest.config import animations_enabled
from devquest.database import SessionLocal
from devquest.enemies import random_enemy
from devquest.git_utils import has_changes, is_git_repo
from devquest.models import Profile
from devquest.profile import add_gold, add_xp, require_profile
from devquest.progression import title_for_level
from devquest.quests import progress_quests
from devquest.ui import border_style, console, style


def _do_commit(message: str) -> None:
    add = subprocess.run(
        ["git", "add", "."],
        capture_output=True,
        text=True,
    )

    if add.returncode != 0:
        console.print(add.stderr.strip() or "Failed to stage files.", style="red")
        raise typer.Exit(1)

    loading("Creating commit")

    commit_process = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True,
        text=True,
    )

    if commit_process.returncode != 0:
        stderr = commit_process.stderr.strip().lower()
        if "nothing to commit" in stderr:
            console.print(style("warning", "Nothing to commit."))
            raise typer.Exit(0)

        console.print(
            commit_process.stderr.strip() or "Failed to create commit.",
            style="red",
        )
        raise typer.Exit(1)


def _reward(enemy: dict) -> None:
    levels_gained = add_xp(enemy["xp"])
    add_gold(enemy["gold"])

    db = SessionLocal()
    profile = db.query(Profile).first()
    profile.commits += 1
    db.commit()
    db.close()

    label = "Boss Defeated" if enemy.get("boss") else "Enemy Defeated"

    victory_panel(
        "Victory!",
        f"{label}: {enemy['name']}\n\n+{enemy['xp']} XP\n+{enemy['gold']} Gold",
    )

    for new_level in levels_gained:
        level_up(new_level, title_for_level(new_level))

    completed_quests, quest_levels = progress_quests("commit", enemy=enemy)

    for quest in completed_quests:
        quest_complete(quest["name"], quest["xp"], quest["gold"])

    for new_level in quest_levels:
        level_up(new_level, title_for_level(new_level))

    for ach in check_achievements("commit", enemy=enemy):
        achievement_unlocked(ach["name"], ach["description"])


def commit(
    message: str | None = typer.Option(
        None,
        "--message",
        "-m",
        help="Commit message (skip prompt; useful in CI).",
    ),
):
    require_profile()

    if not is_git_repo():
        console.print(style("danger", "Not a git repository."))
        raise typer.Exit(1)

    if not has_changes():
        console.print(style("warning", "Nothing to commit."))
        raise typer.Exit(0)

    enemy = random_enemy()
    animate = animations_enabled()

    if animate:
        console.print()
        console.print(
            Panel.fit(
                style("accent", "Prepare for battle!", bold=True),
                border_style=border_style(),
            )
        )
        battle_spin(enemy["name"])
        console.print()

        if enemy.get("boss"):
            console.print(
                Panel.fit(
                    style("boss", "BOSS APPEARS!", bold=True),
                    border_style=border_style(),
                )
            )
            console.print()

        console.print(style("enemy", enemy["name"], bold=True))
        console.print()
        run_battle(enemy)

    if not message:
        message = typer.prompt("Commit message")

    console.print()
    loading("Final strike")
    _do_commit(message)
    _reward(enemy)
