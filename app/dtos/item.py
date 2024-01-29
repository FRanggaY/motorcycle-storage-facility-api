
from typing import Optional
from pydantic import BaseModel, Field

class CreateItem(BaseModel):
    title: str = Field(..., min_length=1)
    brand: str = Field(..., min_length=1)

class EditItem(BaseModel):
    title: Optional[str] = Field(None)
    brand: Optional[str] = Field(None)