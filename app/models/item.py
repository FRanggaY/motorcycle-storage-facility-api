from sqlalchemy import Column, String, Integer, func, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

from app.models.transaction import Transaction

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), unique=True, nullable=False)
    brand = Column(String(256), unique=False, nullable=True)
    created_at = Column(DateTime, server_default=func.NOW(), nullable=False)
    updated_at = Column(DateTime, server_default=func.NOW(), onupdate=func.NOW(), nullable=False)

    transactions = relationship('Transaction', back_populates='item', cascade='all, delete')