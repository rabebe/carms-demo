import os
from typing import List
from fastapi import FastAPI, Query, HTTPException, Depends
from sqlmodel import SQLModel, Session, create_engine

# --- DATABASE SETUP ---
# This looks for the AWS RDS URL first; if not found, it defaults to local SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./carms.db")

# PostgreSQL needs different arguments than SQLite
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)
else:
    # Use this for AWS RDS (PostgreSQL)
    engine = create_engine(DATABASE_URL, echo=True)

# --- IMPORT YOUR CUSTOM LOGIC ---
# Note: Ensure these functions are compatible with the engine above
from app.queries import (
    find_disciplines_by_city, 
    find_disciplines_by_specialty, 
    ask_question
)

# --- APP INITIALIZATION ---
app = FastAPI(title="CaRMS Demo API")

@app.on_event("startup")
def on_startup():
    """
    This is the crucial fix: It creates the tables in RDS 
    if they don't already exist.
    """
    print(f"DEBUG: Connecting to database at {DATABASE_URL.split('@')[-1]}") # Safely logs endpoint
    SQLModel.metadata.create_all(engine)
    print("DEBUG: Database tables initialized successfully.")

# --- ROUTES ---

@app.get("/")
def read_root():
    return {
        "message": "Hello CaRMS! API is live.",
        "database": "PostgreSQL (RDS)" if "rds" in DATABASE_URL else "SQLite (Local)"
    }

@app.get("/disciplines")
def all_disciplines():
    """Returns every discipline in the database."""
    data = find_disciplines_by_city("") 
    return data

@app.get("/disciplines/city/{city}")
def disciplines_by_city(city: str):
    print(f"DEBUG: Searching for city: {city}")
    data = find_disciplines_by_city(city)
    
    if not data:
        # Returns a 404 instead of a 500 if the city isn't found
        raise HTTPException(status_code=404, detail=f"No programs found in '{city}'")
        
    print(f"DEBUG: Found {len(data)} results.")
    return data

@app.get("/disciplines/specialty/{specialty}")
def disciplines_by_specialty(specialty: str):
    data = find_disciplines_by_specialty(specialty)
    if not data:
        raise HTTPException(status_code=404, detail=f"No programs found for specialty '{specialty}'")
    return data

@app.get("/ask")
def ask_carms(q: str = Query(..., description="Ask a question about a specific program")):
    """
    RAG Endpoint: Uses LangChain to answer questions based on .md files.
    """
    try:
        answer = ask_question(q)
        return {"question": q, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Engine Error: {str(e)}")