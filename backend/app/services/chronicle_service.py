import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.chronicle import ChronicleEvent

class ChronicleService:
    @staticmethod
    def record_event(
        db: Session,
        user_id: int,
        event_type: str,
        title: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ChronicleEvent:
        metadata_str = json.dumps(metadata) if metadata else None
        event = ChronicleEvent(
            user_id=user_id,
            event_type=event_type,
            title=title,
            description=description,
            metadata_json=metadata_str,
            created_at=datetime.now(timezone.utc)
        )
        db.add(event)
        return event
