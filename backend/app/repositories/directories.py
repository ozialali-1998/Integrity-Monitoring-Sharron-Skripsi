from sqlalchemy.orm import Session

from app.db.models import MonitoredDirectory


def get_directory(db: Session, directory_id: int) -> MonitoredDirectory | None:
    return db.get(MonitoredDirectory, directory_id)


def list_directories(db: Session) -> list[MonitoredDirectory]:
    return db.query(MonitoredDirectory).order_by(MonitoredDirectory.id.desc()).all()
