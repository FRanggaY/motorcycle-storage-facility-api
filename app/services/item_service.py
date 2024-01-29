from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.dtos.item import CreateItem, EditItem

from app.repositories.item_repository import ItemRepository

class ItemService:
    def __init__(self, db: Session):
        self.db = db
        self.item_repository = ItemRepository(db)
    
    def create_item(self, data: CreateItem):
        return self.item_repository.create_item(data)
    
    def update_item(self, id:str, data: EditItem):
        return self.item_repository.update_item(id, data)
    
    def read_items(self, brand:str = None, offset:int = None, size:int = None):
        return self.item_repository.read_items(brand, offset, size)
    
    def read_item(self, id:str):
        return self.item_repository.read_item(id)
    
    def delete_item(self, id:str):
        return self.item_repository.delete_item(id)




