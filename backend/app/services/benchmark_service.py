from statistics import mean
from sqlalchemy.orm import Session

from app.db.models import BenchmarkResult, MonitoredDirectory
from app.fim.file_scanner import scan_directory
from app.hashing.hashers import hash_file, normalize_algorithm, params_to_json
from app.utils.time import utc_now
from app.utils.timer import Timer


def run_benchmark(db: Session, directory: MonitoredDirectory, algorithms: list[str], params: dict[str, dict] | None = None) -> list[BenchmarkResult]:
    files = scan_directory(directory.path)
    results: list[BenchmarkResult] = []
    params = params or {}

    for algorithm in algorithms:
        normalized = normalize_algorithm(algorithm)
        started_at = utc_now()
        durations: list[int] = []
        total_size = 0
        effective_params = params.get(normalized) or params.get(algorithm) or None
        with Timer() as total_timer:
            for item in files:
                _, duration_ms, used_params = hash_file(item.absolute_path, normalized, effective_params)
                effective_params = used_params
                durations.append(duration_ms)
                total_size += item.file_size_bytes
        finished_at = utc_now()
        duration_seconds = total_timer.duration_ms / 1000 if total_timer.duration_ms else 0
        throughput = (total_size / 1024 / 1024 / duration_seconds) if duration_seconds else None
        result = BenchmarkResult(
            monitored_directory_id=directory.id,
            algorithm=normalized,
            algorithm_params=params_to_json(effective_params),
            total_files=len(files),
            total_size_bytes=total_size,
            total_duration_ms=total_timer.duration_ms,
            average_duration_ms=mean(durations) if durations else None,
            min_duration_ms=min(durations) if durations else None,
            max_duration_ms=max(durations) if durations else None,
            throughput_mb_per_sec=throughput,
            benchmark_started_at=started_at,
            benchmark_finished_at=finished_at,
            created_at=finished_at,
        )
        db.add(result)
        results.append(result)
    db.commit()
    for result in results:
        db.refresh(result)
    return results
