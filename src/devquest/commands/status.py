from rich.panel import Panel
from rich.table import Table

from devquest.achievements import list_achievements
from devquest.profile import DatabaseError, get_profile, sync_level
from devquest.progression import title_for_level, xp_bar, xp_into_level
from devquest.quests import get_daily_quests

from devquest.ui import console


def status():
    try:
        profile = get_profile()
    except DatabaseError:
        return

    if not profile:
        console.print("[red]Run hero init first.[/red]")
        return

    level = sync_level()
    title = title_for_level(level)
    current, needed = xp_into_level(profile.xp)
    achievements = list_achievements()
    unlocked = sum(1 for _, done in achievements if done)
    total = len(achievements)
    daily = get_daily_quests()
    quests_done = sum(1 for q in daily if q["completed"])

    table = Table(show_header=False)

    table.add_row("Hero", profile.name)
    table.add_row("Title", title)
    table.add_row("Level", str(level))
    table.add_row("XP", xp_bar(current, needed))
    table.add_row("Coins", str(profile.coins))
    table.add_row("Commits", str(profile.commits))
    table.add_row("Pushes", str(profile.pushes))
    table.add_row("Streak", f"{profile.streak} days")
    table.add_row("Achievements", f"{unlocked}/{total}")
    table.add_row("Daily Quests", f"{quests_done}/{len(daily)}")

    console.print(
        Panel(
            table,
            title="DevQuest",
            border_style="cyan",
        )
    )
