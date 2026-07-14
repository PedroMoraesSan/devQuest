import subprocess

import typer
from rich.panel import Panel

from devquest.achievements import check_achievements
from devquest.animations import (
    achievement_unlocked,
    level_up,
    loading,
    quest_complete,
    supply_spin,
    victory_panel,
)
from devquest.database import SessionLocal
from devquest.git_utils import (
    current_branch,
    format_pull_error,
    has_remote,
    is_git_repo,
)
from devquest.models import Profile
from devquest.profile import add_gold, add_xp, require_profile
from devquest.progression import title_for_level
from devquest.quests import progress_quests
from devquest.ui import border_style, console, style


PULL_XP = 30
PULL_GOLD = 15


def _run_pull(
    remote: str | None,
    ref: str | None,
) -> subprocess.CompletedProcess[str]:
    args = ["git", "pull"]

    if remote:
        args.append(remote)
        if ref:
            args.append(ref)
        else:
            branch = current_branch()
            if branch and branch != "HEAD":
                args.append(branch)

    return subprocess.run(args, capture_output=True, text=True)


def pull(
    remote: str | None = typer.Argument(
        None,
        help="Remote name (default: configured upstream).",
    ),
    ref: str | None = typer.Argument(
        None,
        help="Branch or ref to pull (default: current branch).",
    ),
):
    """Call reinforcements — pull from a remote (git pull)."""
    require_profile()

    if not is_git_repo():
        console.print(style("danger", "Not a git repository."))
        raise typer.Exit(1)

    target_remote = remote or "origin"

    if remote and not has_remote(remote):
        console.print(style("danger", f"No remote '{remote}' found."))
        raise typer.Exit(1)

    if not remote and not has_remote("origin"):
        console.print(style("danger", "No remote origin found."))
        raise typer.Exit(1)

    branch = current_branch()
    label = f"{target_remote}/{ref or branch or 'HEAD'}"

    console.print()

    console.print(
        Panel.fit(
            style("accent", "Calling reinforcements!", bold=True),
            border_style=border_style(),
        )
    )

    supply_spin(label)

    console.print()
    console.print(style("enemy", "Supply line", bold=True))
    console.print(style("warning", label))
    console.print()

    loading("Contacting fortress")
    loading("Receiving supplies")

    pull_process = _run_pull(remote, ref)

    if pull_process.returncode != 0:
        console.print(format_pull_error(pull_process.stderr), style="red")
        raise typer.Exit(1)

    levels_gained = add_xp(PULL_XP)
    add_gold(PULL_GOLD)

    db = SessionLocal()
    profile = db.query(Profile).first()
    profile.pulls = (profile.pulls or 0) + 1
    db.commit()
    db.close()

    already = "already up to date" in (pull_process.stdout or "").lower()
    body = f"+{PULL_XP} XP\n+{PULL_GOLD} Gold"
    if already:
        body = f"Already up to date.\n\n{body}"

    victory_panel("Reinforcements Arrived!", body)

    for new_level in levels_gained:
        level_up(new_level, title_for_level(new_level))

    completed_quests, quest_levels = progress_quests("pull")

    for quest in completed_quests:
        quest_complete(quest["name"], quest["xp"], quest["gold"])

    for new_level in quest_levels:
        level_up(new_level, title_for_level(new_level))

    for ach in check_achievements("pull"):
        achievement_unlocked(ach["name"], ach["description"])
