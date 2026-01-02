#!/usr/bin/env python3
"""
Seed data script for OSINT MVP
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import AsyncSessionLocal
from models.person import Person
from models.company import Company
from models.cyber import CyberAsset
from models.investigation import Investigation
from core.security import get_password_hash

async def seed_data():
    async with AsyncSessionLocal() as session:
        try:
            # Create sample person
            person = Person(
                name="John Doe",
                email="john.doe@example.com",
                phone="+1-555-0123",
                username="johndoe",
                social_profiles={"twitter": "@johndoe", "linkedin": "john-doe"},
                notes="Sample person for testing",
                tags=["test", "sample"]
            )
            session.add(person)

            # Create sample company
            company = Company(
                name="Example Corp",
                ruc="123456789",
                domain="example.com",
                description="A sample company",
                social_profiles={"twitter": "@examplecorp", "linkedin": "example-corp"},
                employees=["John Doe"],
                notes="Sample company for testing",
                tags=["test", "sample"]
            )
            session.add(company)

            # Create sample cyber asset
            cyber_asset = CyberAsset(
                domain="example.com",
                ip_address="192.168.1.1",
                subdomains=["www.example.com", "api.example.com"],
                dns_records={"A": ["192.168.1.1"]},
                whois_info={"registrar": "Example Registrar"},
                ports=[80, 443],
                notes="Sample cyber asset",
                tags=["test", "sample"]
            )
            session.add(cyber_asset)

            # Create sample investigation
            investigation = Investigation(
                title="Sample Investigation",
                description="Testing the OSINT system",
                target_person_id=1,  # Will be set after commit
                findings={"emails": ["john.doe@example.com"]},
                notes="Sample investigation",
                tags=["test"]
            )
            session.add(investigation)

            await session.commit()
            print("Sample data seeded successfully!")

        except Exception as e:
            await session.rollback()
            print(f"Error seeding data: {e}")
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(seed_data())