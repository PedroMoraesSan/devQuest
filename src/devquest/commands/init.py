import typer
from sqlalchemy.exc import SQLAlchemyError

from devquest.database import engine
from devquest.database import SessionLocal

from devquest.models import Base
from devquest.models import Profile

from devquest.profile import DATABASE_ERROR
from devquest.ui import console


def init():
    try:
        Base.metadata.create_all(engine)
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise typer.Exit(1)

    try:
        db = SessionLocal()

        if db.query(Profile).first():
            console.print("[yellow]Profile already exists.[/yellow]")
            db.close()
            return

        name = typer.prompt("Hero name")

        profile = Profile(name=name)

        db.add(profile)

        db.commit()

        db.close()
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise typer.Exit(1)

    console.print()

    console.print("[green]Welcome, Hero![/green]")

    console.print(f"Your journey begins now, {name}.")
