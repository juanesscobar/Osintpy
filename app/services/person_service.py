from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.person import Person
from schemas.person import PersonCreate, PersonUpdate
from collectors.persons.email import EmailCollector
from collectors.persons.phone import PhoneCollector
from collectors.persons.username import UsernameCollector
from utils.http_client import HttpClient

class PersonService:
    """Service for person-related operations"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.http_client = HttpClient()

    async def get_person(self, person_id: int) -> Optional[Person]:
        """Get person by ID"""
        query = select(Person).where(Person.id == person_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_persons(self, skip: int = 0, limit: int = 100) -> List[Person]:
        """Get all persons with pagination"""
        query = select(Person).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_person(self, person: PersonCreate) -> Person:
        """Create a new person"""
        db_person = Person(**person.dict())
        self.db.add(db_person)
        await self.db.commit()
        await self.db.refresh(db_person)
        return db_person

    async def update_person(self, person_id: int, person_update: PersonUpdate) -> Optional[Person]:
        """Update an existing person"""
        db_person = await self.get_person(person_id)
        if not db_person:
            return None

        for field, value in person_update.dict(exclude_unset=True).items():
            setattr(db_person, field, value)

        await self.db.commit()
        await self.db.refresh(db_person)
        return db_person

    async def delete_person(self, person_id: int) -> bool:
        """Delete a person"""
        db_person = await self.get_person(person_id)
        if not db_person:
            return False

        await self.db.delete(db_person)
        await self.db.commit()
        return True

    async def collect_email_data(self, email: str) -> dict:
        """Collect OSINT data for an email"""
        collector = EmailCollector(self.http_client)
        return await collector.collect(email)

    async def collect_phone_data(self, phone: str) -> dict:
        """Collect OSINT data for a phone number"""
        collector = PhoneCollector(self.http_client)
        return await collector.collect(phone)

    async def collect_username_data(self, username: str) -> dict:
        """Collect OSINT data for a username"""
        collector = UsernameCollector(self.http_client)
        return await collector.collect(username)