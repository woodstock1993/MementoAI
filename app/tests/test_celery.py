import time
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.tasks import update_urls
from app.tests.utils import reset_database

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_update_urls(client, monkeypatch):
    reset_database()
    url = "https://google.com/"
    for _ in range(10):
        response = client.post("/shorten", json={"original_url": url})
        assert response.status_code == 200
    
    time.sleep(5)
    
    result = update_urls.delay()
    rows = result.get()
    assert rows == 10