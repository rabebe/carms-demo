from sqlmodel import SQLModel, Field

class Discipline(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    program_code: str
    program_name: str
    discipline: str
    description: str