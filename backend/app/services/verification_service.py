from sqlalchemy.orm import Session

from app.db.models import BaselineFile, IntegrityLog, MonitoredDirectory
from app.fim.change_classifier import severity_for_event
from app.fim.file_scanner import scan_directory
from app.hashing.hashers import hash_file, normalize_algorithm, params_from_json
from app.utils.time import utc_now
from app.utils.timer import Timer


def _make_log(
    directory_id: int,
    event_type: str,
    relative_path: str,
    baseline_file: BaselineFile | None = None,
    current_hash: str | None = None,
    current_size: int | None = None,
    current_modified_at: str | None = None,
    duration_ms: int | None = None,
    message: str | None = None,
) -> IntegrityLog:
    now = utc_now()
    return IntegrityLog(
        monitored_directory_id=directory_id,
        baseline_file_id=baseline_file.id if baseline_file else None,
        event_type=event_type,
        relative_path=relative_path,
        previous_hash=baseline_file.hash_value if baseline_file else None,
        current_hash=current_hash,
        previous_size_bytes=baseline_file.file_size_bytes if baseline_file else None,
        current_size_bytes=current_size,
        previous_modified_at=baseline_file.last_modified_at if baseline_file else None,
        current_modified_at=current_modified_at,
        severity=severity_for_event(event_type),
        status="RESOLVED" if event_type == "UNCHANGED" else "OPEN",
        message=message or f"File status: {event_type}",
        checked_at=now,
        verification_duration_ms=duration_ms,
        created_at=now,
    )


def verify_directory(db: Session, directory: MonitoredDirectory, algorithm: str) -> tuple[list[IntegrityLog], dict[str, int], int]:
    normalized = normalize_algorithm(algorithm)
    baseline_files = (
        db.query(BaselineFile)
        .filter(BaselineFile.monitored_directory_id == directory.id, BaselineFile.algorithm == normalized)
        .all()
    )
    baseline_by_path = {item.relative_path: item for item in baseline_files}
    current_files = scan_directory(directory.path)
    current_by_path = {item.relative_path: item for item in current_files}
    logs: list[IntegrityLog] = []
    counts = {"UNCHANGED": 0, "MODIFIED": 0, "ADDED": 0, "DELETED": 0, "ERROR": 0}

    with Timer() as timer:
        for relative_path, baseline_file in baseline_by_path.items():
            current = current_by_path.get(relative_path)
            if current is None:
                event_type = "DELETED"
                log = _make_log(directory.id, event_type, relative_path, baseline_file=baseline_file)
            else:
                try:
                    current_hash, duration_ms, _ = hash_file(current.absolute_path, normalized, params_from_json(baseline_file.algorithm_params))
                    event_type = "UNCHANGED" if current_hash == baseline_file.hash_value else "MODIFIED"
                    log = _make_log(
                        directory.id,
                        event_type,
                        relative_path,
                        baseline_file=baseline_file,
                        current_hash=current_hash,
                        current_size=current.file_size_bytes,
                        current_modified_at=current.last_modified_at,
                        duration_ms=duration_ms,
                    )
                except Exception as exc:
                    event_type = "ERROR"
                    log = _make_log(directory.id, event_type, relative_path, baseline_file=baseline_file, message=str(exc))
            counts[event_type] += 1
            db.add(log)
            logs.append(log)

        known_paths = set(baseline_by_path)
        default_params = params_from_json(baseline_files[0].algorithm_params) if baseline_files else None
        for relative_path, current in current_by_path.items():
            if relative_path in known_paths:
                continue
            try:
                current_hash, duration_ms, _ = hash_file(current.absolute_path, normalized, default_params)
                event_type = "ADDED"
                log = _make_log(
                    directory.id,
                    event_type,
                    relative_path,
                    current_hash=current_hash,
                    current_size=current.file_size_bytes,
                    current_modified_at=current.last_modified_at,
                    duration_ms=duration_ms,
                )
            except Exception as exc:
                event_type = "ERROR"
                log = _make_log(directory.id, event_type, relative_path, message=str(exc))
            counts[event_type] += 1
            db.add(log)
            logs.append(log)
    db.commit()
    for log in logs:
        db.refresh(log)
    return logs, counts, timer.duration_ms
