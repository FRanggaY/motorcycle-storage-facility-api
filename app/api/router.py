from fastapi import APIRouter
from .endpoints import item, customer, transaction

router = APIRouter()

router.include_router(item.router, prefix="/item", tags=["Item"])
router.include_router(customer.router, prefix="/customer", tags=["Customer"])
router.include_router(transaction.router, prefix="/transaction", tags=["Transaction"])