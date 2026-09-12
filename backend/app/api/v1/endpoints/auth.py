from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User
from app.models.character import Character, CharacterAttribute
from app.models.streak import Streak
from app.models.species import Species
from app.models.creature import Creature, CollectionEntry
from app.services.chronicle_service import ChronicleService
from app.schemas.auth import UserCreate, UserLogin, UserResponse, Token
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check existing user
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "USERNAME_TAKEN", "message": "Username is already registered."}
        )
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "EMAIL_TAKEN", "message": "Email is already registered."}
        )

    # 1. Create User
    now = datetime.now(timezone.utc)
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        timezone=user_in.timezone or "UTC",
        created_at=now,
        updated_at=now
    )
    db.add(user)
    db.flush()

    # 2. Create Character & 6 Baseline Attributes
    character = Character(user_id=user.id, level=1, current_xp=0, created_at=now, updated_at=now)
    db.add(character)
    db.flush()

    for attr_code in ["STR", "INT", "WIS", "DIS", "VIT", "CHA"]:
        char_attr = CharacterAttribute(character_id=character.id, code=attr_code, value=0.0)
        db.add(char_attr)

    # 3. Create Streak
    streak = Streak(user_id=user.id, current_streak=0, longest_streak=0, updated_at=now)
    db.add(streak)

    # 4. Awaken Starter Companion: Aetherling (Species #1)
    starter_species = db.query(Species).filter(Species.code == "AETHERLING").first()
    if not starter_species:
        # Fallback if seed hadn't run
        from app.services.seed_data import seed_database
        seed_database(db)
        starter_species = db.query(Species).filter(Species.code == "AETHERLING").first()

    creature = Creature(
        user_id=user.id,
        species_id=starter_species.id,
        nickname=f"{user.username}'s Companion",
        level=1,
        current_xp=0,
        bond_score=15,
        is_active=True,
        created_at=now,
        updated_at=now
    )
    db.add(creature)

    # 5. Register starter in Lifedex
    col_entry = CollectionEntry(
        user_id=user.id,
        species_id=starter_species.id,
        status="AWAKENED",
        unlocked_at=now
    )
    db.add(col_entry)

    # 6. Record Welcome Chronicle Entry
    ChronicleService.record_event(
        db=db,
        user_id=user.id,
        event_type="COMPANION_AWAKENED",
        title="An Aetherling has awakened!",
        description="A morphic star-wisp materialized, resonating with your latent ambition.",
        metadata={"species": "AETHERLING", "tier": 1}
    )

    db.commit()
    db.refresh(user)

    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer", user=UserResponse.model_validate(user))

@router.post("/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_in.username).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error_code": "INVALID_CREDENTIALS", "message": "Incorrect username or password."}
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "INACTIVE_USER", "message": "User account is inactive."}
        )

    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer", user=UserResponse.model_validate(user))

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
