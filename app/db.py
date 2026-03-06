import os
from sqlmodel import create_engine, SQLModel

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./carms.db")

# For PostgreSQL, we don't need 'check_same_thread', but SQLite does.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)