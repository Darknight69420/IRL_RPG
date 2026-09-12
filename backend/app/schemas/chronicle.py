from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ChronicleEventResponse(BaseModel):
    id: int
    user_id: int
    event_type: str
    title: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginatedChronicleResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ChronicleEventResponse]
