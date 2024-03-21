import sqlalchemy as db
from db import engine, meta
import csv
from db.operations import insert, read

user_table = db.Table(
    "user",
    meta,
    db.Column("ID", db.Integer, db.Identity(start=2, cycle=True), primary_key=True, unique=True, autoincrement=True),
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
    db.Column("Prosumer_Id", db.Integer, db.ForeignKey("user.ID"), primary_key=True, autoincrement=True),
    db.Column("username", db.String, db.ForeignKey("user.username")),
    db.Column("Storage", db.Float),
    db.Column("Load Forecast (Units)", db.Float),
    db.Column("Profit_pref", db.Float),
    db.Column("Rating_pref", db.Float),
    db.Column("Solar", db.String),
    db.Column("Total (Units)", db.Float),
)

meta.create_all(engine)

# if not read(user_table, "admin"):
#     insert(user_table, {"username": "admin", "password": "admin", "email": "admin@gmail.com"})

# r = read(energy_table, None)
# print(r)

# if not r:
#     with open("solar_data.csv") as csvfile:
#         line = csv.reader(csvfile)
#         for i in line:
#             if i[1] != "Solar":
#                 insert(energy_table, {"Prosumer_Id": i[0], "Solar": i[1]})