import os
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.dtos.transaction import CreateTransaction, EditTransaction
from datetime import datetime, timedelta

from app.models.transaction import Transaction
from app.utils.handling_file import delete_file

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def calculate_cost_final(self, date_come, date_out, cost_hourly, cost_daily):
        date_format = "%Y-%m-%d %H:%M:%S"
        date_come_format = datetime.strptime(date_come, date_format)
        date_out_format = datetime.strptime(date_out, date_format)

        time_difference = date_out_format - date_come_format

        total_hours = time_difference.total_seconds() / 3600
        
        if total_hours > 0:
            total_days = total_hours // 24
            remaining_hours = total_hours % 24

            cost_final = (cost_daily * total_days) + (cost_hourly * remaining_hours)
        else:
            cost_final = 0  # reset cost

        return cost_final
    
    def count_transactions(
        self,
        customer_id: int = None, 
        item_id: int = None, 
        date_come: str = None, 
    ):
        query = self.db.query(Transaction)

        if customer_id is not None:
            query = query.filter(Transaction.customer_id == customer_id)
        
        if item_id is not None:
            query = query.filter(Transaction.item_id == item_id)
       
        if date_come is not None:
            query = query.filter(Transaction.date_come == date_come)

        return query.count()

    def read_transactions(
        self,
        customer_id: int = None, 
        item_id: int = None, 
        date_come: str = None, 
        offset: int = None, 
        size: int = None
    ):
        query = self.db.query(Transaction)

        if customer_id is not None:
            query = query.filter(Transaction.customer_id == customer_id)
        
        if item_id is not None:
            query = query.filter(Transaction.item_id == item_id)
       
        if date_come is not None:
            query = query.filter(Transaction.date_come == date_come)

        if offset is not None and size is not None:
            query = query.offset((offset - 1) * size).limit(size)

        return query.all()

    
    def read_transaction(self, id: str) -> Transaction:
        result = self.db.query(Transaction).filter(Transaction.id == id).first()
        if not result:
            raise ValueError("Transaction not found")

        return result

    def create_transaction(self, data: CreateTransaction):

        cost_final = 0
        if data.date_out:
            cost_final = self.calculate_cost_final(data.date_come, data.date_out, data.cost_hourly, data.cost_daily)

        model = Transaction(
            item_id=data.item_id,
            customer_id=data.customer_id,
            date_come=data.date_come,
            date_out=data.date_out if data.date_out else None,
            cost_hourly=data.cost_hourly,
            cost_daily=data.cost_daily,
            cost_final=cost_final,
            notes=data.notes,
            plat_number=data.plat_number,
        )

        self.db.add(model)
        self.db.commit()
        return model
    
    def update_transaction(self, id: str, data: EditTransaction):
        result = self.read_transaction(id)

        if data.item_id:
            result.item_id = data.item_id

        if data.customer_id:
            result.customer_id = data.customer_id
        
        if data.date_come:
            result.date_come = data.date_come
        
        if data.date_out:
            result.date_out = data.date_out

            result.cost_final = self.calculate_cost_final(result.date_come, result.date_out, data.cost_hourly, data.cost_daily)
        
        if data.cost_hourly:
            result.cost_hourly = data.cost_hourly
        
        if data.cost_daily:
            result.cost_daily = data.cost_daily

        if data.notes:
            result.notes = data.notes
        
        if data.plat_number:
            result.plat_number = data.plat_number
        
        if data.status:
            result.status = data.status.value

        self.db.commit()
        return result
    
    def delete_transaction(self, id: str, folder_photo):
        data = self.read_transaction(id)

        if len(data.transaction_photo_locations) > 0:
            # deleting file
            for location in data.transaction_photo_locations:
                file_path = os.path.join(folder_photo, location.url_photo)
                delete_file(file_path)

        self.db.query(Transaction).filter(Transaction.id == id).delete()
        self.db.commit()
        return id




