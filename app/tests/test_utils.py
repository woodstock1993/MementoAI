from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

from app.utils.gen import gen_key

def test_gen_key():
    assert len(gen_key()) == 6
