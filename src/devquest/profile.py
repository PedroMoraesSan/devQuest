from devquest.database import SessionLocal
from devquest.models import Profile


def get_profile():
    db = SessionLocal()

    profile = db.query(Profile).first()

    db.close()

    return profile
