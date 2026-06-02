from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.baselines import list_baseline_files
from app.repositories.directories import get_directory
from app.schemas.baseline import BaselineFileRead, BaselineGenerateRequest, BaselineGenerateResponse
from app.services.baseline_service import generate_baseline

router = APIRouter(prefix="/baselines", tags=["baselines"])


@router.get("/files", response_model=list[BaselineFileRead])
def list_baseline_files_endpoint(directory_id: int | None = None, algorithm: str | None = None, db: Session = Depends(get_db)):
    return list_baseline_files(db, directory_id=directory_id, algorithm=algorithm)


@router.post("/generate", response_model=BaselineGenerateResponse, status_code=status.HTTP_201_CREATED)
def generate_baseline_endpoint(payload: BaselineGenerateRequest, db: Session = Depends(get_db)):
    directory = get_directory(db, payload.monitored_directory_id)
    if directory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Directory not found")
    try:
        files, total_size, duration_ms = generate_baseline(db, directory, payload.algorithm, payload.algorithm_params)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return BaselineGenerateResponse(
        monitored_directory_id=directory.id,
        algorithm=payload.algorithm,
        total_files=len(files),
        total_size_bytes=total_size,
        duration_ms=duration_ms,
        files=files,
    )
