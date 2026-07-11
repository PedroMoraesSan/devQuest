import typer
from rich.panel import Panel
from rich.table import Table

from devquest.animations import level_up, loading, quest_complete, victory_panel
from devquest.git_utils import (
    branch_exists,
    create_branch,
    current_branch,
    is_git_repo,
    list_branches,
)
from devquest.profile import add_gold, add_xp, require_profile
from devquest.progression import title_for_level
from devquest.quests import progress_quests
from devquest.ui import border_style, console, style


BRANCH_XP = 15
BRANCH_GOLD = 5


def branches():
    """Map the realm — list all branches (git branch -a)."""
    require_profile()

    if not is_git_repo():
        console.print(style("danger", "Not a git repository."))
        raise typer.Exit(1)

    rows = list_branches()
    here = current_branch() or "—"

    if not rows:
        console.print(style("warning", "No branches found."))
        raise typer.Exit(0)

    table = Table(show_header=True, header_style=border_style())
    table.add_column(" ", width=2)
    table.add_column("Branch")
    table.add_column("Type", width=8)

    for branch in rows:
        mark = "*" if branch["current"] else " "
        kind = "remote" if branch["remote"] else "local"
        name = style("accent", branch["name"]) if branch["current"] else branch["name"]
        table.add_row(mark, name, kind)

    console.print(
        Panel(
            table,
            title=f"Branches — you are on {here}",
            border_style=border_style(),
        )
    )

    console.print(
        "[dim]hero checkout <name>  |  hero branch <name>  (create)[/dim]"
    )


def branch(
    name: str = typer.Argument(..., help="New branch name to create and enter"),
):
    """Forge a new path — create and checkout a branch (git checkout -b)."""
    require_profile()

    if not is_git_repo():
        console.print(style("danger", "Not a git repository."))
        raise typer.Exit(1)

    if branch_exists(name):
        console.print(style("warning", f"Branch already exists: {name}"))
        console.print(f"[dim]Switch with: hero checkout {name}[/dim]")
        raise typer.Exit(1)

    console.print()
    console.print(style("accent", f"Forging a new path: {name}", bold=True))
    loading("Opening trail")

    result = create_branch(name)

    if result.returncode != 0:
        console.print(
            result.stderr.strip() or "Failed to create branch.",
            style="red",
        )
        raise typer.Exit(1)

    levels_gained = add_xp(BRANCH_XP)
    add_gold(BRANCH_GOLD)

    victory_panel(
        "New Path Opened!",
        f"Branch: {name}\n\n+{BRANCH_XP} XP\n+{BRANCH_GOLD} Gold",
    )

    for new_level in levels_gained:
        level_up(new_level, title_for_level(new_level))

    completed_quests, quest_levels = progress_quests("branch")

    for quest in completed_quests:
        quest_complete(quest["name"], quest["xp"], quest["gold"])

    for new_level in quest_levels:
        level_up(new_level, title_for_level(new_level))
