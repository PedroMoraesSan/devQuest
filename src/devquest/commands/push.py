import subprocess

import typer
from rich.panel import Panel

from devquest.achievements import check_achievements
from devquest.animations import achievement_unlocked, level_up, loading
from devquest.database import SessionLocal
from devquest.git_utils import (
    current_branch,
    format_push_error,
    has_remote,
    is_git_repo,
)
from devquest.models import Profile
from devquest.profile import add_gold, add_xp, require_profile
from devquest.progression import title_for_level
from devquest.ui import console


PUSH_XP = 50
PUSH_GOLD = 25


def _run_push(branch: str) -> subprocess.CompletedProcess[str]:
    push_process = subprocess.run(
        ["git", "push"],
        capture_output=True,
        text=True,
    )

    if push_process.returncode == 0:
        return push_process

    stderr = push_process.stderr.lower()

    if "has no upstream branch" in stderr or "no upstream branch" in stderr:
        console.print("[yellow]First push detected! Setting upstream...[/yellow]")

        upstream = subprocess.run(
            ["git", "push", "-u", "origin", branch],
            capture_output=True,
            text=True,
        )

        return upstream

    return push_process


def push():
    require_profile()

    if not is_git_repo():
        console.print("[red]Not a git repository.[/red]")
        raise typer.Exit(1)

    if not has_remote("origin"):
        console.print("[red]No remote origin found.[/red]")
        raise typer.Exit(1)

    branch = current_branch()

    if not branch:
        console.print("[red]Could not detect the current branch.[/red]")
        raise typer.Exit(1)

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]Preparing for siege![/bold cyan]",
            border_style="cyan",
        )
    )

    console.print()

    console.print("[bold red]Fortress[/bold red]")
    console.print(f"[yellow]origin/{branch}[/yellow]")

    console.print()

    loading("Preparing assault")

    loading("Uploading artifacts")

    push_process = _run_push(branch)

    if push_process.returncode != 0:
        console.print(format_push_error(push_process.stderr), style="red")
        raise typer.Exit(1)

    levels_gained = add_xp(PUSH_XP)
    add_gold(PUSH_GOLD)

    db = SessionLocal()

    profile = db.query(Profile).first()

    profile.pushes += 1

    db.commit()

    db.close()

    console.print()

    console.print(
        Panel.fit(
            (
                "[bold green]Fortress Captured![/bold green]\n\n"
                f"+{PUSH_XP} XP\n"
                f"+{PUSH_GOLD} Gold"
            ),
            border_style="green",
        )
    )

    for new_level in levels_gained:
        level_up(new_level, title_for_level(new_level))

    for ach in check_achievements("push"):
        achievement_unlocked(ach["name"], ach["description"])
