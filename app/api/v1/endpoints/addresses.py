from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressResponse

router = APIRouter()


@router.get("/", response_model=List[AddressResponse])
def get_addresses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Get current user's addresses"""
    addresses = db.query(Address).filter(Address.user_id == current_user.user_id).all()
    return addresses


@router.post("/", response_model=AddressResponse)
def create_address(
    address_in: AddressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Create new address"""
    address = Address(user_id=current_user.user_id, **address_in.dict())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address