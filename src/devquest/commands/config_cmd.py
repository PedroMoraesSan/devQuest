import typer
from rich.panel import Panel
from rich.table import Table

from devquest.config import CONFIG_PATH, load_config, update
from devquest.themes import THEMES, list_themes
from devquest.ui import border_style, console, style


def config(
    theme: str = typer.Option(None, "--theme", "-t", help="Set theme"),
    sounds: str = typer.Option(None, "--sounds", "-s", help="on or off"),
    animations: str = typer.Option(None, "--animations", "-a", help="on or off"),
):
    changes = {}

    if theme:
        if theme not in THEMES:
            console.print(style("danger", f"Unknown theme: {theme}"))
            console.print(f"Available: {', '.join(list_themes())}")
            raise typer.Exit(1)
        changes["theme"] = theme

    if sounds:
        if sounds not in ("on", "off"):
            console.print(style("danger", "Use --sounds on or --sounds off"))
            raise typer.Exit(1)
        changes["sounds"] = sounds == "on"

    if animations:
        if animations not in ("on", "off"):
            console.print(style("danger", "Use --animations on or --animations off"))
            raise typer.Exit(1)
        changes["animations"] = animations == "on"

    if changes:
        update(**changes)
        console.print(style("victory", "Config updated."))
        console.print()

    cfg = load_config()

    table = Table(show_header=False)
    table.add_row("theme", cfg["theme"])
    table.add_row("animations", "on" if cfg["animations"] else "off")
    table.add_row("sounds", "on" if cfg["sounds"] else "off")
    table.add_row("default_branch", cfg["default_branch"])
    table.add_row("config file", str(CONFIG_PATH))

    console.print(
        Panel(
            table,
            title="DevQuest Config",
            border_style=border_style(),
        )
    )

    console.print()
    console.print("[dim]hero theme <name>  |  hero config --sounds on[/dim]")
