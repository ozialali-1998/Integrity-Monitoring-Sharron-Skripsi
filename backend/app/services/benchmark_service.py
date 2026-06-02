from statistics import mean
from sqlalchemy.orm import Session

from app.db.models import BenchmarkResult, MonitoredDirectory
from app.fim.file_scanner import scan_directory
from app.hashing.hashers import hash_file, normalize_algorithm, params_to_json
from app.utils.benchmark_metrics import calculate_accuracy_percent
from app.utils.resource_monitor import ResourceMonitor
from app.utils.time import utc_now


def run_benchmark(db: Session, directory: MonitoredDirectory, algorithms: list[str], params: dict[str, dict] | None = None) -> list[BenchmarkResult]:
    files = scan_directory(directory.path)
    results: list[BenchmarkResult] = []
    params = params or {}

    for algorithm in algorithms:
        normalized = normalize_algorithm(algorithm)
        started_at = utc_now()
        durations: list[int] = []
        verification_duration_total_ms = 0
        verification_matches = 0
        verification_mismatches = 0
        total_size = 0
        effective_params = params.get(normalized) or params.get(algorithm) or None

        with ResourceMonitor() as resource_monitor:
            for item in files:
                digest, duration_ms, used_params = hash_file(item.absolute_path, normalized, effective_params)
                effective_params = used_params
                durations.append(duration_ms)
                total_size += item.file_size_bytes
                resource_monitor.sample()

                verification_digest, verification_duration_ms, _ = hash_file(item.absolute_path, normalized, used_params)
                verification_duration_total_ms += verification_duration_ms
                if verification_digest == digest:
                    verification_matches += 1
                else:
                    verification_mismatches += 1
                resource_monitor.sample()

        finished_at = utc_now()
        total_duration_ms = sum(durations)
        duration_seconds = total_duration_ms / 1000 if total_duration_ms else 0
        throughput = (total_size / 1024 / 1024 / duration_seconds) if duration_seconds else None
        resource_summary = resource_monitor.summary()
        result = BenchmarkResult(
            monitored_directory_id=directory.id,
            algorithm=normalized,
            algorithm_params=params_to_json(effective_params),
            total_files=len(files),
            total_size_bytes=total_size,
            total_duration_ms=total_duration_ms,
            average_duration_ms=mean(durations) if durations else None,
            min_duration_ms=min(durations) if durations else None,
            max_duration_ms=max(durations) if durations else None,
            throughput_mb_per_sec=throughput,
            verification_duration_ms=verification_duration_total_ms,
            accuracy_percent=calculate_accuracy_percent(len(files), verification_matches),
            verification_matches=verification_matches,
            verification_mismatches=verification_mismatches,
            average_cpu_percent=resource_summary.average_cpu_percent,
            max_cpu_percent=resource_summary.max_cpu_percent,
            memory_start_bytes=resource_summary.memory_start_bytes,
            memory_end_bytes=resource_summary.memory_end_bytes,
            memory_peak_bytes=resource_summary.memory_peak_bytes,
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
