import subprocess

import typer
from rich.panel import Panel

from devquest.achievements import check_achievements
from devquest.animations import (
    achievement_unlocked,
    level_up,
    loading,
    quest_complete,
    siege_spin,
    victory_panel,
)
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
from devquest.quests import progress_quests
from devquest.ui import border_style, console, style


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
        console.print(style("warning", "First push detected! Setting upstream..."))

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
        console.print(style("danger", "Not a git repository."))
        raise typer.Exit(1)

    if not has_remote("origin"):
        console.print(style("danger", "No remote origin found."))
        raise typer.Exit(1)

    branch = current_branch()

    if not branch:
        console.print(style("danger", "Could not detect the current branch."))
        raise typer.Exit(1)

    console.print()

    console.print(
        Panel.fit(
            style("accent", "Preparing for siege!", bold=True),
            border_style=border_style(),
        )
    )

    siege_spin(f"origin/{branch}")

    console.print()

    console.print(style("enemy", "Fortress", bold=True))
    console.print(style("warning", f"origin/{branch}"))

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

    victory_panel(
        "Fortress Captured!",
        f"+{PUSH_XP} XP\n+{PUSH_GOLD} Gold",
    )

    for new_level in levels_gained:
        level_up(new_level, title_for_level(new_level))

    completed_quests, quest_levels = progress_quests("push")

    for quest in completed_quests:
        quest_complete(quest["name"], quest["xp"], quest["gold"])

    for new_level in quest_levels:
        level_up(new_level, title_for_level(new_level))

    for ach in check_achievements("push"):
        achievement_unlocked(ach["name"], ach["description"])
