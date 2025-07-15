from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    parent_category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Self-referencing relationship for hierarchical categories
    parent = relationship("Category", remote_side=[category_id], back_populates="children")
    children = relationship("Category", back_populates="parent")
    
    # Relationship with products
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(name='{self.name}', id={self.category_id})>"