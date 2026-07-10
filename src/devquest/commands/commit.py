import subprocess

import typer
from rich.panel import Panel

from devquest.achievements import check_achievements
from devquest.animations import achievement_unlocked, level_up, loading, quest_complete
from devquest.combat import run_battle
from devquest.database import SessionLocal
from devquest.enemies import random_enemy
from devquest.git_utils import has_changes, is_git_repo
from devquest.models import Profile
from devquest.profile import add_gold, add_xp, require_profile
from devquest.progression import title_for_level
from devquest.quests import progress_quests
from devquest.ui import console


def commit():
    require_profile()

    if not is_git_repo():
        console.print("[red]Not a git repository.[/red]")
        raise typer.Exit(1)

    if not has_changes():
        console.print("[yellow]Nothing to commit.[/yellow]")
        raise typer.Exit(0)

    enemy = random_enemy()

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]Prepare for battle![/bold cyan]",
            border_style="cyan",
        )
    )

    loading("Summoning enemy...")

    console.print()

    if enemy.get("boss"):
        console.print(
            Panel.fit(
                "[bold red]BOSS APPEARS![/bold red]",
                border_style="red",
            )
        )
        console.print()

    console.print(f"[bold red]{enemy['name']}[/bold red]")

    console.print()

    run_battle(enemy)

    message = typer.prompt("Commit message")

    console.print()

    loading("Final strike")

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
            console.print("[yellow]Nothing to commit.[/yellow]")
            raise typer.Exit(0)

        console.print(
            commit_process.stderr.strip() or "Failed to create commit.",
            style="red",
        )
        raise typer.Exit(1)

    levels_gained = add_xp(enemy["xp"])
    add_gold(enemy["gold"])

    db = SessionLocal()

    profile = db.query(Profile).first()

    profile.commits += 1

    db.commit()

    db.close()

    console.print()

    label = "Boss Defeated" if enemy.get("boss") else "Enemy Defeated"

    console.print(
        Panel.fit(
            (
                "[bold green]Victory![/bold green]\n\n"
                f"{label}: {enemy['name']}\n\n"
                f"+{enemy['xp']} XP\n"
                f"+{enemy['gold']} Gold"
            ),
            border_style="green",
        )
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
