from pydantic import BaseModel

from app.schemas.common import OrmModel


class SystemSettingCreate(BaseModel):
    setting_key: str
    setting_value: str
    value_type: str = "string"
    description: str | None = None
    is_editable: bool = True


class SystemSettingRead(OrmModel):
    id: int
    setting_key: str
    setting_value: str
    value_type: str
    description: str | None
    is_editable: int
    created_at: str
    updated_at: str
