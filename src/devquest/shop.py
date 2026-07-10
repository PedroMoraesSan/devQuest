from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from devquest.database import SessionLocal, engine
from devquest.models import Base, InventoryItem, Profile
from devquest.profile import DATABASE_ERROR
from devquest.ui import console

CATALOG = [
    {
        "key": "rubber_duck",
        "name": "Rubber Duck",
        "price": 0,
        "description": "Your faithful debugging companion.",
    },
    {
        "key": "bronze_keyboard",
        "name": "Bronze Keyboard",
        "price": 50,
        "description": "Clacky starter gear.",
    },
    {
        "key": "coffee_mug",
        "name": "Coffee Mug",
        "price": 75,
        "description": "Fuel for late-night commits.",
    },
    {
        "key": "mechanical_keyboard",
        "name": "Mechanical Keyboard",
        "price": 150,
        "description": "Satisfying clicks for every keystroke.",
    },
    {
        "key": "rgb_keyboard",
        "name": "RGB Keyboard",
        "price": 250,
        "description": "Rainbow power. Purely cosmetic.",
    },
    {
        "key": "golden_monitor",
        "name": "Golden Monitor",
        "price": 400,
        "description": "Shine while you ship.",
    },
    {
        "key": "cyber_sword",
        "name": "Cyber Sword",
        "price": 500,
        "description": "Slash bugs in style.",
    },
    {
        "key": "legendary_macbook",
        "name": "Legendary MacBook",
        "price": 800,
        "description": "The ultimate flex. Still cosmetic.",
    },
]


def ensure_tables():
    Base.metadata.create_all(engine)
    _ensure_equipped_column()
    _grant_starter_item()


def _ensure_equipped_column():
    db = SessionLocal()

    try:
        cols = [
            row[1]
            for row in db.execute(text("PRAGMA table_info(profiles)")).fetchall()
        ]
        if "equipped" not in cols:
            db.execute(text("ALTER TABLE profiles ADD COLUMN equipped VARCHAR"))
            db.commit()
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()


def _grant_starter_item():
    db = SessionLocal()

    try:
        if db.query(InventoryItem).filter_by(key="rubber_duck").first():
            return

        profile = db.query(Profile).first()

        if not profile:
            return

        duck = next(item for item in CATALOG if item["key"] == "rubber_duck")
        db.add(InventoryItem(key=duck["key"], name=duck["name"]))

        if not profile.equipped:
            profile.equipped = duck["key"]

        db.commit()
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()


def catalog_item(key: str) -> dict | None:
    return next((item for item in CATALOG if item["key"] == key), None)


def owned_keys() -> set[str]:
    ensure_tables()
    db = SessionLocal()

    try:
        return {row.key for row in db.query(InventoryItem).all()}
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()


def list_inventory() -> list[dict]:
    ensure_tables()
    owned = owned_keys()
    equipped = get_equipped_key()

    return [
        {
            **item,
            "owned": item["key"] in owned,
            "equipped": item["key"] == equipped,
        }
        for item in CATALOG
        if item["key"] in owned
    ]


def list_shop() -> list[dict]:
    ensure_tables()
    owned = owned_keys()

    return [
        {
            **item,
            "owned": item["key"] in owned,
        }
        for item in CATALOG
        if item["price"] > 0
    ]


def get_equipped_key() -> str | None:
    ensure_tables()
    db = SessionLocal()

    try:
        profile = db.query(Profile).first()
        return profile.equipped if profile else None
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()


def get_equipped_name() -> str | None:
    key = get_equipped_key()

    if not key:
        return None

    item = catalog_item(key)
    return item["name"] if item else key


def buy_item(key: str) -> tuple[bool, str]:
    ensure_tables()
    item = catalog_item(key)

    if not item:
        return False, "Item not found in the shop."

    if item["price"] <= 0:
        return False, "That item cannot be bought."

    db = SessionLocal()

    try:
        if db.query(InventoryItem).filter_by(key=key).first():
            return False, "You already own this item."

        profile = db.query(Profile).first()

        if not profile:
            return False, "Run hero init first."

        if profile.coins < item["price"]:
            return False, f"Not enough gold. Need {item['price']}, have {profile.coins}."

        profile.coins -= item["price"]
        db.add(InventoryItem(key=item["key"], name=item["name"]))
        db.commit()
        return True, f"Purchased {item['name']} for {item['price']} gold!"
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()


def equip_item(key: str) -> tuple[bool, str]:
    ensure_tables()
    item = catalog_item(key)

    if not item:
        return False, "Item not found."

    db = SessionLocal()

    try:
        owned = db.query(InventoryItem).filter_by(key=key).first()

        if not owned:
            return False, "You do not own this item. Visit the shop."

        profile = db.query(Profile).first()

        if not profile:
            return False, "Run hero init first."

        profile.equipped = key
        db.commit()
        return True, f"Equipped {item['name']}."
    except SQLAlchemyError:
        console.print(DATABASE_ERROR)
        raise SystemExit(1)
    finally:
        db.close()
