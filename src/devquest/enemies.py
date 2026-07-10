import random

ENEMIES = [
    {"name": "Syntax Goblin", "xp": 15, "gold": 5, "hp": 30},
    {"name": "Legacy Code", "xp": 25, "gold": 10, "hp": 40},
    {"name": "Null Pointer", "xp": 35, "gold": 15, "hp": 45},
    {"name": "Merge Conflict", "xp": 40, "gold": 20, "hp": 50},
    {"name": "Memory Leak", "xp": 60, "gold": 30, "hp": 60},
    {"name": "Production Bug", "xp": 100, "gold": 50, "hp": 80},
]

BOSSES = [
    {"name": "Dependency Hell", "xp": 120, "gold": 60, "hp": 120, "boss": True},
    {"name": "Kernel Panic", "xp": 150, "gold": 75, "hp": 150, "boss": True},
    {"name": "Hotfix Demon", "xp": 130, "gold": 65, "hp": 130, "boss": True},
]

BOSS_CHANCE = 0.15


def random_enemy() -> dict:
    if random.random() < BOSS_CHANCE:
        return random.choice(BOSSES).copy()

    return random.choice(ENEMIES).copy()
