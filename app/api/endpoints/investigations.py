from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "investigations endpoint"}


@router.get("/status")
async def status():
    return {"status": "ok"}
