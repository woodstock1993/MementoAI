from datetime import datetime

from fastapi.testclient import TestClient

from app.crud.crud import create_expiration_date, get_short_url, increment_clicks
from app.main import app, SessionLocal
from app.schemas.schemas import URLBase
from app.models.models import URL

client = TestClient(app)
key = None

def test_get_short_url():
    global key
    
    db = SessionLocal()
    test_key = key
    retrieved_url = get_short_url(db, test_key)
    assert retrieved_url is not None
    assert retrieved_url.key == test_key

    db.rollback()
    db.close()

def test_increment_clicks():
    db = SessionLocal()
    url_obj = URL(original_url="https://google.com", is_active=True, clicks=0)
    db.add(url_obj)
    db.commit()

    increment_clicks(db, url_obj)
    assert url_obj.clicks == 1

    db.rollback()
    db.close()
