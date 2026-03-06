import pandas as pd
from sqlmodel import Session
from .db import engine, create_db_and_tables
from .models import Discipline

# Create tables if they don't exist
create_db_and_tables()

# Load data
df = pd.read_excel("data/1503_program_master.xlsx")

# Insert into DB
with Session(engine) as session:
    for _, row in df.iterrows():
        session.add(Discipline(
            program_code=row['discipline_id'],
            program_name=row['program_name'],
            discipline=row['discipline_name'],
            description=row['program_url']
        ))
    session.commit()