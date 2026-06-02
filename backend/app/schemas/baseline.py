from pydantic import BaseModel

from app.schemas.common import OrmModel


class BaselineGenerateRequest(BaseModel):
    monitored_directory_id: int
    algorithm: str = "SHA-256"
    algorithm_params: dict | None = None


class BaselineFileRead(OrmModel):
    id: int
    monitored_directory_id: int
    relative_path: str
    absolute_path: str
    file_size_bytes: int
    last_modified_at: str | None
    algorithm: str
    algorithm_params: str | None
    hash_value: str
    hash_duration_ms: int | None
    baseline_created_at: str
    created_at: str
    updated_at: str


class BaselineGenerateResponse(BaseModel):
    monitored_directory_id: int
    algorithm: str
    total_files: int
    total_size_bytes: int
    duration_ms: int
    files: list[BaselineFileRead]
