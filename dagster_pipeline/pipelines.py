import pandas as pd
from sqlmodel import Session
from dagster import job, op, In, Definitions
from app.db import engine, create_db_and_tables
from app.models import Discipline

@op(ins={"file_path": In(str, default_value="data/1503_program_master.xlsx")})
def load_excel(file_path: str):
    """Reads the local Excel file."""
    return pd.read_excel(file_path)

@op
def insert_into_db(df):
    """Inserts data into the RDS database."""
    create_db_and_tables()
    with Session(engine) as session:
        for _, row in df.iterrows():
            # Logic to extract city from program_name if city column is missing
            # e.g., "Uni / Specialty / Ottawa" -> parts[2]
            parts = [p.strip() for p in str(row["program_name"]).split("/")]
            city_val = parts[2] if len(parts) >= 3 else "Unknown"

            session.add(
                Discipline(
                    program_code=row["discipline_id"],
                    program_name=row["program_name"],
                    discipline=row["discipline_name"],
                    description=row["program_url"],
                    city=city_val # Ensuring city is populated for your API
                )
            )
        session.commit()

@job
def etl_job():
    df = load_excel()
    insert_into_db(df)

# The "Entry Point" for Dagster
defs = Definitions(
    jobs=[etl_job]
)