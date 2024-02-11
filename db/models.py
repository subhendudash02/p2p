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

meta.create_all(engine)