from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum


class PaymentMethodEnum(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    APPLE_PAY = "apple_pay"
    GOOGLE_PAY = "google_pay"
    BANK_TRANSFER = "bank_transfer"


class PaymentStatusEnum(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"


class PaymentCreate(BaseModel):
    payment_method: PaymentMethodEnum
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    # Stripe token or payment method ID
    payment_token: Optional[str] = None


class PaymentResponse(BaseModel):
    payment_id: int
    order_id: int
    payment_method: PaymentMethodEnum
    payment_status: PaymentStatusEnum
    amount: Decimal
    transaction_id: Optional[str]
    payment_date: datetime
    refund_amount: Decimal
    refund_reason: Optional[str]
    failure_reason: Optional[str]
    gateway_fee: Decimal
    card_last_four: Optional[str]
    card_brand: Optional[str]

    class Config:
        from_attributes = True


class PaymentUpdate(BaseModel):
    payment_status: Optional[PaymentStatusEnum] = None
    failure_reason: Optional[str] = None