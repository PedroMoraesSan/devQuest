import subprocess

import typer

from rich.panel import Panel

from devquest.animations import loading
from devquest.database import SessionLocal
from devquest.models import Profile
from devquest.ui import console


def commit():
    db = SessionLocal()

    profile = db.query(Profile).first()

    if not profile:
        console.print("[red]Run hero init first.[/red]")
        return

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]⚔ Prepare for battle![/bold cyan]",
            border_style="cyan",
        )
    )

    loading("Summoning enemy...")

    console.print()

    console.print("[bold red]👹 Wild Enemy Appears![/bold red]")
    console.print("[yellow]Uncommitted Changes[/yellow]")

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
        return

    loading("Creating commit")

    commit_process = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True,
        text=True,
    )

    if commit_process.returncode != 0:
        console.print(commit_process.stderr, style="red")
        return

    profile.xp += 20
    profile.commits += 1

    db.commit()
    db.close()

    console.print()

    console.print(
        Panel.fit(
            "[bold green]🏆 Victory![/bold green]\n\n"
            "+20 XP\n"
            "+1 Commit",
            border_style="green",
        )
    )
