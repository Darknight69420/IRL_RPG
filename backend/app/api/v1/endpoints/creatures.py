from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.creature import Creature, CollectionEntry
from app.models.species import Species
from app.schemas.creature import CreatureResponse, SpeciesResponse, CollectionEntryResponse
from app.services.creature_service import CreatureService
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/current", response_model=CreatureResponse)
def get_current_creature(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    creature = db.query(Creature).filter(
        Creature.user_id == current_user.id,
        Creature.is_active == True
    ).first()
    
    if not creature:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NO_ACTIVE_CREATURE", "message": "No active companion found."}
        )

    character = current_user.character
    stats = CreatureService.calculate_stats(creature, character)
    streak = current_user.streak
    current_streak = streak.current_streak if streak else 0

    mood = CreatureService.determine_mood(
        bond_score=creature.bond_score,
        current_streak=current_streak,
        active_today=True
    )

    return CreatureResponse(
        id=creature.id,
        nickname=creature.nickname,
        species=SpeciesResponse.model_validate(creature.species),
        level=creature.level,
        current_xp=creature.current_xp,
        bond_score=creature.bond_score,
        mood=mood,
        stats=stats
    )

@router.get("/collection", response_model=List[CollectionEntryResponse])
def get_collection(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch all 15 species
    all_species = db.query(Species).order_by(Species.tier.asc(), Species.id.asc()).all()
    
    # Fetch user's unlocked entries
    unlocked_map = {
        col.species_id: col for col in db.query(CollectionEntry).filter(
            CollectionEntry.user_id == current_user.id
        ).all()
    }

    result = []
    for s in all_species:
        if s.id in unlocked_map:
            col = unlocked_map[s.id]
            result.append(CollectionEntryResponse(
                species_id=s.id,
                species_code=s.code,
                species_name=s.name,
                tier=s.tier,
                status=col.status,
                unlocked_at=col.unlocked_at,
                sprite_asset_key=s.sprite_asset_key,
                silhouette_asset_key=None
            ))
        else:
            result.append(CollectionEntryResponse(
                species_id=s.id,
                species_code=s.code,
                species_name="???",
                tier=s.tier,
                status="LOCKED",
                unlocked_at=None,
                sprite_asset_key=None,
                silhouette_asset_key=f"{s.code.lower()}_locked"
            ))
    return result

@router.post("/active/{species_id}", response_model=CreatureResponse)
def set_active_creature(
    species_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify user has awakened this species in their Lifedex
    unlocked = db.query(CollectionEntry).filter(
        CollectionEntry.user_id == current_user.id,
        CollectionEntry.species_id == species_id,
        CollectionEntry.status == "AWAKENED"
    ).first()

    if not unlocked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "FORM_NOT_UNLOCKED", "message": "You have not yet unlocked this companion in your Lifedex."}
        )

    species = db.query(Species).filter(Species.id == species_id).first()

    # Deactivate current
    db.query(Creature).filter(Creature.user_id == current_user.id).update({"is_active": False})

    # Check if creature instance exists for this species, or switch the existing primary creature's species
    creature = db.query(Creature).filter(
        Creature.user_id == current_user.id
    ).first()

    if creature:
        creature.species_id = species_id
        creature.species = species
        creature.is_active = True
    else:
        creature = Creature(
            user_id=current_user.id,
            species_id=species_id,
            nickname=f"{species.name}",
            level=1,
            current_xp=0,
            bond_score=20,
            is_active=True
        )
        db.add(creature)

    db.commit()
    db.refresh(creature)

    character = current_user.character
    stats = CreatureService.calculate_stats(creature, character)
    streak = current_user.streak
    current_streak = streak.current_streak if streak else 0

    return CreatureResponse(
        id=creature.id,
        nickname=creature.nickname,
        species=SpeciesResponse.model_validate(species),
        level=creature.level,
        current_xp=creature.current_xp,
        bond_score=creature.bond_score,
        mood="CONTENT",
        stats=stats
    )
