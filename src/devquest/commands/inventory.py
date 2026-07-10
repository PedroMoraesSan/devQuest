import typer
from rich.panel import Panel
from rich.table import Table

from devquest.profile import require_profile
from devquest.shop import equip_item, list_inventory
from devquest.ui import console


def inventory(
    equip: str = typer.Option(
        None,
        "--equip",
        "-e",
        help="Equip an owned item by key (e.g. rubber_duck)",
    ),
):
    require_profile()

    if equip:
        ok, message = equip_item(equip)
        style = "green" if ok else "red"
        console.print(f"[{style}]{message}[/{style}]")

        if not ok:
            raise typer.Exit(1)

        console.print()

    rows = list_inventory()

    if not rows:
        console.print("[yellow]Inventory is empty. Visit the shop![/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Key", style="dim")
    table.add_column("Item")
    table.add_column("Status", width=10)
    table.add_column("Description")

    for item in rows:
        status = "[green]equipped[/green]" if item["equipped"] else "[dim]owned[/dim]"
        table.add_row(item["key"], item["name"], status, item["description"])

    console.print(
        Panel(
            table,
            title=f"Inventory ({len(rows)} items)",
            border_style="cyan",
        )
    )

    console.print("[dim]Equip with: hero inventory --equip <key>[/dim]")
