from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class AddressType(enum.Enum):
    SHIPPING = "shipping"
    BILLING = "billing"
    BOTH = "both"


class Address(Base):
    __tablename__ = "addresses"

    address_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    address_type = Column(Enum(AddressType), default=AddressType.BOTH)
    street_address = Column(String(255), nullable=False)
    address_line_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False, default="United States")
    is_default = Column(Boolean, default=False)
    
    # Additional fields
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    company = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"<Address(type='{self.address_type.value}', city='{self.city}', default={self.is_default})>"
    
    @property
    def full_address(self):
        """Get formatted full address"""
        address_parts = [self.street_address]
        if self.address_line_2:
            address_parts.append(self.address_line_2)
        address_parts.extend([self.city, self.state, self.postal_code, self.country])
        return ", ".join(address_parts)
    
    @property
    def full_name(self):
        """Get full name if available"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None