from typing import Optional, Dict, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ActivityBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: str = Field(default="HABIT") # HABIT, TASK
    difficulty: str = Field(default="MEDIUM") # TRIVIAL, EASY, MEDIUM, HARD, HEROIC
    primary_attribute: str = Field(...) # STR, INT, WIS, DIS, VIT, CHA
    secondary_attribute: Optional[str] = None
    cooldown_hours: int = Field(default=24, ge=0)

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    primary_attribute: Optional[str] = None
    secondary_attribute: Optional[str] = None
    cooldown_hours: Optional[int] = None
    is_active: Optional[bool] = None

class ActivityResponse(ActivityBase):
    id: int
    user_id: int
    is_active: bool
    completed_today: bool = False
    last_completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ActivityCompleteRequest(BaseModel):
    notes: Optional[str] = None

# Progression Diff Models
class CharacterProgressionDiff(BaseModel):
    level: int
    current_xp: int
    leveled_up: bool

class CreatureProgressionDiff(BaseModel):
    creature_id: int
    name: str
    species_code: str
    species_name: str
    previous_level: int
    current_level: int
    leveled_up: bool
    bond_score: int
    mood: str
    evolution_triggered: bool
    evolved_from: Optional[str] = None
    evolved_to: Optional[str] = None
    evolution_tier: Optional[int] = None

class StreakDiff(BaseModel):
    current_streak: int
    longest_streak: int
    streak_advanced: bool

class AchievementUnlocked(BaseModel):
    code: str
    name: str
    description: str
    icon_url: str

class ActivityCompletionResponse(BaseModel):
    activity_id: int
    activity_title: str
    completed_at: datetime
    xp_earned: int
    streak_bonus_multiplier: float
    attribute_gains: Dict[str, float]
    character: CharacterProgressionDiff
    creature: CreatureProgressionDiff
    streak: StreakDiff
    new_achievements: List[AchievementUnlocked]
