import typer

from devquest.commands.commit import commit
from devquest.commands.init import init
from devquest.commands.status import status

app = typer.Typer(
    help="⚔ DevQuest - Gamify your developer journey."
)

app.command()(init)
app.command()(status)
app.command()(commit)

if __name__ == "__main__":
    app()


