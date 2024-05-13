from datetime import datetime

from fastapi.testclient import TestClient

from app.crud.crud import get_short_url, increment_clicks
from app.main import app, SessionLocal
from app.models.models import URL
from app.tests.utils import reset_database

client = TestClient(app)

def test_get_short_url():    
    test_url = "https://google.com"
    reset_database()
    
    response = client.post("/shorten", json={"original_url": test_url})
    db = SessionLocal()
    test_key = response.json()["short_url"]
    retrieved_url = get_short_url(db, test_key)
    assert retrieved_url is not None
    assert retrieved_url.key == test_key


def test_increment_clicks():
    test_url = "https://google.com"
    reset_database()
    
    db = SessionLocal()
    url_obj = URL(original_url="https://google.com", is_active=True, clicks=0)

    db.add(url_obj)
    db.commit()

    increment_clicks(db, url_obj)
    assert url_obj.clicks == 1
