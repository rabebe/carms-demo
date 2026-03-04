from sqlmodel import create_engine, SQLModel

# SQLite (for local testing)
DATABASE_URL = "sqlite:///./carms.db"

engine = create_engine(DATABASE_URL, echo=True)

# Optional: a function to initialize tables
def init_db():
    from .etl import load_data  # or your SQLModel models
    SQLModel.metadata.create_all(engine)