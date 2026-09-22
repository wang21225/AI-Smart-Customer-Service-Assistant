from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.responses import success
from app.db.session import get_db
from app.models import SystemConfig

router = APIRouter()


class ConfigUpdate(BaseModel):
    values: dict[str, str]


@router.get("/config")
def get_config(db: Session = Depends(get_db)):
    items = db.query(SystemConfig).all()
    return success({item.config_key: item.config_value for item in items})


@router.put("/config")
def update_config(payload: ConfigUpdate, db: Session = Depends(get_db)):
    for key, value in payload.values.items():
        item = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
        if item:
            item.config_value = value
        else:
            db.add(SystemConfig(config_key=key, config_value=value))
    db.commit()
    return success(True)
