from fastapi import APIRouter, Depends, File, Query, status, HTTPException, Form, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.response import GeneralDataResponse
from app.services.transaction_service import TransactionService
from app.services.transaction_photo_location_service import TransactionPhotoLocationService

router = APIRouter()

@router.post("", response_model=GeneralDataResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction_photo_location(
    transaction_id: int = Form(...),
    title: str = Form(..., min_length=1),
    image: UploadFile = File(),
    db: Session = Depends(get_db)
):
    """
        Create transaction photo location
        - validation transaction
        - validation image (extension, size)
    """
    transaction_service = TransactionService(db)
    transaction_photo_location_service = TransactionPhotoLocationService(db)

    try:
        await transaction_photo_location_service.transaction_photo_location_repository.validation_image(image=image)
        transaction_service.read_transaction(transaction_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    
    content_type = image.content_type if image else ""
    file_extension = content_type.split('/')[1] if image else ""
    
    try:
        data = transaction_photo_location_service.create_transaction_photo_location(transaction_id=transaction_id, title=title, image=image, file_extension=file_extension)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    status_code = status.HTTP_201_CREATED
    data_response = GeneralDataResponse(
        code=status_code,
        status="CREATED",
        data={
            'id': data.id,
        },
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response


@router.delete("/{id}", response_model=GeneralDataResponse, status_code=status.HTTP_200_OK)
def delete_transaction_photo_location(id:int, db: Session = Depends(get_db)):
    """
        Delete transaction photo location
    """
    transaction_photo_location_service = TransactionPhotoLocationService(db)

    try:
        transaction_photo_location_id = transaction_photo_location_service.delete_transaction_photo_location(id=id)
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
            'id': transaction_photo_location_id,
        },
    )
    response = JSONResponse(content=data_response.model_dump(), status_code=status_code)
    return response