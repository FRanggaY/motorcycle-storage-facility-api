from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.dtos.item import CreateItem, EditItem

from app.models.item import Item

class ItemRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def count_items(self,  brand: str = None):
        query = self.db.query(Item)

        if brand is not None:
            query = query.filter(Item.brand == brand)
    
        return query.count()

    def read_items(self, brand: str = None, offset: int = None, size: int = None):
        query = self.db.query(Item)

        if brand is not None:
            query = query.filter(Item.brand == brand)

        if offset is not None and size is not None:
            query = query.offset((offset - 1) * size).limit(size)

        return query.all()
    
    def read_item_by_title(self, title: str) -> Item:
        return self.db.query(Item).filter(Item.title == title).first()
    
    def read_item(self, id: str) -> Item:
        result = self.db.query(Item).filter(Item.id == id).first()
        if not result:
            raise ValueError("Item not found")

        return result

    def create_item(self, data: CreateItem):
        model = Item(
            title=data.title,
            brand=data.brand.lower(),
        )

        if self.read_item_by_title(data.title):
            raise ValueError("Title already used")

        self.db.add(model)
        self.db.commit()
        return model
    
    def update_item(self, id: str, data: EditItem):
        result = self.read_item(id)

        if data.title:
            existing_data = self.read_item_by_title(data.title)
            if existing_data and existing_data.id != result.id:
                raise ValueError("Item with the same title already exists. Please choose a different title.")
            else:
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




