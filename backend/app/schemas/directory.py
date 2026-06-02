from pydantic import BaseModel, Field

from app.schemas.common import OrmModel


class DirectoryCreate(BaseModel):
    name: str = Field(min_length=1)
    path: str = Field(min_length=1)
    description: str | None = None
    is_active: bool = True


class DirectoryUpdate(BaseModel):
    name: str | None = None
    path: str | None = None
    description: str | None = None
    is_active: bool | None = None


class DirectoryRead(OrmModel):
    id: int
    name: str
    path: str
    description: str | None
    is_active: int
    created_at: str
    updated_at: str


class PathValidationRequest(BaseModel):
    path: str


class PathValidationResponse(BaseModel):
    valid: bool
    message: str
    resolved_path: str | None = None
