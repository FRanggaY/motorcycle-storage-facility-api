from fastapi import APIRouter, Depends, Query, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dtos.item import CreateItem, EditItem
from app.models.response import GeneralDataResponse, GeneralDataPaginateResponse
from app.services.item_service import ItemService
from app.utils.manual import get_total_pages

router = APIRouter()

@router.post("", response_model=GeneralDataResponse, status_code=status.HTTP_201_CREATED)
def create_item(create_item: CreateItem, db: Session = Depends(get_db)):
    """
        Create Item
        - title should be unique
        - automatically lowercase of brand
    """
    item_service = ItemService(db)

    try:
        data = item_service.create_item(create_item)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    status_code = status.HTTP_201_CREATED
    data_response = GeneralDataResponse(
        code=status_code,
        status="CREATED",
        data={
            'title': data.title,
        },
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response

@router.patch("/{id}", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def update_item(id:int, edit_item: EditItem, db: Session = Depends(get_db)):
    """
        Update Item
    """
    item_service = ItemService(db)

    try:
        data = item_service.update_item(id=id, data=edit_item)
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
def delete_item(id:int, db: Session = Depends(get_db)):
    """
        Delete Item
    """
    item_service = ItemService(db)

    try:
        item_id = item_service.delete_item(id=id)
    except Exception as error:
        print(f"on item :  {str(error)}")
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
            'id': item_id,
        },
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response

@router.get("/{id}", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def read_item(id:int, db: Session = Depends(get_db)):
    """
        Read Item
    """
    item_service = ItemService(db)

    try:
        data = item_service.read_item(id=id)
    except Exception as error:
        print(f"on item :  {str(error)}")
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
            'id': data.id,
            'title': data.title,
            'brand': data.brand,
        },
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response

@router.get("", response_model=GeneralDataPaginateResponse, status_code=status.HTTP_200_OK)
def read_items(
    brand:str = Query(None),
    offset: int = Query(None, ge=1), 
    size: int = Query(None, ge=1),
    db: Session = Depends(get_db)
):
    """
        Read Items
        - with pagination
    """
    item_service = ItemService(db)

    try:
        result = item_service.read_items(brand=brand, offset=offset, size=size)
    except Exception as error:
        print(f"on item :  {str(error)}")
        error_message = str(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error_message)
        )
    
    count = item_service.item_repository.count_items(brand=brand)
    total_pages = get_total_pages(size, count)
    
    datas = []
    for item in result:
        datas.append({
            'id': item.id,
            'title': item.title,
            'brand': item.brand,
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