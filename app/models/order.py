from sqlalchemy import Column, Integer, String, Decimal, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class OrderStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    total_amount = Column(Decimal(10, 2), nullable=False)
    order_status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    shipping_address_id = Column(Integer, ForeignKey("addresses.address_id"), nullable=False)
    billing_address_id = Column(Integer, ForeignKey("addresses.address_id"), nullable=False)
    
    # Additional order fields
    order_number = Column(String(50), unique=True, nullable=False)
    subtotal = Column(Decimal(10, 2), nullable=False)
    tax_amount = Column(Decimal(10, 2), default=0)
    shipping_amount = Column(Decimal(10, 2), default=0)
    discount_amount = Column(Decimal(10, 2), default=0)
    notes = Column(String(500), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    payment = relationship("Payment", back_populates="order", uselist=False)

    def __repr__(self):
        return f"<Order(order_number='{self.order_number}', status='{self.order_status.value}', total={self.total_amount})>"


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Decimal(10, 2), nullable=False)
    total_price = Column(Decimal(10, 2), nullable=False)
    
    # Additional fields
    product_name = Column(String(200), nullable=False)  # Store product name at time of order
    product_sku = Column(String(50), nullable=True)  # Store SKU at time of order
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(product='{self.product_name}', quantity={self.quantity}, total={self.total_price})>"