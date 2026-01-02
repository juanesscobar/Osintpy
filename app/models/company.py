from sqlalchemy import Column, String, Text, JSON
from .base import BaseModel

class Company(BaseModel):
    __tablename__ = "companies"

    name = Column(String, index=True)
    ruc = Column(String, unique=True, index=True)  # RUC for Paraguay
    domain = Column(String, unique=True, index=True)
    description = Column(Text)
    social_profiles = Column(JSON)  # Dict of social media profiles
    employees = Column(JSON)  # List of employee names or IDs
    notes = Column(Text)
    tags = Column(JSON)  # List of tags