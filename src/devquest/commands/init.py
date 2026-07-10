import typer

from devquest.database import engine
from devquest.database import SessionLocal

from devquest.models import Base
from devquest.models import Profile

from devquest.ui import console


def init():

    Base.metadata.create_all(engine)

    db = SessionLocal()

    if db.query(Profile).first():
        console.print("[yellow]Profile already exists.[/yellow]")
        return

    name = typer.prompt("Hero name")

    profile = Profile(name=name)

    db.add(profile)

    db.commit()

    db.close()

    console.print()

    console.print("[green]⚔ Welcome, Hero![/green]")

    console.print(f"Your journey begins now, {name}.")
