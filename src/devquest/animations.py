from time import sleep

from rich.panel import Panel
from rich.progress import track

from devquest.config import get as config_get
from devquest.sounds import play
from devquest.ui import border_style, console, style


def battle_spin(enemy_name: str):
    from devquest.sprites import BATTLE_FRAMES, play_sprites

    play_sprites(BATTLE_FRAMES, title=f"Summoning {enemy_name}")


def siege_spin(target: str):
    from devquest.sprites import SIEGE_FRAMES, play_sprites

    play_sprites(SIEGE_FRAMES, title=f"Siege: {target}")


def supply_spin(target: str):
    from devquest.sprites import SIEGE_FRAMES, play_sprites

    play_sprites(SIEGE_FRAMES, title=f"Reinforcements: {target}")


def loading(message: str):
    if not config_get("animations"):
        return

    for _ in track(range(40), description=message):
        sleep(0.02)


def level_up(new_level: int, title: str):
    play("level_up")
    console.print()

    console.print(
        Panel.fit(
            (
                f"{style('level_up', 'LEVEL UP!', bold=True)}\n\n"
                f"Level {new_level}\n"
                f"Title: {title}"
            ),
            border_style=border_style(),
        )
    )

    loading("Ascending")


def achievement_unlocked(name: str, description: str):
    play("achievement")
    console.print()

    console.print(
        Panel.fit(
            (
                f"{style('achievement', 'ACHIEVEMENT UNLOCKED!', bold=True)}\n\n"
                f"{name}\n"
                f"{style('muted', description)}"
            ),
            border_style=border_style(),
        )
    )


def quest_complete(name: str, xp: int, gold: int):
    play("quest_complete")
    console.print()

    console.print(
        Panel.fit(
            (
                f"{style('quest', 'QUEST COMPLETE!', bold=True)}\n\n"
                f"{name}\n\n"
                f"+{xp} XP\n"
                f"+{gold} Gold"
            ),
            border_style=border_style(),
        )
    )


def victory_panel(title: str, body: str):
    play("victory")
    console.print()

    console.print(
        Panel.fit(
            f"{style('victory', title, bold=True)}\n\n{body}",
            border_style=border_style(),
        )
    )
