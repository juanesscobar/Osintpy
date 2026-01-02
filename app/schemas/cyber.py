from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class CyberAssetBase(BaseModel):
    domain: Optional[str] = None
    ip_address: Optional[str] = None
    subdomains: Optional[List[str]] = []
    dns_records: Optional[Dict] = {}
    whois_info: Optional[Dict] = {}
    ports: Optional[List[int]] = []
    vulnerabilities: Optional[List[Dict]] = []
    notes: Optional[str] = None
    tags: Optional[List[str]] = []

class CyberAssetCreate(CyberAssetBase):
    domain: str

class CyberAssetUpdate(CyberAssetBase):
    pass

class CyberAsset(CyberAssetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True