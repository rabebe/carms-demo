import os
from typing import List, Optional, Any
from sqlmodel import Session, select, col
from langchain_core.language_models.llms import LLM

# Import your DB engine and Model
# Adjust these imports based on your actual file names
from app.db import engine 
from app.models import Discipline 

# Path to data folder for RAG
DATA_DIR = os.path.join("data", "program_descriptions")

# --- Local mock LLM (RAG Logic) ---

class FakeLLM(LLM):
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        if "Context:" in prompt:
            actual_text = prompt.split("Context:")[1].strip()
            return f"FOUND IN DOCUMENT: {actual_text[:300]}..."
        return "I couldn't find a specific document for that city."

    @property
    def _identifying_params(self): return {}
    @property
    def _llm_type(self): return "fake"

# --- RAG Helper Functions ---

def get_program_context(program_keywords: str) -> str:
    target = program_keywords.lower()
    if not os.path.exists(DATA_DIR):
        return ""
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".md"):
            with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
                content = f.read()
                if target in content[:500].lower():
                    return content
    return ""

def ask_question(question: str) -> str:
    """RAG flow: Retrieve text from MD files and feed it to the LLM."""
    medical_cities = [
        "vancouver", "victoria", "kelowna", "calgary", "edmonton", 
        "saskatoon", "winnipeg", "london", "hamilton", "toronto", 
        "kingston", "ottawa", "sudbury", "thunder bay", "montreal", 
        "sherbrooke", "quebec city", "saguenay", "halifax", "st. john's"
    ]
    program_context = ""
    
    for city in medical_cities:
        if city in question.lower():
            program_context = get_program_context(city)
            break

    prompt = f"System: Use this context.\nContext: {program_context[:2000]}\n\nQ: {question}" if program_context else question
    llm = FakeLLM()
    return llm.invoke(prompt)

# --- Database Query Functions (The "Production" Way) ---

def find_disciplines_by_city(city: str):
    """Uses SQL 'ILIKE' to find cities within the program_name string in RDS."""
    with Session(engine) as session:
        if not city:
            statement = select(Discipline)
        else:
            # We search the 'program_name' column for the city string
            # ilike makes it case-insensitive (e.g., 'ottawa' matches 'Ottawa')
            statement = select(Discipline).where(Discipline.program_name.ilike(f"%{city}%"))
        
        results = session.exec(statement).all()
        # Convert SQLModel objects to dictionaries for FastAPI JSON response
        return [r.dict() for r in results]

def find_disciplines_by_specialty(specialty: str):
    """Filters the RDS database by the 'discipline' column."""
    with Session(engine) as session:
        target = specialty.strip().lower()
        # Using col().lower() ensures a case-insensitive match on the DB side
        statement = select(Discipline).where(col(Discipline.discipline).ilike(target))
        
        results = session.exec(statement).all()
        return [r.dict() for r in results]