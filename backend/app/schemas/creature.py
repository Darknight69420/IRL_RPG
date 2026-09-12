from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class SpeciesResponse(BaseModel):
    id: int
    code: str
    name: str
    archetype: str
    tier: int
    dominant_attribute: Optional[str] = None
    description: str
    sprite_asset_key: str

    model_config = ConfigDict(from_attributes=True)

class CreatureStats(BaseModel):
    hp: int
    attack: int
    defense: int
    focus: int
    presence: int

class CreatureResponse(BaseModel):
    id: int
    nickname: str
    species: SpeciesResponse
    level: int
    current_xp: int
    bond_score: int
    mood: str
    stats: CreatureStats

    model_config = ConfigDict(from_attributes=True)

class CollectionEntryResponse(BaseModel):
    species_id: int
    species_code: str
    species_name: str
    tier: int
    status: str # AWAKENED, LOCKED, DISCOVERED
    unlocked_at: Optional[datetime] = None
    sprite_asset_key: Optional[str] = None
    silhouette_asset_key: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
