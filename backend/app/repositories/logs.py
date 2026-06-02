from sqlalchemy.orm import Session

from app.db.models import IntegrityLog


def list_logs(db: Session, directory_id: int | None = None, event_type: str | None = None) -> list[IntegrityLog]:
    query = db.query(IntegrityLog)
    if directory_id is not None:
        query = query.filter(IntegrityLog.monitored_directory_id == directory_id)
    if event_type is not None:
        query = query.filter(IntegrityLog.event_type == event_type)
    return query.order_by(IntegrityLog.id.desc()).all()
