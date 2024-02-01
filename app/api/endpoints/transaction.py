from datetime import datetime
from fastapi import APIRouter, Depends, Query, Request, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dtos.transaction import CreateTransaction, EditTransaction
from app.models.response import GeneralDataResponse, GeneralDataPaginateResponse
from app.models.transaction import TransactionStatus
from app.repositories.transaction_photo_location_repository import TransactionPhotoLocationRepository
from app.services.transaction_service import TransactionService
from app.services.customer_service import CustomerService
from app.services.item_service import ItemService
from app.utils.manual import get_total_pages

router = APIRouter()

@router.post("", response_model=GeneralDataResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(create_transaction: CreateTransaction, db: Session = Depends(get_db)):
    """
        Create transaction
        - validation customer
        - validation item

        - date_come should be a datetime yyyy-mm-dd hh:mm:ss
        - date_out is a optional datetime yyyy-mm-dd hh:mm:ss
        - notes is a optional string
        - plat_number is a optional string
    """
    transaction_service = TransactionService(db)
    customer_service = CustomerService(db)
    item_service = ItemService(db)
    # validation
    date_format = "%Y-%m-%d %H:%M:%S"

    try:
        datetime.strptime(create_transaction.date_come, date_format)
        if create_transaction.date_out:
            datetime.strptime(create_transaction.date_out, date_format)
    except Exception as e:
        print(f"on transaction :  {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) 

    try:
        customer_service.read_customer(create_transaction.customer_id)
        item_service.read_item(create_transaction.item_id)
        data = transaction_service.create_transaction(create_transaction)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    status_code = status.HTTP_201_CREATED
    data_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data={
            'id': data.id,
        },
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response

@router.patch("/{id}", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def update_transaction(id:int, edit_transaction: EditTransaction, db: Session = Depends(get_db)):
    """
        Update transaction
        - validation customer
        - validation item

        - status option : reserved or taken
        - date_come should be a datetime yyyy-mm-dd hh:mm:ss
        - date_out should be datetime yyyy-mm-dd hh:mm:ss
        - notes is a optional string
        - plat_number is a optional string
    """
    transaction_service = TransactionService(db)
    customer_service = CustomerService(db)
    item_service = ItemService(db)

    # validation
    date_format = "%Y-%m-%d %H:%M:%S"

    try:
        date_come_format = datetime.strptime(edit_transaction.date_come, date_format)
        date_out_format = datetime.strptime(edit_transaction.date_out, date_format)
        if date_out_format < date_come_format:
            raise ValueError("date_out cant lower than date_come")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) 

    try:
        customer_service.read_customer(edit_transaction.customer_id)
        item_service.read_item(edit_transaction.item_id)
        data = transaction_service.update_transaction(id=id, data=edit_transaction)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    status_code = status.HTTP_200_OK
    data_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data={
            'id': data.id,
        },
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response

@router.delete("/{id}", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def delete_transaction(id:int, db: Session = Depends(get_db)):
    """
        Delete transaction
    """
    transaction_service = TransactionService(db)
    transaction_photo_location_service = TransactionPhotoLocationRepository(db)

    try:
        transaction_id = transaction_service.delete_transaction(id=id, folder_photo=transaction_photo_location_service.static_transaction_photo_location_folder_image)
    except Exception as error:
        print(f"on transaction :  {str(error)}")
        error_message = str(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error_message)
        )

    status_code = status.HTTP_200_OK
    data_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data={
            'id': transaction_id,
        },
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response

@router.get("/{id}", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def read_transaction(id:int, request: Request = None, db: Session = Depends(get_db)):
    """
        Read transaction
    """
    base_url = str(request.base_url) if request else ""
    transaction_service = TransactionService(db)

    try:
        data = transaction_service.read_transaction(id=id)
    except Exception as error:
        print(f"on transaction :  {str(error)}")
        error_message = str(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error_message)
        )
    
    attachment = []
    if len(data.transaction_photo_locations) > 0:
        # deleting file
        for location in data.transaction_photo_locations:
            attachment.append({
                'id': location.id,
                'title': location.title,
                'url_photo': f"{base_url}static/transaction/image/{location.url_photo}" if location.url_photo else None,
            })

    status_code = status.HTTP_200_OK
    data_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data={
            'id': data.id,
            'item': {
                'id': data.item.id,
                'title': data.item.title,
                'brand': data.item.brand,
            },
            'customer': {
                'id': data.customer.id,
                'name': data.customer.name,
                'no_hp': data.customer.no_hp,
            },
            'date_come': str(data.date_come) if data.date_come else None,
            'date_out': str(data.date_out) if data.date_out else None,
            'cost_hourly': data.cost_hourly,
            'cost_daily': data.cost_daily,
            'cost_final': data.cost_final,
            'notes': data.notes,
            'plat_number': data.plat_number,
            'status': data.status,
            'attachment': attachment,
        },
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response

@router.get("", response_model=GeneralDataPaginateResponse, status_code=status.HTTP_200_OK)
def read_transactions(
    item_id:int = Query(None),
    customer_id:int = Query(None),
    date_come:str = Query(None),
    transaction_status:TransactionStatus = Query(None),
    offset: int = Query(None, ge=1), 
    size: int = Query(None, ge=1),
    db: Session = Depends(get_db)
):
    """
        Read transactions
        - with pagination
    """
    transaction_service = TransactionService(db)

    try:
        result = transaction_service.read_transactions(
            item_id=item_id,
            customer_id=customer_id,
            date_come=date_come,
            status=transaction_status.value if transaction_status else None,
            offset=offset,
            size=size
        )
    except Exception as error:
        print(f"on transaction :  {str(error)}")
        error_message = str(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error_message)
        )
    
    count = transaction_service.transaction_repository.count_transactions(
        item_id=item_id,
        customer_id=customer_id,
        date_come=date_come
    )
    total_pages = get_total_pages(size, count)
    
    datas = []
    for transaction in result:
        datas.append({
            'id': transaction.id,
            'item': {
                'id': transaction.item.id,
                'title': transaction.item.title,
                'brand': transaction.item.brand,
            },
            'customer': {
                'id': transaction.customer.id,
                'name': transaction.customer.name,
                'no_hp': transaction.customer.no_hp,
            },
            'date_come': str(transaction.date_come) if transaction.date_come else None,
            'date_out': str(transaction.date_out) if transaction.date_out else None,
            'cost_final': transaction.cost_final,
            'status': transaction.status,
        })

    if len(datas) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found"
        )

    status_code = status.HTTP_200_OK
    data_response = GeneralDataPaginateResponse(
        code=status_code,
        status="OK",
        data=datas,
        meta={
            "size": size,
            "total": count,
            "total_pages": total_pages,
            "offset": offset
        },
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response