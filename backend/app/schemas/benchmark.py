from pydantic import BaseModel

from app.schemas.common import OrmModel


class BenchmarkRequest(BaseModel):
    monitored_directory_id: int
    algorithms: list[str] = ["SHA-256", "PBKDF2", "Argon2id"]
    params: dict[str, dict] | None = None


class BenchmarkResultRead(OrmModel):
    id: int
    monitored_directory_id: int | None
    algorithm: str
    algorithm_params: str | None
    total_files: int
    total_size_bytes: int
    total_duration_ms: int
    average_duration_ms: float | None
    min_duration_ms: float | None
    max_duration_ms: float | None
    throughput_mb_per_sec: float | None
    verification_duration_ms: int | None
    accuracy_percent: float | None
    verification_matches: int
    verification_mismatches: int
    average_cpu_percent: float | None
    max_cpu_percent: float | None
    memory_start_bytes: int | None
    memory_end_bytes: int | None
    memory_peak_bytes: int | None
    benchmark_started_at: str
    benchmark_finished_at: str | None
    created_at: str
