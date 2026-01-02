from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class InvestigationBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "active"
    target_person_id: Optional[int] = None
    target_company_id: Optional[int] = None
    target_cyber_asset_id: Optional[int] = None
    findings: Optional[Dict] = {}
    notes: Optional[str] = None
    tags: Optional[List[str]] = []

class InvestigationCreate(InvestigationBase):
    title: str

class InvestigationUpdate(InvestigationBase):
    pass

class Investigation(InvestigationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True