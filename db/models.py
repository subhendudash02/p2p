import sqlalchemy as db
from db import engine, meta

user_table = db.Table(
    "user",
    meta,
    db.Column("ID", db.String, primary_key=True, unique=True),
    db.Column("username", db.String, unique=True),
    db.Column("password", db.String),
    db.Column("email", db.String, unique=True),
)

session_table = db.Table(
    "sessions",
    meta,
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column("username", db.String, db.ForeignKey("user.username")),
    db.Column("jwt_token", db.String, unique=True),
)

energy_table = db.Table(
    "energy",
    meta,
    db.Column("username", db.String, db.ForeignKey("user.username")),
    db.Column("storageUnits", db.Float),
    db.Column("loadForecast", db.Float),
    db.Column("profitPref", db.Float),
    db.Column("ratingPref", db.Float),
    db.Column("type", db.String)
)

solar_table = db.Table(
    "solar",
    meta,
    db.Column("username", db.String, db.ForeignKey("user.username")),
    db.Column("solarUnits", db.Float)
)

meta.create_all(engine)

ins = db.insert(solar_table).values({"username": "subhendu", "solarUnits": 100})

with engine.connect() as conn:
    conn.execute(ins)
    conn.commit()
