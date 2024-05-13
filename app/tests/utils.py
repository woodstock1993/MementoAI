from app.main import app, SessionLocal
from app.models.models import URL

def reset_database():
    db = SessionLocal()
    db.query(URL).delete()
    db.commit()
    db.close()