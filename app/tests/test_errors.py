from fastapi import HTTPException, Request
from unittest.mock import MagicMock
import pytest

from app.errors.errors import raise_400_url, raise_url_404, raise_key_400

@pytest.fixture
def mock_request():
    return MagicMock(spec=Request)

def test_raise_400_url():
    message = "Test message"
    with pytest.raises(HTTPException) as exc_info:
        raise_400_url(message)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == message

def test_raise_url_404(mock_request):
    mock_request.url = "http://test.com"
    with pytest.raises(HTTPException) as exc_info:
        raise_url_404(mock_request)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Provided {mock_request.url} does not exist"

def test_raise_key_400(mock_request):
    with pytest.raises(HTTPException) as exc_info:
        raise_key_400(mock_request)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Provided key does not exist"
