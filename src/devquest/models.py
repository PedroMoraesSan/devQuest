from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    level = Column(Integer, default=1)

    xp = Column(Integer, default=0)

    coins = Column(Integer, default=0)

    commits = Column(Integer, default=0)

    pushes = Column(Integer, default=0)

    streak = Column(Integer, default=0)


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True)

    key = Column(String, unique=True, nullable=False)

    name = Column(String, nullable=False)


class DailyQuest(Base):
    __tablename__ = "daily_quests"

    id = Column(Integer, primary_key=True)

    key = Column(String, nullable=False)

    name = Column(String, nullable=False)

    description = Column(String, nullable=False)

    date = Column(String, nullable=False)

    progress = Column(Integer, default=0)

    target = Column(Integer, nullable=False)

    xp_reward = Column(Integer, nullable=False)

    gold_reward = Column(Integer, nullable=False)

    completed = Column(Integer, default=0)
