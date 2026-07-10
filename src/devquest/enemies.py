import random

ENEMIES = [
    {
        "name": "Merge Conflict",
        "xp": 40,
        "gold": 20,
    },
    {
        "name": "Legacy Code",
        "xp": 25,
        "gold": 10,
    },
    {
        "name": "Syntax Goblin",
        "xp": 15,
        "gold": 5,
    },
    {
        "name": "Production Bug",
        "xp": 100,
        "gold": 50,
    },
    {
        "name": "Memory Leak",
        "xp": 60,
        "gold": 30,
    },
    {
        "name": "Null Pointer",
        "xp": 35,
        "gold": 15,
    },
]


def random_enemy():
    return random.choice(ENEMIES)
