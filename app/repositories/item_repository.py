from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.dtos.item import CreateItem, EditItem

from app.models.item import Item

class ItemRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def count_items(self):
        return self.db.query(Item).count()

    def read_items(self, brand: str = None, offset: int = None, size: int = None):
        query = self.db.query(Item)

        if brand is not None:
            query = query.filter(Item.brand == brand)

        if offset is not None and size is not None:
            query = query.offset((offset - 1) * size).limit(size)

        return query.all()
    
    def read_item(self, id: str) -> Item:
        result = self.db.query(Item).filter(Item.id == id).first()
        if not result:
            raise ValueError("Data not found")

        return result

    def create_item(self, data: CreateItem):
        model = Item(
            title=data.title,
            brand=data.brand.lower(),
        )

        self.db.add(model)
        self.db.commit()
        return model
    
    def update_item(self, id: str, data: EditItem):
        result = self.read_item(id)

        if data.title:
            result.title = data.title
        
        if data.brand:
            result.brand = data.brand

        self.db.commit()
        return result
    
    def delete_item(self, id: str):
        self.read_item(id)

        self.db.query(Item).filter(Item.id == id).delete()
        self.db.commit()
        return id




