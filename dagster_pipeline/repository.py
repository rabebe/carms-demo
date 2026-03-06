from sqlmodel import Session, select, col
from app.db import engine
from app.models import Discipline
from typing import List

def get_all_disciplines() -> List[Discipline]:
    """Fetches everything from RDS."""
    with Session(engine) as session:
        statement = select(Discipline)
        return session.exec(statement).all()

def get_disciplines_by_city(city: str) -> List[Discipline]:
    """Case-insensitive search for city."""
    with Session(engine) as session:
        # Using .ilike allows searching for 'ottawa' to find 'Ottawa'
        statement = select(Discipline).where(col(Discipline.city).ilike(f"%{city}%"))
        return session.exec(statement).all()

def get_disciplines_by_specialty(specialty: str) -> List[Discipline]:
    """Case-insensitive search for specialty/discipline."""
    with Session(engine) as session:
        statement = select(Discipline).where(col(Discipline.discipline).ilike(f"%{specialty}%"))
        return session.exec(statement).all()