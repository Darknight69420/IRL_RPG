from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class QuestStepCreate(BaseModel):
    step_order: int
    title: str = Field(..., min_length=1, max_length=200)
    difficulty: str = Field(default="MEDIUM")
    primary_attribute: str = Field(default="INT")

class QuestStepResponse(BaseModel):
    id: int
    chain_id: int
    step_order: int
    title: str
    difficulty: str
    primary_attribute: str
    status: str # LOCKED, UNLOCKED, COMPLETED
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class QuestChainCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    steps: List[QuestStepCreate] = Field(..., min_length=1)

class QuestChainResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    status: str # IN_PROGRESS, COMPLETED, ABANDONED
    total_steps: int
    completed_steps: int
    steps: List[QuestStepResponse]
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
