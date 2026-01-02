from sqlalchemy import Column, String, Text, JSON, Integer
from .base import BaseModel

class CyberAsset(BaseModel):
    __tablename__ = "cyber_assets"

    domain = Column(String, index=True)
    ip_address = Column(String)
    subdomains = Column(JSON)  # List of subdomains
    dns_records = Column(JSON)  # DNS records
    whois_info = Column(JSON)  # WHOIS data
    ports = Column(JSON)  # Open ports
    vulnerabilities = Column(JSON)  # Known vulnerabilities
    notes = Column(Text)
    tags = Column(JSON)  # List of tags