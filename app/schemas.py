from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TermBase(BaseModel):
    term: str = Field(..., description="Термин для глоссария")
    definition: str = Field(..., description="Определение термина")
    source: Optional[str] = Field(None, description="Источник определения")

class TermCreate(TermBase):
    pass

class TermUpdate(BaseModel):
    term: Optional[str] = None
    definition: Optional[str] = None
    source: Optional[str] = None

class Term(TermBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True