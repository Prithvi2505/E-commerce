from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    parent_category_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    parent_category_id: Optional[int] = None


class CategoryResponse(CategoryBase):
    category_id: int
    created_at: datetime
    children: List['CategoryResponse'] = []
    product_count: int = 0

    class Config:
        from_attributes = True


# Update forward reference
CategoryResponse.model_rebuild()