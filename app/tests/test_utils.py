from collections import defaultdict

from fastapi.testclient import TestClient

from app.main import app
from app.utils.gen import gen_key

client = TestClient(app)
test_cnt = 1000000

def test_gen_key():
    assert len(gen_key()) == 9

def test_create_unique_key():
    dict = defaultdict(int)
    
    for _ in range(test_cnt):
        k = gen_key()
        dict[k] += 1
    count = sum(1 for value in dict.values() if value == 1)        
    
    assert test_cnt == count
