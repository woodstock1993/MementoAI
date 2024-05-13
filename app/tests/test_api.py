import requests

from fastapi.testclient import TestClient
from app.main import app, SessionLocal
from app.tests.utils import reset_database

client = TestClient(app)

def test_create_url():
    reset_database()
    
    test_url = "https://google.com"
    response = client.post("/shorten", json={"original_url": test_url})
    assert response.status_code == 200
    key = response.json()["short_url"]
    assert "short_url" in response.json()
    
def test_get_forward():
    reset_database()
    
    test_url = "https://google.com"
    response = client.post("/shorten", json={"original_url": test_url})    
    key = response.json()["short_url"]
    response = requests.get(f"http://localhost:8000/{key}")
    assert response.status_code == 200

def test_get_stats():
    reset_database()
    
    test_url = "https://google.com"
    response = client.post("/shorten", json={"original_url": test_url})    
    key = response.json()["short_url"]    
    response = client.get(f"/stats/{key}")
    assert response.status_code == 200
    assert "clicks" in response.json()
