from fastapi import APIRouter
from .endpoints import item, customer

router = APIRouter()

router.include_router(item.router, prefix="/item", tags=["Item"])
router.include_router(customer.router, prefix="/customer", tags=["Customer"])