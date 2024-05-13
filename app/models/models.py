from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.databases.database import Base

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True)
    original_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
    
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    
    expiration_date = Column(DateTime)  # 만료기간 필드 추가