import random

from devquest.animations import loading
from devquest.ui import console

BASE_DAMAGE = 20
CRIT_MULTIPLIER = 2
MAX_ROUNDS = 4


def hp_bar(current: int, maximum: int, width: int = 20) -> str:
    filled = int((current / maximum) * width) if maximum else width
    filled = min(filled, width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {current}/{maximum}"


def roll_attack() -> str:
    roll = random.random()

    if roll < 0.10:
        return "crit"

    if roll < 0.25:
        return "miss"

    return "hit"


def attack_damage(roll: str) -> int:
    if roll == "miss":
        return 0

    damage = BASE_DAMAGE + random.randint(-5, 10)

    if roll == "crit":
        damage *= CRIT_MULTIPLIER

    return damage


def show_attack_result(roll: str, damage: int):
    if roll == "crit":
        console.print(f"[bold yellow]CRITICAL HIT![/bold yellow] {damage} damage!")
        return

    if roll == "miss":
        console.print("[dim]Miss! No damage.[/dim]")
        return

    console.print(f"[green]Hit![/green] {damage} damage.")


def run_battle(enemy: dict) -> int:
    hp = enemy["hp"]
    max_hp = hp

    console.print(f"HP {hp_bar(hp, max_hp)}")
    console.print()

    for round_num in range(1, MAX_ROUNDS + 1):
        if hp <= 0:
            break

        loading(f"Attack {round_num}")

        roll = roll_attack()
        damage = attack_damage(roll)
        hp = max(0, hp - damage)

        show_attack_result(roll, damage)
        console.print(f"HP {hp_bar(hp, max_hp)}")
        console.print()

    if hp > 0:
        console.print("[yellow]Enemy weakened! Finish with your commit.[/yellow]")
        console.print()

    return hp
