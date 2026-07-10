import typer
from rich.panel import Panel
from rich.table import Table

from devquest.profile import require_profile
from devquest.shop import buy_item, list_shop
from devquest.ui import console


def shop(
    buy: str = typer.Option(
        None,
        "--buy",
        "-b",
        help="Buy an item by key (e.g. coffee_mug)",
    ),
):
    profile = require_profile()

    if buy:
        ok, message = buy_item(buy)
        style = "green" if ok else "red"
        console.print(f"[{style}]{message}[/{style}]")

        if not ok:
            raise typer.Exit(1)

        console.print()
        profile = require_profile()

    rows = list_shop()

    table = Table(show_header=True, header_style="bold yellow")
    table.add_column("Key", style="dim")
    table.add_column("Item")
    table.add_column("Price", width=10)
    table.add_column("Status", width=10)
    table.add_column("Description")

    for item in rows:
        status = "[green]owned[/green]" if item["owned"] else "[dim]for sale[/dim]"
        table.add_row(
            item["key"],
            item["name"],
            f"{item['price']}g",
            status,
            item["description"],
        )

    console.print(
        Panel(
            table,
            title=f"Shop — Gold: {profile.coins}",
            border_style="yellow",
        )
    )

    console.print("[dim]Buy with: hero shop --buy <key>[/dim]")
