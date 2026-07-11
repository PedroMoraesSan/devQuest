"""Hand-drawn ASCII sprite intros for commit (battle) and push (siege)."""

import sys
import time

from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from devquest.config import get as config_get
from devquest.ui import border_style, console

FRAME_SLEEP = 0.12
HOLD_LAST = 0.25

# Battle: void → portal → enemy materializes → ready
BATTLE_FRAMES = [
    [
        "",
        "",
        "       ·    ",
        "      * *   ",
        "       ·    ",
        "",
        "",
    ],
    [
        "",
        "      .·:.  ",
        "     ·   ·  ",
        "    ·  *  · ",
        "     ·   ·  ",
        "      '·:'  ",
        "",
    ],
    [
        "",
        "      .==.  ",
        "     //||\\\\ ",
        "    || ** ||",
        "     \\\\||// ",
        "      '=='  ",
        "",
    ],
    [
        "",
        "       /\\   ",
        "      /  \\  ",
        "     | .. | ",
        "     |/\\/\\| ",
        "      /  \\  ",
        "",
    ],
    [
        "",
        "       /\\   ",
        "      /..\\  ",
        "     | o o| ",
        "     | \\/ | ",
        "     /|  |\\ ",
        "",
    ],
    [
        "       * *  ",
        "       /\\   ",
        "      /##\\  ",
        "     |o  o| ",
        "     | \\/ | ",
        "     /|__|\\ ",
        "        *   ",
    ],
    [
        "      · * · ",
        "       /\\   ",
        "      /##\\  ",
        "     |@  @| ",
        "     | \\_/ |",
        "     /|##|\\ ",
        "      ·   · ",
    ],
    [
        "",
        "       /\\   ",
        "      /##\\  ",
        "     |@  @| ",
        "     | \\_/ |",
        "     /|##|\\ ",
        "",
    ],
]

# Siege: distant keep → cracks → breach → gate open
SIEGE_FRAMES = [
    [
        "",
        "",
        "      /\\_/\\ ",
        "     |     |",
        "     | [_] |",
        "     |_____|",
        "",
    ],
    [
        "",
        "",
        "     /\\___/\\",
        "    |       |",
        "    |  [_]  |",
        "    |_______|",
        "",
    ],
    [
        "",
        "",
        "     /\\___/\\",
        "    |  /    |",
        "    | /[_]  |",
        "    |/______|",
        "",
    ],
    [
        "",
        "",
        "     /\\___/\\",
        "    | //\\   |",
        "    |//[_] \\|",
        "    |/______|",
        "",
    ],
    [
        "",
        "       *    ",
        "     /\\_/_/\\",
        "    | //\\\\  |",
        "    |//[_]\\\\|",
        "    |/_/\\__/|",
        "       *    ",
    ],
    [
        "       .    ",
        "      * *   ",
        "     /\\ / /\\",
        "    | //\\\\ /|",
        "    |X [_] X|",
        "    |/_/\\_/\\|",
        "      · ·   ",
    ],
    [
        "      · · · ",
        "     /  \\  /\\",
        "    |  /\\\\ / |",
        "    | X  X  |",
        "    |/_/  \\_|",
        "      * * * ",
        "",
    ],
    [
        "",
        "     /      \\",
        "    |   __   |",
        "    |  |  |  |",
        "    |__|  |__|",
        "      *    *  ",
        "",
    ],
]


def _normalize(lines: list[str]) -> str:
    width = max(len(line) for line in lines) if lines else 0
    return "\n".join(line.ljust(width) for line in lines)


def play_sprites(frames: list[list[str]], title: str = "") -> None:
    if not config_get("animations"):
        return

    if not sys.stdout.isatty():
        return

    cleaned = [_normalize(f) for f in frames]

    with Live(console=console, refresh_per_second=16, transient=True) as live:
        for i, frame in enumerate(cleaned):
            live.update(
                Panel(
                    Text(frame, justify="center"),
                    title=title or " ",
                    border_style=border_style(),
                    padding=(0, 2),
                )
            )
            time.sleep(HOLD_LAST if i == len(cleaned) - 1 else FRAME_SLEEP)
