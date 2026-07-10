def xp_to_next(level: int) -> int:
    return 100 * level


def total_xp_for_level(level: int) -> int:
    if level <= 1:
        return 0
    return sum(xp_to_next(i) for i in range(1, level))


def level_from_xp(total_xp: int) -> int:
    level = 1
    remaining = total_xp

    while remaining >= xp_to_next(level):
        remaining -= xp_to_next(level)
        level += 1

    return level


def xp_into_level(total_xp: int) -> tuple[int, int]:
    level = level_from_xp(total_xp)
    current = total_xp - total_xp_for_level(level)
    needed = xp_to_next(level)
    return current, needed


def title_for_level(level: int) -> str:
    if level >= 15:
        return "Legendary Engineer"
    if level >= 10:
        return "Senior Warrior"
    if level >= 5:
        return "Bug Hunter"
    return "Code Apprentice"


def xp_bar(current: int, needed: int, width: int = 20) -> str:
    filled = int((current / needed) * width) if needed else width
    filled = min(filled, width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {current}/{needed}"
