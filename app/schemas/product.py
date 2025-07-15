from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0, decimal_places=2)
    category_id: int
    image_url: Optional[str] = Field(None, max_length=500)
    sku: Optional[str] = Field(None, max_length=50)
    weight: Optional[Decimal] = Field(None, decimal_places=2)
    dimensions: Optional[str] = Field(None, max_length=100)


class ProductCreate(ProductBase):
    stock_quantity: int = Field(..., ge=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stock_quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None
    image_url: Optional[str] = Field(None, max_length=500)
    sku: Optional[str] = Field(None, max_length=50)
    weight: Optional[Decimal] = Field(None, decimal_places=2)
    dimensions: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    product_id: int
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    average_rating: float = 0.0
    review_count: int = 0
    is_in_stock: bool

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    pages: int
    per_page: int


class ProductSearch(BaseModel):
    query: Optional[str] = None
    category_id: Optional[int] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    in_stock_only: bool = True
    sort_by: str = "name"  # name, price, rating, created_at
    sort_order: str = "asc"  # asc, desc