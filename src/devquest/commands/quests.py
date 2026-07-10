from rich.panel import Panel
from rich.table import Table

from devquest.profile import require_profile
from devquest.quests import get_daily_quests
from devquest.ui import console


def quests():
    require_profile()

    rows = get_daily_quests()
    done = sum(1 for q in rows if q["completed"])

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Status", width=8)
    table.add_column("Quest")
    table.add_column("Progress", width=12)
    table.add_column("Reward", width=14)

    for quest in rows:
        status = "[green]done[/green]" if quest["completed"] else "[dim]----[/dim]"
        progress = f"{quest['progress']}/{quest['target']}"
        reward = f"+{quest['xp_reward']} XP / +{quest['gold_reward']}g"
        table.add_row(status, quest["description"], progress, reward)

    day = rows[0]["date"] if rows else "today"

    console.print(
        Panel(
            table,
            title=f"Daily Quests — {day} ({done}/{len(rows)})",
            border_style="cyan",
        )
    )
