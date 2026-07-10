import subprocess

import typer
from rich.panel import Panel

from devquest.animations import loading
from devquest.database import SessionLocal
from devquest.enemies import random_enemy
from devquest.models import Profile
from devquest.profile import add_gold, add_xp
from devquest.ui import console


def commit():
    db = SessionLocal()

    profile = db.query(Profile).first()

    if not profile:
        console.print("[red]Run hero init first.[/red]")
        db.close()
        raise typer.Exit()

    db.close()

    enemy = random_enemy()

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]⚔ Prepare for battle![/bold cyan]",
            border_style="cyan",
        )
    )

    loading("Summoning enemy...")

    console.print()

    console.print(f"[bold red]👹 {enemy['name']}[/bold red]")

    console.print()

    loading("Battle")

    console.print()

    message = typer.prompt("Commit message")

    console.print()

    loading("Adding files")

    add = subprocess.run(
        ["git", "add", "."],
        capture_output=True,
        text=True,
    )

    if add.returncode != 0:
        console.print(add.stderr, style="red")
        raise typer.Exit()

    loading("Creating commit")

    commit_process = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True,
        text=True,
    )

    if commit_process.returncode != 0:
        console.print(commit_process.stderr, style="red")
        raise typer.Exit()

    add_xp(enemy["xp"])
    add_gold(enemy["gold"])

    db = SessionLocal()

    profile = db.query(Profile).first()

    profile.commits += 1

    db.commit()

    db.close()

    console.print()

    console.print(
        Panel.fit(
            (
                "[bold green]🏆 Victory![/bold green]\n\n"
                f"Enemy Defeated: {enemy['name']}\n\n"
                f"+{enemy['xp']} XP\n"
                f"+{enemy['gold']} Gold"
            ),
            border_style="green",
        )
    )
