import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

try:
    with engine.connect() as connection:
        print("Connection Successful! AWS RDS is talking to Mac.")
except Exception as e:
    print(f"Connection Failed: {e}")