from devquest.database import SessionLocal
from devquest.models import Profile


def get_profile():
    db = SessionLocal()

    profile = db.query(Profile).first()

    db.close()

    return profile


def add_xp(amount: int):
    db = SessionLocal()

    profile = db.query(Profile).first()

    profile.xp += amount

    db.commit()

    db.close()


def add_gold(amount: int):
    db = SessionLocal()

    profile = db.query(Profile).first()

    profile.coins += amount

    db.commit()

    db.close()
