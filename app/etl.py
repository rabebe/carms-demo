import pandas as pd
from db import engine, create_db_and_tables
from models import Discipline
from sqlmodel import Session

# Create tables
create_db_and_tables()

# Load data
df = pd.read_excel("data/1503_discipline.xlsx")

# Insert into DB
with Session(engine) as session:
    for _, row in df.iterrows():
        session.add(Discipline(
            program_code=row['Program Code'],
            program_name=row['Program Name'],
            discipline=row['Discipline'],
            description=row['Description']
        ))
    session.commit()