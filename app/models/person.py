from sqlalchemy import Column, String, Text, JSON
from .base import BaseModel

class Person(BaseModel):
    __tablename__ = "persons"

    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    username = Column(String, unique=True, index=True)
    social_profiles = Column(JSON)  # Dict of social media profiles
    notes = Column(Text)
    tags = Column(JSON)  # List of tags