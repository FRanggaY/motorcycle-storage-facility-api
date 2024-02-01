from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.models.item import Item

from app.models.transaction import Transaction, TransactionStatus

class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def monthly_date_come(
        self, 
        year: int = None,
        item_id: int = None,
        customer_id: int = None,
        status: TransactionStatus = None,
    ):
        query = (
            self.db.query(
                func.DATE_FORMAT(Transaction.date_come, '%Y-%m').label('month'),
                func.count().label('total_transactions')
            )
            .group_by('month')
            .order_by('month')
        )

        if year:
            query = query.filter(func.YEAR(Transaction.date_come) == year)

        if item_id:
            query = query.filter(Transaction.item_id == item_id)

        if customer_id:
            query = query.filter(Transaction.customer_id == customer_id)

        if status:
            query = query.filter(Transaction.status == status)

        monthly_data = query.all()
        return monthly_data
    
    def grouped_item_brand(
        self, 
        year: int = None,
        customer_id: int = None,
        status: TransactionStatus = None,
    ):
        query = (
            self.db.query(
                Item.brand.label('brand'),
                func.count().label('total_transactions')
            )
            .join(Transaction, Transaction.item_id == Item.id)
            .group_by('brand')
            .order_by('brand')
        )

        if year:
            query = query.filter(func.YEAR(Transaction.date_come) == year)

        if customer_id:
            query = query.filter(Transaction.customer_id == customer_id)

        if status:
            query = query.filter(Transaction.status == status)

        monthly_data = query.all()
        return monthly_data
    
    def grouped_customer(
        self, 
        year: int = None,
        item_id: int = None,
        status: TransactionStatus = None,
    ):
        query = (
            self.db.query(
                Customer.name.label('name'),
                func.count().label('total_transactions')
            )
            .join(Transaction, Transaction.customer_id == Customer.id)
            .group_by('name')
            .order_by('name')
        )

        if year:
            query = query.filter(func.YEAR(Transaction.date_come) == year)

        if item_id:
            query = query.filter(Transaction.item_id == item_id)

        if status:
            query = query.filter(Transaction.status == status)

        monthly_data = query.all()
        return monthly_data