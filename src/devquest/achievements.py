from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from devquest.database import SessionLocal, engine
from devquest.models import Achievement, Base, Profile
from devquest.profile import DATABASE_ERROR
from devquest.ui import console


def ensure_tables():
    Base.metadata.create_all(engine)


ACHIEVEMENTS = [
    {
        "key": "first_commit",
        "name": "First Commit",
        "description": "Make your first commit.",
    },
    {
        "key": "commits_10",
        "name": "10 Commits",
        "description": "Reach 10 commits.",
    },
    {
        "key": "commits_100",
        "name": "100 Commits",
        "description": "Reach 100 commits.",
    },
    {
        "key": "commits_1000",
        "name": "1000 Commits",
        "description": "Reach 1000 commits.",
    },
    {
        "key": "first_push",
        "name": "First Push",
        "description": "Push for the first time.",
    },
    {
        "key": "night_owl",
        "name": "Night Owl",
        "description": "Commit between 22:00 and 05:00.",
    },
    {
        "key": "weekend_warrior",
        "name": "Weekend Warrior",
        "description": "Commit on a Saturday or Sunday.",
    },
    {
        "key": "merge_master",
        "name": "Merge Master",
        "description": "Defeat a Merge Conflict.",
    },
    {
        "key": "bug_slayer",
        "name": "Bug Slayer",
        "description": "Defeat a Production Bug or a Boss.",
    },
    {
        "key": "legendary_hero",
        "name": "Legendary Hero",
        "description": "Reach level 15.",
    },
]


def _unlocked_keys(db) -> set[str]:
    rows = db.query(Achievement).all()
    return {row.key for row in rows}


def _is_earned(key: str, profile: Profile, event: str, enemy: dict | None) -> bool:
    now = datetime.now()

    if key == "first_commit":
        return profile.commits >= 1

    if key == "commits_10":
        return profile.commits >= 10

    if key == "commits_100":
        return profile.commits >= 100

    if key == "commits_1000":
        return profile.commits >= 1000

    if key == "first_push":
        return profile.pushes >= 1

    if key == "night_owl":
        return event == "commit" and (now.hour >= 22 or now.hour < 5)

    if key == "weekend_warrior":
        return event == "commit" and now.weekday() >= 5

    if key == "merge_master":
        return bool(enemy and enemy.get("name") == "Merge Conflict")

    if key == "bug_slayer":
        return bool(
            enemy
            and (enemy.get("name") == "Production Bug" or enemy.get("boss"))
        )

    if key == "legendary_hero":
        return profile.level >= 15

    return False


def unlock_achievement(key: str, name: str) -> bool:
    ensure_tables()
    db = SessionLocal()

    try:
        if db.query(Achievement).filter_by(key=key).first():
            return False

        db.add(Achievement(key=key, name=name))
        db.commit()
        return True
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()


def check_achievements(
    event: str,
    enemy: dict | None = None,
) -> list[dict]:
    ensure_tables()
    db = SessionLocal()

    try:
        profile = db.query(Profile).first()

        if not profile:
            return []

        unlocked = _unlocked_keys(db)
        newly = []

        for ach in ACHIEVEMENTS:
            if ach["key"] in unlocked:
                continue

            if _is_earned(ach["key"], profile, event, enemy):
                db.add(Achievement(key=ach["key"], name=ach["name"]))
                newly.append(ach)

        if newly:
            db.commit()

        return newly
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()


def sync_milestones() -> list[dict]:
    """Unlock count/level achievements already earned by existing profiles."""
    ensure_tables()
    db = SessionLocal()

    try:
        profile = db.query(Profile).first()

        if not profile:
            return []

        unlocked = _unlocked_keys(db)
        newly = []
        milestone_keys = {
            "first_commit",
            "commits_10",
            "commits_100",
            "commits_1000",
            "first_push",
            "legendary_hero",
        }

        for ach in ACHIEVEMENTS:
            if ach["key"] not in milestone_keys or ach["key"] in unlocked:
                continue

            if _is_earned(ach["key"], profile, "sync", None):
                db.add(Achievement(key=ach["key"], name=ach["name"]))
                newly.append(ach)

        if newly:
            db.commit()

        return newly
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()


def list_achievements() -> list[tuple[dict, bool]]:
    ensure_tables()
    sync_milestones()
    db = SessionLocal()

    try:
        unlocked = _unlocked_keys(db)
        return [(ach, ach["key"] in unlocked) for ach in ACHIEVEMENTS]
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()
