from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum

from .address import AddressResponse


class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    shipping_address_id: int
    billing_address_id: int
    notes: Optional[str] = Field(None, max_length=500)


class OrderItemResponse(BaseModel):
    order_item_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    product_name: str
    product_sku: Optional[str]

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    order_number: str
    order_date: datetime
    order_status: OrderStatusEnum
    subtotal: Decimal
    tax_amount: Decimal
    shipping_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    notes: Optional[str]
    items: List[OrderItemResponse] = []
    shipping_address: AddressResponse
    billing_address: AddressResponse

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    order_status: Optional[OrderStatusEnum] = None
    notes: Optional[str] = Field(None, max_length=500)