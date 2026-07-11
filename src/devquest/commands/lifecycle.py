import subprocess
import sys

from rich.panel import Panel

from devquest.config import get as config_get
from devquest.config import update
from devquest.ui import border_style, console, style


def disable():
    """Pause DevQuest — gameplay commands become no-ops until hero enable."""
    update(enabled=False)
    console.print(
        Panel.fit(
            (
                f"{style('warning', 'DevQuest disabled.', bold=True)}\n\n"
                "Gameplay commands will skip until you run:\n"
                f"  {style('accent', 'hero enable')}"
            ),
            border_style=border_style(),
        )
    )


def enable():
    """Re-enable DevQuest after hero disable."""
    update(enabled=True)
    console.print(
        Panel.fit(
            style("victory", "DevQuest enabled. Adventure resumes!", bold=True),
            border_style=border_style(),
        )
    )


def update_cmd():
    """Upgrade DevQuest from PyPI (pip install -U devquest)."""
    console.print(style("accent", "Updating DevQuest from PyPI..."))
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-U", "devquest"],
        capture_output=False,
    )
    if result.returncode != 0:
        console.print(style("danger", "Update failed."))
        raise SystemExit(1)
    console.print(style("victory", "DevQuest is up to date."))


def guard_enabled(subcommand: str | None) -> None:
    """Block gameplay when disabled; always allow lifecycle/config helpers."""
    if subcommand in {None, "enable", "disable", "update", "config", "theme"}:
        return

    if config_get("enabled"):
        return

    console.print(
        style("warning", "DevQuest is disabled. Run: hero enable")
    )
    raise SystemExit(0)
