from rich.panel import Panel
from rich.table import Table

from devquest.achievements import list_achievements
from devquest.profile import require_profile
from devquest.ui import console


def achievements():
    require_profile()

    rows = list_achievements()
    unlocked_count = sum(1 for _, done in rows if done)

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Status", width=8)
    table.add_column("Achievement")
    table.add_column("Description")

    for ach, done in rows:
        status = "[green]done[/green]" if done else "[dim]----[/dim]"
        table.add_row(status, ach["name"], ach["description"])

    console.print(
        Panel(
            table,
            title=f"Achievements ({unlocked_count}/{len(rows)})",
            border_style="magenta",
        )
    )
