from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewResponse

router = APIRouter()


@router.get("/product/{product_id}", response_model=List[ReviewResponse])
def get_product_reviews(
    product_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """Get reviews for a product"""
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    return reviews


@router.post("/", response_model=ReviewResponse)
def create_review(
    review_in: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Create new review"""
    review = Review(user_id=current_user.user_id, **review_in.dict())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review