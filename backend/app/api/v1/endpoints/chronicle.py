import json
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.chronicle import ChronicleEvent
from app.schemas.chronicle import ChronicleEventResponse, PaginatedChronicleResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.get("", response_model=PaginatedChronicleResponse)
def get_chronicle(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(ChronicleEvent).filter(ChronicleEvent.user_id == current_user.id)
    total = query.count()
    events = query.order_by(ChronicleEvent.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    items = []
    for ev in events:
        meta_dict = None
        if ev.metadata_json:
            try:
                meta_dict = json.loads(ev.metadata_json)
            except Exception:
                meta_dict = None
        items.append(ChronicleEventResponse(
            id=ev.id,
            user_id=ev.user_id,
            event_type=ev.event_type,
            title=ev.title,
            description=ev.description,
            metadata=meta_dict,
            created_at=ev.created_at
        ))

    return PaginatedChronicleResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=items
    )
