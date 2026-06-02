from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.logs import list_logs
from app.schemas.verification import IntegrityLogRead

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("", response_model=list[IntegrityLogRead])
def list_integrity_logs_endpoint(directory_id: int | None = None, event_type: str | None = None, db: Session = Depends(get_db)):
    return list_logs(db, directory_id=directory_id, event_type=event_type)
