from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Label, ListItem, ListView, Static

from devquest.achievements import list_achievements
from devquest.profile import get_profile, sync_level
from devquest.progression import title_for_level, xp_bar, xp_into_level
from devquest.quests import get_daily_quests
from devquest.shop import get_equipped_name, list_inventory


MENU = [
    ("player", "Player"),
    ("quests", "Quests"),
    ("achievements", "Achievements"),
    ("inventory", "Inventory"),
    ("stats", "Statistics"),
]


def _player_panel() -> str:
    profile = get_profile()

    if not profile:
        return "Run hero init first."

    level = sync_level()
    title = title_for_level(level)
    current, needed = xp_into_level(profile.xp)
    equipped = get_equipped_name() or "—"

    return "\n".join(
        [
            f"Hero:      {profile.name}",
            f"Title:     {title}",
            f"Equipped:  {equipped}",
            f"Level:     {level}",
            f"XP:        {xp_bar(current, needed)}",
            f"Gold:      {profile.coins}",
        ]
    )


def _quests_panel() -> str:
    quests = get_daily_quests()

    if not quests:
        return "No daily quests."

    lines = [f"Daily Quests — {quests[0]['date']}", ""]

    for quest in quests:
        mark = "[x]" if quest["completed"] else "[ ]"
        lines.append(
            f"{mark} {quest['description']}  "
            f"({quest['progress']}/{quest['target']})  "
            f"+{quest['xp_reward']} XP / +{quest['gold_reward']}g"
        )

    return "\n".join(lines)


def _achievements_panel() -> str:
    rows = list_achievements()
    done = sum(1 for _, unlocked in rows if unlocked)
    lines = [f"Achievements ({done}/{len(rows)})", ""]

    for ach, unlocked in rows:
        mark = "[x]" if unlocked else "[ ]"
        lines.append(f"{mark} {ach['name']} — {ach['description']}")

    return "\n".join(lines)


def _inventory_panel() -> str:
    items = list_inventory()

    if not items:
        return "Inventory empty. Visit hero shop."

    lines = [f"Inventory ({len(items)} items)", ""]

    for item in items:
        mark = "*" if item["equipped"] else " "
        lines.append(f"[{mark}] {item['name']} — {item['description']}")

    return "\n".join(lines)


def _stats_panel() -> str:
    profile = get_profile()

    if not profile:
        return "Run hero init first."

    achievements = list_achievements()
    unlocked = sum(1 for _, done in achievements if done)
    daily = get_daily_quests()
    quests_done = sum(1 for q in daily if q["completed"])

    return "\n".join(
        [
            "Statistics",
            "",
            f"Commits:       {profile.commits}",
            f"Pushes:        {profile.pushes}",
            f"Streak:        {profile.streak} days",
            f"Achievements:  {unlocked}/{len(achievements)}",
            f"Daily Quests:  {quests_done}/{len(daily)}",
            f"Gold:          {profile.coins}",
            f"Total XP:      {profile.xp}",
        ]
    )


PANELS = {
    "player": _player_panel,
    "quests": _quests_panel,
    "achievements": _achievements_panel,
    "inventory": _inventory_panel,
    "stats": _stats_panel,
}


class DashboardApp(App):
    TITLE = "DevQuest"
    CSS = """
    Screen {
        layout: horizontal;
    }

    #sidebar {
        width: 24;
        border: solid $accent;
        padding: 1;
    }

    #content {
        width: 1fr;
        border: solid $primary;
        padding: 1 2;
    }

    ListView {
        height: 1fr;
    }

    .hint {
        color: $text-muted;
        margin-top: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("escape", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
    ]

    def __init__(self):
        super().__init__()
        self.current = "player"

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("Menu", classes="hint")
                yield ListView(
                    *[ListItem(Label(label), id=key) for key, label in MENU],
                    id="menu",
                )
                yield Label("↑↓ navigate  Enter open", classes="hint")
                yield Label("r refresh  q quit", classes="hint")

            yield Static(_player_panel(), id="content")

        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#menu", ListView).index = 0
        self.query_one("#menu", ListView).focus()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id:
            self.current = event.item.id
            self._render_panel()

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if event.item and event.item.id:
            self.current = event.item.id
            self._render_panel()

    def action_refresh(self) -> None:
        self._render_panel()

    def _render_panel(self) -> None:
        panel = PANELS.get(self.current, _player_panel)
        self.query_one("#content", Static).update(panel())


def run_dashboard():
    DashboardApp().run()
