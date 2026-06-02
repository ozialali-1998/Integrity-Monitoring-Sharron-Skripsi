from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.fim.path_validator import validate_directory_path
from app.repositories.directories import get_directory, list_directories
from app.schemas.directory import DirectoryCreate, DirectoryRead, DirectoryUpdate, PathValidationRequest, PathValidationResponse
from app.services.directory_service import create_directory, update_directory

router = APIRouter(prefix="/directories", tags=["directories"])


@router.get("", response_model=list[DirectoryRead])
def list_directory_endpoint(db: Session = Depends(get_db)):
    return list_directories(db)


@router.post("", response_model=DirectoryRead, status_code=status.HTTP_201_CREATED)
def create_directory_endpoint(payload: DirectoryCreate, db: Session = Depends(get_db)):
    try:
        return create_directory(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{directory_id}", response_model=DirectoryRead)
def get_directory_endpoint(directory_id: int, db: Session = Depends(get_db)):
    directory = get_directory(db, directory_id)
    if directory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Directory not found")
    return directory


@router.put("/{directory_id}", response_model=DirectoryRead)
def update_directory_endpoint(directory_id: int, payload: DirectoryUpdate, db: Session = Depends(get_db)):
    directory = get_directory(db, directory_id)
    if directory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Directory not found")
    try:
        return update_directory(db, directory, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{directory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_directory_endpoint(directory_id: int, db: Session = Depends(get_db)):
    directory = get_directory(db, directory_id)
    if directory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Directory not found")
    db.delete(directory)
    db.commit()


@router.post("/validate-path", response_model=PathValidationResponse)
def validate_path_endpoint(payload: PathValidationRequest):
    try:
        resolved = validate_directory_path(payload.path)
        return PathValidationResponse(valid=True, message="Path is valid", resolved_path=str(resolved))
    except ValueError as exc:
        return PathValidationResponse(valid=False, message=str(exc), resolved_path=None)
