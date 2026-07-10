import subprocess

import typer
from rich.panel import Panel

from devquest.animations import loading
from devquest.database import SessionLocal
from devquest.models import Profile
from devquest.profile import add_gold, add_xp
from devquest.ui import console


PUSH_XP = 50
PUSH_GOLD = 25


def push():
    db = SessionLocal()

    profile = db.query(Profile).first()

    if not profile:
        console.print("[red]Run hero init first.[/red]")
        db.close()
        raise typer.Exit()

    db.close()

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]🚀 Preparing for siege![/bold cyan]",
            border_style="cyan",
        )
    )

    console.print()

    console.print("[bold red]🏰 Fortress[/bold red]")
    console.print("[yellow]origin/main[/yellow]")

    console.print()

    loading("Preparing assault")

    loading("Uploading artifacts")

    push_process = subprocess.run(
        ["git", "push"],
        capture_output=True,
        text=True,
    )

    if push_process.returncode != 0:

        stderr = push_process.stderr.lower()

        if "has no upstream branch" in stderr:

            console.print(
                "[yellow]First push detected! Setting upstream...[/yellow]"
            )

            upstream = subprocess.run(
                ["git", "push", "-u", "origin", "main"],
                capture_output=True,
                text=True,
            )

            if upstream.returncode != 0:
                console.print(upstream.stderr, style="red")
                raise typer.Exit()

        else:
            console.print(push_process.stderr, style="red")
            raise typer.Exit()

    add_xp(PUSH_XP)
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
                "[bold green]🏆 Fortress Captured![/bold green]\n\n"
                f"+{PUSH_XP} XP\n"
                f"+{PUSH_GOLD} Gold"
            ),
            border_style="green",
        )
    )
