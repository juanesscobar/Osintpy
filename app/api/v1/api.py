from fastapi import APIRouter

from api.endpoints import auth, persons, companies, cyber, investigations

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(persons.router, prefix="/persons", tags=["persons"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(cyber.router, prefix="/cyber", tags=["cyber"])
api_router.include_router(investigations.router, prefix="/investigations", tags=["investigations"])