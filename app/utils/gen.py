import secrets
import string

from sqlalchemy.orm import Session
from app.crud import crud

def gen_key(length: int=6) -> str:
    candidates = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(candidates) for _ in range(length))

def create_unique_key(db: Session) -> str:
    key = gen_key()
    while crud.get_short_url(db, key):
        key = gen_key()
    return key

