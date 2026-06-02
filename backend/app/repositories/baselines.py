from sqlalchemy.orm import Session

from app.db.models import BaselineFile


def list_baseline_files(db: Session, directory_id: int | None = None, algorithm: str | None = None) -> list[BaselineFile]:
    query = db.query(BaselineFile)
    if directory_id is not None:
        query = query.filter(BaselineFile.monitored_directory_id == directory_id)
    if algorithm is not None:
        query = query.filter(BaselineFile.algorithm == algorithm)
    return query.order_by(BaselineFile.relative_path.asc()).all()
