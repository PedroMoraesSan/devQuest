from sqlalchemy.exc import SQLAlchemyError

from devquest.database import SessionLocal
from devquest.models import Profile
from devquest.progression import level_from_xp
from devquest.ui import console

DATABASE_ERROR = (
    "[red]DevQuest database error. "
    "Delete ~/.devquest/devquest.db and run hero init again.[/red]"
)


class DatabaseError(Exception):
    pass


def get_profile():
    try:
        db = SessionLocal()
        profile = db.query(Profile).first()
        db.close()
        return profile
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise DatabaseError()


def require_profile():
    try:
        db = SessionLocal()
        profile = db.query(Profile).first()
        db.close()
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)

    if not profile:
        console.print("[red]Run hero init first.[/red]")
        raise SystemExit(1)

    return profile


def sync_level() -> int:
    db = SessionLocal()

    try:
        profile = db.query(Profile).first()
        new_level = level_from_xp(profile.xp)

        if profile.level != new_level:
            profile.level = new_level
            db.commit()

        level = profile.level
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()

    return level


def add_xp(amount: int) -> list[int]:
    db = SessionLocal()

    try:
        profile = db.query(Profile).first()
        old_level = level_from_xp(profile.xp)
        profile.xp += amount
        new_level = level_from_xp(profile.xp)
        profile.level = new_level
        db.commit()

        if new_level > old_level:
            return list(range(old_level + 1, new_level + 1))

        return []
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()


def add_gold(amount: int):
    db = SessionLocal()

    try:
        profile = db.query(Profile).first()
        profile.coins += amount
        db.commit()
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()
