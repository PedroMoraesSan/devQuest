import random
from datetime import date

from sqlalchemy.exc import SQLAlchemyError

from devquest.database import SessionLocal, engine
from devquest.models import Base, DailyQuest
from devquest.profile import DATABASE_ERROR, add_gold, add_xp
from devquest.ui import console

QUESTS_PER_DAY = 3

QUEST_POOL = [
    {
        "key": "daily_commit",
        "name": "Daily Commit",
        "description": "Make 1 commit",
        "event": "commit",
        "target": 1,
        "xp": 20,
        "gold": 10,
    },
    {
        "key": "commits_3",
        "name": "Triple Strike",
        "description": "Make 3 commits",
        "event": "commit",
        "target": 3,
        "xp": 50,
        "gold": 25,
    },
    {
        "key": "push_1",
        "name": "Ship It",
        "description": "Make 1 push",
        "event": "push",
        "target": 1,
        "xp": 30,
        "gold": 15,
    },
    {
        "key": "pushes_2",
        "name": "Double Siege",
        "description": "Make 2 pushes",
        "event": "push",
        "target": 2,
        "xp": 45,
        "gold": 20,
    },
    {
        "key": "merge_conflict",
        "name": "Conflict Resolver",
        "description": "Defeat a Merge Conflict",
        "event": "enemy:Merge Conflict",
        "target": 1,
        "xp": 50,
        "gold": 25,
    },
    {
        "key": "boss_hunt",
        "name": "Boss Hunter",
        "description": "Defeat a Boss",
        "event": "boss",
        "target": 1,
        "xp": 60,
        "gold": 30,
    },
    {
        "key": "create_branch",
        "name": "Pathfinder",
        "description": "Create a new branch",
        "event": "branch",
        "target": 1,
        "xp": 25,
        "gold": 10,
    },
]


def ensure_tables():
    Base.metadata.create_all(engine)


def _today() -> str:
    return date.today().isoformat()


def _pick_quests_for_day(day: str) -> list[dict]:
    rng = random.Random(day)
    return rng.sample(QUEST_POOL, k=min(QUESTS_PER_DAY, len(QUEST_POOL)))


def ensure_daily_quests() -> list[dict]:
    ensure_tables()
    day = _today()
    db = SessionLocal()

    try:
        existing = db.query(DailyQuest).filter_by(date=day).all()

        if not existing:
            for quest in _pick_quests_for_day(day):
                db.add(
                    DailyQuest(
                        key=quest["key"],
                        name=quest["name"],
                        description=quest["description"],
                        date=day,
                        progress=0,
                        target=quest["target"],
                        xp_reward=quest["xp"],
                        gold_reward=quest["gold"],
                        completed=0,
                    )
                )
            db.commit()
            existing = db.query(DailyQuest).filter_by(date=day).all()

        return [
            {
                "key": q.key,
                "name": q.name,
                "description": q.description,
                "date": q.date,
                "progress": q.progress,
                "target": q.target,
                "xp_reward": q.xp_reward,
                "gold_reward": q.gold_reward,
                "completed": bool(q.completed),
            }
            for q in existing
        ]
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()


def get_daily_quests() -> list[dict]:
    return ensure_daily_quests()


def _matches_event(quest_key: str, event: str, enemy: dict | None) -> bool:
    pool = next((q for q in QUEST_POOL if q["key"] == quest_key), None)

    if not pool:
        return False

    quest_event = pool["event"]

    if quest_event == event:
        return True

    if quest_event == "boss" and enemy and enemy.get("boss"):
        return True

    if quest_event.startswith("enemy:") and enemy:
        return enemy.get("name") == quest_event.split(":", 1)[1]

    return False


def progress_quests(event: str, enemy: dict | None = None) -> tuple[list[dict], list[int]]:
    ensure_daily_quests()
    day = _today()
    db = SessionLocal()
    completed = []

    try:
        quests = db.query(DailyQuest).filter_by(date=day, completed=0).all()

        for quest in quests:
            if not _matches_event(quest.key, event, enemy):
                continue

            quest.progress = min(quest.progress + 1, quest.target)

            if quest.progress >= quest.target:
                quest.completed = 1
                completed.append(
                    {
                        "name": quest.name,
                        "description": quest.description,
                        "xp": quest.xp_reward,
                        "gold": quest.gold_reward,
                    }
                )

        db.commit()
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()

    levels_gained: list[int] = []

    for quest in completed:
        levels_gained.extend(add_xp(quest["xp"]))
        add_gold(quest["gold"])

    return completed, levels_gained
