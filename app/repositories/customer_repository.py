from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.dtos.customer import CreateCustomer, EditCustomer

from app.models.customer import Customer

class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def count_customers(self):
        return self.db.query(Customer).count()

    def read_customers(self, offset: int = None, size: int = None):
        query = self.db.query(Customer)

        if offset is not None and size is not None:
            query = query.offset((offset - 1) * size).limit(size)

        return query.all()
    
    def read_customer(self, id: str) -> Customer:
        result = self.db.query(Customer).filter(Customer.id == id).first()
        if not result:
            raise ValueError("Data not found")

        return result

    def create_customer(self, data: CreateCustomer):
        model = Customer(
            name=data.name,
            no_hp=data.no_hp,
        )

        self.db.add(model)
        self.db.commit()
        return model
    
    def update_customer(self, id: str, data: EditCustomer):
        result = self.read_customer(id)

        if data.name:
            result.name = data.name
        
        if data.no_hp:
            result.no_hp = data.no_hp

        self.db.commit()
        return result
    
    def delete_customer(self, id: str):
        self.read_customer(id)

        self.db.query(Customer).filter(Customer.id == id).delete()
        self.db.commit()
        return id




