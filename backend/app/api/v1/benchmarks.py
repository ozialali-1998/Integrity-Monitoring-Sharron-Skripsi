from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import BenchmarkResult
from app.repositories.directories import get_directory
from app.schemas.benchmark import BenchmarkRequest, BenchmarkResultRead
from app.services.benchmark_service import run_benchmark

router = APIRouter(prefix="/benchmarks", tags=["benchmarks"])


@router.get("", response_model=list[BenchmarkResultRead])
def list_benchmarks_endpoint(db: Session = Depends(get_db)):
    return db.query(BenchmarkResult).order_by(BenchmarkResult.id.desc()).all()


@router.post("/run", response_model=list[BenchmarkResultRead], status_code=status.HTTP_201_CREATED)
def run_benchmark_endpoint(payload: BenchmarkRequest, db: Session = Depends(get_db)):
    directory = get_directory(db, payload.monitored_directory_id)
    if directory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Directory not found")
    try:
        return run_benchmark(db, directory, payload.algorithms, payload.params)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
