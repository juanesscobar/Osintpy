from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.person import Person
from models.company import Company
from models.cyber import CyberAsset
from models.investigation import Investigation

class CorrelationService:
    """Service for correlating data between different entities"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_connections(self, entity_type: str, entity_id: int) -> Dict[str, Any]:
        """Find connections between entities"""
        if entity_type == "person":
            return await self._find_person_connections(entity_id)
        elif entity_type == "company":
            return await self._find_company_connections(entity_id)
        elif entity_type == "cyber_asset":
            return await self._find_cyber_connections(entity_id)
        else:
            return {"error": "Invalid entity type"}

    async def _find_person_connections(self, person_id: int) -> Dict[str, Any]:
        """Find connections for a person"""
        # Get person
        query = select(Person).where(Person.id == person_id)
        result = await self.db.execute(query)
        person = result.scalar_one_or_none()

        if not person:
            return {"error": "Person not found"}

        connections = {
            "person": person,
            "companies": [],
            "cyber_assets": [],
            "investigations": []
        }

        # Find related companies (by email or name)
        company_query = select(Company).where(
            (Company.employees.contains([person.name])) |
            (Company.domain == person.email.split('@')[1] if person.email else False)
        )
        company_result = await self.db.execute(company_query)
        connections["companies"] = company_result.scalars().all()

        # Find related cyber assets (by email domain)
        if person.email:
            domain = person.email.split('@')[1]
            cyber_query = select(CyberAsset).where(CyberAsset.domain == domain)
            cyber_result = await self.db.execute(cyber_query)
            connections["cyber_assets"] = cyber_result.scalars().all()

        # Find related investigations
        inv_query = select(Investigation).where(Investigation.target_person_id == person_id)
        inv_result = await self.db.execute(inv_query)
        connections["investigations"] = inv_result.scalars().all()

        return connections

    async def _find_company_connections(self, company_id: int) -> Dict[str, Any]:
        """Find connections for a company"""
        # Get company
        query = select(Company).where(Company.id == company_id)
        result = await self.db.execute(query)
        company = result.scalar_one_or_none()

        if not company:
            return {"error": "Company not found"}

        connections = {
            "company": company,
            "persons": [],
            "cyber_assets": [],
            "investigations": []
        }

        # Find related persons (by domain or employees)
        person_query = select(Person).where(
            (Person.email.contains(company.domain)) |
            (Person.name.in_(company.employees or []))
        )
        person_result = await self.db.execute(person_query)
        connections["persons"] = person_result.scalars().all()

        # Find related cyber assets
        cyber_query = select(CyberAsset).where(CyberAsset.domain == company.domain)
        cyber_result = await self.db.execute(cyber_query)
        connections["cyber_assets"] = cyber_result.scalars().all()

        # Find related investigations
        inv_query = select(Investigation).where(Investigation.target_company_id == company_id)
        inv_result = await self.db.execute(inv_query)
        connections["investigations"] = inv_result.scalars().all()

        return connections

    async def _find_cyber_connections(self, asset_id: int) -> Dict[str, Any]:
        """Find connections for a cyber asset"""
        # Get cyber asset
        query = select(CyberAsset).where(CyberAsset.id == asset_id)
        result = await self.db.execute(query)
        asset = result.scalar_one_or_none()

        if not asset:
            return {"error": "Cyber asset not found"}

        connections = {
            "cyber_asset": asset,
            "companies": [],
            "persons": [],
            "investigations": []
        }

        # Find related companies
        company_query = select(Company).where(Company.domain == asset.domain)
        company_result = await self.db.execute(company_query)
        connections["companies"] = company_result.scalars().all()

        # Find related persons (by domain in email)
        person_query = select(Person).where(Person.email.contains(asset.domain))
        person_result = await self.db.execute(person_query)
        connections["persons"] = person_result.scalars().all()

        # Find related investigations
        inv_query = select(Investigation).where(Investigation.target_cyber_asset_id == asset_id)
        inv_result = await self.db.execute(inv_query)
        connections["investigations"] = inv_result.scalars().all()

        return connections