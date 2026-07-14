import typer

from devquest.commands.achievements import achievements
from devquest.commands.branches import branch, branches
from devquest.commands.checkout import checkout
from devquest.commands.commit import commit
from devquest.commands.config_cmd import config
from devquest.commands.dashboard import dashboard
from devquest.commands.init import init
from devquest.commands.inventory import inventory
from devquest.commands.lifecycle import (
    disable,
    enable,
    guard_enabled,
    update_cmd,
)
from devquest.commands.push import push
from devquest.commands.pull import pull
from devquest.commands.quests import quests
from devquest.commands.remotes import remotes
from devquest.commands.shop import shop
from devquest.commands.status import status
from devquest.commands.theme import theme


app = typer.Typer(
    help=(
        "DevQuest — gamify your developer journey.\n\n"
        "Install globally:\n"
        "  pip install --user devquest\n"
        "  # or: pipx install devquest\n\n"
        "Pause anytime:\n"
        "  hero disable\n"
        "  hero enable\n\n"
        "Stay current:\n"
        "  hero update"
    ),
    no_args_is_help=True,
)


@app.callback()
def _main(ctx: typer.Context):
    guard_enabled(ctx.invoked_subcommand)


app.command()(init)
app.command()(status)
app.command()(commit)
app.command()(push)
app.command()(pull)
app.command("achievements")(achievements)
app.command()(quests)
app.command()(inventory)
app.command()(shop)
app.command()(dashboard)
app.command()(config)
app.command()(theme)
app.command()(remotes)
app.command()(branches)
app.command()(branch)
app.command()(checkout)
app.command("disable")(disable)
app.command("enable")(enable)
app.command("update")(update_cmd)

if __name__ == "__main__":
    app()
