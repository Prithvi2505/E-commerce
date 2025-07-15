from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentResponse

router = APIRouter()


@router.post("/process", response_model=PaymentResponse)
def process_payment(
    payment_in: PaymentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Process payment for order"""
    # Implementation would handle payment processing with Stripe/PayPal
    pass