from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

class PersonBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    social_profiles: Optional[Dict[str, str]] = {}
    notes: Optional[str] = None
    tags: Optional[List[str]] = []

class PersonCreate(PersonBase):
    name: str
    email: EmailStr

class PersonUpdate(PersonBase):
    pass

class Person(PersonBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True