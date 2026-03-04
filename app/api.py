# app/api.py
from fastapi import FastAPI
from sqlmodel import Session, select
from .db import engine
from .models import Discipline

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello CaRMS!"}

@app.get("/disciplines")
def get_disciplines():
    with Session(engine) as session:
        disciplines = session.exec(select(Discipline)).all()
        return disciplines