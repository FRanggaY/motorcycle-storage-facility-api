
from typing import Optional
from pydantic import BaseModel, Field

class CreateCustomer(BaseModel):
    name: str = Field(..., min_length=1)
    no_hp: str = Field(..., min_length=1)

class EditCustomer(BaseModel):
    name: Optional[str] = Field(None)
    no_hp: Optional[str] = Field(None)