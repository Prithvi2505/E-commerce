from sqlalchemy import Column, Integer, String, Decimal, DateTime, ForeignKey, Enum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class PaymentMethod(enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    APPLE_PAY = "apple_pay"
    GOOGLE_PAY = "google_pay"
    BANK_TRANSFER = "bank_transfer"


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, unique=True)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    amount = Column(Decimal(10, 2), nullable=False)
    transaction_id = Column(String(255), nullable=True, unique=True)
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Additional payment fields
    gateway_response = Column(Text, nullable=True)  # Store gateway response
    refund_amount = Column(Decimal(10, 2), default=0)
    refund_reason = Column(String(500), nullable=True)
    failure_reason = Column(String(500), nullable=True)
    gateway_fee = Column(Decimal(10, 2), default=0)
    
    # Card details (last 4 digits only for security)
    card_last_four = Column(String(4), nullable=True)
    card_brand = Column(String(20), nullable=True)  # Visa, MasterCard, etc.
    
    # Relationships
    order = relationship("Order", back_populates="payment")

    def __repr__(self):
        return f"<Payment(order_id={self.order_id}, amount={self.amount}, status='{self.payment_status.value}')>"