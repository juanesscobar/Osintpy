from sqlalchemy import Column, String, Text, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Investigation(BaseModel):
    __tablename__ = "investigations"

    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="active")  # active, completed, paused
    target_person_id = Column(Integer, ForeignKey("persons.id"))
    target_company_id = Column(Integer, ForeignKey("companies.id"))
    target_cyber_asset_id = Column(Integer, ForeignKey("cyber_assets.id"))
    findings = Column(JSON)  # Collected data
    notes = Column(Text)
    tags = Column(JSON)  # List of tags

    # Relationships
    target_person = relationship("Person")
    target_company = relationship("Company")
    target_cyber_asset = relationship("CyberAsset")