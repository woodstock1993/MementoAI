from datetime import datetime
import requests

from fastapi.testclient import TestClient

from app.main import app
from app.tests.utils import reset_database

client = TestClient(app)

def test_create_url():
    reset_database()
    
    test_url = "https://google.com"
    response = client.post("/shorten", json={"original_url": test_url})
    assert response.status_code == 200
    key = response.json()["short_url"]
    assert "short_url" in response.json()

def test_create_url_2():
    reset_database()
    
    test_url = "https://google.com"
    response = client.post("/shorten", json={"original_url": test_url, "expiration_date": datetime.today().isoformat()})
    assert response.status_code == 200
    key = response.json()["short_url"]
    assert "short_url" in response.json()

def test_invalid_url():
    reset_database()
    
    invalid_url = "invalid_url"
    response = client.post("/shorten", json={"original_url": invalid_url})
    assert response.status_code == 400
    assert "Provided URL is not valid" in response.text
    
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
