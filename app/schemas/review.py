from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from .user import UserResponse


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    title: Optional[str] = Field(None, max_length=200)


class ReviewCreate(ReviewBase):
    product_id: int


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
    title: Optional[str] = Field(None, max_length=200)


class ReviewResponse(ReviewBase):
    review_id: int
    user_id: int
    product_id: int
    created_at: datetime
    verified_purchase: bool
    helpful_votes: int
    total_votes: int
    helpfulness_ratio: float
    user: UserResponse

    class Config:
        from_attributes = True


class ReviewVote(BaseModel):
    helpful: bool  # True for helpful, False for not helpful