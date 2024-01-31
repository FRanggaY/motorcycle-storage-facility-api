import os
from fastapi import File, HTTPException, status
from sqlalchemy.orm import Session

from app.models.transaction import TransactionPhotoLocation
from app.utils.handling_file import delete_file, upload_file

class TransactionPhotoLocationRepository:
    def __init__(self, db: Session):
        self.db = db
        self.static_transaction_photo_location_folder_image = "./static/transaction/image/"

    async def validation_image(self, image: File, limit_file_size_mb: int = 5, allowed_extension: list = ["image/jpeg", "image/png"]):
        image.file.seek(0, 2)
        file_size = image.file.tell()

        # move the cursor back to the beginning
        await image.seek(0)
        if file_size > limit_file_size_mb * 1024 * 1024:
            # more than 5 MB
            raise ValueError(f"Image too large. only allow image lower than {limit_file_size_mb} mb")

        # check the content type (MIME type)
        content_type = image.content_type
        if content_type not in allowed_extension:
            image_formats = ', '.join([mime.split('/')[-1] for mime in allowed_extension])
            raise ValueError(f"Invalid image file type. only allow image with type {image_formats}")

    def create_transaction_photo_location(self, transaction_id, title, image, file_extension):
        # upload file
        file_name = upload_file(image, self.static_transaction_photo_location_folder_image, file_extension)

        model = TransactionPhotoLocation(
            transaction_id=transaction_id,
            title=title,
            url_photo=file_name,
        )

        self.db.add(model)
        self.db.commit()
        return model
    
    def read_transaction_photo_location(self, id: str) -> TransactionPhotoLocation:
        result = self.db.query(TransactionPhotoLocation).filter(TransactionPhotoLocation.id == id).first()
        if not result:
            raise ValueError("Data not found")

        return result
    
    def delete_transaction_photo_location(self, id: str):
        data = self.read_transaction_photo_location(id)

        # deleting file
        file_path = os.path.join(self.static_transaction_photo_location_folder_image, data.url_photo)
        delete_file(file_path)

        self.db.query(TransactionPhotoLocation).filter(TransactionPhotoLocation.id == id).delete()
        self.db.commit()
        return id




