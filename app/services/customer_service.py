from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.dtos.customer import CreateCustomer, EditCustomer

from app.repositories.customer_repository import CustomerRepository

class CustomerService:
    def __init__(self, db: Session):
        self.db = db
        self.customer_repository = CustomerRepository(db)
    
    def create_customer(self, data: CreateCustomer):
        return self.customer_repository.create_customer(data)
    
    def update_customer(self, id:str, data: EditCustomer):
        return self.customer_repository.update_customer(id, data)
    
    def read_customers(self, offset:int = None, size:int = None):
        return self.customer_repository.read_customers(offset, size)
    
    def read_customer(self, id:str):
        return self.customer_repository.read_customer(id)
    
    def delete_customer(self, id:str):
        return self.customer_repository.delete_customer(id)




