from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from decimal import Decimal

from .product import ProductResponse


class CartItemBase(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemCreate(CartItemBase):
    product_id: int


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemResponse(CartItemBase):
    cart_item_id: int
    product_id: int
    added_at: datetime
    product: ProductResponse
    subtotal: Decimal

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    cart_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    items: List[CartItemResponse] = []
    total_items: int
    total_price: Decimal

    class Config:
        from_attributes = True