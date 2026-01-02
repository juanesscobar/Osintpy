#!/bin/bash

# Initialize OSINT database

echo "Initializing OSINT database..."

# Create database tables
python3 -c "
import asyncio
from core.database import engine, Base
from models.person import Person
from models.company import Company
from models.cyber import CyberAsset
from models.investigation import Investigation

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())
"

echo "Database initialized successfully!"