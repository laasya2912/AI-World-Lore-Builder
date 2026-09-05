from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LoreBase(BaseModel):
    world_id: int
    type: str = Field(..., pattern="^(REGION|FACTION|CHARACTER|EVENT)$")
    name: str
    description: str
    facts: Optional[str] = None
    relationships: Optional[str] = None


class LoreCreate(LoreBase):
    pass


class LoreUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    facts: Optional[str] = None
    relationships: Optional[str] = None


class LoreResponse(LoreBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WorldGenerateRequest(BaseModel):
    genre: str
    tone: str
    concept: str