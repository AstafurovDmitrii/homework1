from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Advertisement(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    author: str
    created_at: datetime = datetime.now()

class AdvertisementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None