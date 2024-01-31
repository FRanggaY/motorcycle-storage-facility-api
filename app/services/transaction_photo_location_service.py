from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.transaction_photo_location_repository import TransactionPhotoLocationRepository

class TransactionPhotoLocationService:
    def __init__(self, db: Session):
        self.db = db
        self.transaction_photo_location_repository = TransactionPhotoLocationRepository(db)
    
    def create_transaction_photo_location(self, transaction_id, title, image, file_extension):
        return self.transaction_photo_location_repository.create_transaction_photo_location(transaction_id, title, image, file_extension)
    
    def read_transaction_photo_location(self, id:str):
        return self.transaction_photo_location_repository.read_transaction_photo_location(id)
    
    def delete_transaction_photo_location(self, id:str):
        return self.transaction_photo_location_repository.delete_transaction_photo_location(id)




