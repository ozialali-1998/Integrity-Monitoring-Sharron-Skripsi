from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import SystemSetting
from app.schemas.settings import SystemSettingCreate, SystemSettingRead
from app.services.settings_service import create_setting

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=list[SystemSettingRead])
def list_settings_endpoint(db: Session = Depends(get_db)):
    return db.query(SystemSetting).order_by(SystemSetting.setting_key.asc()).all()


@router.post("", response_model=SystemSettingRead, status_code=status.HTTP_201_CREATED)
def create_setting_endpoint(payload: SystemSettingCreate, db: Session = Depends(get_db)):
    return create_setting(db, payload)
