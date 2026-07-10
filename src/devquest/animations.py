from time import sleep

from rich.panel import Panel
from rich.progress import track

from devquest.ui import console


def loading(message: str):
    for _ in track(range(40), description=message):
        sleep(0.02)


def level_up(new_level: int, title: str):
    console.print()

    console.print(
        Panel.fit(
            (
                "[bold yellow]LEVEL UP![/bold yellow]\n\n"
                f"Level {new_level}\n"
                f"Title: {title}"
            ),
            border_style="yellow",
        )
    )

    loading("Ascending")


def achievement_unlocked(name: str, description: str):
    console.print()

    console.print(
        Panel.fit(
            (
                "[bold magenta]ACHIEVEMENT UNLOCKED![/bold magenta]\n\n"
                f"{name}\n"
                f"[dim]{description}[/dim]"
            ),
            border_style="magenta",
        )
    )
