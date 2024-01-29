from fastapi import APIRouter
from .endpoints import item

router = APIRouter()

router.include_router(item.router, prefix="/item", tags=["Item"])