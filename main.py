from fastapi import FastAPI
from routes import auth

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(auth.auth_router)
