from datetime import datetime

from celery import Celery

from sqlalchemy.orm import Session

from .models import models
from celeryconfig import *

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.config_from_object('celeryconfig')

@celery.task
def update_urls():
    import logging
    from .main import get_db
    """
    만료된 URL의 active를 False로 설정하는 Task
    """    
    db: Session = next(get_db())
    today = datetime.now()
    try:        
        expired_urls = db.query(models.URL).filter(models.URL.expiration_date < today, models.URL.is_active == True).all()
        for url in expired_urls:
            url.is_active = False        
        db.commit()
        logging.info('--------------------------------------------')
        logging.info(f'inactive 처리된 key 개수: {len(expired_urls)}')        
        logging.info('--------------------------------------------')
    except Exception as e:
        # 에러 발생 시 롤백
        db.rollback()
        raise e
    finally:
        db.close()
    return len(expired_urls)
