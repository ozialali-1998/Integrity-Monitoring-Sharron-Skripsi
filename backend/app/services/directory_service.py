from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import MonitoredDirectory
from app.fim.path_validator import validate_directory_path
from app.schemas.directory import DirectoryCreate, DirectoryUpdate
from app.utils.time import utc_now


def create_directory(db: Session, payload: DirectoryCreate) -> MonitoredDirectory:
    resolved = validate_directory_path(payload.path)
    now = utc_now()
    directory = MonitoredDirectory(
        name=payload.name,
        path=str(resolved),
        description=payload.description,
        is_active=1 if payload.is_active else 0,
        created_at=now,
        updated_at=now,
    )
    db.add(directory)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("Directory path already exists") from exc
    db.refresh(directory)
    return directory


def update_directory(db: Session, directory: MonitoredDirectory, payload: DirectoryUpdate) -> MonitoredDirectory:
    if payload.name is not None:
        directory.name = payload.name
    if payload.path is not None:
        directory.path = str(validate_directory_path(payload.path))
    if payload.description is not None:
        directory.description = payload.description
    if payload.is_active is not None:
        directory.is_active = 1 if payload.is_active else 0
    directory.updated_at = utc_now()
    db.commit()
    db.refresh(directory)
    return directory
