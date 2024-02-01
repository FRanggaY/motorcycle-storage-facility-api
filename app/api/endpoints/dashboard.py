from fastapi import APIRouter, Depends, Query, Request, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.response import GeneralDataResponse
from app.models.transaction import TransactionStatus
from app.repositories.transaction_photo_location_repository import TransactionPhotoLocationRepository
from app.services.dashboard_service import DashboardService
from app.services.transaction_service import TransactionService
from app.services.customer_service import CustomerService
from app.services.item_service import ItemService

router = APIRouter()

@router.get("/items", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def count_item(brand:str = Query(None), db: Session = Depends(get_db)):
    """
        Count Item
    """
    item_service = ItemService(db)

    status_code = status.HTTP_200_OK
    data_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data={
            'total': item_service.item_repository.count_items(brand=brand)
        },
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response

@router.get("/customers", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def count_customer(db: Session = Depends(get_db)):
    """
        Count Customer
    """
    customer_service = CustomerService(db)

    status_code = status.HTTP_200_OK
    data_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data={
            'total': customer_service.customer_repository.count_customers()
        },
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response

@router.get("/transactions", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def count_transaction(
    item_id:int = Query(None),
    customer_id:int = Query(None),
    date_come:str = Query(None),
    transaction_status:TransactionStatus = Query(None),
    db: Session = Depends(get_db)
):
    """
        Count Transaction
    """
    transaction_service = TransactionService(db)

    count = transaction_service.transaction_repository.count_transactions(
        item_id=item_id,
        customer_id=customer_id,
        date_come=date_come,
        status=transaction_status.value if transaction_status else None,
    )

    status_code = status.HTTP_200_OK
    data_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data={
            'total': count
        },
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response

@router.get("/transactions/monthly-date-come", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def transaction_monthly_date_come(
    year:int = Query(None),
    item_id:int = Query(None),
    customer_id:int = Query(None),
    transaction_status:TransactionStatus = Query(None),
    db: Session = Depends(get_db)
):
    """
        Monthly date_come
    """
    dashboard_service = DashboardService(db)

    datas = []
    result = dashboard_service.dashboard_repository.monthly_date_come(
        year=year,
        item_id=item_id,
        customer_id=customer_id,
        status=transaction_status.value if transaction_status else None,
    )
    for result in result:
        datas.append({
            'month': result.month,
            'total': result.total_transactions,
        })

    if len(datas) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='data not found'
        )

    status_code = status.HTTP_200_OK
    data_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data=datas,
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response

@router.get("/transactions/grouped-item-brand", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def transaction_grouped_item_brand(
    year:int = Query(None),
    customer_id:int = Query(None),
    transaction_status:TransactionStatus = Query(None),
    db: Session = Depends(get_db)
):
    """
        Grouped brand
    """
    dashboard_service = DashboardService(db)

    datas = []
    result = dashboard_service.dashboard_repository.grouped_item_brand(
        year=year,
        customer_id=customer_id,
        status=transaction_status.value if transaction_status else None,
    )
    for result in result:
        datas.append({
            'brand': result.brand,
            'total': result.total_transactions,
        })

    if len(datas) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='data not found'
        )

    status_code = status.HTTP_200_OK
    data_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data=datas,
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response

@router.get("/transactions/grouped-customer", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def transaction_grouped_customer(
    year:int = Query(None),
    item_id:int = Query(None),
    transaction_status:TransactionStatus = Query(None),
    db: Session = Depends(get_db)
):
    """
        Grouped customer
    """
    dashboard_service = DashboardService(db)

    datas = []
    result = dashboard_service.dashboard_repository.grouped_customer(
        year=year,
        item_id=item_id,
        status=transaction_status.value if transaction_status else None,
    )
    for result in result:
        datas.append({
            'name': result.name,
            'total': result.total_transactions,
        })

    if len(datas) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='data not found'
        )

    status_code = status.HTTP_200_OK
    data_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data=datas,
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response