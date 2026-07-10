import typer

from devquest.commands.achievements import achievements
from devquest.commands.commit import commit
from devquest.commands.init import init
from devquest.commands.push import push
from devquest.commands.quests import quests
from devquest.commands.status import status


app = typer.Typer(
    help="DevQuest - Gamify your developer journey."
)

app.command()(init)
app.command()(status)
app.command()(commit)
app.command()(push)
app.command("achievements")(achievements)
app.command()(quests)

if __name__ == "__main__":
    app()
