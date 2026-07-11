import typer

from devquest.commands.achievements import achievements
from devquest.commands.commit import commit
from devquest.commands.config_cmd import config
from devquest.commands.dashboard import dashboard
from devquest.commands.init import init
from devquest.commands.inventory import inventory
from devquest.commands.push import push
from devquest.commands.quests import quests
from devquest.commands.shop import shop
from devquest.commands.status import status
from devquest.commands.theme import theme


app = typer.Typer(
    help="DevQuest - Gamify your developer journey."
)

app.command()(init)
app.command()(status)
app.command()(commit)
app.command()(push)
app.command("achievements")(achievements)
app.command()(quests)
app.command()(inventory)
app.command()(shop)
app.command()(dashboard)
app.command()(config)
app.command()(theme)

if __name__ == "__main__":
    app()
