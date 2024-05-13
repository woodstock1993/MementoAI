from pydantic import BaseModel

class URLBase(BaseModel):
    original_url: str

class URL(URLBase):
    is_active: bool
    clicks: int
    
    class Config:
        orm_mode = True

class URLInfo(URL):
    short_url: str
    admin_url: str
    
class ShortURLInfo(BaseModel):
    short_url: str