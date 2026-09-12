from typing import Dict, Optional
from datetime import date
from pydantic import BaseModel, ConfigDict

class StreakInfo(BaseModel):
    current_streak: int
    longest_streak: int
    last_activity_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)

class CharacterResponse(BaseModel):
    id: int
    user_id: int
    level: int
    current_xp: int
    xp_for_next_level: int
    streak: StreakInfo
    attributes: Dict[str, float]

    model_config = ConfigDict(from_attributes=True)

class AttributesResponse(BaseModel):
    attributes: Dict[str, float]
    dominant_attribute: Optional[str] = None
    attribute_percentages: Dict[str, float]
