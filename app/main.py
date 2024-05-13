import validators

from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse

from sqlalchemy.orm import Session

from app.crud import crud
from app.databases.database import SessionLocal, engine
from app.errors.errors import *
from app.models import models
from app.schemas import schemas

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/shorten", response_model=schemas.ShortURLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """
    원본 URL을 기반으로 축약된 URL을 생성합니다
    """
    if not validators.url(url.original_url):
        return raise_400_url(message="Provided URL is not valid")
    
    obj_url = crud.create_short_url(db=db, url=url)
    obj_url.short_url = obj_url.key
    return obj_url


@app.get("/{key}", status_code=301)
def get_forward(key: str, request: Request, db: Session = Depends(get_db)):
    import requests
    """
    원본 URL을 기반으로 생성된 key로 조회시 원본 URL로 redirect 합니다.
    key가 존재하지 않을 경우 404를 Response 합니다
    """        
    obj_url = crud.get_short_url(db=db, key=key)
    if obj_url:
        crud.increment_clicks(db=db, obj_model=obj_url)
        return RedirectResponse(url=obj_url.original_url, status_code=301)
    else:        
        return raise_url_404(request)


@app.get("/stats/{short_key}")
def get_stats(short_key: str, request: Request, db: Session = Depends(get_db)):
    """
    원본 URL을 기반으로 생성된 key로 조회시 해당 URL의 요청회수를 리턴합니다.
    """
    obj_url = crud.get_short_url(db=db, key=short_key)
    if obj_url:
        return JSONResponse(content={"clicks": obj_url.clicks}, status_code=200)
    return raise_key_400(request)
