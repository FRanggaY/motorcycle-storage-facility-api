from fastapi import APIRouter
from .endpoints import dashboard, item, customer, transaction, transaction_photo_location

router = APIRouter()

router.include_router(item.router, prefix="/item", tags=["Item"])
router.include_router(customer.router, prefix="/customer", tags=["Customer"])
router.include_router(transaction.router, prefix="/transaction", tags=["Transaction"])
router.include_router(transaction_photo_location.router, prefix="/transaction-photo-location", tags=["Transaction"])

router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])