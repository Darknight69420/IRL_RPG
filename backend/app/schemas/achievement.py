from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AchievementResponse(BaseModel):
    id: int
    code: str
    name: str
    description: str
    icon_url: str
    is_unlocked: bool = False
    unlocked_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
