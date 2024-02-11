import sqlalchemy as db

engine = db.create_engine("sqlite:///./database.db")
meta = db.MetaData()