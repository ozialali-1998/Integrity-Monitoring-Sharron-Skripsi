from sqlalchemy.orm import Session

from app.db.models import BaselineFile, MonitoredDirectory
from app.fim.file_scanner import scan_directory
from app.hashing.hashers import hash_file, normalize_algorithm, params_to_json
from app.utils.time import utc_now
from app.utils.timer import Timer


def generate_baseline(db: Session, directory: MonitoredDirectory, algorithm: str, params: dict | None = None) -> tuple[list[BaselineFile], int, int]:
    normalized = normalize_algorithm(algorithm)
    scanned_files = scan_directory(directory.path)
    now = utc_now()
    total_size = 0
    saved_files: list[BaselineFile] = []

    with Timer() as timer:
        for scanned in scanned_files:
            digest, hash_duration_ms, effective_params = hash_file(scanned.absolute_path, normalized, params)
            total_size += scanned.file_size_bytes
            existing = (
                db.query(BaselineFile)
                .filter(
                    BaselineFile.monitored_directory_id == directory.id,
                    BaselineFile.relative_path == scanned.relative_path,
                    BaselineFile.algorithm == normalized,
                )
                .one_or_none()
            )
            baseline_file = existing or BaselineFile(monitored_directory_id=directory.id, relative_path=scanned.relative_path, algorithm=normalized)
            baseline_file.absolute_path = scanned.absolute_path
            baseline_file.file_size_bytes = scanned.file_size_bytes
            baseline_file.last_modified_at = scanned.last_modified_at
            baseline_file.algorithm_params = params_to_json(effective_params)
            baseline_file.hash_value = digest
            baseline_file.hash_duration_ms = hash_duration_ms
            baseline_file.baseline_created_at = now
            baseline_file.updated_at = now
            if existing is None:
                baseline_file.created_at = now
                db.add(baseline_file)
            saved_files.append(baseline_file)
    db.commit()
    for item in saved_files:
        db.refresh(item)
    return saved_files, total_size, timer.duration_ms
