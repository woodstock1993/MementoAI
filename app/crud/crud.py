from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ..models import models

from app.schemas import schemas

from ..utils import gen

def create_short_url(db: Session, url: schemas.URLBase) -> models.URL:
    key = gen.create_unique_key(db)
    secret_key = f"{key}_{gen.gen_key(length=8)}"
    exp_date = create_expiration_date(5)
    obj_url = models.URL(original_url=url.original_url, key=key, secret_key=secret_key, expiration_date=exp_date)    
    db.add(obj_url)
    db.commit()
    db.refresh(obj_url)
    return obj_url

def create_expiration_date(expiration_days: int) -> datetime:
    current_date = datetime.now()
    return current_date + timedelta(seconds=expiration_days)

def get_short_url(db: Session, key: str) -> models.URL:
    return db.query(models.URL).filter(models.URL.key==key, models.URL.is_active).first()

def increment_clicks(db: Session, obj_model: models.URL):
    obj_model.clicks += 1
    db.commit()