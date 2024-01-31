from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.dtos.transaction import CreateTransaction, EditTransaction

from app.repositories.transaction_repository import TransactionRepository

class TransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.transaction_repository = TransactionRepository(db)
    
    def create_transaction(self, data: CreateTransaction):
        return self.transaction_repository.create_transaction(data)
    
    def update_transaction(self, id:str, data: EditTransaction):
        return self.transaction_repository.update_transaction(id, data)
    
    def read_transactions(
        self, 
        customer_id: int = None,
        item_id: int = None,
        date_come: str = None,
        offset:int = None, 
        size:int = None
    ):
        return self.transaction_repository.read_transactions(customer_id, item_id, date_come, offset, size)
    
    def read_transaction(self, id:str):
        return self.transaction_repository.read_transaction(id)
    
    def delete_transaction(self, id:str):
        return self.transaction_repository.delete_transaction(id)




