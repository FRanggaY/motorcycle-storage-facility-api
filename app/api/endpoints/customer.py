from fastapi import APIRouter, Depends, Query, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dtos.customer import CreateCustomer, EditCustomer
from app.models.response import GeneralDataResponse, GeneralDataPaginateResponse
from app.services.customer_service import CustomerService
from app.utils.manual import get_total_pages

router = APIRouter()

@router.post("", response_model=GeneralDataResponse, status_code=status.HTTP_201_CREATED)
def create_customer(create_customer: CreateCustomer, db: Session = Depends(get_db)):
    """
        Create customer
    """
    customer_service = CustomerService(db)

    try:
        data = customer_service.create_customer(create_customer)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    status_code = status.HTTP_201_CREATED
    auth_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data={
            'name': data.name,
        },
    )
    response = JSONResponse(content=auth_response.model_dump(), status_code=status_code)
    return response

@router.patch("/{id}", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def update_customer(id:int, edit_customer: EditCustomer, db: Session = Depends(get_db)):
    """
        Update customer
    """
    customer_service = CustomerService(db)

    try:
        data = customer_service.update_customer(id=id, data=edit_customer)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    status_code = status.HTTP_200_OK
    auth_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data={
            'id': data.id,
        },
    )
    response = JSONResponse(content=auth_response.model_dump(), status_code=status_code)
    return response

@router.delete("/{id}", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def delete_customer(id:int, db: Session = Depends(get_db)):
    """
        Delete customer
    """
    customer_service = CustomerService(db)

    try:
        customer_id = customer_service.delete_customer(id=id)
    except Exception as error:
        print(f"on customer :  {str(error)}")
        error_message = str(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error_message)
        )

    status_code = status.HTTP_200_OK
    auth_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data={
            'id': customer_id,
        },
    )
    response = JSONResponse(content=auth_response.model_dump(), status_code=status_code)
    return response

@router.get("/{id}", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def read_customer(id:int, db: Session = Depends(get_db)):
    """
        Read customer
    """
    customer_service = CustomerService(db)

    try:
        data = customer_service.read_customer(id=id)
    except Exception as error:
        print(f"on customer :  {str(error)}")
        error_message = str(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error_message)
        )

    status_code = status.HTTP_200_OK
    auth_response = GeneralDataResponse(
        code=status_code,
        status="OK",
        data={
            'id': data.id,
            'name': data.name,
            'no_hp': data.no_hp,
        },
    )
    response = JSONResponse(content=auth_response.model_dump(), status_code=status_code)
    return response

@router.get("", response_model=GeneralDataPaginateResponse, status_code=status.HTTP_200_OK)
def read_customers(
    offset: int = Query(None, ge=1), 
    size: int = Query(None, ge=1),
    db: Session = Depends(get_db)
):
    """
        Read customers
        - with pagination
    """
    customer_service = CustomerService(db)

    try:
        result = customer_service.read_customers(offset=offset, size=size)
    except Exception as error:
        print(f"on customer :  {str(error)}")
        error_message = str(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error_message)
        )
    
    count = customer_service.customer_repository.count_customers()
    total_pages = get_total_pages(size, count)
    
    datas = []
    for customer in result:
        datas.append({
            'id': customer.id,
            'name': customer.name,
            'no_hp': customer.no_hp,
        })

    if len(datas) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found"
        )

    status_code = status.HTTP_200_OK
    auth_response = GeneralDataPaginateResponse(
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
    response = JSONResponse(content=auth_response.model_dump(), status_code=status_code)
    return response