from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.directories import get_directory
from app.repositories.logs import list_logs
from app.schemas.verification import IntegrityLogRead, VerificationRequest, VerificationResponse
from app.services.verification_service import verify_directory

router = APIRouter(prefix="/verifications", tags=["verifications"])


@router.post("/run", response_model=VerificationResponse, status_code=status.HTTP_201_CREATED)
def run_verification_endpoint(payload: VerificationRequest, db: Session = Depends(get_db)):
    directory = get_directory(db, payload.monitored_directory_id)
    if directory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Directory not found")
    try:
        logs, counts, duration_ms = verify_directory(db, directory, payload.algorithm)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return VerificationResponse(
        monitored_directory_id=directory.id,
        algorithm=payload.algorithm,
        total_checked=len(logs),
        unchanged_count=counts["UNCHANGED"],
        modified_count=counts["MODIFIED"],
        added_count=counts["ADDED"],
        deleted_count=counts["DELETED"],
        error_count=counts["ERROR"],
        duration_ms=duration_ms,
        logs=logs,
    )


@router.get("/logs", response_model=list[IntegrityLogRead])
def list_verification_logs_endpoint(directory_id: int | None = None, event_type: str | None = None, db: Session = Depends(get_db)):
    return list_logs(db, directory_id=directory_id, event_type=event_type)
