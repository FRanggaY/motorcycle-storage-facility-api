
from typing import Optional
from pydantic import BaseModel, Field

from app.models.transaction import TransactionStatus

class CreateTransaction(BaseModel):
    item_id: int = Field(...)
    customer_id: int = Field(...)
    date_come: str = Field(..., min_length=1)
    date_out: Optional[str] = Field(None)
    cost_hourly: int = Field(...)
    cost_daily: int = Field(...)
    notes: Optional[str] = Field(None)
    plat_number: Optional[str] = Field(None)

class EditTransaction(BaseModel):
    item_id: int = Field(...)
    customer_id: int = Field(...)
    date_come: str = Field(..., min_length=1)
    date_out: str = Field(..., min_length=1)
    cost_hourly: int = Field(...)
    cost_daily: int = Field(...)
    status: TransactionStatus = Field(...)
    notes: Optional[str] = Field(None)
    plat_number: Optional[str] = Field(None)