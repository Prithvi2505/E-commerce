from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Additional fields
    title = Column(String(200), nullable=True)
    verified_purchase = Column(Integer, default=0)  # 1 if from verified purchase
    helpful_votes = Column(Integer, default=0)
    total_votes = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

    # Add constraint to ensure rating is between 1 and 5
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
    )

    def __repr__(self):
        return f"<Review(product_id={self.product_id}, rating={self.rating}, user_id={self.user_id})>"
    
    @property
    def helpfulness_ratio(self):
        """Calculate helpfulness ratio"""
        if self.total_votes == 0:
            return 0
        return self.helpful_votes / self.total_votes