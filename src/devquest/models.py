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
