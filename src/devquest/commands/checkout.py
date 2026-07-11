import typer
from rich.panel import Panel

from devquest.animations import loading
from devquest.git_utils import (
    branch_exists,
    checkout_branch,
    current_branch,
    is_git_repo,
    ref_exists,
)
from devquest.profile import require_profile
from devquest.ui import border_style, console, style


def checkout(
    name: str = typer.Argument(..., help="Branch to enter"),
):
    """Travel to another realm — switch branch (git checkout)."""
    require_profile()

    if not is_git_repo():
        console.print(style("danger", "Not a git repository."))
        raise typer.Exit(1)

    current = current_branch()

    if current == name:
        console.print(style("warning", f"Already on {name}."))
        raise typer.Exit(0)

    if not branch_exists(name) and not ref_exists(name):
        console.print(style("danger", f"Branch not found: {name}"))
        console.print(
            f"[dim]Create with: hero branch {name}  |  List: hero branches[/dim]"
        )
        raise typer.Exit(1)

    console.print()
    console.print(style("accent", f"Traveling to {name}...", bold=True))
    loading("Crossing realms")

    result = checkout_branch(name)

    if result.returncode != 0:
        err = result.stderr.strip().lower()
        if "your local changes" in err or "would be overwritten" in err:
            console.print(
                style(
                    "danger",
                    "Local changes would be overwritten. Commit or stash first.",
                )
            )
        else:
            console.print(
                result.stderr.strip() or "Checkout failed.",
                style="red",
            )
        raise typer.Exit(1)

    console.print()
    console.print(
        Panel.fit(
            (
                f"{style('victory', 'Arrived!', bold=True)}\n\n"
                f"Now on: {style('accent', name)}\n"
                f"From: {current or '—'}"
            ),
            border_style=border_style(),
        )
    )
