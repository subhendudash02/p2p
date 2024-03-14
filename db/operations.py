import sqlalchemy as db
from db import engine, meta

def insert(table_name: db.Table | str, values: dict):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    ins = db.insert(table_name).values(**values)

    with engine.connect() as conn:
        conn.execute(ins)
        conn.commit()
    
def read(table_name: db.Table | str, cond: str):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    if (cond == None):
        sel = db.select(table_name)
    sel = db.select(table_name).where(table_name.c.username == cond)

    with engine.connect() as conn:
        result = conn.execute(sel)
        return result.fetchone()
    
def update(table_name: db.Table | str, cond: str, values: dict):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    if (cond == None):
        raise ValueError("Condition cannot be None")
    upd = db.update(table_name).where(table_name.c.username == cond).values(**values)

    with engine.connect() as conn:
        conn.execute(upd)
        conn.commit()