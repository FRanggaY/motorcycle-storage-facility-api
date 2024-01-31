from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as EnumType

from app.models.customer import Customer

class TransactionStatus(EnumType):
    reserved = "reserved"
    taken = "taken"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(ForeignKey('items.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    customer_id = Column(ForeignKey('customers.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    date_come = Column(DateTime, nullable=False)
    date_out = Column(DateTime, nullable=True)
    cost_hourly = Column(Integer, nullable=False, default=0)
    cost_daily = Column(Integer, nullable=False, default=0)
    cost_final = Column(Integer, nullable=False, default=0)
    notes = Column(String(1024), nullable=True)
    plat_number = Column(String(512), nullable=True)
    status = Column(Enum("reserved", "taken"), nullable=False, default="reserved")
    created_at = Column(DateTime, server_default=func.NOW(), nullable=False)
    updated_at = Column(DateTime, server_default=func.NOW(), onupdate=func.NOW(), nullable=False)
   
    item = relationship('Item', back_populates='transactions')
    customer = relationship('Customer', back_populates='transactions')

    transaction_photo_locations = relationship('TransactionPhotoLocation', back_populates='transaction', cascade='all, delete')
    

class TransactionPhotoLocation(Base):
    __tablename__ = "transaction_photo_locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(ForeignKey('transactions.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    title = Column(String(1024), nullable=False)
    url_photo = Column(String(1024), nullable=False)
    created_at = Column(DateTime, server_default=func.NOW(), nullable=False)
    updated_at = Column(DateTime, server_default=func.NOW(), onupdate=func.NOW(), nullable=False)

    transaction = relationship('Transaction', back_populates='transaction_photo_locations')