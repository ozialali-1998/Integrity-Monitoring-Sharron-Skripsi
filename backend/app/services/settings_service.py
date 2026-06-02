from sqlalchemy.orm import Session

from app.db.models import SystemSetting
from app.schemas.settings import SystemSettingCreate
from app.utils.time import utc_now


def create_setting(db: Session, payload: SystemSettingCreate) -> SystemSetting:
    now = utc_now()
    setting = SystemSetting(
        setting_key=payload.setting_key,
        setting_value=payload.setting_value,
        value_type=payload.value_type,
        description=payload.description,
        is_editable=1 if payload.is_editable else 0,
        created_at=now,
        updated_at=now,
    )
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting
