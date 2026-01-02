from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class CompanyBase(BaseModel):
    name: Optional[str] = None
    ruc: Optional[str] = None
    domain: Optional[str] = None
    description: Optional[str] = None
    social_profiles: Optional[Dict[str, str]] = {}
    employees: Optional[List[str]] = []
    notes: Optional[str] = None
    tags: Optional[List[str]] = []

class CompanyCreate(CompanyBase):
    name: str
    ruc: str

class CompanyUpdate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True