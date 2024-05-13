import requests

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
key = None

def test_create_url():
    global key
    test_url = "https://google.com"
    response = client.post("/shorten", json={"original_url": test_url})
    assert response.status_code == 200
    key = response.json()["short_url"]
    assert "short_url" in response.json()
    
def test_get_forward():
    global key
    response = requests.get(f"http://localhost:8000/{key}")
    assert response.status_code == 200

def test_get_stats():
    global key
    response = client.get(f"/stats/{key}")
    assert response.status_code == 200
    assert "clicks" in response.json()