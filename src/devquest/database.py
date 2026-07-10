from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path.home() / ".devquest"
BASE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = BASE_DIR / "devquest.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
