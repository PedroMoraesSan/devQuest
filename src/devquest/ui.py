from rich.console import Console

from devquest.themes import theme_color

console = Console()


def style(key: str, text: str, bold: bool = False) -> str:
    color = theme_color(key)
    prefix = "bold " if bold else ""
    return f"[{prefix}{color}]{text}[/{prefix}{color}]"


def border_style() -> str:
    return theme_color("border")


def accent_style() -> str:
    return theme_color("accent")
