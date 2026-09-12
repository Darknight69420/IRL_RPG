from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.activity import Activity
from app.core.exceptions import ResourceNotFoundException, UnauthorizedResourceAccessException
from app.schemas.activity import (
    ActivityCreate, ActivityUpdate, ActivityResponse,
    ActivityCompleteRequest, ActivityCompletionResponse
)
from app.services.game_engine import GameEngine
from app.services.streak_service import StreakService
from app.api.deps import get_current_user

router = APIRouter()

def _to_response(activity: Activity, user_tz: str) -> ActivityResponse:
    today_local = StreakService.get_user_current_date(user_tz)
    completed_today = False
    if activity.last_completed_at:
        last_date = activity.last_completed_at.astimezone(timezone.utc).date()
        completed_today = (last_date == today_local)

    return ActivityResponse(
        id=activity.id,
        user_id=activity.user_id,
        title=activity.title,
        description=activity.description,
        category=activity.category,
        difficulty=activity.difficulty,
        primary_attribute=activity.primary_attribute,
        secondary_attribute=activity.secondary_attribute,
        cooldown_hours=activity.cooldown_hours,
        is_active=activity.is_active,
        completed_today=completed_today,
        last_completed_at=activity.last_completed_at,
        created_at=activity.created_at
    )

@router.get("", response_model=List[ActivityResponse])
def get_activities(
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Activity).filter(Activity.user_id == current_user.id)
    if category:
        query = query.filter(Activity.category == category.upper())
    if is_active is not None:
        query = query.filter(Activity.is_active == is_active)
    
    activities = query.order_by(Activity.created_at.desc()).all()
    user_tz = current_user.timezone or "UTC"
    return [_to_response(a, user_tz) for a in activities]

@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_activity(
    activity_in: ActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    activity = Activity(
        user_id=current_user.id,
        title=activity_in.title,
        description=activity_in.description,
        category=activity_in.category.upper(),
        difficulty=activity_in.difficulty.upper(),
        primary_attribute=activity_in.primary_attribute.upper(),
        secondary_attribute=activity_in.secondary_attribute.upper() if activity_in.secondary_attribute else None,
        cooldown_hours=activity_in.cooldown_hours,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return _to_response(activity, current_user.timezone or "UTC")

@router.get("/{activity_id}", response_model=ActivityResponse)
def get_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise ResourceNotFoundException("Activity", activity_id)
    if activity.user_id != current_user.id:
        raise UnauthorizedResourceAccessException()
    return _to_response(activity, current_user.timezone or "UTC")

@router.patch("/{activity_id}", response_model=ActivityResponse)
def update_activity(
    activity_id: int,
    activity_in: ActivityUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise ResourceNotFoundException("Activity", activity_id)
    if activity.user_id != current_user.id:
        raise UnauthorizedResourceAccessException()

    update_data = activity_in.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        if field in ["category", "difficulty", "primary_attribute", "secondary_attribute"] and val:
            setattr(activity, field, val.upper())
        else:
            setattr(activity, field, val)

    db.commit()
    db.refresh(activity)
    return _to_response(activity, current_user.timezone or "UTC")

@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise ResourceNotFoundException("Activity", activity_id)
    if activity.user_id != current_user.id:
        raise UnauthorizedResourceAccessException()

    db.delete(activity)
    db.commit()
    return None

@router.post("/{activity_id}/complete", response_model=ActivityCompletionResponse)
def complete_activity(
    activity_id: int,
    request: Optional[ActivityCompleteRequest] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notes = request.notes if request else None
    return GameEngine.process_activity_completion(
        db=db,
        user=current_user,
        activity_id=activity_id,
        notes=notes
    )
