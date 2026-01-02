from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.cyber import CyberAsset
from schemas.cyber import CyberAssetCreate, CyberAssetUpdate
from collectors.cyber.dns import DNSCollector
from collectors.cyber.subdomains import SubdomainCollector
from collectors.cyber.whois import WhoisCollector
from utils.http_client import HttpClient

class CyberService:
    """Service for cyber asset-related operations"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.http_client = HttpClient()

    async def get_cyber_asset(self, asset_id: int) -> Optional[CyberAsset]:
        """Get cyber asset by ID"""
        query = select(CyberAsset).where(CyberAsset.id == asset_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_cyber_assets(self, skip: int = 0, limit: int = 100) -> List[CyberAsset]:
        """Get all cyber assets with pagination"""
        query = select(CyberAsset).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_cyber_asset(self, asset: CyberAssetCreate) -> CyberAsset:
        """Create a new cyber asset"""
        db_asset = CyberAsset(**asset.dict())
        self.db.add(db_asset)
        await self.db.commit()
        await self.db.refresh(db_asset)
        return db_asset

    async def update_cyber_asset(self, asset_id: int, asset_update: CyberAssetUpdate) -> Optional[CyberAsset]:
        """Update an existing cyber asset"""
        db_asset = await self.get_cyber_asset(asset_id)
        if not db_asset:
            return None

        for field, value in asset_update.dict(exclude_unset=True).items():
            setattr(db_asset, field, value)

        await self.db.commit()
        await self.db.refresh(db_asset)
        return db_asset

    async def delete_cyber_asset(self, asset_id: int) -> bool:
        """Delete a cyber asset"""
        db_asset = await self.get_cyber_asset(asset_id)
        if not db_asset:
            return False

        await self.db.delete(db_asset)
        await self.db.commit()
        return True

    async def collect_dns_data(self, domain: str) -> dict:
        """Collect DNS records for domain"""
        collector = DNSCollector(self.http_client)
        return await collector.collect(domain)

    async def collect_subdomain_data(self, domain: str) -> dict:
        """Collect subdomains for domain"""
        collector = SubdomainCollector(self.http_client)
        return await collector.collect(domain)

    async def collect_whois_data(self, domain: str) -> dict:
        """Collect WHOIS information for domain"""
        collector = WhoisCollector(self.http_client)
        return await collector.collect(domain)