import typer
from rich.panel import Panel
from rich.table import Table

from devquest.git_utils import is_git_repo, list_remotes
from devquest.profile import require_profile
from devquest.ui import border_style, console, style


def remotes():
    """Scout the fortresses — list git remotes (git remote -v)."""
    require_profile()

    if not is_git_repo():
        console.print(style("danger", "Not a git repository."))
        raise typer.Exit(1)

    rows = list_remotes()

    if not rows:
        console.print(style("warning", "No remotes found."))
        console.print("[dim]Add one with: git remote add origin <url>[/dim]")
        raise typer.Exit(0)

    table = Table(show_header=True, header_style=border_style())
    table.add_column("Name")
    table.add_column("URL")
    table.add_column("Mode", width=8)

    for name, url, mode in rows:
        table.add_row(name, url, mode)

    console.print(
        Panel(
            table,
            title="Remotes — Fortresses",
            border_style=border_style(),
        )
    )
