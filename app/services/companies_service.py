from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.company import Company
from schemas.company import CompanyCreate, CompanyUpdate
from collectors.companies.domains import DomainCollector
from collectors.companies.ruc import RUCCollector
from collectors.companies.socials import SocialMediaCollector
from utils.http_client import HttpClient

class CompaniesService:
    """Service for company-related operations"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.http_client = HttpClient()

    async def get_company(self, company_id: int) -> Optional[Company]:
        """Get company by ID"""
        query = select(Company).where(Company.id == company_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_companies(self, skip: int = 0, limit: int = 100) -> List[Company]:
        """Get all companies with pagination"""
        query = select(Company).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_company(self, company: CompanyCreate) -> Company:
        """Create a new company"""
        db_company = Company(**company.dict())
        self.db.add(db_company)
        await self.db.commit()
        await self.db.refresh(db_company)
        return db_company

    async def update_company(self, company_id: int, company_update: CompanyUpdate) -> Optional[Company]:
        """Update an existing company"""
        db_company = await self.get_company(company_id)
        if not db_company:
            return None

        for field, value in company_update.dict(exclude_unset=True).items():
            setattr(db_company, field, value)

        await self.db.commit()
        await self.db.refresh(db_company)
        return db_company

    async def delete_company(self, company_id: int) -> bool:
        """Delete a company"""
        db_company = await self.get_company(company_id)
        if not db_company:
            return False

        await self.db.delete(db_company)
        await self.db.commit()
        return True

    async def collect_domain_data(self, domain: str) -> dict:
        """Collect domain registration data"""
        collector = DomainCollector(self.http_client)
        return await collector.collect(domain)

    async def collect_ruc_data(self, ruc: str) -> dict:
        """Collect RUC data for Paraguayan companies"""
        collector = RUCCollector(self.http_client)
        return await collector.collect(ruc)

    async def collect_social_data(self, company_name: str) -> dict:
        """Collect social media profiles for company"""
        collector = SocialMediaCollector(self.http_client)
        return await collector.collect(company_name)