import typer
from rich.panel import Panel
from rich.table import Table

from devquest.config import get as config_get, update
from devquest.themes import THEMES, get_theme, list_themes
from devquest.ui import border_style, console, style


def theme(
    name: str = typer.Argument(None, help="Theme name to apply"),
):
    if name:
        if name not in THEMES:
            console.print(style("danger", f"Unknown theme: {name}"))
            console.print(f"Available: {', '.join(list_themes())}")
            raise typer.Exit(1)

        update(theme=name)
        active = get_theme(name)
        console.print(
            style("victory", f"Theme set to {active['name']}.", bold=True)
        )
        return

    current_key = config_get("theme")

    table = Table(show_header=True, header_style=border_style())
    table.add_column("Key")
    table.add_column("Name")
    table.add_column("Active", width=8)

    for key in list_themes():
        t = THEMES[key]
        mark = "yes" if key == current_key else ""
        table.add_row(key, t["name"], mark)

    console.print(
        Panel(
            table,
            title="Themes",
            border_style=border_style(),
        )
    )

    console.print("[dim]hero theme <key>  e.g. hero theme matrix[/dim]")
