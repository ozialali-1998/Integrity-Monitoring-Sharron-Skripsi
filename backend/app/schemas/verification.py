from pydantic import BaseModel

from app.schemas.common import OrmModel


class VerificationRequest(BaseModel):
    monitored_directory_id: int
    algorithm: str = "SHA-256"


class IntegrityLogRead(OrmModel):
    id: int
    monitored_directory_id: int
    baseline_file_id: int | None
    event_type: str
    relative_path: str
    previous_hash: str | None
    current_hash: str | None
    previous_size_bytes: int | None
    current_size_bytes: int | None
    previous_modified_at: str | None
    current_modified_at: str | None
    severity: str
    status: str
    message: str | None
    checked_at: str
    verification_duration_ms: int | None
    created_at: str


class VerificationResponse(BaseModel):
    monitored_directory_id: int
    algorithm: str
    total_checked: int
    unchanged_count: int
    modified_count: int
    added_count: int
    deleted_count: int
    error_count: int
    duration_ms: int
    logs: list[IntegrityLogRead]
