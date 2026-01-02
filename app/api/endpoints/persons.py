from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from api.endpoints.auth import get_current_user
from services.person_service import PersonService
from schemas.person import Person, PersonCreate, PersonUpdate

router = APIRouter()

@router.get("/", response_model=List[Person])
async def read_persons(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Get all persons"""
    service = PersonService(db)
    return await service.get_persons(skip=skip, limit=limit)

@router.post("/", response_model=Person)
async def create_person(
    person: PersonCreate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Create a new person"""
    service = PersonService(db)
    return await service.create_person(person)

@router.get("/{person_id}", response_model=Person)
async def read_person(
    person_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Get person by ID"""
    service = PersonService(db)
    db_person = await service.get_person(person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@router.put("/{person_id}", response_model=Person)
async def update_person(
    person_id: int,
    person: PersonUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Update a person"""
    service = PersonService(db)
    db_person = await service.update_person(person_id, person)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@router.delete("/{person_id}")
async def delete_person(
    person_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Delete a person"""
    service = PersonService(db)
    success = await service.delete_person(person_id)
    if not success:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"message": "Person deleted successfully"}

# OSINT collection endpoints
@router.post("/{person_id}/collect/email")
async def collect_email_data(
    person_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Collect email breach data for a person"""
    service = PersonService(db)
    person = await service.get_person(person_id)
    if not person or not person.email:
        raise HTTPException(status_code=404, detail="Person not found or no email")

    result = await service.collect_email_data(person.email)
    return result

@router.post("/{person_id}/collect/phone")
async def collect_phone_data(
    person_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Collect phone data for a person"""
    service = PersonService(db)
    person = await service.get_person(person_id)
    if not person or not person.phone:
        raise HTTPException(status_code=404, detail="Person not found or no phone")

    result = await service.collect_phone_data(person.phone)
    return result

@router.post("/{person_id}/collect/username")
async def collect_username_data(
    person_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Collect username data for a person"""
    service = PersonService(db)
    person = await service.get_person(person_id)
    if not person or not person.username:
        raise HTTPException(status_code=404, detail="Person not found or no username")

    result = await service.collect_username_data(person.username)
    return result