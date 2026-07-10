from rich.panel import Panel
from rich.table import Table

from devquest.profile import DatabaseError, get_profile

from devquest.ui import console


def status():
    try:
        profile = get_profile()
    except DatabaseError:
        return

    if not profile:
        console.print("[red]Run hero init first.[/red]")
        return

    table = Table(show_header=False)

    table.add_row("Hero", profile.name)

    table.add_row("Level", str(profile.level))

    table.add_row("XP", str(profile.xp))

    table.add_row("Coins", str(profile.coins))

    table.add_row("Commits", str(profile.commits))

    table.add_row("Pushes", str(profile.pushes))

    table.add_row("Streak", f"{profile.streak} days")

    console.print(
        Panel(
            table,
            title="⚔ DevQuest",
            border_style="cyan",
        )
    )
